import requests
import pytest
import allure
from utils.assertions import assert_booking_structure_is_valid, assert_booking_equal
from utils.data_generator import get_booking_payload
from utils.api_client import get_booking, update_booking_put, update_booking_patch


@pytest.mark.positive()
def test_update_booking(base_url, auth_token, prepared_booking):
    # Генерю данные для заполнения бронирования и создаю его
    booking = prepared_booking
    payload = booking['payload']
    booking_id = booking['id']

    # Изменяю некоторые значения в изначальном payload, затем PUT Запрос на обновление данных
    payload['firstname'] = 'UpdatedName'
    payload['lastname'] = 'UpdatedLastName'
    payload['depositpaid'] = True
    response = update_booking_put(base_url, booking_id, payload, auth_token)
    assert response.status_code == 200

    # GET Обращаюсь к обновленному бронированию
    updated_response = get_booking(base_url, booking_id)
    updated_data = updated_response.json()

    assert updated_data['firstname'] == 'UpdatedName'
    assert updated_data['lastname'] == 'UpdatedLastName'
    assert updated_data['depositpaid'] == True
    assert_booking_structure_is_valid(updated_data)


@pytest.mark.negative()
def test_invalid_update_body(base_url, prepared_booking, auth_token):
    booking = prepared_booking
    booking_id = booking['id']

    payload = {
        'firstname': 'NewFirstname'
    }
    response = update_booking_put(base_url, booking_id, payload, auth_token)

    with allure.step('Бронирование не обновлено без обязательных полей'):
        assert response.status_code == 400


@pytest.mark.negative()
def test_update_booking_no_auth(base_url):
    payload = get_booking_payload()
    response = requests.put(f'{base_url}/booking/1', json=payload)

    with allure.step('Без токена ответ 403'):
        assert response.status_code == 403


# ------------------ PATCH ------------------


@pytest.mark.positive()
def test_partial_update_booking(base_url, prepared_booking, auth_token):
    booking = prepared_booking
    booking_id = booking['id']
    original_payload = booking['payload']
    expected_payload = original_payload.copy()
    expected_payload['firstname'] = 'NewName'

    update = {
        'firstname': 'NewName'
    }

    response = update_booking_patch(base_url, booking_id, update, auth_token)
    with allure.step('Бронирование частично обновлено'):
        assert response.status_code == 200

    updated_response = get_booking(base_url, booking_id)
    with allure.step('Обновленное бронирование получено'):
        assert updated_response.status_code == 200

    updated_data = updated_response.json()

    with allure.step('Бронирование обновлено корректно'):
        assert_booking_equal(updated_data, expected_payload)
