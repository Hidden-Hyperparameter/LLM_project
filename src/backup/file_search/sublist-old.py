import os,sys
if not os.path.exists('/ssdshare/.it/query.txt'):
    raise RuntimeError('[SUBLIST.PY]: cannot find query.txt')
with open('/ssdshare/.it/query.txt', 'r') as file:
    query = file.read()

print(f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a smart file finder. Each file may have several tags. DO NOT MAKE UP FILES!
If there are none, just output none.

# Output Format (ONLY OUTPUT THE FILE DIRECTORIES, NO OTHER WORDS)
/path_to_file/file1
/path_to_file/file2
./file3
<|eot_id|>
<|start_header_id|>user<|end_header_id|>

Find all files that might be related to "{query}".

Possible files list:
""")

file_path = '/ssdshare/.it/file_search/ans.txt'
file_lists = []
if not os.path.exists(file_path):
    raise RuntimeError('[SUBLIST.PY]: cannot find file_search/ans.txt')

with open(file_path, 'r') as file:
    file_list = file.read().splitlines()

file_list = list(set(file_list))
for line in file_list:
    if line.strip():  # Check if the line is not empty
        ############## ZHH has modified this line #################
        file_lists.append(line.strip())
        ###########################################################

sys.stderr.write(f'[SUBLIST.PY]: file_lists {file_lists}')

test_path = '/ssdshare/.it/all_files.txt'
test_lists = []
with open(test_path, 'r') as file:
    test_list = file.read().splitlines()
test_list = list(set(test_list))
for line in test_list:
    if line.strip():  # Check if the line is not empty
        ############## ZHH has modified this line #################
        test_lists.append(line.strip())
        ###########################################################
sys.stderr.write(f'\n\n[SUBLIST.PY]: test_lists {test_lists}')


for line in test_lists:
    file_name, tags = line.split(',   ')
    file_name = file_name.split(':')[1].strip()
    if file_name in file_lists:
        print(line)
        sys.stderr.write('\n'+line+'\n')


print("""<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
""")


      
      
# # Instruction
# You are a smart file finder. Each file may have several tags. DO NOT MAKE UP FILES!
# Find all files that might be related to "{query}".
# If there are none, just output none.

# # Output Format (ONLY OUTPUT THE FILE DIRECTORIES, NO OTHER WORDS)
# /path_to_file/file1
# /path_to_file/file2
# ./file3

# # Possible Files List