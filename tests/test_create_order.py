
import allure
import requests

from urls import CREATE_ORDER_URL, LOGIN_USER_URL


@allure.feature("Создание заказа")
@allure.title("Авторизованный пользователь может создать заказ")
def test_create_order_with_authorization(created_user, ingredients):
    login_data = {
        "email": created_user["email"],
        "password": created_user["password"]
    }

    with allure.step("Авторизоваться и получить токен"):
        login_response = requests.post(
            LOGIN_USER_URL,
            json=login_data,
            timeout=10
        )

        assert login_response.status_code == 200
        access_token = login_response.json()["accessToken"]

    with allure.step("Создать заказ с ингредиентами"):
        response = requests.post(
            CREATE_ORDER_URL,
            json={"ingredients": ingredients},
            headers={"Authorization": access_token},
            timeout=10
        )

    with allure.step("Проверить успешное создание заказа"):
        assert response.status_code == 200

        response_data = response.json()

        assert response_data["success"] is True
        assert "order" in response_data
        assert "number" in response_data["order"]



@allure.feature("Создание заказа")
@allure.title("Создание заказа без авторизации")
def test_create_order_without_authorization(ingredients):
    with allure.step("Отправить запрос без токена авторизации"):
        response = requests.post(
            CREATE_ORDER_URL,
            json={"ingredients": ingredients},
            timeout=10
        )

    with allure.step("Проверить успешное создание заказа"):
        assert response.status_code == 200

        response_data = response.json()

        assert response_data["success"] is True
        assert "order" in response_data
        assert "number" in response_data["order"]



@allure.feature("Создание заказа")
@allure.title("Нельзя создать заказ без ингредиентов")
def test_create_order_without_ingredients():
    with allure.step("Отправить запрос с пустым списком ингредиентов"):
        response = requests.post(
            CREATE_ORDER_URL,
            json={"ingredients": []},
            timeout=10
        )

    with allure.step("Проверить ошибку создания заказа"):
        assert response.status_code == 400

        response_data = response.json()

        assert response_data["success"] is False
        assert response_data["message"] == (
            "Ingredient ids must be provided"
        )



@allure.feature("Создание заказа")
@allure.title("Создание заказа с неверным хешем ингредиента")
def test_create_order_with_invalid_ingredient():
    with allure.step("Отправить запрос с неверным хешем"):
        response = requests.post(
            CREATE_ORDER_URL,
            json={"ingredients": ["invalid_ingredient_hash"]},
            timeout=10
        )

    with allure.step("Проверить ответ сервера"):
        assert response.status_code == 500


