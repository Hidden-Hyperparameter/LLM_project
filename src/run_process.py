import os
import threading
import subprocess
import json
import PyPDF2
import os
import subprocess
import mimetypes
from jzc_utils import Encode, query_llm, gen_10_pages, WriteTag, WriteDBLog, GetDBLog, make_db_from_text, filetype
from utils.ocr import OCR
TMP_DIR = '/ssdshare/.it/.tmp/'
MAX_THREADS = 4
query_lock = threading.Lock()
write_tag_lock = threading.Lock()
cnt_lock = threading.Lock()
dblog_lock = threading.Lock()
make_db_lock = threading.Lock()
cnt_sem = threading.Semaphore(0)
# global ocr_finish_cnt_success
# ocr_finish_cnt_success = 0
# global ocr_finish_cnt_fail
# ocr_finish_cnt_fail = 0
def GenerateTagsFromPath(file_path, quiet):
    # guess the file type
    abs_path = os.path.abspath(file_path)
    guess_type=filetype(abs_path)
    # generate tags based on the file type

    ### Case 1: Regular File
    if guess_type in ['text', 'image']:
        texts = OCR(abs_path, quiet=quiet)
        with query_lock:
            tags = query_llm(texts)
        with write_tag_lock:
            WriteTag(abs_path, tags)
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
        tags = query_llm(texts)
    with write_tag_lock:
        WriteTag(abs_path,tags)

def GenerateTagsFromList(file_list, quiet):
    for file in file_list:
        GenerateTagsFromPath(file, quiet)

def GenerateTagsFromDir(dir, quiet):
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
        thread = threading.Thread(target=GenerateTagsFromList, args=(File_lists[i], quiet))
        threads.append(thread)
    for t in threads:
        t.start()
    # wait for the threads to finish
    for t in threads:
        t.join()

def MakeDBFromPath(file_path, quiet):
    file_path = os.path.abspath(file_path)
    texts = file_path + "(This file can't be handled by ocr, maybe a binary file)"
    successful = False
    finished_list = GetDBLog()
    if file_path in finished_list:
        successful = True
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

def MakeDBFromDir(dir, quiet):
    target_files = []
    for root, _, files in os.walk(dir):
        for file in files:
            target_files.append(os.path.join(root, file))
    for file in target_files:
        MakeDBFromPath(file, quiet)

def Main(root_dir, quiet):
    if os.path.isdir(root_dir):
        GenerateTagsFromDir(root_dir, quiet)
    else:
        GenerateTagsFromPath(root_dir, quiet)
    print("Tags generated successfully")
    MakeDBFromDir(root_dir, quiet)

if __name__ == '__main__':
    Main(root_dir='../XQC/READ',quiet=False)