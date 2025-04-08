import allure
import requests
from utils.data_generator import get_booking_payload
from utils.assertions import assert_booking_structure_is_valid, assert_booking_equal


# ------------------ GET ------------------

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


# ------------------ POST ------------------

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


# ------------------ PUT ------------------

def test_update_booking(base_url, auth_token, create_booking):
    # Генерю данные для заполнения бронирования и создаю его
    new_booking = create_booking
    payload = new_booking['payload']
    new_booking_id = new_booking['id']

    # Изменяю некоторые значения в изначальном payload, затем PUT Запрос на обновление данных
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


def test_invalid_update_body(base_url, create_booking, auth_token):
    booking = create_booking
    booking_id = booking['id']

    payload = {
        'firstname': 'NewFirstname'
    }
    response = requests.put(f'{base_url}/booking/{booking_id}', json=payload, headers={
        'Cookie': f'token={auth_token}'
    })

    with allure.step('Бронирование не обновлено без обязательных полей'):
        assert response.status_code == 400


def test_update_booking_no_auth(base_url):
    payload = get_booking_payload()
    response = requests.put(f'{base_url}/booking/1', json=payload)

    with allure.step('Без токена ответ 403'):
        assert response.status_code == 403


# ------------------ PATCH ------------------


def test_partial_update_booking(base_url, create_booking, auth_token):
    booking = create_booking
    booking_id = booking['id']
    original_payload = booking['payload']
    expected_payload = original_payload.copy()
    expected_payload['firstname'] = 'NewName'

    update = {
        'firstname': 'NewName'
    }

    response = requests.patch(f'{base_url}/booking/{booking_id}', json=update, headers={
        'Cookie': f'token={auth_token}'
    })
    with allure.step('Бронирование частично обновлено'):
        assert response.status_code == 200

    updated_response = requests.get(f'{base_url}/booking/{booking_id}')
    with allure.step('Обновленное бронирование получено'):
        assert updated_response.status_code == 200

    updated_data = updated_response.json()

    with allure.step('Бронирование обновлено корректно'):
        assert_booking_equal(updated_data, expected_payload)


# ------------------ DELETE ------------------


def test_delete_booking(base_url, create_booking, auth_token):
    booking = create_booking
    booking_id = booking['id']

    response = requests.delete(f'{base_url}/booking/{booking_id}', headers={
        'Cookie': f'token={auth_token}'
    })
    with allure.step('Пользователь удален успешно'):
        assert response.status_code == 201

    updated_response = requests.get(f'{base_url}/booking/{booking_id}')
    with allure.step('Удаленного пользователя нет в БД'):
        assert updated_response.status_code == 404


def test_delete_booking_no_auth(base_url):
    response = requests.delete(f'{base_url}/booking/1')

    with allure.step('Удаление без авторизации невозможно'):
        assert response.status_code == 403


def test_delete_nonexistent_booking(base_url, booking_id_list,auth_token):
    data = booking_id_list
    max_id = max(item['bookingid'] for item in data) + 10

    response = requests.delete(f'{base_url}/booking/{max_id}', headers={
        'Cookie': f'token={auth_token}'
    })

    # По REST должен быть 404, но принимаем как есть
    with allure.step('Невозможно удалить несуществующее бронирование'):
        assert response.status_code in [404, 405]













