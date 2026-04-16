from fastapi import APIRouter, HTTPException
from app.services.user_service import UserService
from app.models.user import UserCreate

router = APIRouter()
service = UserService()

@router.post("/")
def create_user(user: UserCreate):
    try:
        return service.create_user(user)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

@router.get("/{user_id}")
def get_user(user_id: int):
    user = service.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/")
def list_users():
    return service.list_users()
