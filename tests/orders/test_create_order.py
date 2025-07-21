import pytest
import allure
from unittest.mock import patch

from data import ORDER_DATA_1, ORDER_DATA_2


@allure.suite("Создание заказа")
class TestCreateOrder:

    @allure.title("Успешное создание заказа — статус 201")
    @patch('methods.order_methods.OrderMethods.post_order', return_value=(201, {"id": 1}))
    def test_create_order_status(self, mock_post_order, courier, order_methods):
        status_code, _ = order_methods.post_order(id=courier[1])
        assert status_code == 201

    @allure.title("Успешное создание заказа — ответ содержит id")
    @patch('methods.order_methods.OrderMethods.post_order', return_value=(201, {"id": 1}))
    def test_create_order_response(self, mock_post_order, courier, order_methods):
        _, response = order_methods.post_order(id=courier[1])
        assert response == {"id": 1}

    @allure.title("Создание заказа с одним цветом — статус 201")
    @pytest.mark.parametrize("order_data", [ORDER_DATA_1, ORDER_DATA_2], ids=["BLACK", "GREY"])
    def test_create_order_single_color_status(self, courier, order_methods, order_data):
        status_code, _ = order_methods.post_order(params=order_data)
        assert status_code == 201

    @allure.title("Создание заказа с одним цветом — ответ содержит track")
    @pytest.mark.parametrize("order_data", [ORDER_DATA_1, ORDER_DATA_2], ids=["BLACK", "GREY"])
    def test_create_order_single_color_has_track(self, courier, order_methods, order_data):
        _, response = order_methods.post_order(params=order_data)
        assert "track" in response

    @allure.title("Создание заказа с двумя цветами — статус 201")
    def test_create_order_two_colors_status(self, courier, order_methods):
        data = {"color": ["BLACK", "GREY"], "metro": "Киевская"}
        status_code, _ = order_methods.post_order(params=data)
        assert status_code == 201

    @allure.title("Создание заказа с двумя цветами — ответ содержит track")
    def test_create_order_two_colors_has_track(self, courier, order_methods):
        data = {"color": ["BLACK", "GREY"], "metro": "Киевская"}
        _, response = order_methods.post_order(params=data)
        assert "track" in response

    @allure.title("Создание заказа без указания цвета — статус 201")
    def test_create_order_no_color_status(self, courier, order_methods):
        data = {"metro": "Киевская"}
        status_code, _ = order_methods.post_order(params=data)
        assert status_code == 201

    @allure.title("Создание заказа без указания цвета — ответ содержит track")
    def test_create_order_no_color_has_track(self, courier, order_methods):
        data = {"metro": "Киевская"}
        _, response = order_methods.post_order(params=data)
        assert "track" in response
