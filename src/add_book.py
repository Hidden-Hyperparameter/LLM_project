from run_process import GenerateTagsFromPath,MakeDBFromPath,MakeDBFromDir,GenerateTagsFromDir
from utils.dependency import CheckDependencies
import os
ADD_BOOK_LOG = '/ssdshare/.it/add_book_log.txt'

def add_book(file_path):
    if os.path.isdir(file_path):
        GenerateTagsFromDir(file_path, quiet=False,force=True)
        print("Tags generated successfully")
        MakeDBFromDir(file_path, quiet=False,force=True)
    else:
        GenerateTagsFromPath(file_path,quiet=False,force=True)
        print("Tags generated successfully")
        MakeDBFromPath(file_path, quiet=False,force=True)

if __name__ == '__main__':
    CheckDependencies()
    # open(ADD_BOOK_LOG,'w').write('')
    files = open('data_list.txt').readlines()
    for filen in files:
        if filen.startswith('#') or filen.strip(' \n')=='':
            continue
        add_book(filen.strip(' \n'))