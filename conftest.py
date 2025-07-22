import pytest
from data import BASE_URL, COURIERS_URL, ORDERS_URL
from methods.counter_methods import CourierMethods
from methods.order_methods import OrderMethods


@pytest.fixture()
def courier_methods():
    return CourierMethods(url=f'{BASE_URL}{COURIERS_URL}')

@pytest.fixture()
def order_methods():
    return OrderMethods(url=f'{BASE_URL}{ORDERS_URL}')

@pytest.fixture(autouse=True)
def setup_valid_courier(courier_methods):
    """Создание валидного курьера перед тестами, где нужен курьер"""
    data = courier_methods.generate_courier_data()
    courier_methods.create_courier(data)
