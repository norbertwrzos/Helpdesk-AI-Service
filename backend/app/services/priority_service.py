from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.priority import Priority
from app.schemas.priority import PriorityCreate, PriorityUpdate


def get_priorities(db: Session) -> list[Priority]:
    return db.query(Priority).all()


def get_priority(db: Session, priority_id: int) -> Priority:
    priority = db.query(Priority).filter(Priority.id == priority_id).first()
    if not priority:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Priority '{priority_id}' was not found.",
        )
    return priority


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


def update_priority(db: Session, priority_id: int, data: PriorityUpdate) -> Priority:
    priority = get_priority(db, priority_id)
    updates = data.model_dump(exclude_unset=True)

    if "name" in updates:
        duplicate = (
            db.query(Priority)
            .filter(Priority.name == updates["name"], Priority.id != priority_id)
            .first()
        )
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Priority '{updates['name']}' already exists.",
            )

    for field, value in updates.items():
        setattr(priority, field, value)

    try:
        db.commit()
        db.refresh(priority)
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Priority '{priority.name}' already exists.",
        )

    return priority
