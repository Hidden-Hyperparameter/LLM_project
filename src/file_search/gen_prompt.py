with open('query.txt', 'r') as file:
    query = file.read()

print(f"""# Instruction
You are a smart file finder. Each file may have several tags. YOU MUST NOT MAKE UP FILE NAMES!
Find all files that might be related to "{query}".

# Output Format (ONLY OUTPUT THE FILE DIRECTORIES, NO OTHER WORDS)
./path_to_file/file1
./path_to_file/file2
./path_to_file/file3
...

# Files list""")