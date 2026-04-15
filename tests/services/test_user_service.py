from app.services.user_service import UserService

def test_create_user_service():
    service = UserService()
    user = {"name": "Test", "birth_year": 1990}

    result = service.create_user(type("U", (), {"dict": lambda self: user})())
    assert result["name"] == "Test"