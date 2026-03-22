from helpers.storage.helper import hex_uuid5


def test_uuid5():
    assert hex_uuid5("https://tour.ibon.com.tw/event/69006c6b4d7ea70aea213694") == "43113c8037145e8eae95e4096a8c528a"
