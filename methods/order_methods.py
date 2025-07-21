import allure
import requests

from json import JSONDecodeError
from data import BASE_URL, ORDERS_URL


class OrderMethods:

    def __init__(self,url=None):
        self.url = url

    @allure.step("Создание заказа")
    def post_order(self, params):
        response = requests.post(self.url, json=params)
        try:
            return response.status_code, response.json()
        except JSONDecodeError:
            return response.status_code, response.text

    @allure.step("Удаление заказа")
    def delete_order(self, id):
        response = requests.delete(f'{self.url}/{id}')
        return response.status_code, response

    @allure.step("Получение одного заказа по id")
    def get_order(self, id):
        response = requests.get(f'{self.url}/{id}')
        return response.status_code, response.json()

    @allure.step("Получение списка заказов")
    def get_orders(self):
        response = requests.get(self.url)
        return response.status_code, response.json()

    @allure.step("Проверка статуса ответа")
    def check_response(self, expected_value, response):
        return response.status_code == expected_value



