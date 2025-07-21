import allure
import requests
import random
import string


class CourierMethods:

    def __init__(self, url):
        self.url = url

    @allure.step("Создать курьера")
    def create_courier(self, params=None):
        if params is None:
            params = self.generate_courier_data()
        response = requests.post(self.url, json=params)

        return response.json(), response.status_code

    def get_courier(self, name, lastname):
        response = requests. get(f'{self.url}id')
        return response.status_code

    @staticmethod
    def generate_courier_data():
        def random_string(length=8):
            return ''.join(random.choices(string.ascii_letters, k=length))

        return {
            "login": random_string(),
            "password": random_string(),
            "firstName": random_string()
        }

    @allure.step("Логин курьера")
    def login(self, login, password):
        payload = {"login": login, "password": password}
        response = requests.post(f"{self.url}/login", json=payload)
        return response.json().get("id")

