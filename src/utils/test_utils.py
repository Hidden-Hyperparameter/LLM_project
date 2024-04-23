from utils import CheckDependencies,OCR,gen_10_pages
def main():
    CheckDependencies()
    with open('./data/out.txt','w') as f:
        f.write('begin!\n')
    def wt(s:str):
        with open('./data/out.txt','a') as f:
            f.write('\n'+'-'*20+'\n')
            f.write(s)

    # check pdf ocr
    gen_10_pages('./data/test.pdf','./data/')
    txt1 = OCR('./data/test_10pages.pdf')
    txt2 = OCR('./data/test.pdf',remove_mid=True)
    assert txt2.startswith(txt1)
    wt(txt2[len(txt2)*3//7:len(txt2)*4//7])

    # check image ocr
    txt3 = OCR('./data/image.png')
    wt(txt3)

    # check other ocr
    txt4 = OCR('./data/proposal_ppt_04162057.pptx',remove_mid=True)
    wt(txt4)
    txt5 = OCR('./data/第十二讲.docx')
    wt(txt5)

    txt6 = OCR('./data/out.txt',remove_mid=True)
    assert txt6.find(txt4)!=-1
    print('Success!')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Exception occurs while testing: {e}')