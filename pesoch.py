import requests
BASE_URL = 'https://restful-booker.herokuapp.com/booking/1'

response = requests.get(f'{BASE_URL}')
data = response.json()

print(data)