import allure
import requests
from utils.data_generator import get_booking_payload
from utils.assertions import assert_booking_structure_is_valid, assert_booking_equal


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


def test_create_booking(base_url):
    # Получаем данные для заполнения из data_generator
    payload = get_booking_payload()
    response = requests.post(f'{base_url}/booking', json=payload)
    data = response.json()
    # Вытаскиываем айдишник получившегося бронирования
    booking = data['booking']
    booking_id = data['bookingid']
    # Основные проверки POST запроса.
    expected_keys = ['firstname', 'lastname', 'totalprice', 'depositpaid', 'bookingdates', 'additionalneeds']

    with allure.step('Статус код при создании нового бронирования = 200'):
        assert response.status_code == 200

    with allure.step('Присутствуют переданные ключи'):
        for key in expected_keys:
            assert key in booking

    # Делаем GET с указанием айдишника только что созданного бронирования и проверяем ответ.
    new_booking = requests.get(f'{base_url}/booking/{booking_id}')
    new_booking_data = new_booking.json()

    with allure.step('Статус код при запросе бронирования = 200'):
        assert new_booking.status_code == 200

    with allure.step('Созданное бронирование соответствует вводу'):
        assert_booking_equal(new_booking_data, payload)


def test_update_booking(base_url, auth_token):
    # Генерю данные для заполнения бронирования и создаю его
    payload = get_booking_payload()
    new_booking = requests.post(f'{base_url}/booking', json=payload)
    new_booking_data = new_booking.json()
    new_booking_id = new_booking_data['bookingid']

    # PUT Запрос на обновление данных
    payload['firstname'] = 'UpdatedName'
    payload['lastname'] = 'UpdatedLastName'
    payload['depositpaid'] = True
    response = requests.put(f'{base_url}/booking/{new_booking_id}', json=payload, headers={
        'Cookie': f'token={auth_token}'
    })
    assert response.status_code == 200

    # GET Обращаюсь к обновленному бронированию
    updated_response = requests.get(f'{base_url}/booking/{new_booking_id}')
    updated_data = updated_response.json()

    assert updated_data['firstname'] == 'UpdatedName'
    assert updated_data['lastname'] == 'UpdatedLastName'
    assert updated_data['depositpaid'] == True
    assert_booking_structure_is_valid(updated_data)

def test_update_token_no_auth(base_url):
    payload = get_booking_payload()
    response = requests.put(f'{base_url}/booking/1', json=payload)

    with allure.step('Без токена ответ 403'):
        assert response.status_code == 403










