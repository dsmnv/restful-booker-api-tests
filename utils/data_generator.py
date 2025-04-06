from faker import Faker
import random
fake = Faker()


def get_booking_payload():
    firstname = fake.first_name()
    lastname = fake.last_name()
    totalprice = fake.random_int(10, 3000)
    depositpaid = fake.boolean()
    bookingdates = {
        'checkin': '2018-01-01',
        'checkout': "2019-01-01"
    }
    additionalneeds = random.choice(['Breakfast', 'SeaView', 'All Inclusive'])

    return {
        'firstname': firstname,
        'lastname': lastname,
        'totalprice': totalprice,
        'depositpaid': depositpaid,
        'bookingdates': bookingdates,
        'additionalneeds': additionalneeds
    }

