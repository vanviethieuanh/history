import json
import re

VOLUME_PATTERN = re.compile(
    r'^Quyển\s([I|V|X]+)\s?$',
    re.MULTILINE
)
RECORD_PATTERN = re.compile(
    r'^(Kỷ(?! (Sửu|Mão|Tỵ|Mùi|Dậu|Hợi|cương)).*)',
    re.MULTILINE
)
YEAR_PATTERN = re.compile(
    r'^(?P<can>Giáp|Ất|Bính|Đinh|Mậu|Kỷ|Canh|Tân|Nhâm|Quý) (?P<chi>Tý|Sửu|Dần|Mão|Thìn|Tỵ|Ngọ|Mùi|Thân|Dậu|Tuất|Hợi)(?P<des>.*?)[\[|\(](?P<year>\d+.*?)[\]|\)](?P<cn_year>,\s\(.+? năm thứ \d+(.|\n)*?\))*',
    re.MULTILINE | re.IGNORECASE
)
REGNAL_YEAR_PATTERN = re.compile(
    r'^[\[\/\(]?(?P<regnal_name>.*?)[\[\/\(]?\s*năm\s*thứ (?P<year>\d+)',
    re.MULTILINE
)
PAGE_PATTERN = re.compile(
    r"^(?P<page>\d+)\s+Đại Việt Sử Ký Toàn Thư \- (?P<records>.+) \- (?P<volume>.+)"
)


def split_records(record_path: str):
    data_file = open(record_path, "r", encoding="utf-8")
    FILE_CONTENT = data_file.read()
    res = re.split(VOLUME_PATTERN, FILE_CONTENT)[1:]

    RESULT = []

    i = 1
    while i < len(res):
        volume = res[i]
        i += 2
        RESULT.append(split_volume(volume))

    return RESULT


def split_volume(volume):
    result = re.split(RECORD_PATTERN, volume)

    result = [r for r in result if r]
    result = [r.strip() for r in result]
    result = [re.sub(r'\[\d{1,}[a-z]{1}\]', '', r) for r in result]
    result = [r.strip() for r in result]
    result = [r for r in result if r]

    records = []

    i = 0
    while i < len(result):
        record = result[i]

        record_name = re.search(RECORD_PATTERN, record)
        if record_name:
            records.append({
                'name': record_name.string,
                'content': split_record(result[i+1])
            })
            i += 2
        else:
            records.append({
                'name': None,
                'content': split_record(record)
            })
            i += 1
    return records


def split_record(record):
    events = []
    last_start = -1

    for m in re.finditer(YEAR_PATTERN, record):
        event_obj, match = process_event_time(m)

        if last_start != -1:
            events[-1]['event'] = process_event_text(
                record[last_start:match.span()[0]])
        last_start = match.span()[1]

        events.append(event_obj)

    if not events:
        return events
    events[-1]['event'] = process_event_text(record[last_start:])

    return events


def process_event(match, record):
    pass


def process_event_time(event_match):
    print(event_match)

    can = event_match.group('can')
    chi = event_match.group('chi')
    des = event_match.group('des')
    year = event_match.group('year')
    cn_year = event_match.group('cn_year')

    des = process_des(des=des)
    cn_year = process_des(des=cn_year)

    return {
        'time': event_match.group(0),
        'can': can,
        'chi': chi,
        'regnalYear': process_regnal_year(des),
        'year': year,
        'cn_year': process_cn_regnal_year(cn_year)
    }, event_match


def process_cn_regnal_year(cn_year):
    cn_year = cn_year.strip()
    cn_year = re.sub(r'[\(\)]', '', cn_year)

    cn_regnal_years = re.split(r'[;,]', cn_year)
    cn_regnal_years = {
        'extracted': [
            process_regnal_year(regnal_year) for regnal_year in cn_regnal_years if process_regnal_year(regnal_year)
        ],
        'plain': cn_year
    }

    return cn_regnal_years


def process_des(des):
    if des is None:
        return ''

    des = re.sub(r'\s{2,}', '', des)
    des = re.sub('năm đầu', 'năm thứ 1', des)
    des = re.sub('năm thứ nhất', 'năm thứ 1', des)
    des = re.sub('năm thứ ba', 'năm thứ 3', des)
    des = re.sub('na8m', 'năm', des)
    des = des.strip()
    des = des.lstrip(',')

    return des


def process_regnal_year(des):
    des_match = re.match(REGNAL_YEAR_PATTERN, des)

    regnal_year = {}
    if des_match:
        regnal_name = re.sub(r'[\]\/\)\(\[]', '',
                             des_match.group('regnal_name'))
        regnal_name = regnal_name.strip()

        regnal_year = {
            'regnalName': regnal_name,
            'year': des_match.group('year'),
        }

    if regnal_year == {}:
        return None

    return regnal_year


def process_event_text(t):
    t = re.sub(r'\n{2,}', '\n', t)
    t = re.sub(r' {2,}', ' ', t)
    t = re.sub(r' \,', ',', t)
    t = re.sub(r'^\. ', '', t)
    t = re.sub(r'\,\n', ',', t)
    t = re.sub(r'\,(\w)', r', \1', t)
    t = re.sub(r'\n', r' ', t)
    t = re.sub(r'\s{2,}', r' ', t)
    t = t.strip()
    # t = [s.strip() for s in t.split('.') if s.strip()]

    return {
        'plain': t
    }


RESULT = [
    {
        "name": "Nguyên kỷ",
        "from": None,
        "to": 968,
        "volumes": split_records("../outputs/peripheral_records.txt")
    },
    {
        "name": "Bản kỷ",
        "from": 968,
        "to": 1675,
        "volumes": split_records("../outputs/basic_records.txt")
    }
]

with open("../outputs/result.json", "w", encoding="utf-8") as file:
    json.dump(RESULT, file, ensure_ascii=False, indent=4)

flatten = {}
for records in RESULT:
    for vol_index, volume in enumerate(records.get('volumes', [])):
        for record in volume:
            for event in record.get('content', []):
                year = event.get('year', 0)
                if 'TCN' in year:
                    year = int(year.replace(' TCN', ''))
                    year = -year
                else:
                    year = int(year)

                flatten[year] = event
                flatten[year]['records'] = records.get("name", "")
                flatten[year]['volume'] = vol_index + 1
                flatten[year]['record'] = record.get("name", "")
with open("../outputs/flat.json", "w", encoding="utf-8") as file:
    json.dump(flatten, file, ensure_ascii=False, indent=4)
