PERSIST_DIR = '/scratch2'
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
    docs = ch.similarity_search(q)
    return [doc.page_content for doc in docs]

def _gen_chroma_name(name:str):
    return encode(name)

def clear_cache():
    open(LOG_DIR,'w').write('')
    print('[DB.PY]:cache cleared')

def query_db_from_file(file:str,query:str,quiet=True):
    """query `query` from chroma db, given context `file`"""
    file = os.path.abspath(file)
    files = None
    # check whether the file is in record, so we can reuse the old chroma
    try:
        files = open(LOG_DIR,'r').read()
    except FileNotFoundError:
        open(LOG_DIR,'w').write('')
        files = ''
    files = [c.strip() for c in files.split('\n') if c.strip()!='']
    # load chroma embedding
    minilm_embedding = SentenceTransformerEmbeddings(model_name="/share/embedding/all-MiniLM-L6-v2/")
    chroma_dir = "/scratch2/chroma_db"
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
        from langchain_community.document_loaders import TextLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        if not quiet:
            print('[DB.PY]:running ocr for texts')
        texts = OCR(file,remove_mid=True)
        tmp_dir = os.path.join(PERSIST_DIR,'tmp_'+encode(file)+'.txt')
        with open(tmp_dir,'w') as f:
            f.write(texts)
        texts = TextLoader(tmp_dir).load()
        os.remove(tmp_dir)
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)    
        texts = text_splitter.split_documents(texts)

        docsearch_chroma=Chroma.from_documents(
            texts,
            minilm_embedding,
            collection_name=_gen_chroma_name(file),
            persist_directory=chroma_dir)
        docsearch_chroma.persist()

        # save records
        files.append(file)
        with open(LOG_DIR,'w') as f:
            f.write('\n'.join(files))

        return _query_chroma(docsearch_chroma,query)

        

