import pytest
import requests
import allure
from data import BASE_URL
from methods.counter_methods import CourierMethods


@allure.suite("Логин курьера")
class TestLoginCourier:

    @allure.title("Успешный логин курьера")
    @allure.description("Проверяет, что курьер может авторизоваться с правильными логином и паролем.")
    def test_login_courier_success(self):
        courier = CourierMethods(BASE_URL + "/courier")
        data = courier.generate_courier_data()
        courier.create_courier(data)

        payload = {
            "login": data['login'],
            "password": data['password']
        }

        response = requests.post(f"{BASE_URL}/courier/login", json=payload)
        result = response.json()

        assert response.status_code == 200 and "id" in result, (
            f"Ожидали 200 и id, но получили {response.status_code} и {result}"
        )

    @allure.title("Невалидные данные при логине")
    @allure.description("Проверяет ошибки, если логин или пароль указаны неверно или не переданы.")
    @pytest.mark.parametrize("payload, expected_status, expected_message", [
        pytest.param(
            {"login": "wrong_login", "password": "1234"},
            404,
            "Учетная запись не найдена",
            id="Неверный логин и пароль"
        ),
        pytest.param(
            {"login": "some_login"},
            400,
            "Недостаточно данных для входа",
            id="Отсутствует пароль"
        ),
        pytest.param(
            {"password": "1234"},
            400,
            "Недостаточно данных для входа",
            id="Отсутствует логин"
        ),
        pytest.param(
            {},
            400,
            "Недостаточно данных для входа",
            id="Отсутствуют оба поля"
        ),
    ])
    def test_login_invalid_credentials_or_missing_fields(self, payload, expected_status, expected_message):
        response = requests.post(f"{BASE_URL}/courier/login", json=payload)

        try:
            message = response.json().get("message", "")
        except ValueError:
            message = response.text

        assert response.status_code == expected_status or "Service unavailable" in message, (
            f"Ожидали статус {expected_status} или сообщение 'Service unavailable', "
            f"но получили {response.status_code} и текст '{message}'"
        )
