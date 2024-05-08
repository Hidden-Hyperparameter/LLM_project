PERSIST_DIR = '/ssdshare/.it/chroma/'
import os
import importlib
import utils.ocr
importlib.reload(utils.ocr)
from utils.ocr import OCR
from utils.others import encode
LOG_DIR = os.path.join(PERSIST_DIR,'.chroma_data')
from langchain.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
def _query_chroma(ch:Chroma,q:str):
    if q == '':
        return
    docs = ch.similarity_search(q)
    return [doc.page_content for doc in docs]

def _gen_chroma_name(name:str):
    return encode(name)

def clear_cache():
    os.makedirs(PERSIST_DIR,exist_ok=True)
    assert os.path.exists(PERSIST_DIR),'Some strange error'
    try:
        open(LOG_DIR,'r').read()
    except FileNotFoundError:
        open(LOG_DIR,'w').write('')
    open(LOG_DIR,'w').write('')
    print('[DB.PY]:cache cleared')

def getlogs():
    os.makedirs(PERSIST_DIR,exist_ok=True)
    files = None
    # check whether the file is in record, so we can reuse the old chroma
    try:
        files = open(LOG_DIR,'r').read()
    except FileNotFoundError:
        open(LOG_DIR,'w').write('')
        files = ''
    files = [c.strip() for c in files.split('\n') if c.strip()!='']
    return files

def make_db_from_text(filename:str,texts:str,quiet=True):
    assert filename not in getlogs(),NotImplementedError()
    from langchain_community.document_loaders import TextLoader
    from langchain.text_splitter import RecursiveCharacterTextSplitter
    minilm_embedding = SentenceTransformerEmbeddings(model_name="/share/embedding/all-MiniLM-L6-v2/")
    chroma_dir = os.path.join(PERSIST_DIR,'chroma_db')
    tmp_dir = os.path.join(PERSIST_DIR,'tmp_'+encode(filename)+'.txt')
    with open(tmp_dir,'w') as f:
        f.write(texts)
    texts = TextLoader(tmp_dir).load()
    os.remove(tmp_dir)
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)    
    texts = text_splitter.split_documents(texts)
    docsearch_chroma=Chroma.from_documents(
        texts,
        minilm_embedding,
        collection_name=_gen_chroma_name(filename),
        persist_directory=chroma_dir)
    docsearch_chroma.persist()
    return docsearch_chroma

def query_db_from_file(file:str,query:str,quiet=True):
    """query `query` from chroma db, given context `file`
    notice that `file` is a path."""
    file = os.path.abspath(file)
    files = getlogs()
    # load chroma embedding
    minilm_embedding = SentenceTransformerEmbeddings(model_name="/share/embedding/all-MiniLM-L6-v2/")
    chroma_dir = os.path.join(PERSIST_DIR,'chroma_db')
    if file in files:
        # load old chroma db
        if not quiet:
            print('[DB.PY]:returning old chroma db')
        return _query_chroma(Chroma(
            persist_directory=chroma_dir,
            collection_name=_gen_chroma_name(file),
            embedding_function=minilm_embedding),query)
    else:
        # create new chroma db
        if not quiet:
            print('[DB.PY]:running ocr')
        texts = OCR(file,remove_mid=True)
        docsearch_chroma = make_db_from_text(file,texts,quiet=quiet)
        # save records
        files.append(file)
        with open(LOG_DIR,'w') as f:
            f.write('\n'.join(files))
        return _query_chroma(docsearch_chroma,query)

def query_files_with_citation(files,query:str,save_dir:str,quiet=True):
    """Arguments
    files: the possible file list
    query: the query 
    save_dir: the directory to save the results (i.e. related.txt)
    """
    s = []
    for file in files:
        list_of_texts = query_db_from_file(file,query,quiet=quiet)
        s.extend([f'File Name: {file}\n------------\n','']+[c+'\n==========\n' for c in list_of_texts])
    open(save_dir,'w').writelines(s)
    

