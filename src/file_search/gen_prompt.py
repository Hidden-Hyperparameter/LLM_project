import os,json
import sys
sys.path.append('.')
args = sys.argv[1:]
assert len(args)<2,NotImplementedError()
if len(args)==0:
    filter = None
else:
    filter = args[0]
    if filter == '':
        filter = None
    else:
        if filter.startswith('"'):
            filter = filter.strip('"')
        # filter = os.path.abspath(filter)
if not os.path.exists('/ssdshare/.it/query.txt'):
    raise RuntimeError('[FILE_SEARCH/GEN_PROMPT.py]: cannot find query.txt')
with open('/ssdshare/.it/query.txt', 'r') as file:
    query = file.read()
# save tag into all_files.txt
# from run_process import LOG_DIR
LOG_DIR = '/ssdshare/.it/tags.json'
ALL_FILES_TXT = '/ssdshare/.it/all_files.txt'
if not os.path.exists(LOG_DIR):
    raise RuntimeError('[FILE_SEARCH/GEN_PROMPT.py]: The tags are not properly loaded!')
file_dict = json.load(open(LOG_DIR))
lines = []
for file,tags in file_dict.items():
    if filter is not None and file.find(filter) == -1:
        sys.stderr.write('[INFO]: skipping '+file+' since it does not contain '+filter+'\n')
        continue
    tag_joined = ', '.join(tags)
    lines.append(f'File:{file},   tags:{tag_joined}\n')
open(ALL_FILES_TXT,'w').writelines(lines)
sys.stderr.write(f'[FILE_SEARCH/GEN_PROMPT.PY]: all_files.txt written in {ALL_FILES_TXT}')
# print(f'[FILE_SEARCH/GEN_PROMPT.PY]: all_files.txt written in {ALL_FILES_TXT}')

print(f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a smart file finder. Each file may have several tags. YOU MUST NOT MAKE UP FILE NAMES!

# Output Format: (ONLY OUTPUT THE FILE DIRECTORIES, NO OTHER WORDS)
/path_to_file/file1
/path_to_file/file2
./file3
<|eot_id|>
<|start_header_id|>user<|end_header_id|>

Find all files that might be related to "{query}".

""")


# # Instruction
# You are a smart file finder. Each file may have several tags. YOU MUST NOT MAKE UP FILE NAMES!
# Find all files that might be related to "{query}".

# # Output Format (ONLY OUTPUT THE FILE DIRECTORIES, NO OTHER WORDS)
# /path_to_file/file1
# /path_to_file/file2
# ./file3

# # Files list