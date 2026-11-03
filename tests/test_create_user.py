
import allure
import pytest
import requests

from helpers import generate_user_data
from urls import CREATE_USER_URL


@allure.feature("Создание пользователя")
class TestCreateUser:

    # Проверить успешное создание уникального пользователя
    @allure.title("Успешное создание уникального пользователя")
    def test_create_unique_user(self, user_registration_data):
        user_data, registration = user_registration_data

        with allure.step("Отправить запрос на регистрацию"):
            response = requests.post(
                CREATE_USER_URL,
                json=user_data,
                timeout=10
            )

            if response.status_code == 200:
                registration["access_token"] = response.json().get(
                    "accessToken"
                )

        with allure.step("Проверить успешную регистрацию"):
            assert response.status_code == 200

            response_data = response.json()

            assert response_data["success"] is True
            assert response_data["user"]["email"] == user_data["email"]
            assert response_data["user"]["name"] == user_data["name"]

    # Проверить запрет повторной регистрации пользователя
    @allure.title("Нельзя зарегистрировать пользователя повторно")
    def test_create_existing_user(self, created_user):
        with allure.step("Повторно зарегистрировать существующего пользователя"):
            response = requests.post(
                CREATE_USER_URL,
                json=created_user,
                timeout=10
            )

        with allure.step("Проверить ошибку повторной регистрации"):
            assert response.status_code == 403
            assert response.json()["success"] is False
            assert response.json()["message"] == "User already exists"

    # Проверить регистрацию без обязательного поля
    @allure.title(
        "Нельзя зарегистрироваться без обязательного поля: {missing_field}"
    )
    @pytest.mark.parametrize(
        "missing_field",
        ["email", "password", "name"]
    )
    def test_create_user_without_required_field(self, missing_field):
        user_data = generate_user_data()
        del user_data[missing_field]

        with allure.step(f"Отправить запрос без поля {missing_field}"):
            response = requests.post(
                CREATE_USER_URL,
                json=user_data,
                timeout=10
            )

        with allure.step("Проверить ошибку регистрации"):
            assert response.status_code == 403
            assert response.json()["success"] is False
            assert response.json()["message"] == (
                "Email, password and name are required fields"
            )
