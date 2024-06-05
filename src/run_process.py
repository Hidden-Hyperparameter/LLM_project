import os
import threading
import subprocess
import json
import PyPDF2
import os
import subprocess
import mimetypes
from new_utils import Encode, query_llm, gen_10_pages, WriteTag, WriteDBLog, GetDBLog, make_db_from_text, filetype,TAG_DIR
from utils.ocr import OCR
from utils.dependency import CheckDependencies
TMP_DIR = '/ssdshare/.it/.tmp/'
MAX_THREADS = 4
query_lock = threading.Lock()
write_tag_lock = threading.Lock()
dblog_lock = threading.Lock()
make_db_lock = threading.Lock()
cnt_sem = threading.Semaphore(0)
gpu_lock = threading.Lock() # prevent from cuda out of memory

def CheckTagFinished(file:str)->bool:
    if not os.path.exists(TAG_DIR):
        return False
    with write_tag_lock:
        with open(TAG_DIR) as f:
            tag_files = json.load(f)
    if file in tag_files and len(tag_files[file])>0:
        return True
    return False

def GenerateTagsFromPath(file_path, quiet,force=False):
    # guess the file type
    abs_path = os.path.abspath(file_path)
    if CheckTagFinished(abs_path) and not force:
        return
    guess_type=filetype(abs_path)
    # generate tags based on the file type
    ### Case 1: Regular File
    if guess_type == 'text':
        texts = OCR(abs_path, quiet=quiet)
        with query_lock:
            tags = query_llm(f'The file {abs_path} contain contents:\n'+texts)
        with write_tag_lock:
            WriteTag(abs_path, tags)
        ### If certain file types, then run DB
        MakeDBFromText(file_path,texts,quiet=quiet,force=force)
        return
    elif guess_type in [ 'image','video']:
        with gpu_lock:
            texts = OCR(abs_path, quiet=quiet)
            with query_lock:
                tags = query_llm(f'The file {abs_path} contain contents:\n'+texts)
            with write_tag_lock:
                WriteTag(abs_path, tags)
            ### If certain file types, then run DB
            MakeDBFromText(file_path,texts,quiet=quiet,force=force)
        return
    
    ### Case 2: Other File Types
    out_path_10_pages = os.path.join(TMP_DIR,Encode(abs_path)+'_10pages.pdf')
    try:
        gen_10_pages(abs_path,out_path=out_path_10_pages)
    ### Not Successful
    except BaseException as e:
        if not quiet:
            print('[RUN_PROCESS]: \033[31m[FATAL]\033[0m OCR EXCEPTION:',e)
        with query_lock:
            tags = query_llm(abs_path+"(This is a file that can't be handled by ocr, maybe a binary file)",quiet=quiet)
        with write_tag_lock:
            WriteTag(abs_path,tags)
        return
    ### Successful
    texts = OCR(out_path_10_pages,quiet=quiet)
    with query_lock:
        tags = query_llm(f'The file {abs_path} contain contents:\n'+texts)
    with write_tag_lock:
        WriteTag(abs_path,tags)

def GenerateTagsFromList(file_list, quiet,force=False):
    for file in file_list:
        GenerateTagsFromPath(file, quiet,force=force)

def GenerateTagsFromDir(dir, quiet,force=False):
    '''
    Generate tags for all files in the root directory
    '''
    # create a file list containing all files in the root directory
    File_list = []
    for root, _, files in os.walk(dir):
        for file in files:
            File_list.append(os.path.join(root, file))
    # start threads to generate tags for each file
    File_lists = []
    for i in range(MAX_THREADS):
        File_lists.append([])
    for i in range(len(File_list)):
        File_lists[i % MAX_THREADS].append(File_list[i])
    threads = []
    for i in range(MAX_THREADS):
        thread = threading.Thread(target=GenerateTagsFromList, args=(File_lists[i], quiet,force))
        threads.append(thread)
    for t in threads:
        t.start()
    # wait for the threads to finish
    for t in threads:
        t.join()

def MakeDBFromText(file_path,text,quiet,force=False):
    file_path = os.path.abspath(file_path)
    finished_list = GetDBLog()
    if file_path in finished_list and not force:
        return
    make_db_from_text(file_path,text,quiet=quiet)
    with dblog_lock:
        WriteDBLog(file_path)

def MakeDBFromPath(file_path, quiet,force=False):
    # if file in list then return
    guess_type = filetype(file_path)
    if guess_type in ['text','image','video']:
        return
    # original
    file_path = os.path.abspath(file_path)
    texts = file_path + "(This file can't be handled by ocr, maybe a binary file)"
    successful = False
    finished_list = GetDBLog()
    if file_path in finished_list and not force:
        successful = True
        return
    if not successful:
        try:
            texts = OCR(file_path, quiet=quiet)
            successful = True
        except:
            # print(f"OCR failed for {file_path}")
            print( Exception(f"OCR failed for {file_path}"))
        texts = file_path + "\n" + texts
        make_db_from_text(file_path,texts,quiet=quiet)
    if successful:
        with dblog_lock:
            WriteDBLog(file_path)

def MakeDBFromDir(dir, quiet,force=False):
    target_files = []
    for root, _, files in os.walk(dir):
        for file in files:
            target_files.append(os.path.join(root, file))
    for file in target_files:
        MakeDBFromPath(file, quiet,force=force)

def Main(root_dir, quiet):
    if os.path.isdir(root_dir):
        GenerateTagsFromDir(root_dir, quiet)
    else:
        GenerateTagsFromPath(root_dir, quiet)
    print("Tags generated successfully")
    MakeDBFromDir(root_dir, quiet)

if __name__ == '__main__':
    CheckDependencies()
    Main(root_dir='../demo',quiet=True)