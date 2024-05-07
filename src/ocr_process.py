import argparse
import os
from db.db import query_db_from_file
parser = argparse.ArgumentParser()

parser.add_argument('--file', type=str)
parser.add_argument('--log-dir', type=str)

args = parser.parse_args()
print(args.file)
file = args.file.replace('"','')
logs = args.log_dir.replace('"','')
print(file)
query_db_from_file(file,'',quiet=True)
if os.path.exists(logs):
    open(logs,'a').write(f'\nOCR file [{file}] finished\n')
else:
    open(logs,'w').write(f'\nOCR file [{file}] finished\n')