import pytest
import allure
import json
from utils.assertions import assert_booking_equal
from utils.api_client import get_booking, create_booking


@allure.title('Создание бронирования и валидация данных')
@allure.description('''
Тест создает новое бронирование, сохраняет его ID и переданные в него данные.
Обращается к бронированию по этому ID.
Проверяет, что переданные данные соответствуют записанным. 
''')
@allure.feature('Booking API')
@allure.story('POST /booking')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.positive()
def test_create_booking(base_url, prepared_booking):
    # Создаем новое бронирование фикстурой
    booking = prepared_booking
    # Вытаскиываем айдишник получившегося бронирования
    booking_id = booking['id']
    # Переданные в бронирование данные
    payload = booking['payload']
    # Делаем GET с указанием айдишника только что созданного бронирования и проверяем ответ.
    new_booking = get_booking(base_url, booking_id)
    # Полученные данные нового бронирования
    new_booking_data = new_booking.json()

    with allure.step('Статус код при запросе бронирования = 200'):
        assert new_booking.status_code == 200

    with allure.step('Созданное бронирование соответствует вводу'):
        assert_booking_equal(new_booking_data, payload)
        allure.attach(
            json.dumps(payload, indent=2, ensure_ascii=False),
            name='Переданные в бронирование данные',
            attachment_type=allure.attachment_type.JSON
        )

        allure.attach(
            json.dumps(new_booking_data, indent=2, ensure_ascii=False),
            name='Полученные данные по бронированию',
            attachment_type=allure.attachment_type.JSON
        )


@allure.title('Создание бронирования без обязательных полей')
@allure.description('''
Тест пытается создать бронирование без обязательных полей
''')
@allure.feature('Booking API')
@allure.story('POST /booking')
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.negative()
def test_create_invalid_booking(base_url):
    payload = {
        'firstname': 'Firstname'
    }
    response = create_booking(base_url, payload)

    # API должен возвращать 400, но по факту отдает 500. Баг на стороне сервера
    with allure.step('Бронирование не создано без обязательных полей, статус код = 500'):
        assert response.status_code == 500
        allure.attach(str(response.status_code), name='Код ответа', attachment_type=allure.attachment_type.TEXT)
