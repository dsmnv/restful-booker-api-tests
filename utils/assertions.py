import allure


def assert_booking_structure_is_valid(data: dict):
    with allure.step('Проверка firstname'):
        assert isinstance(data['firstname'], str) and data['firstname'], "Invalid firstname"

    with allure.step('Проверка lastname'):
        assert isinstance(data['lastname'], str) and data['lastname'], "Invalid lastname"

    with allure.step('Проверка totalprice'):
        assert isinstance(data['totalprice'], int) and data['totalprice'] > 0, "Invalid totalprice"

    with allure.step('Проверка depositpaid'):
        assert isinstance(data['depositpaid'], bool), "Invalid depositpaid"

    with allure.step('Проверка bookingdates'):
        assert isinstance(data['bookingdates'], dict), "Invalid bookingdates format"

    with allure.step('Проверка checkin'):
        assert 'checkin' in data['bookingdates'], "Missing checkin"

    with allure.step('Проверка checkout'):
        assert 'checkout' in data['bookingdates'], "Missing checkout"


def assert_booking_equal(actual: dict, expected: dict):
    assert actual['firstname'] == expected['firstname']
    assert actual['lastname'] == expected['lastname']
    assert actual['totalprice'] == expected['totalprice']
    assert actual['depositpaid'] == expected['depositpaid']
    assert actual['bookingdates'] == expected['bookingdates']
    assert actual['additionalneeds'] == expected['additionalneeds']

