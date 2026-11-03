
import pytest
import requests

from helpers import generate_user_data
from urls import (
    CREATE_USER_URL,
    DELETE_USER_URL,
    INGREDIENTS_URL,
    LOGIN_USER_URL
)


# Создать тестового пользователя и удалить его после теста
@pytest.fixture
def created_user():
    user_data = generate_user_data()

    response = requests.post(
        CREATE_USER_URL,
        json=user_data,
        timeout=10
    )

    if response.status_code != 200:
        pytest.fail(
            f"Не удалось создать тестового пользователя: {response.text}"
        )

    access_token = response.json()["accessToken"]

    yield user_data

    requests.delete(
        DELETE_USER_URL,
        headers={"Authorization": access_token},
        timeout=10
    )


# Авторизовать созданного пользователя и получить токен
@pytest.fixture
def authorized_user(created_user):
    login_data = {
        "email": created_user["email"],
        "password": created_user["password"]
    }

    response = requests.post(
        LOGIN_USER_URL,
        json=login_data,
        timeout=10
    )

    if response.status_code != 200:
        pytest.fail(
            f"Не удалось авторизовать пользователя: {response.text}"
        )

    return response.json()["accessToken"]


# Получить идентификаторы ингредиентов для тестов
@pytest.fixture
def ingredients():
    response = requests.get(
        INGREDIENTS_URL,
        timeout=10
    )

    if response.status_code != 200:
        pytest.fail(
            f"Не удалось получить ингредиенты: {response.text}"
        )

    ingredients_data = response.json()["data"]

    if len(ingredients_data) < 2:
        pytest.fail(
            "Недостаточно ингредиентов для создания заказа"
        )

    return [
        ingredients_data[0]["_id"],
        ingredients_data[1]["_id"]
    ]


# Подготовить данные и удалить зарегистрированного пользователя после теста
@pytest.fixture
def user_registration_data():
    user_data = generate_user_data()
    registration = {"access_token": None}

    yield user_data, registration

    access_token = registration["access_token"]

    if access_token:
        requests.delete(
            DELETE_USER_URL,
            headers={"Authorization": access_token},
            timeout=10
        )
