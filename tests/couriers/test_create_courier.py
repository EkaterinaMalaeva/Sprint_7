import allure
import pytest
from methods.counter_methods import CourierMethods


@allure.feature("Курьеры")
class TestCourier:

    @allure.story("Создание курьера")
    @allure.title("Курьер создаётся успешно")
    @allure.description("Создание нового курьера с валидными данными возвращает статус 201")
    def test_create_courier_success_status(self, courier_methods):
        data = courier_methods.generate_courier_data()
        _, status = courier_methods.create_courier(data)
        assert status == 201, f"Ожидали статус 201, но получили {status}"

    @allure.story("Создание курьера")
    @allure.title("Ответ успешного создания содержит 'ok': true")
    @allure.description("Проверка, что в теле ответа при успешном создании есть {'ok': True}")
    def test_create_courier_success_response(self, courier_methods):
        data = courier_methods.generate_courier_data()
        response, _ = courier_methods.create_courier(data)
        assert response == {"ok": True}, f"Ожидали {{'ok': True}}, но получили {response}"

    @allure.story("Создание курьера")
    @allure.title("Нельзя создать дубликат логина — статус 409")
    @allure.description("Если дважды отправить одни и те же данные, должен вернуться статус 409")
    def test_create_duplicate_courier_status(self, courier_methods):
        data = courier_methods.generate_courier_data()
        courier_methods.create_courier(data)
        _, status = courier_methods.create_courier(data)
        assert status == 409, f"Ожидали статус 409, но получили {status}"

    @allure.story("Создание курьера")
    @allure.title("Нельзя создать дубликат логина — сообщение об ошибке")
    @allure.description("Проверка текста ошибки при создании курьера с уже занятым логином")
    def test_create_duplicate_courier_message(self, courier_methods):
        data = courier_methods.generate_courier_data()
        courier_methods.create_courier(data)
        response, _ = courier_methods.create_courier(data)
        assert response['message'] == "Этот логин уже используется. Попробуйте другой.", \
            f"Ожидали сообщение об ошибке, но получили: {response}"

    @allure.story("Создание курьера")
    @allure.title("Создание без поля {field} — ожидается статус {expected_status}")
    @allure.description("Проверка обязательных и необязательных полей при создании курьера")
    @pytest.mark.parametrize("field, expected_status", [
        ("login", 400),
        ("password", 400),
        ("firstName", 201),  # firstName — необязательное поле
    ])
    def test_create_courier_without_field_status(self, courier_methods, field, expected_status):
        data = courier_methods.generate_courier_data()
        data.pop(field)
        _, status = courier_methods.create_courier(data)
        assert status == expected_status, f"Ожидали статус {expected_status} при отсутствии поля {field}, но получили {status}"
