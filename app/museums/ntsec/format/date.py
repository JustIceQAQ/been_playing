import re

import bs4


def _normalize_year(year: int) -> int:
    return year + 1911 if year < 1000 else year


def _parse_chinese_date_range(text: str) -> str | None:
    matches = re.findall(r"(\d{2,4})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日", text)
    if len(matches) >= 2:
        y0, m0, d0 = [int(x) for x in matches[0]]
        y1, m1, d1 = [int(x) for x in matches[1]]
        start = f"{_normalize_year(y0)}-{m0:02d}-{d0:02d}"
        end = f"{_normalize_year(y1)}-{m1:02d}-{d1:02d}"
        return f"{start} ~ {end}"
    if len(matches) == 1:
        y, m, d = [int(x) for x in matches[0]]
        start = f"{_normalize_year(y)}-{m:02d}-{d:02d}"
        return f"{start} ~" if "起" in text else start
    return None


def try_except(func, value):
    try:
        return func(value)
    except Exception:
        return None


def _parse_date_range(text: str) -> str | None:
    matches = re.findall(r"(\d{4})[/\-.](\d{1,2})[/\-.](\d{1,2})", text)
    if len(matches) >= 2:
        start = "{}-{:02d}-{:02d}".format(*[int(x) for x in matches[0]])
        end = "{}-{:02d}-{:02d}".format(*[int(x) for x in matches[1]])
        return f"{start} ~ {end}"
    if len(matches) == 1:
        start = "{}-{:02d}-{:02d}".format(*[int(x) for x in matches[0]])
        return start
    return None


def date_case_1(soup: bs4.BeautifulSoup) -> str | None:
    for strong in soup.select("div.newsin-text strong"):
        if "展覽時間" in strong.text:
            sibling = strong.parent.next_sibling
            if sibling:
                text = sibling.strip() if isinstance(sibling, str) else sibling.get_text(strip=True)
                return _parse_date_range(text)
    return None


def date_case_2(soup: bs4.BeautifulSoup) -> str | None:
    target = soup.select_one("div.newsin-text")
    if target is None:
        return None
    for line in target.get_text("\n").split("\n"):
        if "展覽期間" in line:
            return _parse_chinese_date_range(line.split("：")[-1].strip())
    return None


def date_case_3(soup: bs4.BeautifulSoup) -> str | None:
    for p in soup.select("div.newsin-text p"):
        if "展覽日期" in p.text:
            for span in p.find_all("span"):
                if "展覽日期" in span.text:
                    sibling = span.next_sibling
                    if sibling:
                        text = sibling.strip() if isinstance(sibling, str) else sibling.get_text(strip=True)
                        return _parse_chinese_date_range(text)
    return None


def date_case_4(soup: bs4.BeautifulSoup) -> str | None:
    for h3 in soup.select("div.newsin-text h3"):
        if "展覽日期" in h3.text:
            p = h3.find_next_sibling("p")
            if p:
                return _parse_chinese_date_range(p.get_text(strip=True))
    return None


def date_case_5(soup: bs4.BeautifulSoup) -> str | None:
    for p in soup.select("div.newsin-text p"):
        if "展覽日期" in p.text and "｜" in p.text:
            for line in p.decode_contents().split("<br/>"):
                if "展覽日期" in line:
                    sub_soup = bs4.BeautifulSoup(line, "html.parser")
                    text = sub_soup.get_text()
                    if "｜" in text:
                        return _parse_chinese_date_range(text.split("｜")[1].strip())
    return None


def get_page_date(soup: bs4.BeautifulSoup) -> str | None:
    result = try_except(date_case_1, soup)
    if result is not None:
        return result
    result = try_except(date_case_2, soup)
    if result is not None:
        return result
    result = try_except(date_case_3, soup)
    if result is not None:
        return result
    result = try_except(date_case_4, soup)
    if result is not None:
        return result
    result = try_except(date_case_5, soup)
    if result is not None:
        return result
    return None
