import requests
import allure
from data import BASE_URL


@allure.suite("Получение списка заказов")
class TestGetOrders:

    @allure.title("Получение списка заказов — статус 200 и список в ответе")
    @allure.description("Проверяет, что ручка /orders возвращает статус 200 и содержит список заказов в теле ответа.")
    def test_get_orders_list(self):
        with allure.step("Отправка GET-запроса на /orders"):
            response = requests.get(f"{BASE_URL}/orders")
            assert response.status_code == 200, f"Ожидали статус 200, получили {response.status_code}"

        with allure.step("Проверка структуры ответа — наличие поля 'orders' и что это список"):
            body = response.json()
            assert "orders" in body, "Поле 'orders' не найдено в ответе"
            assert isinstance(body["orders"], list), "'orders' должен быть списком"
