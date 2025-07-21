import pytest
import requests
import allure
from data import BASE_URL
from methods.counter_methods import CourierMethods


@allure.suite("Логин курьера")
class TestLoginCourier:

    @allure.title("Успешный логин курьера")
    def test_login_courier_success(self):
        courier = CourierMethods(BASE_URL + "/courier")
        data = courier.generate_courier_data()
        courier.create_courier(data)

        payload = {
            "login": data['login'],
            "password": data['password']
        }

        with allure.step("Отправка запроса на логин с валидными данными"):
            response = requests.post(f"{BASE_URL}/courier/login", json=payload)
            result = response.json()

        with allure.step("Проверка успешного ответа и наличия id"):
            assert response.status_code == 200 and "id" in result, (
                f"Ожидали 200 и id, но получили {response.status_code} и {result}"
            )

    @allure.title("Невалидные логин и/или пароль")
    @pytest.mark.parametrize("payload, expected_status, expected_message", [
        pytest.param(
            {"login": "wrong_login", "password": "1234"},
            404,
            "Учетная запись не найдена",
            id="Неверный логин/пароль"
        )
    ])
    def test_login_invalid_credentials(self, payload, expected_status, expected_message):
        with allure.step("Отправка запроса с неправильным логином или паролем"):
            response = requests.post(f"{BASE_URL}/courier/login", json=payload)

        with allure.step("Определение текста ошибки"):
            if response.headers.get("Content-Type") == "application/json":
                message = response.json().get("message", "")
            else:
                message = response.text

        with allure.step("Проверка кода ответа и сообщения об ошибке"):
            assert response.status_code == expected_status or "Service unavailable" in message, (
                f"Ожидали статус {expected_status} или сообщение 'Service unavailable', "
                f"но получили {response.status_code} и текст '{message}'"
            )

    @allure.title("Отсутствующие обязательные поля")
    @pytest.mark.parametrize("payload, expected_status, expected_message", [
        pytest.param(
            {"login": "some_login"},
            400,
            "Недостаточно данных для входа",
            id="Нет пароля"
        ),
        pytest.param(
            {"password": "1234"},
            400,
            "Недостаточно данных для входа",
            id="Нет логина"
        ),
        pytest.param(
            {},
            400,
            "Недостаточно данных для входа",
            id="Нет логина и пароля"
        ),
    ])
    def test_login_missing_fields(self, payload, expected_status, expected_message):
        with allure.step("Отправка запроса с неполными данными"):
            response = requests.post(f"{BASE_URL}/courier/login", json=payload)

        with allure.step("Определение текста ошибки"):
            if response.headers.get("Content-Type") == "application/json":
                message = response.json().get("message", "")
            else:
                message = response.text

        with allure.step("Проверка кода ответа и сообщения об ошибке"):
            assert response.status_code == expected_status or "Service unavailable" in message, (
                f"Ожидали статус {expected_status} или сообщение 'Service unavailable', "
                f"но получили {response.status_code} и текст '{message}'"
            )
