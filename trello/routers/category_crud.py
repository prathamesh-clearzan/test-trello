from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from trello.dbConnection import get_session
from trello.models import Category, Task
from trello.schemas import CategoryCreate, CategoryRead, TaskRead

router = APIRouter(prefix="/categories", tags=["Categories"])



@router.post("/", response_model=CategoryRead)
def create_category(category: CategoryCreate, session: Session = Depends(get_session)):
    new_category = Category(**category.dict())
    session.add(new_category)
    session.commit()
    session.refresh(new_category)
    return new_category



@router.get("/", response_model=list[CategoryRead])
def get_categories(session: Session = Depends(get_session)):
    return session.exec(select(Category)).all()



@router.get("/{category_id}", response_model=CategoryRead)
def get_category(category_id: int, session: Session = Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category



@router.put("/{category_id}", response_model=CategoryRead)
def update_category(category_id: int, updated_data: CategoryCreate, session: Session = Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    for key, value in updated_data.dict().items():
        setattr(category, key, value)

    session.add(category)
    session.commit()
    session.refresh(category)
    return category



@router.delete("/{category_id}")
def delete_category(category_id: int, session: Session = Depends(get_session)):
    category = session.get(Category, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    session.delete(category)
    session.commit()
    return {"detail": "Category deleted successfully"}



@router.get("/{category_id}/tasks", response_model=list[TaskRead])
def get_tasks_by_category(category_id: int, session: Session = Depends(get_session)):
    return session.exec(select(Task).where(Task.category_id == category_id)).all()
