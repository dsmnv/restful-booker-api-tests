import requests


def get_booking(base_url: str, booking_id: int) -> requests.Response:
    return requests.get(f'{base_url}/booking/{booking_id}')


def create_booking(base_url: str, payload: dict) -> requests.Response:
    return requests.post(f'{base_url}/booking', json=payload)


def update_booking_put(base_url: str, booking_id: int, payload: dict, token: str) -> requests.Response:
    return requests.put(f'{base_url}/booking/{booking_id}', json=payload, headers={
        'Cookie': f'token={token}'
    })


def update_booking_patch(base_url: str, booking_id: int, payload: dict, token: str) -> requests.Response:
    return requests.patch(f'{base_url}/booking/{booking_id}', json=payload, headers={
        'Cookie': f'token={token}'
    })


def delete_booking(base_url: str, booking_id: int, token:str) -> requests.Response:
    return requests.delete(f'{base_url}/booking/{booking_id}', headers={
        'Cookie': f'token={token}'
    })


def authorization(base_url: str, auth_data: dict):
    return requests.post(f'{base_url}/auth', json=auth_data)


