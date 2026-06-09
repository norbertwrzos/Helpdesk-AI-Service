from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.knowledge_article import (
    KnowledgeArticleCreate,
    KnowledgeArticleResponse,
    KnowledgeArticleUpdate,
)
from app.schemas.rag import (
    KnowledgeReindexRequest,
    KnowledgeReindexResponse,
    KnowledgeSearchRequest,
    KnowledgeSearchResult,
)
from app.services.knowledge_embedding_service import KnowledgeEmbeddingService
from app.services.rag_retriever import RagRetriever
from app.services import knowledge_service

router = APIRouter()
_embedding_service = KnowledgeEmbeddingService()
_rag_retriever = RagRetriever()


@router.get("/knowledge", response_model=list[KnowledgeArticleResponse])
def list_articles(db: Session = Depends(get_db)) -> list[KnowledgeArticleResponse]:
    return knowledge_service.get_articles(db)


@router.post("/knowledge", response_model=KnowledgeArticleResponse, status_code=201)
def create_article(
    data: KnowledgeArticleCreate, db: Session = Depends(get_db)
) -> KnowledgeArticleResponse:
    return knowledge_service.create_article(db, data)


@router.get("/knowledge/{article_id}", response_model=KnowledgeArticleResponse)
def get_article(
    article_id: int, db: Session = Depends(get_db)
) -> KnowledgeArticleResponse:
    return knowledge_service.get_article(db, article_id)


@router.patch("/knowledge/{article_id}", response_model=KnowledgeArticleResponse)
def update_article(
    article_id: int, data: KnowledgeArticleUpdate, db: Session = Depends(get_db)
) -> KnowledgeArticleResponse:
    return knowledge_service.update_article(db, article_id, data)


@router.delete("/knowledge/{article_id}", status_code=204)
def delete_article(
    article_id: int, db: Session = Depends(get_db)
) -> None:
    knowledge_service.delete_article(db, article_id)


@router.post("/knowledge/reindex", response_model=KnowledgeReindexResponse)
def reindex_knowledge(
    data: KnowledgeReindexRequest,
    db: Session = Depends(get_db),
) -> KnowledgeReindexResponse:
    summary = _embedding_service.reindex_all(db, force=data.force)
    return KnowledgeReindexResponse.model_validate(summary)


@router.post("/knowledge/search", response_model=list[KnowledgeSearchResult])
def search_knowledge(
    data: KnowledgeSearchRequest,
    db: Session = Depends(get_db),
) -> list[KnowledgeSearchResult]:
    return _rag_retriever.retrieve_for_query(db, data.query, top_k=data.top_k)
