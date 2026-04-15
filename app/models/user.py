from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    birth_year: int