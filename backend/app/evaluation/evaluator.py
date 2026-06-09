from __future__ import annotations

import csv
import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from typing import Any

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.db.base import Base
from app.evaluation.answer_quality import evaluate_answer_quality
from app.evaluation.mail_response_quality import evaluate_mail_response
from app.evaluation.metrics import (
    accuracy_score,
    classification_report_as_dict,
    confusion_matrix_as_dict,
    macro_f1,
    weighted_f1,
)
from app.evaluation.rag_metrics import (
    average_retrieval_score,
    hit_at_k,
    mean_reciprocal_rank,
    source_keyword_coverage,
)
from app.models.category import Category
from app.models.knowledge_article import KnowledgeArticle
from app.models.priority import Priority
from app.services.ai_generator import MockAIGenerator
from app.services.ai_generation.base import BaseAIResponseProvider
from app.services.ai_generation.mock_provider import MockAIResponseProvider
from app.services.ai_generation.openai_provider import OpenAIResponseProvider
from app.services.ai_generation.schemas import (
    RetrievedArticleForGeneration,
    TicketResponseGenerationInput,
    TicketResponseGenerationResult,
)
from app.services.classification_service import ClassificationService
from app.services.embeddings.mock_embedding_provider import MockEmbeddingProvider
from app.services.priority_analysis_service import PriorityAnalysisService
from app.services.rag_retriever import RagRetriever

_THIS_DIR = os.path.dirname(__file__)
_SEED_DIR = os.path.normpath(os.path.join(_THIS_DIR, "../../../data/seed"))
_DEFAULT_AGENT_NAME = "Agent IT Support"

CATEGORY_LABELS = [
    "Konto i dostęp",
    "Sieć i VPN",
    "Aplikacje biznesowe",
    "Sprzęt komputerowy",
    "Poczta e-mail",
    "Bezpieczeństwo",
    "System operacyjny",
    "Inne",
]

PRIORITY_LABELS = ["Niski", "Średni", "Wysoki", "Krytyczny"]
EVALUATION_MODES = {"mock", "rag", "openai_rag"}


def _make_stub_ticket(row: dict[str, str]) -> SimpleNamespace:
    return SimpleNamespace(
        id=row.get("id", ""),
        title=row.get("title", ""),
        description=row.get("description", ""),
        status="new",
        source="csv",
        category_id=None,
        priority_id=None,
        requester_name=row.get("requester_name"),
        assigned_agent_name=row.get("assigned_agent_name") or _DEFAULT_AGENT_NAME,
    )


def _parse_keywords(raw: str) -> list[str]:
    if not raw:
        return []
    return [keyword.strip() for keyword in raw.split(";") if keyword.strip()]


def _load_json_file(path: str) -> list[dict[str, Any]]:
    with open(path, encoding="utf-8") as file_handle:
        return json.load(file_handle)


def _resolve_seed_path(filename: str) -> str:
    return str(Path(_SEED_DIR) / filename)


def _default_limitations(mode: str, openai_used: bool) -> list[str]:
    limitations = [
        "Metryki retrievalu opierają się na dopasowaniu słów kluczowych do tytułów i fragmentów artykułów, a nie na eksperckim oznaczeniu relewantnych źródeł.",
        "Ocena formatu odpowiedzi mailowej ma charakter heurystyczny i nie zastępuje weryfikacji człowieka.",
        "Zbiór testowy jest syntetyczny i został rozszerzony tylko o podstawowe oczekiwania dotyczące źródeł oraz formatu odpowiedzi.",
    ]
    if mode == "mock":
        limitations.append("Tryb mock nie uruchamia retrievalu RAG, więc metryki retrievalu są zerowe i stanowią punkt odniesienia dla kolejnych trybów.")
    if mode == "openai_rag" and not openai_used:
        limitations.append("Tryb openai_rag został uruchomiony bez rzeczywistego użycia OpenAI i bez kosztów API; zastosowano fallback do providera mock.")
    return limitations


@dataclass
class CaseResult:
    id: str
    title: str
    expected_category: str
    predicted_category: str
    category_correct: bool
    category_confidence: float
    expected_priority: str
    predicted_priority: str
    priority_correct: bool
    priority_confidence: float
    generated_answer: str
    answer_quality_score: int
    answer_quality_notes: str
    expected_article_keywords: list[str] = field(default_factory=list)
    expected_answer_format: str = "mail"
    expected_rag_category: str | None = None
    retrieved_article_ids: list[int] = field(default_factory=list)
    retrieved_article_titles: list[str] = field(default_factory=list)
    retrieval_hit_at_1: float = 0.0
    retrieval_hit_at_3: float = 0.0
    retrieval_hit_at_5: float = 0.0
    retrieval_mrr: float = 0.0
    retrieval_average_score: float = 0.0
    retrieval_keyword_coverage: float = 0.0
    mail_format_score: int = 0
    mail_format_notes: str = ""
    provider_name: str = "mock"
    model_name: str = "mock-ai-generator"
    matched_keywords: list[str] = field(default_factory=list)
    missing_keywords: list[str] = field(default_factory=list)


