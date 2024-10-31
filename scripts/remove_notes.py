import re

NOTES_PATTERN = re.compile(
    r'(^1\n(.+?)\d(.+?))*\d+\s+Đại Việt Sử Ký Toàn Thư - Bản (.+?) - Quyển ([IVX]+)', re.MULTILINE | re.DOTALL)
NMARK_PATTERN = re.compile(r'\[\d+[a-z]\]', re.MULTILINE | re.DOTALL)

for file_path in ['basic_records.txt']:
    with open(f'./data/{file_path}', 'r', encoding='utf-8') as file:
        records = file.read()

    records = NOTES_PATTERN.sub('', records)
    records = NMARK_PATTERN.sub('', records)

    with open(f'./outputs/{file_path}', 'w', encoding='utf-8') as file:
        file.write(records)
