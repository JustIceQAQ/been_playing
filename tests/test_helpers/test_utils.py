from app.exhibition.twtc.utils import get_next_element


def test_get_next_element():
    assert get_next_element([1, 2, 3], 1) == 2
    assert get_next_element([1, 2, 3], 2) == 3
    assert get_next_element([1, 2, 3], 3) == 1


class QQ:
    def __init__(
        self,
        a: int,
    ):
        self.a = a

    def __hash__(self):
        return hash(self.a)

    def __eq__(self, other):
        if isinstance(other, QQ):
            return self.a == other.a
        return False


def test_hash():
    aa = QQ(1)
    bb = QQ(2)
    cc = QQ(1)
    ll = [aa, bb, cc]
    print(set(ll))
