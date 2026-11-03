
import allure
import requests

from urls import CREATE_ORDER_URL


@allure.feature("Создание заказа")
class TestCreateOrder:

    # Проверить создание заказа авторизованным пользователем
    @allure.title("Авторизованный пользователь может создать заказ")
    def test_create_order_with_authorization(self, authorized_user, ingredients):
        with allure.step("Создать заказ с ингредиентами"):
            response = requests.post(
                CREATE_ORDER_URL,
                json={"ingredients": ingredients},
                headers={"Authorization": authorized_user},
                timeout=10
            )

        with allure.step("Проверить успешное создание заказа"):
            assert response.status_code == 200

            response_data = response.json()

            assert response_data["success"] is True
            assert "order" in response_data
            assert "number" in response_data["order"]

    # Проверить создание заказа без авторизации
    @allure.title("Создание заказа без авторизации")
    def test_create_order_without_authorization(self, ingredients):
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

    # Проверить создание заказа без ингредиентов
    @allure.title("Нельзя создать заказ без ингредиентов")
    def test_create_order_without_ingredients(self):
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

    # Проверить создание заказа с неверным хешем ингредиента
    @allure.title("Создание заказа с неверным хешем ингредиента")
    def test_create_order_with_invalid_ingredient(self):
        with allure.step("Отправить запрос с неверным хешем"):
            response = requests.post(
                CREATE_ORDER_URL,
                json={"ingredients": ["invalid_ingredient_hash"]},
                timeout=10
            )

        with allure.step("Проверить ответ сервера"):
            assert response.status_code == 500
