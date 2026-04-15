from fastapi import FastAPI
from app.api.routes_users import router as users_router
from app.api.routes_health import router as health_router

app = FastAPI(title="Self-Healing API")

app.include_router(users_router, prefix="/users")
app.include_router(health_router, prefix="/health")