from utils import extract_text_from_pdf,OCR
# text = extract_text_from_pdf('./data/test_10pages_ocr.pdf')
# with open('./1.txt','w') as f:
#     f.write(text)
text = extract_text_from_pdf('./data/test_ocr.pdf')
with open('./data/full_alg.txt','w') as f:
    f.write(text)