from utils import CheckDependencies,OCR,gen_10_pages
def main():
    CheckDependencies()
    gen_10_pages('./data/test.pdf','./data/')
    txt1 = OCR('./data/test_10pages.pdf')
    txt2 = OCR('./data/test.pdf')
    assert txt2.startswith(txt1)
    with open('./data/out.txt','w') as f:
        f.write(txt2[len(txt2)*3//7:len(txt2)*4//7])
    print('Success!')

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(f'Exception occurs while testing: {e}')