from db.db import query_files_with_citation
import os
files = []
if not os.path.exists('/ssdshare/.it/files.txt'):
    raise RuntimeError('[SIM_SEARCH.PY]: cannot find files.txt')
with open('/ssdshare/.it/files.txt', 'r') as file:
    file_list = file.read().splitlines()

for line in file_list:
    if line.strip():
        files.append(line)

if not os.path.exists('/ssdshare/.it/query.txt'):
    raise RuntimeError('[SIM_SEARCH.PY]: cannot find query.txt')
with open('/ssdshare/.it/query.txt', 'r') as file:
    query = file.read()

for file in files:
    if not os.path.exists(file):
        print(f'[SIM_SEARCH.PY][WARNING]: cannot locate file {file}!')

query_files_with_citation(files, query, '/ssdshare/.it/final_query/related.txt')