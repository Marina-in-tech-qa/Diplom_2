
import allure
import requests
import pytest

from urls import LOGIN_USER_URL


@allure.feature("Авторизация пользователя")
@allure.title("Успешный вход зарегистрированного пользователя")
def test_login_existing_user(created_user):
    login_data = {
        "email": created_user["email"],
        "password": created_user["password"]
    }

    with allure.step("Отправить запрос на авторизацию"):
        response = requests.post(
            LOGIN_USER_URL,
            json=login_data,
            timeout=10
        )

    with allure.step("Проверить успешную авторизацию"):
        assert response.status_code == 200

        response_data = response.json()

        assert response_data["success"] is True
        assert response_data["user"]["email"] == created_user["email"]
        assert "accessToken" in response_data
        assert "refreshToken" in response_data



@allure.feature("Авторизация пользователя")
@allure.title("Ошибка входа с неверными данными: {invalid_field}")
@pytest.mark.parametrize(
    "invalid_field",
    ["email", "password"]
)
def test_login_with_invalid_credentials(created_user, invalid_field):
    login_data = {
        "email": created_user["email"],
        "password": created_user["password"]
    }

    login_data[invalid_field] = "incorrect_value"

    with allure.step(f"Авторизоваться с неверным полем {invalid_field}"):
        response = requests.post(
            LOGIN_USER_URL,
            json=login_data,
            timeout=10
        )

    with allure.step("Проверить отказ в авторизации"):
        assert response.status_code == 401

        response_data = response.json()

        assert response_data["success"] is False
        assert response_data["message"] == "email or password are incorrect"


