N = 10
# read from test.txt, and cut it in to little files of N lines,
# and write them to test1.txt , test2.txt, test3.txt, ...
# and return the number of files created
def cut():
    with open('/ssdshare/.it/all_files.txt', 'r') as f:
        lines = f.readlines()
    n = len(lines)
    i = 0
    j = 1
    while i < n:
        with open('/ssdshare/.it/all_files_cutted' + str(j) + '.txt', 'w') as f:
            f.writelines(lines[i:i+N])
        i += N
        j += 1
    return j - 1
if __name__ == '__main__':
    print('Number of files created:', cut())
    exit(cut())