from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.category import Category
from app.schemas.category import CategoryCreate


def get_categories(db: Session) -> list[Category]:
    return db.query(Category).all()


def create_category(db: Session, data: CategoryCreate) -> Category:
    category = Category(name=data.name, description=data.description)
    db.add(category)
    try:
        db.commit()
        db.refresh(category)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Category '{data.name}' already exists.",
        )
    return category
