# Business logic and AI services for the Helpdesk AI Service backend.
#
# Key modules:
#   - ticket_service.py            — ticket CRUD and lifecycle
#   - classification_service.py    — rule-based category classification
#   - priority_analysis_service.py — rule-based priority analysis
#   - rag_retriever.py             — RAG retrieval with similarity fallback
#   - analysis_pipeline.py         — orchestrates classification, RAG and AI response
#   - ai_generation/, embeddings/  — provider-based AI/embedding generation (mock / OpenAI)
