from utils import extract_text_from_pdf,OCR
# text = extract_text_from_pdf('./data/test_10pages_ocr.pdf')
# with open('./1.txt','w') as f:
#     f.write(text)
text = extract_text_from_pdf('./course_desc.pdf')
with open('./dec.txt','w') as f:
    f.write(text)