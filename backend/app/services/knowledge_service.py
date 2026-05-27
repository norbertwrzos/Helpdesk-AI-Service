"""
KnowledgeService — operacje CRUD na artykułach bazy wiedzy.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.knowledge_article import KnowledgeArticle
from app.schemas.knowledge_article import KnowledgeArticleCreate, KnowledgeArticleUpdate


def get_articles(db: Session) -> list[KnowledgeArticle]:
    return db.query(KnowledgeArticle).all()


def get_article(db: Session, article_id: int) -> KnowledgeArticle:
    article = db.query(KnowledgeArticle).filter(KnowledgeArticle.id == article_id).first()
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Artykuł nie został znaleziony.",
        )
    return article


def create_article(db: Session, data: KnowledgeArticleCreate) -> KnowledgeArticle:
    article = KnowledgeArticle(
        title=data.title,
        content=data.content,
        category_id=data.category_id,
        tags=data.tags,
    )
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


def update_article(
    db: Session, article_id: int, data: KnowledgeArticleUpdate
) -> KnowledgeArticle:
    article = get_article(db, article_id)
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(article, field, value)
    db.commit()
    db.refresh(article)
    return article


def delete_article(db: Session, article_id: int) -> None:
    article = get_article(db, article_id)
    db.delete(article)
    db.commit()
