import PyPDF2
import os

Len = 16**6
def Jzchash(s:str,mod=1000000007):
    code = 0
    for c in s:
        code = (code*(Len+1)+int(c.encode().hex(),base=16)) % mod
    return code

def encode(s:str):
    return str(Jzchash(s)).replace('-','n')

def gen_10_pages(file_path,out_path=None):
    if out_path is None:
        out_path = file_path.replace('.pdf','')+'_10pages.pdf'
    elif os.path.isdir(out_path):
        file_name = os.path.basename(file_path)
        if file_name.find('.pdf') == -1:
            raise ValueError('Cannot done with a non-pdf file')
        file_name = file_name.replace('.pdf','')+'_10pages.pdf'
        out_path = os.path.join(out_path, file_name)
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()
        for page_num in range(10):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)
        with open(out_path, 'wb') as output_file:
            pdf_writer.write(output_file)
