from app.exhibition.twtc.utils import get_next_element


def test_get_next_element():
    assert get_next_element([1, 2, 3], 1) == 2
    assert get_next_element([1, 2, 3], 2) == 3
    assert get_next_element([1, 2, 3], 3) == 1
