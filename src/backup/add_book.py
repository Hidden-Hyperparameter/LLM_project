from db.db import query_db_from_file

import os
from os.path import join
from utils.ocr import OCR

with open('./new_files_path.txt', 'r') as f:
    file_path = f.read()

out_path = './ocr_data/'

# cut 10 pages

from utils.others import gen_10_pages

gen_10_pages(file_path=file_path, out_path=join(out_path, '10pages.pdf'))

# OCR

txt = OCR(join(out_path, '10pages.pdf'),quiet=False)
with open(join(out_path, '10pages.txt'), 'w') as f:
    f.write(txt)


os.system(f"sh ../prompts/run.sh {join(out_path), '10pages.txt'}")

query_db_from_file(file_path, '')

