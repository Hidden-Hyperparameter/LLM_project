import PyPDF2
import os
import subprocess
import mimetypes
TMP_DIR_1 = '/ssdshare/.it/utils/'

Len = 16**6
def Jzchash(s:str,mod=1000000007):
    code = 0
    for c in s:
        code = (code*(Len+1)+int(c.encode().hex(),base=16)) % mod
    return code

def encode(s:str):
    return str(Jzchash(s)).replace('-','n')

def _gen_10_pages(file_path,out_path=None):
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
        for page_num in range(min(10,len(pdf_reader.pages))):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)
        with open(out_path, 'wb') as output_file:
            pdf_writer.write(output_file)

def gen_10_pages(file_path,out_path=None):
    os.makedirs(TMP_DIR_1,exist_ok=True)
    if not file_path.endswith('.pdf'):
        file_real,file_suffix = os.path.splitext(file_path)[:2]
        file_name = os.path.basename(file_real)
        try:
            # print(' '.join(['soffice', '--headless', '--convert-to', 'pdf',file_path]))
            subprocess.check_output(['soffice', '--headless', '--convert-to', 'pdf',file_path])
        except subprocess.CalledProcessError:
            raise RuntimeError(f'[GEN_PAGES]\033[31m[ERROR]\033[0m:Failure to OCR file {file_path}')
        tmp_out_path = f'./{file_name}.pdf'
        if not os.path.exists(tmp_out_path):
            raise RuntimeError(f'[GEN_PAGES]\033[31m[ERROR]\033[0m:Failure to OCR file {file_path}')
        _gen_10_pages(tmp_out_path,out_path)
        os.remove(tmp_out_path)
    else:
        _gen_10_pages(file_path,out_path)


def gen_last_pages(file_path,out_path):
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        pdf_writer = PyPDF2.PdfWriter()
        for page_num in range(10,len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)
        with open(out_path, 'wb') as output_file:
            pdf_writer.write(output_file)

def filetype(filename):
    """
    Input: file name optionally with path
    Output: file type: 'text', 'image', 'audio', 'video', 'application' (binary file)
    """
    kind, _ = mimetypes.guess_type(filename)
    if kind == None:
        return 'text'
    return kind.split('/')[0]

if __name__ == '__main__':
    print(Jzchash('/ssdshare/.db_project/src/tests/data/hierarchical_data_simple/dir/note_for_lec07.md'))