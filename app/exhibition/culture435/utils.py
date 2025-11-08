import re
import datetime


def roc_to_ad(year):
    return year + 1911


def normalize_date(date_str):
    date_str = date_str.strip()

    m = re.match(r"(?P<y>\d{3})(?P<m>\d{1,2})[.](?P<d>\d{1,2})$", date_str)
    if m:
        y = roc_to_ad(int(m.group("y")))
        return y, int(m.group("m")), int(m.group("d"))

    m = re.match(r"(?P<y>\d{2,3})[./](?P<m>\d{1,2})[./](?P<d>\d{1,2})", date_str)
    if m:
        y = roc_to_ad(int(m.group("y")))
        return y, int(m.group("m")), int(m.group("d"))

    m = re.match(r"(?P<y>20\d{2})\D*(?P<m>\d{1,2})\D*(?P<d>\d{1,2})", date_str)
    if m:
        return int(m.group("y")), int(m.group("m")), int(m.group("d"))

    m = re.match(r"(?P<m>\d{1,2})\D*(?P<d>\d{1,2})", date_str)
    if m:
        return None, int(m.group("m")), int(m.group("d"))

    raise ValueError(f"無法解析日期: {date_str}")


def parse_range(s):
    s = re.sub(r"（.*?）|\(.*?\)", "", s)
    parts = re.split(r"[~－–\-]", s)
    if len(parts) != 2:
        raise ValueError(f"日期範圍格式錯誤: {s}")

    start_raw, end_raw = parts[0], parts[1]

    sy, sm, sd = normalize_date(start_raw)
    ey, em, ed = normalize_date(end_raw)
    if ey is None:
        ey = sy

    start_date = datetime.datetime(sy, sm, sd)
    end_date = datetime.datetime(ey, em, ed)

    return f"{start_date:%Y-%m-%d} ~ {end_date:%Y-%m-%d}"


def parse_range_with_location(s):
    s = s.strip()

    range_sep = r"[-–—―－~]"

    pattern = rf"([\d./年月日\s（）\(\)一二三四五六日]+{range_sep}[\d./年月日\s（）\(\)一二三四五六日]+)"

    m = re.search(pattern, s)
    if not m:
        print("DEBUG 無法匹配：", repr(s))
        raise ValueError(f"無法從字串擷取日期: {s}")

    date_part = m.group(1).strip()
    return parse_range(date_part)
