def main():
    master_dir = './tests/data'
    try:
        from utils.dependency import CheckDependencies
        from db.db import query_db_from_file
    except ImportError:
        raise RuntimeError('please cd to src/ folder, then run \n`python -m tests.test_db`')
    CheckDependencies()
    ###########################################
    #               FIXME:                    #
    #       The line below currently will     #
    #       lead to an error, due to the      #
    #       version of ocrmypdf. See README   #
    #       for more info.                    #
    ###########################################
    ans1 = query_db_from_file('./tests/data/test.pdf','what is the definition of quotient group')
    ###########################################
    #                                         #
    ###########################################
    ans2 = query_db_from_file('./tests/data/ailab_rdm.md','how to check if a pod is running')
    txt = open('/scratch2/.chroma_data').read()
    import os
    with open(os.path.join(master_dir,'out.txt'),'w') as f:
        f.write('\n\n'.join(ans1)+'\n-------------------------\n'+'\n\n'.join(ans2)+'\n-------log-----------\n'+txt)
if __name__ == '__main__':
    main()