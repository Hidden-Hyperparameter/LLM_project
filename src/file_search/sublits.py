path = './answer.txt'
file_lists = []
with open(path, 'r') as file:
    line = file.read().splitlines()
    # find the name of the file ends with ".pdf" in this line
    for l in line:
        l = l.split()
        for i in l:
            if i.find('.pdf') != -1:
                i = i.split(':')[-1]
                # delete all the * and , in i
                i = i.replace('*', '')
                i = i.replace(',', '')
                i = i.replace('\'', '')
                i = i.replace('\"', '')
                print(i)
        