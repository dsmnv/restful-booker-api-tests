import requests
import allure
from utils.assertions import assert_booking_structure_is_valid


def test_get_booking_by_id(base_url, create_booking):
    # Создаем новое бронирование, которое запросим через GET для проверок.
    booking = create_booking
    booking_id = booking['id']

    # Основные проверки GET запроса.
    response = requests.get(f'{base_url}/booking/{booking_id}')
    data = response.json()
    expected_keys = ['firstname', 'lastname', 'totalprice', 'depositpaid', 'bookingdates', 'additionalneeds']

    with allure.step('Статус код = 200'):
        assert response.status_code == 200

    with allure.step('Присутствуют переданные ключи'):
        for key in expected_keys:
            assert key in data

    with allure.step('Дата выезда после даты заселения'):
        assert data['bookingdates']['checkin'] < data['bookingdates']['checkout']

    with allure.step('Поля имею валидные значения'):
        assert_booking_structure_is_valid(data)


def test_get_booking_by_invalid_id(base_url, booking_id_list):
    # Получаем список всех айдишников, находим максимальный и накидываем к нему 10
    data = booking_id_list
    max_id = max(item['bookingid'] for item in data) + 10

    response = requests.get(f'{base_url}/booking/{max_id}')
    with allure.step('Несуществующий id возвращает 404'):
        assert response.status_code == 404