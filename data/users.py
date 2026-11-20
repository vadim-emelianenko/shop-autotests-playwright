import uuid

from faker import Faker

fake = Faker()


def new_user() -> dict:
    """Unique user for one test, so parallel and repeated runs never collide."""
    first, last = fake.first_name(), fake.last_name()
    return {
        "name": f"{first} {last}",
        "email": f"qa.{uuid.uuid4().hex[:12]}@example.com",
        "password": uuid.uuid4().hex,
        "title": "Mr",
        "birth_date": "10",
        "birth_month": "5",
        "birth_year": "1995",
        "firstname": first,
        "lastname": last,
        "company": "Test Co",
        "address1": fake.street_address(),
        "address2": "",
        "country": "Canada",
        "zipcode": fake.postcode(),
        "state": fake.state(),
        "city": fake.city(),
        "mobile_number": fake.msisdn(),
    }
