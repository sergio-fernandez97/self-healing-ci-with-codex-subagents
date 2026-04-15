from app.db.fake_db import db

class UserService:

    def create_user(self, user):
        user_id = len(db) + 1
        db[user_id] = user.dict()
        return {"id": user_id, **db[user_id]}

    def get_user(self, user_id: int):
        return db.get(user_id)

    def list_users(self):
        return list(db.values())