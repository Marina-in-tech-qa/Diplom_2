
import pytest
import requests

from helpers import generate_user_data
from urls import CREATE_USER_URL, DELETE_USER_URL, INGREDIENTS_URL


@pytest.fixture
def created_user():
    user_data = generate_user_data()

    response = requests.post(
        CREATE_USER_URL,
        json=user_data,
        timeout=10
    )

    assert response.status_code == 200, (
        f"Не удалось создать тестового пользователя: {response.text}"
    )

    access_token = response.json()["accessToken"]

    yield user_data

    requests.delete(
        DELETE_USER_URL,
        headers={"Authorization": access_token},
        timeout=10
    )



@pytest.fixture
def ingredients():
    response = requests.get(
        INGREDIENTS_URL,
        timeout=10
    )

    assert response.status_code == 200, (
        f"Не удалось получить ингредиенты: {response.text}"
    )

    ingredients_data = response.json()["data"]

    assert len(ingredients_data) >= 2, (
        "Недостаточно ингредиентов для создания заказа"
    )

    return [
        ingredients_data[0]["_id"],
        ingredients_data[1]["_id"]
    ]