@dataclass
class EvaluationResult:
    generated_at: str
    mode: str
    total_cases: int
    case_results: list[CaseResult]
    classification_accuracy: float
    classification_macro_f1: float
    classification_weighted_f1: float
    priority_accuracy: float
    priority_macro_f1: float
    priority_weighted_f1: float
    average_answer_quality_score: float
    average_mail_format_score: float
    average_response_length: float
    retrieval_hit_at_1: float
    retrieval_hit_at_3: float
    retrieval_hit_at_5: float
    retrieval_mrr: float
    average_retrieval_score: float
    average_retrieval_keyword_coverage: float
    provider_mode: str
    openai_used: bool
    limitations: list[str]
    classification_report: list[dict]
    priority_report: list[dict]
    classification_confusion_matrix: dict[str, dict[str, int]]
    priority_confusion_matrix: dict[str, dict[str, int]]


class EvaluationRunner:
    def __init__(
        self,
        mode: str = "rag",
        allow_openai: bool = False,
        agent_name: str = _DEFAULT_AGENT_NAME,
        ai_response_provider: BaseAIResponseProvider | None = None,
        rag_retriever: RagRetriever | None = None,
    ) -> None:
        normalized_mode = mode.strip().lower()
        if normalized_mode not in EVALUATION_MODES:
            raise ValueError(f"Unsupported evaluation mode: {mode}")

        self.mode = normalized_mode
        self.allow_openai = allow_openai
        self.agent_name = agent_name
        self.classifier = ClassificationService()
        self.priority_analyzer = PriorityAnalysisService()
        self.ai_generator = MockAIGenerator()
        self.ai_response_provider = ai_response_provider
        self.fallback_ai_response_provider = MockAIResponseProvider()
        self.rag_retriever = rag_retriever or RagRetriever(provider=MockEmbeddingProvider())

    def run(self, input_path: str, output_dir: str | None = None) -> EvaluationResult:
        rows = self._load_input(input_path)
        provider = self._resolve_generation_provider()
        session, engine = self._build_session()
        try:
            categories = session.query(Category).all()
            priorities = session.query(Priority).all()
            case_results = [
                self._evaluate_case(
                    row=row,
                    db=session,
                    categories=categories,
                    priorities=priorities,
                    generation_provider=provider,
                )
                for row in rows
            ]
        finally:
            session.close()
            engine.dispose()

        y_true_cat = [result.expected_category for result in case_results]
        y_pred_cat = [result.predicted_category for result in case_results]
        y_true_pri = [result.expected_priority for result in case_results]
        y_pred_pri = [result.predicted_priority for result in case_results]
        openai_used = any(case.provider_name == "openai" for case in case_results)

        result = EvaluationResult(
            generated_at=datetime.now(timezone.utc).isoformat(),
            mode=self.mode,
            total_cases=len(case_results),
            case_results=case_results,
            classification_accuracy=accuracy_score(y_true_cat, y_pred_cat),
            classification_macro_f1=macro_f1(y_true_cat, y_pred_cat),
            classification_weighted_f1=weighted_f1(y_true_cat, y_pred_cat),
            priority_accuracy=accuracy_score(y_true_pri, y_pred_pri),
            priority_macro_f1=macro_f1(y_true_pri, y_pred_pri),
            priority_weighted_f1=weighted_f1(y_true_pri, y_pred_pri),
            average_answer_quality_score=(
                sum(case.answer_quality_score for case in case_results) / len(case_results)
                if case_results
                else 0.0
            ),
            average_mail_format_score=(
                sum(case.mail_format_score for case in case_results) / len(case_results)
                if case_results
                else 0.0
            ),
            average_response_length=(
                sum(len(case.generated_answer) for case in case_results) / len(case_results)
                if case_results
                else 0.0
            ),
            retrieval_hit_at_1=(
                sum(case.retrieval_hit_at_1 for case in case_results) / len(case_results)
                if case_results
                else 0.0
            ),
            retrieval_hit_at_3=(
                sum(case.retrieval_hit_at_3 for case in case_results) / len(case_results)
                if case_results
                else 0.0
            ),
            retrieval_hit_at_5=(
                sum(case.retrieval_hit_at_5 for case in case_results) / len(case_results)
                if case_results
                else 0.0
            ),
            retrieval_mrr=(
                sum(case.retrieval_mrr for case in case_results) / len(case_results)
                if case_results
                else 0.0
            ),
            average_retrieval_score=(
                sum(case.retrieval_average_score for case in case_results) / len(case_results)
                if case_results
                else 0.0
            ),
            average_retrieval_keyword_coverage=(
                sum(case.retrieval_keyword_coverage for case in case_results) / len(case_results)
                if case_results
                else 0.0
            ),
            provider_mode=self.mode,
            openai_used=openai_used,
            limitations=_default_limitations(self.mode, openai_used),
            classification_report=classification_report_as_dict(y_true_cat, y_pred_cat, CATEGORY_LABELS),
            priority_report=classification_report_as_dict(y_true_pri, y_pred_pri, PRIORITY_LABELS),
            classification_confusion_matrix=confusion_matrix_as_dict(y_true_cat, y_pred_cat, CATEGORY_LABELS),
            priority_confusion_matrix=confusion_matrix_as_dict(y_true_pri, y_pred_pri, PRIORITY_LABELS),
        )

        if output_dir:
            from app.evaluation.report_writer import ReportWriter

            ReportWriter().write_all(result, output_dir)

        return result

    def _load_input(self, path: str) -> list[dict[str, str]]:
        if path.endswith(".json"):
            return self._load_json(path)
        return self._load_csv(path)

    @staticmethod
    def _load_csv(path: str) -> list[dict[str, str]]:
        with open(path, encoding="utf-8", newline="") as file_handle:
            return [dict(row) for row in csv.DictReader(file_handle)]

    @staticmethod
    def _load_json(path: str) -> list[dict[str, str]]:
        with open(path, encoding="utf-8") as file_handle:
            return json.load(file_handle)

    def _build_session(self) -> tuple[Session, Any]:
        engine = create_engine(
            "sqlite:///:memory:",
            connect_args={"check_same_thread": False},
            poolclass=StaticPool,
        )
        Base.metadata.create_all(bind=engine)
        session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = session_factory()
        self._seed_runtime_data(session)
        return session, engine

    def _seed_runtime_data(self, db: Session) -> None:
        categories_data = _load_json_file(_resolve_seed_path("categories.json"))
        priorities_data = _load_json_file(_resolve_seed_path("priorities.json"))
        knowledge_data = _load_json_file(_resolve_seed_path("knowledge_base.json"))

        category_map: dict[str, int] = {}
        for item in categories_data:
            category = Category(name=item["name"], description=item.get("description"))
            db.add(category)
            db.flush()
            category_map[category.name] = category.id

        for item in priorities_data:
            db.add(
                Priority(
                    name=item["name"],
                    level=item["level"],
                    description=item.get("description"),
                )
            )
        db.flush()

        for item in knowledge_data:
            db.add(
                KnowledgeArticle(
                    title=item["title"],
                    content=item["content"],
                    category_id=category_map.get(item.get("category_name", "")),
                    tags=item.get("tags"),
                )
            )

        db.commit()

    def _evaluate_case(
        self,
        row: dict[str, str],
        db: Session,
        categories: list[Category],
        priorities: list[Priority],
        generation_provider: BaseAIResponseProvider,
    ) -> CaseResult:
        title = row.get("title", "")
        description = row.get("description", "")
        expected_category = row.get("expected_category", "")
        expected_priority = row.get("expected_priority", "")
        expected_keywords = _parse_keywords(row.get("expected_solution_keywords", ""))
        expected_article_keywords = _parse_keywords(row.get("expected_article_keywords", ""))
        expected_answer_format = (row.get("expected_answer_format", "mail") or "mail").strip().lower()
        expected_rag_category = row.get("expected_rag_category") or expected_category or None

        classification = self.classifier.classify(title, description, categories)
        priority = self.priority_analyzer.analyze(title, description, priorities)

        ticket = _make_stub_ticket(row)
        ticket.category_id = classification.category_id
        ticket.priority_id = priority.priority_id
        retrieved_articles = self._retrieve_articles(db, ticket)
        generation_result = self._generate_response(
            ticket=ticket,
            classification=classification,
            priority=priority,
            retrieved_articles=retrieved_articles,
            generation_provider=generation_provider,
        )

        answer_quality = evaluate_answer_quality(generation_result.email_body, expected_keywords)
        mail_quality = evaluate_mail_response(
            generation_result.email_body if expected_answer_format == "mail" else "",
            expected_keywords,
            ticket.assigned_agent_name,
        )

        return CaseResult(
            id=row.get("id", ""),
            title=title,
            expected_category=expected_category,
            predicted_category=classification.category_name,
            category_correct=classification.category_name == expected_category,
            category_confidence=classification.confidence,
            expected_priority=expected_priority,
            predicted_priority=priority.priority_name,
            priority_correct=priority.priority_name == expected_priority,
            priority_confidence=priority.confidence,
            generated_answer=generation_result.email_body,
            answer_quality_score=answer_quality["score"],
            answer_quality_notes=answer_quality["notes"],
            expected_article_keywords=expected_article_keywords,
            expected_answer_format=expected_answer_format,
            expected_rag_category=expected_rag_category,
            retrieved_article_ids=[article.article_id for article in retrieved_articles],
            retrieved_article_titles=[article.title for article in retrieved_articles],
            retrieval_hit_at_1=hit_at_k(expected_article_keywords, retrieved_articles, 1),
            retrieval_hit_at_3=hit_at_k(expected_article_keywords, retrieved_articles, 3),
            retrieval_hit_at_5=hit_at_k(expected_article_keywords, retrieved_articles, 5),
            retrieval_mrr=mean_reciprocal_rank(expected_article_keywords, retrieved_articles),
            retrieval_average_score=average_retrieval_score(retrieved_articles),
            retrieval_keyword_coverage=source_keyword_coverage(expected_article_keywords, retrieved_articles),
            mail_format_score=mail_quality["score"],
            mail_format_notes=mail_quality["notes"],
            provider_name=generation_result.provider_name,
            model_name=generation_result.model_name,
            matched_keywords=answer_quality["matched_keywords"],
            missing_keywords=answer_quality["missing_keywords"],
        )

    def _resolve_generation_provider(self) -> BaseAIResponseProvider:
        if self.mode == "mock":
            return self.fallback_ai_response_provider
        if self.mode == "rag":
            return self.ai_response_provider or self.fallback_ai_response_provider
        if not self.allow_openai:
            return self.fallback_ai_response_provider
        if self.ai_response_provider is not None:
            return self.ai_response_provider

        api_key = settings.OPENAI_API_KEY.strip()
        if not api_key:
            return self.fallback_ai_response_provider

        try:
            return OpenAIResponseProvider(
                api_key=api_key,
                model_name=settings.OPENAI_CHAT_MODEL,
                temperature=settings.OPENAI_RESPONSE_TEMPERATURE,
                max_output_tokens=settings.OPENAI_MAX_OUTPUT_TOKENS,
            )
        except Exception:
            return self.fallback_ai_response_provider

    def _retrieve_articles(self, db: Session, ticket: SimpleNamespace) -> list[Any]:
        if self.mode == "mock":
            return []
        return self.rag_retriever.retrieve_for_ticket(db, ticket)

    def _build_generation_input(
        self,
        ticket: SimpleNamespace,
        classification: Any,
        priority: Any,
        retrieved_articles: list[Any],
    ) -> TicketResponseGenerationInput:
        return TicketResponseGenerationInput(
            ticket_id=ticket.id,
            title=ticket.title,
            description=ticket.description,
            category_name=classification.category_name,
            priority_name=priority.priority_name,
            requester_name=ticket.requester_name,
            agent_name=ticket.assigned_agent_name,
            retrieved_articles=[
                RetrievedArticleForGeneration(
                    article_id=article.article_id,
                    title=article.title,
                    excerpt=article.excerpt,
                    score=article.score,
                    category_id=article.category_id,
                )
                for article in retrieved_articles
            ],
            classification_explanation=classification.explanation,
            priority_explanation=priority.explanation,
        )

    def _generate_response(
        self,
        ticket: SimpleNamespace,
        classification: Any,
        priority: Any,
        retrieved_articles: list[Any],
        generation_provider: BaseAIResponseProvider,
    ) -> TicketResponseGenerationResult:
        if self.mode == "mock":
            generated = self.ai_generator.generate(
                ticket=ticket,
                classification=classification,
                priority=priority,
                similar_articles=[],
            )
            return TicketResponseGenerationResult(
                subject=f"Odpowiedź do zgłoszenia #{ticket.id}: {ticket.title}",
                email_body=generated.response_text,
                confidence=0.55,
                used_sources=[],
                requires_human_review=True,
                limitations="Odpowiedź została przygotowana przez historyczny mock generator.",
                model_name=generated.model_name,
                provider_name=generated.provider_name,
            )

        generation_input = self._build_generation_input(ticket, classification, priority, retrieved_articles)

        try:
            return generation_provider.generate_ticket_response(generation_input)
        except Exception:
            return self.fallback_ai_response_provider.generate_ticket_response(generation_input)