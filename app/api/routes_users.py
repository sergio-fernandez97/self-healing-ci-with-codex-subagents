from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.services.user_service import UserService
from app.models.user import UserCreate

router = APIRouter()
service = UserService()

@router.post("/")
def create_user(user: UserCreate):
    current_year = datetime.utcnow().year
    if user.birth_year > current_year:
        raise HTTPException(status_code=400, detail="Birth year cannot be in the future")
    created_user = service.create_user(user)
    created_user["age"] = current_year - user.birth_year
    return created_user

@router.get("/{user_id}")
def get_user(user_id: int):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/")
def list_users():
    return service.list_users()
