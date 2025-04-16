import json
import requests
import pytest
import allure
from utils.assertions import assert_booking_structure_is_valid, assert_booking_equal
from utils.data_generator import get_booking_payload
from utils.api_client import get_booking, update_booking_put, update_booking_patch


@allure.title('Обновление существующего бронирования')
@allure.description('''
Тест создает новое бронирование, сохраняет его ID и переданные в него данные.
Обращается к бронированию по этому ID.
Проверяет, что переданные данные соответствуют записанным. 
''')
@allure.feature('Booking API')
@allure.story('PUT /booking')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.positive()
def test_update_booking(base_url, auth_token, prepared_booking):
    # Генерю данные для заполнения бронирования и создаю его
    booking = prepared_booking
    payload = booking['payload']
    booking_id = booking['id']

    # Изменяю некоторые значения в изначальном payload, затем PUT Запрос на обновление данных
    updated_payload = payload.copy()
    updated_payload['firstname'] = 'UpdatedName'
    updated_payload['lastname'] = 'UpdatedLastName'
    updated_payload['depositpaid'] = True
    response = update_booking_put(base_url, booking_id, updated_payload, auth_token)

    with allure.step('Бронирование обновлено успешно, статус код = 200'):
        assert response.status_code == 200

    # GET Обращаюсь к обновленному бронированию
    updated_response = get_booking(base_url, booking_id)
    updated_data = updated_response.json()

    with allure.step('Обновлены только нужные данные'):
        assert updated_data['firstname'] == 'UpdatedName'
        assert updated_data['lastname'] == 'UpdatedLastName'
        assert updated_data['depositpaid'] == True
        allure.attach(
            json.dumps(payload, indent=2, ensure_ascii=False),
            name='Данные созданного бронирования',
            attachment_type=allure.attachment_type.JSON
        )
        allure.attach(
            json.dumps(updated_payload, indent=2, ensure_ascii=False),
            name='Данные, которыми обновляем бронирование',
            attachment_type=allure.attachment_type.JSON
        )
        assert_booking_structure_is_valid(updated_data)
        allure.attach(
            json.dumps(updated_data, indent=2, ensure_ascii=False),
            name='Данные в обновленном бронировании',
            attachment_type=allure.attachment_type.JSON
        )


@allure.title('Обновление бронирования с невалидным телом запроса')
@allure.description('''
Тест пытается обновить бронирование методом PUT с передачей не полного Body.
''')
@allure.feature('Booking API')
@allure.story('PUT /booking')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.negative()
def test_invalid_update_body(base_url, prepared_booking, auth_token):
    booking = prepared_booking
    booking_id = booking['id']

    payload = {
        'firstname': 'NewFirstname'
    }
    response = update_booking_put(base_url, booking_id, payload, auth_token)

    with allure.step('Бронирование не обновлено без обязательных полей, статус код = 400'):
        assert response.status_code == 400


@allure.title('Обновление бронирования без авторизации')
@allure.description('''
Тест пытается обновить бронирование без авторизационного токена
''')
@allure.feature('Booking API')
@allure.story('PUT /booking')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.negative()
def test_update_booking_no_auth(base_url):
    payload = get_booking_payload()
    response = requests.put(f'{base_url}/booking/1', json=payload)

    with allure.step('Без токена ответ 403'):
        assert response.status_code == 403


# ------------------ PATCH ------------------


@allure.title('Частичное обновление бронирования')
@allure.description('''
Тест создает новое бронирование, сохраняет его данные и тело запроса. 
Обновляет это бронирование с передачей только одного поля firstname
Проверяет, что обновление прошло успешно и fistname соответствует обновленному. 
''')
@allure.feature('Booking API')
@allure.story('PATCH /booking')
@allure.severity(allure.severity_level.CRITICAL)
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
    with allure.step('Бронирование обновлено'):
        assert response.status_code == 200

    updated_response = get_booking(base_url, booking_id)
    with allure.step('Обновленное бронирование получено'):
        assert updated_response.status_code == 200

    updated_data = updated_response.json()

    with allure.step('Бронирование обновлено корректно'):
        assert_booking_equal(updated_data, expected_payload)

        allure.attach(
            json.dumps(original_payload, indent=2, ensure_ascii=False),
            name='Данные созданного бронирования',
            attachment_type=allure.attachment_type.JSON
        )
        allure.attach(
            json.dumps(update, indent=2, ensure_ascii=False),
            name='Данные, которыми обновляем бронирование',
            attachment_type=allure.attachment_type.JSON
        )
        allure.attach(
            json.dumps(updated_data, indent=2, ensure_ascii=False),
            name='Данные в обновленном бронировании',
            attachment_type=allure.attachment_type.JSON
        )


