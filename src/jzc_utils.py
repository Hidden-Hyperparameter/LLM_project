import os
import threading
import subprocess
import json
import PyPDF2
import mimetypes
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
DICT_LEN = 16 ** 6
TAG_DIR = '/ssdshare/.it/tags.json'
DB_LOG_DIR = '/ssdshare/.it/db_log.txt'
TMP_DIR = '/ssdshare/.it/.tmp/'
CHROMA_DIR = '/ssdshare/.it/chroma'
def GetDBLog():
    if not os.path.exists(DB_LOG_DIR):
        return []
    with open(DB_LOG_DIR, 'r') as f:
        logs = f.readlines()
        logs = [log.replace('\n', '') for log in logs]
    return logs

def WriteDBLog(file_name):
    logs = GetDBLog()
    logs.append(file_name)
    with open(DB_LOG_DIR, 'w') as f:
        for log in logs:
            f.write(log + '\n')

def query_llm(texts:str,quiet=True):
    prompt = "Give me some(about 10-20) tags based on the context below, without any other things!\n"+texts
    prompt_path = os.path.join(TMP_DIR,'prompt_for_tag.txt')
    tag_path = os.path.join(TMP_DIR,'generated_tags.txt')
    with open(prompt_path, 'w') as f:
        f.write(prompt)
    if not quiet:
        print('[QUERY_LLM] running llama3 70b')
    os.system(f"/share/ollama/ollama run llama3:70b < {prompt_path} > {tag_path}")
    tags = []
    with open(tag_path, 'r') as f:
        lines = f.readlines()
        for line in lines:
            # check if it starts with a number
            if line[0].isdigit():
                items = line.split(' ')[1:]
                string = ''
                for item in items:
                    string += item + ' '
                tags.append(string.replace('\n', '').replace('*','').replace('#','').replace('\'','').replace('\"','')[:-1])
    return tags

def WriteTag(file_name, tags):
    dict_tags = {}
    if os.path.exists(TAG_DIR):
        with open(TAG_DIR, 'r') as f:
            dict_tags = json.load(f)
    dict_tags[file_name] = tags
    with open(TAG_DIR, 'w') as f:
        json.dump(dict_tags, f)

def Encode(s:str,mod = 1000000007):
    code = 0
    for c in s:
        code = (code*(DICT_LEN+1)+int(c.encode().hex(),base=16)) % mod
    return str(code).replace('-','n')

def _gen_10_pages(file_path,out_path=None):
    if out_path is None:
        out_path = file_path.replace('.pdf','')+'_10pages.pdf'
    elif os.path.isdir(out_path):
        file_name = os.path.basename(file_path)
        if file_name.find('.pdf') == -1:
            raise ValueError('Cannot done with a non-pdf file')
        file_name = file_name.replace('.pdf','')+'_10pages.pdf'
        out_path = os.path.join(out_path, file_name)
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()
        for page_num in range(min(10,len(pdf_reader.pages))):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)
        with open(out_path, 'wb') as output_file:
            pdf_writer.write(output_file)

def gen_10_pages(file_path,out_path=None):
    os.makedirs(TMP_DIR,exist_ok=True)
    if not file_path.endswith('.pdf'):
        file_real,file_suffix = os.path.splitext(file_path)[:2]
        file_name = os.path.basename(file_real)
        try:
            subprocess.check_output(['soffice', '--headless', '--convert-to', 'pdf',file_path])
        except subprocess.CalledProcessError:
            raise RuntimeError(f'[GEN_PAGES]\033[31m[ERROR]\033[0m:Failure to OCR file {file_path}')
        tmp_out_path = f'./{file_name}.pdf'
        if not os.path.exists(tmp_out_path):
            raise RuntimeError(f'[GEN_PAGES]\033[31m[ERROR]\033[0m:Failure to OCR file {file_path}')
        _gen_10_pages(tmp_out_path,out_path)
        os.remove(tmp_out_path)
    else:
        _gen_10_pages(file_path,out_path)

def make_db_from_text(filename:str,texts:str,quiet=True):
    os.makedirs(CHROMA_DIR,exist_ok=True)
    minilm_embedding = SentenceTransformerEmbeddings(model_name="/share/embedding/all-MiniLM-L6-v2/")
    chroma_dir = os.path.join(CHROMA_DIR,'chroma_db')
    tmp_dir = os.path.join(CHROMA_DIR,'tmp_'+Encode(filename)+'.txt')
    with open(tmp_dir,'w') as f:
        f.write(texts)
    texts = TextLoader(tmp_dir).load()
    os.remove(tmp_dir)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)    
    texts = text_splitter.split_documents(texts)
    docsearch_chroma=Chroma.from_documents(
        texts,
        minilm_embedding,
        collection_name=Encode(filename),
        persist_directory=chroma_dir)
    docsearch_chroma.persist()
    return docsearch_chroma

def filetype(filename):
    """
    Input: file name optionally with path
    Output: file type: 'text', 'image', 'audio', 'video', 'application' (binary file)
    """
    kind, _ = mimetypes.guess_type(filename)
    if kind == None:
        return 'text'
    return kind.split('/')[0]
