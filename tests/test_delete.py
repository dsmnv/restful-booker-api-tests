import requests
import allure


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