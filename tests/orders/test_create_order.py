import pytest
import allure
from data import ORDER_DATA_1, ORDER_DATA_2
from methods.order_methods import OrderMethods


@allure.suite("Создание заказа")
class TestCreateOrder:

    @allure.title("Успешное создание заказа")
    @allure.description("Проверяет, что заказ создается успешно: статус 201 и тело ответа содержит id или track.")
    def test_successful_order_creation(self, order_methods):
        payload = {"color": ["BLACK", "GREY"], "metro": "Киевская"}
        status_code, response = order_methods.post_order(params=payload)

        with allure.step("Проверка, что вернулся статус 201"):
            assert status_code == 201, f"Ожидали статус 201, получили {status_code}"

        with allure.step("Проверка, что тело ответа содержит track"):
            assert "track" in response, f"Ожидали ключ 'track' в ответе, получили {response}"

    @allure.title("Создание заказа с одним цветом — параметры BLACK и GREY")
    @allure.description("Проверка, что заказы с одним цветом создаются успешно")
    @pytest.mark.parametrize("order_data", [ORDER_DATA_1, ORDER_DATA_2], ids=["BLACK", "GREY"])
    def test_order_with_single_color(self, order_methods, order_data):
        status_code, response = order_methods.post_order(params=order_data)

        with allure.step("Проверка, что вернулся статус 201"):
            assert status_code == 201, f"Ожидали статус 201, получили {status_code}"

        with allure.step("Проверка, что тело ответа содержит track"):
            assert "track" in response, f"Ожидали ключ 'track' в ответе, получили {response}"

    @allure.title("Создание заказа без указания цвета")
    @allure.description("Проверка, что можно создать заказ без поля 'color'")
    def test_order_without_color(self, order_methods):
        data = {"metro": "Киевская"}
        status_code, response = order_methods.post_order(params=data)

        with allure.step("Проверка, что вернулся статус 201"):
            assert status_code == 201, f"Ожидали статус 201, получили {status_code}"

        with allure.step("Проверка, что тело ответа содержит track"):
            assert "track" in response, f"Ожидали ключ 'track' в ответе, получили {response}"
