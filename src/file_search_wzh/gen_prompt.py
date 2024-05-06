with open('search_tag.txt', 'r') as file:
    tag = file.read()

print(f"""# Instruction
You are a smart file finder. Each file may have several tags. YOU MUST NOT MAKE UP FILE NAMES!
Find all files related with "{tag}".

# Output Format (DO NOT OUTPUT ANYTHING ELSE)
file_name_1
file_name_2
file_name_3
...

# Files list
""")