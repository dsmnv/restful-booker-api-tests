import allure
import pytest
import shutil
import os
import requests
from utils.data_generator import get_booking_payload
from utils.assertions import assert_booking_equal

BASE_URL = 'https://restful-booker.herokuapp.com'


@pytest.fixture(scope='session', autouse=True)
def clean_reports():
    reports_dir = 'reports'
    if os.path.exists(reports_dir):
        shutil.rmtree(reports_dir)
    os.makedirs(reports_dir)


@pytest.fixture()
def base_url():
    return BASE_URL


@pytest.fixture()
def create_booking():
    payload = get_booking_payload()
    response = requests.post(f'{BASE_URL}/booking', json=payload)
    with allure.step('Бронирование создано'):
        assert response.status_code == 200
    data = response.json()
    booking = data['booking']
    with allure.step('Данные в бронирование записаны корректно'):
        assert_booking_equal(payload, booking)
    return {
        'id': data['bookingid'],
        'payload': payload
    }


@pytest.fixture()
def auth_token():
    auth_data = {
        'username': 'admin',
        'password': 'password123'
    }
    response = requests.post(f'{BASE_URL}/auth', json=auth_data)
    assert response.status_code == 200
    data = response.json()
    token = data['token']
    return token

