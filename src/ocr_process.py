import argparse
import os
from db.db import query_db_from_file
parser = argparse.ArgumentParser()

parser.add_argument('--file', type=str)
parser.add_argument('--log-dir', type=str)

args = parser.parse_args()
file = args.file.replace('"','')
logs = args.log_dir.replace('"','')
query_db_from_file(file,'',quiet=True)
if not os.path.exists(logs):
    with open(logs,'w') as f:
        f.write(f'\n{file}\n')
else:
    with open(logs,'a') as f:
        f.write(f'\n{file}\n')