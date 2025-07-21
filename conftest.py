import pytest
from data import BASE_URL, COURIERS_URL, ORDERS_URL
from methods.counter_methods import CourierMethods
from methods.order_methods import OrderMethods
from data import BASE_URL, COURIERS_URL, ORDERS_URL


@pytest.fixture()
def courier_methods():
    return CourierMethods(url=f'{BASE_URL}{COURIERS_URL}')

@pytest.fixture()
def order_methods():
    return OrderMethods(url=f'{BASE_URL}{ORDERS_URL}')

@pytest.fixture()
def courier():
    full_url = f"{BASE_URL}{COURIERS_URL}"
    courier_methods = CourierMethods(url=full_url)

    response_data, _ = courier_methods.create_courier()
    courier_id = response_data.get("id")

    yield courier_id, response_data, response_data

    if courier_id:
        courier_methods.delete_courier(courier_id)

def delete_courier(self, courier_id):
    return requests.delete(f"{self.url}/{courier_id}")

@pytest.fixture()
def authorize_courier(courier):
    response = CourierMethods().authorize_courier(courier[2])
    return response.json()['id']

@pytest.fixture(scope='function')
def collector():
    collector = BooksCollector()
    return collector

@pytest.fixture(scope='function')
def collector_w_book():
    collector = BooksCollector()
