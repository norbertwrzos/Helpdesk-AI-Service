from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.priority import PriorityCreate, PriorityResponse, PriorityUpdate
from app.services import priority_service

router = APIRouter()


@router.get("/priorities", response_model=list[PriorityResponse])
def list_priorities(db: Session = Depends(get_db)) -> list[PriorityResponse]:
    return priority_service.get_priorities(db)


@router.post("/priorities", response_model=PriorityResponse, status_code=201)
def create_priority(
    data: PriorityCreate, db: Session = Depends(get_db)
) -> PriorityResponse:
    return priority_service.create_priority(db, data)


@router.patch("/priorities/{priority_id}", response_model=PriorityResponse)
def update_priority(
    priority_id: int, data: PriorityUpdate, db: Session = Depends(get_db)
) -> PriorityResponse:
    return priority_service.update_priority(db, priority_id, data)
