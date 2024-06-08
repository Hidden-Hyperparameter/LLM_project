import os,sys
if not os.path.exists('/ssdshare/.it/query.txt'):
    raise RuntimeError('[SUBLIST.PY]: cannot find query.txt')
with open('/ssdshare/.it/query.txt', 'r') as file:
    query = file.read()

PROMPT_FINAL_DIR = '/ssdshare/.it/file_search' ## prompt_final.txt

N = 5
def cut():
    with open('/ssdshare/.it/file_search/ans.txt', 'r') as f:
        lines = f.readlines()
    lines = [c.strip(' \n') for c in lines]
    lines = [c for c in lines if c!='']
    n = len(lines)
    i = 0
    j = 1
    l = []
    while i < n:
        l.append(lines[i:i+N])
        i += N
        j += 1
    return l

if __name__ == '__main__':
    l = cut()
    for i,file1 in enumerate(l):
        with open(f'/ssdshare/.it/file_search/prompt_final{i+1}.txt','w') as f:
            f.write(f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a smart file finder. Each file may have several tags. DO NOT MAKE UP FILES!
If there are none, just output none.

# Output Format (ONLY OUTPUT THE FILE DIRECTORIES, NO OTHER WORDS)
/path_to_file/file1
/path_to_file/file2
./file3
<|eot_id|>
<|start_header_id|>user<|end_header_id|>

Find all files that might be related to "{query}".

Possible files list:\n\n""")

            file_list = list(set(file1))
            # sys.stderr.write(f'[SUBLIST.PY]: file_lists {file_list}')

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
            # sys.stderr.write(f'\n\n[SUBLIST.PY]: test_lists {test_lists}')


            for line in test_lists:
                file_name, tags = line.split(',   ')
                file_name = file_name.split(':')[1].strip()
                if file_name in file_list:
                    f.write(line+'\n')
                    # sys.stderr.write('\n'+line+'\n')


            f.write("""<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>\n
            """)
    exit(len(l))

      
      
# # Instruction
# You are a smart file finder. Each file may have several tags. DO NOT MAKE UP FILES!
# Find all files that might be related to "{query}".
# If there are none, just output none.

# # Output Format (ONLY OUTPUT THE FILE DIRECTORIES, NO OTHER WORDS)
# /path_to_file/file1
# /path_to_file/file2
# ./file3

# # Possible Files List