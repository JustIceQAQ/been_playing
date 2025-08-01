from bs4 import BeautifulSoup


def test_get_url():
    with open("TurboImage.html", "r", encoding="utf-8") as f:
        s = BeautifulSoup(f)
    img_code_ipms = s.select_one("#imgCodeIPMS")
    print(img_code_ipms.get("value").split("](")[1][:-1])
