import pytest
from faker import Faker


@pytest.fixture(scope="function")
def fake_dict() -> dict:
    fake = Faker()
    return {
        "title": fake.paragraph(),
        "date": fake.date(),
        "address": fake.address(),
        "figure": fake.image_url(),
        "source_url": fake.uri(),
    }
