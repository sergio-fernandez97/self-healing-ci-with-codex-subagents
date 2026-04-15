def test_create_user(client):
    res = client.post("/users/", json={
        "name": "Sergio",
        "birth_year": 2000
    })
    assert res.status_code == 200
    assert res.json()["name"] == "Sergio"


def test_get_user_not_found(client):
    res = client.get("/users/999")
    assert res.status_code == 404


def test_create_user_invalid_birth_year(client):
    res = client.post("/users/", json={
        "name": "Sergio",
        "birth_year": 3000  # invalid future year
    })
    assert res.status_code == 400


def test_user_has_age(client):
    res = client.post("/users/", json={
        "name": "Sergio",
        "birth_year": 2000
    })
    data = res.json()
    assert "age" in data


def test_list_users_returns_list(client):
    res = client.get("/users/")
    assert isinstance(res.json(), list)