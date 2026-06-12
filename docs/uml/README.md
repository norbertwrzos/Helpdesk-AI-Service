# Diagramy UML — TicketService.ai

Niniejszy katalog zawiera diagramy UML przeznaczone do pracy inżynierskiej opisującej system **TicketService.ai** (Helpdesk-AI-Service). Wszystkie diagramy zostały opracowane na podstawie rzeczywistego kodu źródłowego i dokumentacji repozytorium.

## Zawartość

| Plik `.puml` | Plik `.png` | Typ diagramu | Opis |
|---|---|---|---|
| `usecase_diagram.puml` | `usecase_diagram.png` | Use Case | Role użytkowników (Agent IT, Użytkownik końcowy) i ich przypadki użycia |
| `activity_ai_pipeline.puml` | `activity_ai_pipeline.png` | Activity | Przepływ procesu analizy AI (`AnalysisPipeline.analyze_ticket`) |
| `collaboration_analysis.puml` | `collaboration_analysis.png` | Collaboration / Communication | Interakcje między komponentami warstwy serwisowej podczas analizy AI |
| `sequence_ai_analysis.puml` | `sequence_ai_analysis.png` | Sequence | Sekwencja wywołań HTTP i serwisowych od kliknięcia przycisku do odpowiedzi AI |
| `class_diagram.puml` | `class_diagram.png` | Class | Modele SQLAlchemy (7 encji) i warstwa serwisów AI |
| `state_ticket.puml` | `state_ticket.png` | State | Stany zgłoszenia (`TicketStatus`: open, ai_reviewed, pending, resolved, rejected) |
| `component_diagram.puml` | `component_diagram.png` | Component | Architektura warstwowa: Frontend → Backend → PostgreSQL + pgvector → OpenAI API |
| `deployment_diagram.puml` | `deployment_diagram.png` | Deployment | Topologia wdrożenia: Docker (PostgreSQL), uvicorn (FastAPI), Vite (React) |

## Architektura systemu (skrót)

- **Frontend:** React 18 + TypeScript + Vite, role mockowe `agent` i `end_user`, uwierzytelnienie przez localStorage
- **Backend:** Python 3.12 + FastAPI, endpointy: `/tickets`, `/ai`, `/knowledge`, `/categories`, `/priorities`, `/ticket_messages`, `/health`
- **Baza danych:** PostgreSQL 16 + pgvector (kontener Docker `pgvector/pgvector:pg16`, wolumen `postgres_data`)
- **Warstwa AI/RAG:** `AnalysisPipeline`, `ClassificationService`, `PriorityAnalysisService`, `RagRetriever`, `SimilarityService`, `KnowledgeEmbeddingService`, `MockAIResponseProvider`, `OpenAIResponseProvider` (fallback mock przy braku/błędzie klucza OpenAI)

## Regeneracja plików PNG

Wymagania: Java 11+ oraz [PlantUML](https://plantuml.com/download) (`plantuml.jar`).

```bash
# Przykład (zakładając plantuml.jar w bieżącym katalogu lub PATH)
java -jar plantuml.jar -tpng docs/uml/*.puml
```

Alternatywnie można użyć skryptu pomocniczego:

```bash
bash scripts/generate_uml.sh
```

## Przeznaczenie

Diagramy są przeznaczone do wykorzystania w pracy inżynierskiej jako ilustracje projektu i architektury systemu TicketService.ai. Bazują wyłącznie na aktualnym kodzie i dokumentacji repozytorium.
