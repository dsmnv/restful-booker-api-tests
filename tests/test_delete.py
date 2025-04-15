import requests
import pytest
import allure
from utils.api_client import get_booking, delete_booking


@pytest.mark.positive()
def test_delete_booking(base_url, prepared_booking, auth_token):
    booking = prepared_booking
    booking_id = booking['id']

    response = delete_booking(base_url, booking_id, auth_token)
    with allure.step('Бронирование успешно'):
        assert response.status_code == 201

    updated_response = get_booking(base_url, booking_id)
    with allure.step('Удаленного бронирования нет в БД'):
        assert updated_response.status_code == 404


@pytest.mark.negative()
def test_delete_booking_no_auth(base_url):
    response = requests.delete(f'{base_url}/booking/1')

    with allure.step('Удаление без авторизации невозможно'):
        assert response.status_code == 403


@pytest.mark.negative()
def test_delete_nonexistent_booking(base_url, booking_id_list,auth_token):
    data = booking_id_list
    max_id = max(item['bookingid'] for item in data) + 100

    response = delete_booking(base_url, max_id, auth_token)

    # По REST должен быть 404, но принимаем как есть
    with allure.step('Невозможно удалить несуществующее бронирование'):
        assert response.status_code in [404, 405]