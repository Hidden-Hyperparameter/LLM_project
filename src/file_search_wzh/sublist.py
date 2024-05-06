with open('search_tag.txt', 'r') as file:
    tag = file.read()

print(f"""# Instruction
You are a smart file finder. Each file may have several tags. DO NOT MAKE UP FILES!
Find all files related with "{tag}".

# Output Format (DO NOT OUTPUT ANYTHING ELSE)
file_name_1
file_name_2
file_name_3
...

# Possible Files List""")

file_path = 'ans.txt'
file_lists = []

with open(file_path, 'r') as file:
    file_list = file.read().splitlines()

file_list = list(set(file_list))

for line in file_list:
    if line.strip():  # Check if the line is not empty
        file_lists.append(line.split(' ')[0].strip())

test_path = 'test.txt'
test_lists = []
with open(test_path, 'r') as file:
    test_list = file.read().splitlines()
test_list = list(set(test_list))
for line in test_list:
    if line.strip():  # Check if the line is not empty
        test_lists.append(line)


for line in test_lists:
    file_name, tags = line.split(',\t')
    file_name = file_name.split(':')[1].strip()
    if file_name in file_lists:
        print(line)


print("""
# Output
""")