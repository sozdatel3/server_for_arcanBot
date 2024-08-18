import random

from app.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to the Telegram Bot Backend"
    }


# Users API tests
def test_create_user():
    response = client.post(
        "/api/users/",
        json={
            "username": "testuser",
            "user_id": random.randrange(1, 999999999, 1),
            "chat_id": 456,
        },
    )
    assert response.status_code == 200
    assert "message" in response.json()


def test_get_user():
    response = client.get("/api/users/123")
    assert response.status_code == 200
    assert "username" in response.json()


# Cities API tests


# def test_add_user_to_city_table():
#     response = client.post(
#         "/api/cities/users",
#         json={"user_id": random.randint(1, 9999999)},
#     )
#     assert response.status_code == 200
#     assert "message" in response.json()


# # add_user_to_city_table


# def test_add_checked_city():
#     response = client.post(
#         "/api/cities/checked_cities",
#         json={"user_id": 123, "city_name": "New York"},
#     )
#     assert response.status_code == 200
#     assert "message" in response.json()


def test_add_user_to_city_table():
    response = client.post(
        "/api/cities/users",
        json={"user_id": random.randint(1, 9999999)},
    )
    assert response.status_code == 200
    assert "message" in response.json()


def test_add_checked_city():
    response = client.post(
        "/api/cities/checked_cities",
        json={"user_id": 123, "city_name": "New York"},
    )
    assert response.status_code == 200
    assert "message" in response.json()


def test_get_checked_cities():
    response = client.get("/api/cities/checked_cities/123")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# Loyalty API tests
def test_add_user_to_loyalty():
    response = client.post(
        "/api/loyalty/users/",
        json={"user_id": random.randrange(1, 999999999, 1)},
    )
    assert response.status_code == 200
    assert "message" in response.json()


def test_get_user_balance():
    response = client.get("/api/loyalty/users/123/balance")
    assert response.status_code == 200
    assert isinstance(response.json(), int)


# Forecasts API tests
def test_add_user_to_forecast():
    response = client.post(
        "/api/forecasts/users/",
        json={"user_id": random.randrange(1, 999999999, 1), "arcan": 5},
    )
    assert response.status_code == 200
    assert "message" in response.json()


def test_get_subscription_status():
    response = client.get("/api/forecasts/users/123/subscription")
    assert response.status_code == 200
    assert isinstance(response.json(), bool)


# Statistics API tests
def test_get_statistics():
    response = client.get("/api/statistics/?period=week")
    assert response.status_code == 200
    assert "new_users" in response.json()


def test_get_formatted_statistics():
    response = client.get("/api/statistics/formatted?period=month")
    assert response.status_code == 200
    assert "formatted_statistics" in response.json()


# Covers API tests
def test_add_arcan_description():
    response = client.post(
        "/api/covers/arcan_descriptions",
        params={"arcan": 1, "description": "Test description"},
    )
    assert response.status_code == 200
    assert "message" in response.json()


def test_get_arcan_description():
    response = client.get("/api/covers/arcan_descriptions/1")
    assert response.status_code == 200
    assert isinstance(response.json(), str)


# Test invalid requests
def test_invalid_user_id():
    response = client.get("/api/users/invalid")
    assert response.status_code == 422


def test_invalid_period():
    response = client.get("/api/statistics/?period=invalid")
    assert response.status_code == 400
