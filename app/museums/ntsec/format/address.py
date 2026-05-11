import re

import bs4


def try_except(func, value):
    try:
        return func(value)
    except Exception:
        return None


def address_case_1(soup: bs4.BeautifulSoup):
    p_tag = soup.select("div.newsin-text > p")
    target_tag = None
    for p in p_tag:
        if "展覽地點" in p.text:
            target_tag = p
            break
    if target_tag is None:
        return None
    lines = target_tag.decode_contents().split("<br/>")
    location = None
    for line in lines:
        if "展覽地點" in line:
            sub_soup = bs4.BeautifulSoup(line, "html.parser")
            if "｜" in sub_soup.text:
                location = sub_soup.text.split("｜")[1].strip()
            else:
                location = sub_soup.find("span").text
            break
    return location


def address_case_2(soup: bs4.BeautifulSoup) -> str | None:
    location = None
    for p in soup.select("div.newsin-text p"):
        if "展覽地點" in p.text:
            lines = p.text.split("\n")
            for line in lines:
                if "展覽地點" in line:
                    location = line.split("：")[-1].strip()
                    break
    return location


def address_case_3(soup: bs4.BeautifulSoup) -> str | None:
    target_tag = None
    for h3 in soup.select("div.newsin-text h3"):
        if "展出地點" in h3.text:
            target_tag = h3
            break
    if target_tag is None:
        return None

    location = target_tag.next_sibling.next_sibling
    return location.text.strip()


def address_case_4(soup: bs4.BeautifulSoup) -> str | None:
    target_tag = None
    for span in soup.select("div.newsin-text span"):
        if "展出地點" in span.text:
            target_tag = span
            break
    if target_tag is None:
        return None
    location = target_tag.next_sibling
    return location.text.strip()


def address_case_5(soup: bs4.BeautifulSoup) -> str | None:
    for strong in soup.select("div.newsin-text strong"):
        if "展覽地點" in strong.text:
            sibling = strong.parent.next_sibling
            if sibling:
                text = sibling.strip() if isinstance(sibling, str) else sibling.get_text(strip=True)
                if text:
                    return text
    return None


def address_case_6(soup: bs4.BeautifulSoup) -> str | None:
    target = soup.select_one("div.newsin-text")
    if target is None:
        return None
    for line in target.get_text("\n").split("\n"):
        if "展出地點" in line:
            match = re.search(r"（(.+?)）", line)
            if match:
                return match.group(1)
            location = line.split("：")[-1].strip()
            return location if location else None
    return None


def address_case_7(soup: bs4.BeautifulSoup) -> str | None:
    for h3 in soup.select("div.newsin-text h3"):
        if "展覽地點" in h3.text:
            p = h3.find_next_sibling("p")
            if p:
                return p.get_text(strip=True)
    return None


def get_page_address(soup: bs4.BeautifulSoup) -> str | None:
    result = try_except(address_case_1, soup)
    if result is not None:
        return result
    result = try_except(address_case_2, soup)
    if result is not None:
        return result
    result = try_except(address_case_3, soup)
    if result is not None:
        return result
    result = try_except(address_case_4, soup)
    if result is not None:
        return result
    result = try_except(address_case_5, soup)
    if result is not None:
        return result
    result = try_except(address_case_6, soup)
    if result is not None:
        return result
    result = try_except(address_case_7, soup)
    if result is not None:
        return result
    return None
