import json
import pytest
import allure
from utils.assertions import assert_booking_structure_is_valid
from utils.api_client import get_booking


@allure.title('Получение бронирования по ID')
@allure.description('''
Тест создает новое бронирование, затем запрашивает его через GET и проверяет ответ на наличие
обязательных полей, на пустоту и сверяет тип данных. 
''')
@allure.feature('Booking API')
@allure.story('GET /booking')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.positive()
def test_get_booking_by_id(base_url, prepared_booking):
    # Создаем новое бронирование, которое запросим через GET для проверок.
    booking = prepared_booking
    booking_id = booking['id']

    # Основные проверки GET запроса.
    response = get_booking(base_url, booking_id)
    data = response.json()
    expected_keys = ['firstname', 'lastname', 'totalprice', 'depositpaid', 'bookingdates', 'additionalneeds']

    with allure.step('Проверка успешного ответа от GET /booking'):
        assert response.status_code == 200

    with allure.step('Присутствуют переданные ключи'):
        for key in expected_keys:
            assert key in data

    with allure.step('Дата выезда после даты заселения'):
        assert data['bookingdates']['checkin'] < data['bookingdates']['checkout']

    with allure.step('Поля имею валидные значения'):
        assert_booking_structure_is_valid(data)
        allure.attach(str(booking_id), name='Booking ID', attachment_type=allure.attachment_type.TEXT)
        allure.attach(
            json.dumps(data, indent=2),
            name='Полученные данные по бронированию',
            attachment_type=allure.attachment_type.JSON
        )


@allure.title('Получение бронирования по невалидному ID')
@allure.description('''
Тест получает список всех ID для существующих бронирований, добавляет к нему 100 и пытается 
обратиться к бронированию по ID+100.  
''')
@allure.feature('Booking API')
@allure.story('GET /booking')
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.negative()
def test_get_booking_by_invalid_id(base_url, booking_id_list):
    # Получаем список всех айдишников, находим максимальный и накидываем к нему 10
    data = booking_id_list
    max_id = max(item['bookingid'] for item in data) + 100

    with allure.step('Несуществующий id возвращает 404'):
        response = get_booking(base_url, max_id)
        assert response.status_code == 404
        allure.attach(str(max_id), name='Booking ID', attachment_type=allure.attachment_type.TEXT)
