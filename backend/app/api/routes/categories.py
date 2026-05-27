from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.category import CategoryCreate, CategoryResponse
from app.services import category_service

router = APIRouter()


@router.get("/categories", response_model=list[CategoryResponse])
def list_categories(db: Session = Depends(get_db)) -> list[CategoryResponse]:
    return category_service.get_categories(db)


@router.post("/categories", response_model=CategoryResponse, status_code=201)
def create_category(
    data: CategoryCreate, db: Session = Depends(get_db)
) -> CategoryResponse:
    return category_service.create_category(db, data)
