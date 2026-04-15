from fastapi import APIRouter, HTTPException
from app.services.user_service import UserService
from app.models.user import UserCreate

router = APIRouter()
service = UserService()

@router.post("/")
def create_user(user: UserCreate):
    return service.create_user(user)

@router.get("/{user_id}")
def get_user(user_id: int):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/")
def list_users():
    return service.list_users()