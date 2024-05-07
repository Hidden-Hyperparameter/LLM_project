from db.db import query_db_from_file
from db.db import query_files_with_citation

with open('./new_files_path.txt', 'r') as f:
    file_path = f.read()

out_path = './ocr_data/'

# cut 10 pages

from utils.others import gen_10_pages

gen_10_pages(file_path=file_path, out_path=join(out_path, '10pages.pdf'))

# OCR

txt = OCR(file_path,quiet=False)
with open(join(out_path, '10pages.txt'), 'w') as f:
    f.write(txt)

query_db_from_file(out_path, '')
query_db_from_file(file_path, '')

