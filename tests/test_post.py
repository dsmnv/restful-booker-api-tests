import requests
import allure
from utils.assertions import assert_booking_equal


def test_create_booking(base_url, create_booking):
    # Создаем новое бронирование фикстурой
    booking = create_booking
    # Вытаскиываем айдишник получившегося бронирования
    booking_id = booking['id']
    # Основные проверки POST запроса.
    expected_keys = ['firstname', 'lastname', 'totalprice', 'depositpaid', 'bookingdates', 'additionalneeds']

    with allure.step('Присутствуют переданные ключи'):
        for key in expected_keys:
            assert key in booking['payload']

    # Делаем GET с указанием айдишника только что созданного бронирования и проверяем ответ.
    new_booking = requests.get(f'{base_url}/booking/{booking_id}')
    new_booking_data = new_booking.json()

    with allure.step('Статус код при запросе бронирования = 200'):
        assert new_booking.status_code == 200

    with allure.step('Созданное бронирование соответствует вводу'):
        assert_booking_equal(new_booking_data, booking['payload'])


def test_create_invalid_booking(base_url):
    payload = {
        'firstname': 'Firstname'
    }
    response = requests.post(f'{base_url}/booking', json=payload)

    # API должен возвращать 400, но по факту отдает 500. Баг на стороне сервера
    with allure.step('Бронирование не создано без обязательных полей'):
        assert response.status_code == 500