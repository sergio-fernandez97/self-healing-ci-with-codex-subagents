from datetime import date
from typing import Any

from app.db.fake_db import db


class UserService:
    def create_user(self, user: Any) -> dict[str, int | str]:
        payload: dict[str, Any]
        if hasattr(user, "model_dump"):
            payload = user.model_dump()
        else:
            payload = user.dict()

        birth_year = int(payload["birth_year"])
        current_year = date.today().year
        if birth_year > current_year:
            raise ValueError("birth_year cannot be in the future")

        user_id = len(db) + 1
        record: dict[str, int | str] = {
            "name": str(payload["name"]),
            "birth_year": birth_year,
            "age": current_year - birth_year,
        }
        db[user_id] = record
        return {"id": user_id, **record}

    def get_user(self, user_id: int) -> dict[str, int | str] | None:
        return db.get(user_id)

    def list_users(self) -> list[dict[str, int | str]]:
        return list(db.values())
