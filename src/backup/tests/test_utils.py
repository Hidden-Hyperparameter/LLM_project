import importlib
def main():
    try:
        from utils.ocr import OCR
        from utils.others import gen_10_pages
        from utils.dependency import CheckDependencies
    except ImportError as e:
        print(e)
        raise RuntimeError('please cd to src/ folder, then run \n`python -m tests.test_utils`')
    CheckDependencies()
    master_dir = './tests/data'
    from os.path import join
    with open(join(master_dir,'out.txt'),'w') as f:
        f.write('begin!\n')
    def wt(s:str):
        with open(join(master_dir,'out.txt'),'a') as f:
            f.write('\n'+'-'*20+'\n')
            f.write(s)

    # check pdf ocr
    gen_10_pages(join(master_dir,'test.pdf'),master_dir)
    txt1 = OCR(join(master_dir,'test_10pages.pdf'),quiet=False)
    txt2 = OCR(join(master_dir,'test.pdf'),quiet=False)
    wt(txt2[len(txt2)*3//7:len(txt2)*4//7])

    # check image ocr
    txt3 = OCR(join(master_dir,'image.png'),remove_mid=False,quiet=False)
    wt(txt3)

    # check other ocr
    txt4 = OCR(join(master_dir,'proposal.pptx'),quiet=False)
    wt(txt4)
    txt5 = OCR(join(master_dir,'lec.docx'),remove_mid=False,quiet=False)
    wt(txt5)

    txt6 = OCR(join(master_dir,'out.txt'),quiet=False)
    assert txt6.find(txt4)!=-1
    print('Success!')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Exception occurs while testing: {e}')