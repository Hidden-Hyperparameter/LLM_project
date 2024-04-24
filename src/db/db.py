PERSIST_DIR = '/scratch2'
from langchain.vectorstores import Chroma
from langchain_community.embeddings.sentence_transformer import SentenceTransformerEmbeddings
def _query_chroma(ch:Chroma,q:str):
    docs = ch.similarity_search(q)
    return [doc.page_content for doc in docs]

def _gen_chroma_name(name:str):
    name = name.replace('.','-').replace('/','_')
    name = name[:60]
    if len(name) <= 5:
        name = 'Chroma_'+name
    if not name[0].isalpha():
        name='a'+name[1:]
    if not name[-1].isalpha():
        name=name[:-1]+'a'
    return name

def query_db_from_file(file:str,query:str):
    """query `query` from chroma db, given context `file`"""
    files = None
    # check whether the file is in record, so we can reuse the old chroma
    import os
    try:
        files = open(os.path.join(PERSIST_DIR,'.chroma_data'),'r').read()
    except FileNotFoundError:
        # print('rewriting...')
        open(os.path.join(PERSIST_DIR,'.chroma_data'),'w').write('')
        files = ''
    files = files.split('\n')
    # load chroma embedding
    minilm_embedding = SentenceTransformerEmbeddings(model_name="/share/embedding/all-MiniLM-L6-v2/")
    chroma_dir = "/scratch2/chroma_db"
    if file in files:
        # load old chroma db
        return _query_chroma(Chroma(
            persist_directory=chroma_dir,
            collection_name=_gen_chroma_name(file),
            embedding_function=minilm_embedding),query)
    else:
        # create new chroma db
        from utils.ocr import OCR
        import os
        from langchain_community.document_loaders import TextLoader
        from langchain.text_splitter import RecursiveCharacterTextSplitter
        
        texts = OCR(file,remove_mid=True)
        tmp_dir = os.path.join(PERSIST_DIR,'tmp_'+file.replace('/','_')+'.txt')
        with open(tmp_dir,'w') as f:
            f.write(texts)
        texts = TextLoader(tmp_dir).load()
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
        with open(os.path.join(PERSIST_DIR,'.chroma_data'),'w') as f:
            f.write('\n'.join(files))

        return _query_chroma(docsearch_chroma,query)

        

