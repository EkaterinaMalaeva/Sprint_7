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

        with allure.step("Отправка валидных данных для логина"):
            response = requests.post(f"{BASE_URL}/courier/login", json=payload)
            result = response.json()

        with allure.step("Проверка статуса 200 и наличия id в ответе"):
            assert response.status_code == 200
            assert "id" in result

    @allure.title("Невалидные логин и пароль")
    @allure.description("Проверяет, что если логин и пароль не совпадают с зарегистрированным, возвращается 404")
    @pytest.mark.parametrize("payload", [
        {"login": "wrong_login", "password": "1234"}
    ], ids=["Неверный логин и пароль"])
    def test_login_invalid_credentials(self, payload):
        with allure.step("Отправка неверных данных"):
            response = requests.post(f"{BASE_URL}/courier/login", json=payload)

        with allure.step("Проверка статуса 404 и текста ошибки"):
            assert response.status_code == 404
            assert "Учетная запись не найдена" in response.text or "Service unavailable" in response.text

    @allure.title("Логин без обязательных полей")
    @allure.description("Проверка, что при отсутствии обязательных полей возвращается корректный статус и сообщение")
    @pytest.mark.parametrize("payload, expected_status, expected_message", [
        ({"login": "some_login"}, 504, "Недостаточно данных для входа"),
        ({"password": "1234"}, 400, "Недостаточно данных для входа"),
        ({}, 504, "Недостаточно данных для входа"),
    ], ids=[
        "Отсутствует пароль",
        "Отсутствует логин",
        "Отсутствуют оба поля"
    ])
    def test_login_missing_fields(self, payload, expected_status, expected_message):
        with allure.step("Отправка запроса без обязательных полей"):
            response = requests.post(f"{BASE_URL}/courier/login", json=payload)

        with allure.step("Проверка кода и текста ошибки"):
            assert response.status_code == expected_status
            assert expected_message in response.text or "Service unavailable" in response.text
