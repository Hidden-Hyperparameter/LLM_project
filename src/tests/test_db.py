import importlib
def main():
    master_dir = './tests/data'
    try:
        import utils.dependency
        import db.db
        from utils.dependency import CheckDependencies
        from db.db import query_db_from_file,clear_cache
        importlib.reload(utils.dependency)
        importlib.reload(db.db)
    except ImportError:
        raise RuntimeError('please cd to src/ folder, then run \n`python -m tests.test_db`')
    # raise RuntimeError()
    CheckDependencies()
    clear_cache()
    # pdf
    ans1 = query_db_from_file('./tests/data/test.pdf','what is the definition of quotient group',quiet=False)
    # text file
    ans2 = query_db_from_file('./tests/data/ailab_rdm.md','how to check if a pod is running',quiet=False)
    
    print('\n'*20)
    print('[INFO-Test-db] Loading file 1 again, the program should not run OCR again!')
    ans1 = query_db_from_file('./tests/data/test.pdf','what is the definition of quotient group',quiet=False)
    txt = open('/scratch2/.chroma_data').read()
    import os
    with open(os.path.join(master_dir,'out.txt'),'w') as f:
        f.write('\n====\n'.join(ans1)+'\n-------------------------\n'+'\n====\n'.join(ans2)+'\n-------log-----------\n'+txt)
if __name__ == '__main__':
    main()