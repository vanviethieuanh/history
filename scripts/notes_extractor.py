import re
import json

PAGE_PATTERN = re.compile(
    r"^(?P<page>\d+)\s+Đại Việt Sử Ký Toàn Thư - (?P<records>.+) - (?P<volume>.+)", re.MULTILINE)
NOTES_POS = re.compile(
    r'[a-zÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚĂĐĨŨƠàáâãèéêìíòóôõùúăđĩũơƯĂẠẢẤẦẨẪẬẮẰẲẴẶẸẺẼỀỀỂưăạảấầẩẫậắằẳẵặẹẻẽềềểỄỆỈỊỌỎỐỒỔỖỘỚỜỞỠỢỤỦỨỪễệỉịọỏốồổỗộớờởỡợụủứừỬỮỰỲỴÝỶỸửữựỳỵỷỹ]\d')

data_file = open("./data/dai-viet-su-ky-toan-thu.txt", "r", encoding="utf-8")
FILE_CONTENT = data_file.read()

pages = re.split(PAGE_PATTERN, FILE_CONTENT)[1:]

RESULT = []
for i in range(0, len(pages), 4):
    RESULT.append({
        'page':pages[i],
        'record':pages[i+1],
        'volume':pages[i+2],
        'content':pages[i+3],
    })
    pass


with open("pages.json", "w", encoding="utf-8") as file:
    json.dump(RESULT, file, ensure_ascii=False, indent=4)
