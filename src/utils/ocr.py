import PyPDF2
import subprocess
import os
def extract_text_from_pdf(file_path):
    """return text from one text-pdf"""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

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

def OCR_PDF(file_path:str,remove_mid=False):
    out_path = file_path.replace('.pdf','')+'_ocr.pdf'
    try:
        subprocess.check_output(['ocrmypdf','-l','eng+chi_sim', '--force-ocr', file_path, out_path])
    except Exception as e:
        raise RuntimeError(f"An error occurred during OCR: {e}")
    tfile = extract_text_from_pdf(out_path)
    if remove_mid:
        os.remove(out_path)
    return tfile

def OCR_PNG(file_path:str,suffix:str,remove_mid=False):
    out_path = file_path.replace(suffix,'')+'_ocr'
    try:
        subprocess.run(['tesseract', file_path, out_path, '-l','eng+chi_sim'])
    except Exception as e:
        print(f"An error occurred during OCR: {e}")
    out_path+='.txt'
    tfile = open(out_path).read()
    if remove_mid:
        os.remove(out_path)
    return tfile

def _replace_space(s:str):
    l = [c for c in s]
    lc = l.copy()
    import string
    alls = string.ascii_lowercase+string.ascii_uppercase
    j = 0
    for i,c in enumerate(lc):
        if c==' ' and (i==0 or not lc[i-1] in alls) and (i+1<len(lc) or not lc[i+1] in alls):
            l = l[:j]+l[j+1:]
        else:
            j += 1
    return ''.join(l)

def _raw_OCR(file_path:str,remove_mid=False):
    file_real,file_suffix = os.path.splitext(file_path)[:2]
    file_name = os.path.basename(file_real)
    if os.path.isdir(file_path):
        raise NotImplementedError(f'have not implemented ocr on file type as {file_path}')    
    elif file_suffix=='.pdf':
        return OCR_PDF(file_path,remove_mid)
    elif file_suffix in ['.jpg', '.jpeg', '.png']:
        return OCR_PNG(file_path,file_suffix,remove_mid)
    elif file_suffix in ['.py', '.txt', '.cpp', '.tex', '.md', '.java', '.html', '.css','','.sh','.bat']:
        return open(file_path, 'r').read()
    else:
        try:
            subprocess.check_output(['soffice', '--headless', '--convert-to', 'pdf',file_path])
        except subprocess.CalledProcessError:
            raise RuntimeError(f'Failure to OCR file {file_path}')        
        out_path = f'./{file_name}.pdf'
        txt = OCR_PDF(out_path,remove_mid)
        if remove_mid:
            os.remove(out_path)
        else:
            subprocess.run(['mv',out_path,file_real + '.pdf'])
        return txt
        
def OCR(file_path:str,remove_mid=False):
    """Do OCR for all files. Return the text string"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'Cannot locate file {file_path}')
    return _replace_space(_raw_OCR(file_path,remove_mid))