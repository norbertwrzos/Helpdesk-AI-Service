# Import all models so that Alembic can detect them via Base.metadata
from app.models.ai_response import AIResponse  # noqa: F401
from app.models.category import Category  # noqa: F401
from app.models.feedback import Feedback  # noqa: F401
from app.models.knowledge_article import KnowledgeArticle  # noqa: F401
from app.models.priority import Priority  # noqa: F401
from app.models.ticket import Ticket  # noqa: F401
