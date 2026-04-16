from app.db.fake_db import db
from datetime import datetime, timezone

class UserService:

    def create_user(self, user):
        payload = user.model_dump() if hasattr(user, "model_dump") else user.dict()
        current_year = datetime.now(timezone.utc).year
        if payload["birth_year"] > current_year:
            raise ValueError("birth_year cannot be in the future")
        payload["age"] = current_year - payload["birth_year"]
        user_id = len(db) + 1
        db[user_id] = payload
        return {"id": user_id, **db[user_id]}

    def get_user(self, user_id: int):
        return db.get(user_id)

    def list_users(self):
        return list(db.values())
