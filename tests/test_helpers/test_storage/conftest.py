import pytest
from faker import Faker


@pytest.fixture(scope="function")
def fake_exhibition_data() -> dict:
    fake = Faker()
    return {
        "title": fake.paragraph(),
        "date": fake.date(),
        "address": fake.address(),
        "figure": fake.image_url(),
        "source_url": fake.uri(),
    }


@pytest.fixture(scope="function")
def fake_exhibition_information() -> dict:
    fake = Faker()
    return {
        "fullname": fake.name(),
        "code_name": fake.name(),
        "external_link": fake.uri(),
    }
