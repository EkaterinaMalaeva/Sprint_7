import pytest
from data import BASE_URL, COURIERS_URL, ORDERS_URL
from methods.counter_methods import CourierMethods
from methods.order_methods import OrderMethods
# from data import BASE_URL, COURIERS_URL, ORDERS_URL


@pytest.fixture()
def courier_methods():
    return CourierMethods(url=f'{BASE_URL}{COURIERS_URL}')

@pytest.fixture()
def order_methods():
    return OrderMethods(url=f'{BASE_URL}{ORDERS_URL}')

# @pytest.fixture()
# def authorize_courier(courier):
#     response = CourierMethods().authorize_courier(courier[2])
#     return response.json()['id']

