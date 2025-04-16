from faker import Faker
from datetime import date, timedelta
import random
fake = Faker()


def get_booking_payload():
    checkin = date.today()
    checkout = checkin + timedelta(days=random.randint(1, 14))

    firstname = fake.first_name()
    lastname = fake.last_name()
    totalprice = fake.random_int(10, 3000)
    depositpaid = fake.boolean()
    bookingdates = {
        'checkin': checkin.isoformat(),
        'checkout': checkout.isoformat()
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

