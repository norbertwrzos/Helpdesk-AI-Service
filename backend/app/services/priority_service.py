from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.priority import Priority
from app.schemas.priority import PriorityCreate


def get_priorities(db: Session) -> list[Priority]:
    return db.query(Priority).all()


def create_priority(db: Session, data: PriorityCreate) -> Priority:
    priority = Priority(
        name=data.name, level=data.level, description=data.description
    )
    db.add(priority)
    try:
        db.commit()
        db.refresh(priority)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Priority '{data.name}' already exists.",
        )
    return priority
