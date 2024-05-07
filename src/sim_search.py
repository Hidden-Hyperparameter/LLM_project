from db.db import query_files_with_citation
import os
files = []
with open('./files.txt', 'r') as file:
    file_list = file.read().splitlines()

for line in file_list:
    if line.strip():
        files.append(line)

with open('./query.txt', 'r') as file:
    query = file.read()

for file in files:
    assert os.path.exists(file),file

query_files_with_citation(files, query, './final_query/related.txt')