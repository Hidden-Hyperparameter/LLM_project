# read from test.txt, and cut it in to little files of 50 lines,
# and write them to test1.txt , test2.txt, test3.txt, ...
# and return the number of files created
def cut():
    with open('/ssdshare/2024040125_2023040165_2023040163_project/src/file_search/test.txt', 'r') as f:
        lines = f.readlines()
    n = len(lines)
    i = 0
    j = 1
    while i < n:
        with open('/ssdshare/2024040125_2023040165_2023040163_project/src/file_search/test' + str(j) + '.txt', 'w') as f:
            f.writelines(lines[i:i+50])
        i += 50
        j += 1
    return j - 1
if __name__ == '__main__':
    print('Number of files created:', cut())
    exit(cut())