import PyPDF2
import subprocess
import os
import fitz
from .others import encode
TMP_DIR = '/ssdshare/.it/ocr'


def extract_text_from_pdf(file_path):
    """return text from one text-pdf"""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def _ocr_pdf(file_path:str,remove_mid=True):
    out_path = file_path.replace('.pdf','')+'_ocr.pdf'
    try:
        subprocess.check_output(['ocrmypdf','-l','eng+chi_sim', '--force-ocr', file_path, out_path])
    except Exception as e:
        raise RuntimeError(f"An error occurred during OCR: {e}")
    tfile = extract_text_from_pdf(out_path)
    if remove_mid:
        os.remove(out_path)
    return tfile

def OCR_PNG(file_path:str,suffix:str,remove_mid=True):
    out_path = os.path.join(TMP_DIR,encode(file_path.replace(suffix,'')+'_ocr'))
    try:
        subprocess.run(['tesseract', file_path, out_path, '-l','eng+chi_sim'])
    except Exception as e:
        print(f"[OCR.PY]:An error occurred during OCR: {e}")
    out_path+='.txt'
    tfile = open(out_path).read()
    if remove_mid:
        os.remove(out_path)
    return tfile

def pdf_ocr(page_start,page_end,py_pdf_reader:PyPDF2.PdfReader,output_folder,remove=True,quiet=True):
    pdf_writer = PyPDF2.PdfWriter()
    for page in py_pdf_reader.pages[page_start:page_end]:
        pdf_writer.add_page(page)
    out_path = os.path.join(output_folder,f'page{page_start}-page{page_end}.pdf')
    with open(out_path, 'wb') as output_file:
        pdf_writer.write(output_file)
        if not quiet:
            print(f'[OCR.PY]:pdf file written in {out_path}')
    texts = _ocr_pdf(out_path)
    if remove:
        os.remove(out_path)
    return [texts]

def fitz_ocr(page_start,page_end,fitx_pdf_doc:fitz.Document,output_folder,remove=True):
    texts = []
    for page_num in range(page_start,page_end):
        page = fitx_pdf_doc.load_page(page_num)
        pix = page.get_pixmap()
        output_path = os.path.join(output_folder, f"page{page_num}.jpg")
        pix._writeIMG(output_path, format_='jpg', jpg_quality=100)
        texts.append(OCR_PNG(output_path,suffix='.jpg',remove_mid=remove))
        if remove:
            os.remove(output_path)
    return texts

def OCR_PDF(input_pdf:str,max_step:int=10,quiet=True,remove=True):
    # print(input_pdf)
    output_folder = os.path.join(TMP_DIR,encode(input_pdf.replace('.pdf','')+'_ocr'))
    if os.path.exists(output_folder) and os.path.isfile(output_folder):
        os.remove(output_folder)
    os.makedirs(output_folder,exist_ok=True)
    # print(f'made folder in {output_folder}')
    # exit()
    text = []
    py_pdf_reader = PyPDF2.PdfReader(open(input_pdf,'rb'))
    pdf_document = fitz.open(input_pdf)
    page_range = len(py_pdf_reader.pages)
    # perform binary search
    i = 0
    while i < page_range:
        step = max_step
        while True:
            if step==0:
                # must use fitz ocr
                text += fitz_ocr(i,i+1,pdf_document,output_folder=output_folder,remove=remove)
                if not quiet:
                    print(f"[OCR.PY]\033[31m[INFO]\033[0m using fitz for page {i}")
                i += 1
                break
            try:
                text += pdf_ocr(i,i+step,py_pdf_reader,output_folder=output_folder,quiet=quiet,remove=remove)
                i += step
                break
            except RuntimeError:
                if not quiet:
                    print(f"[OCR.PY]\033[31m[INFO]\033[0m ocr failed when opening page {i} to page {i+step}")
                if remove:
                    pdf_ocrout_path = os.path.join(output_folder,f'page{i}-page{i+step}.pdf')
                    if os.path.exists(pdf_ocrout_path):
                        os.remove(pdf_ocrout_path)
                step = step//2

    if remove:
        # forcely remove output_folder, since it isn't empty
        subprocess.run(['rm','-rf',output_folder])
    return '\n'.join(text)


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

def _raw_OCR(file_path:str,remove_mid=True,quiet=True):
    # first convert path to absolute path
    file_path = os.path.abspath(file_path)
    if not quiet:
        print(f'[OCR.PY]: running ocr for {file_path}')
    file_real,file_suffix = os.path.splitext(file_path)[:2]
    file_name = os.path.basename(file_real)
    if os.path.isdir(file_path):
        raise NotImplementedError(f'have not implemented ocr on file type as {file_path}')    
    elif file_suffix=='.pdf':
        print('[OCR.PY]:Running ocr for pdf files')
        return OCR_PDF(file_path,quiet=quiet,remove=remove_mid)
    elif file_suffix in ['.jpg', '.jpeg', '.png']:
        return OCR_PNG(file_path,file_suffix,remove_mid)
    else:
        try:
            subprocess.check_output(['soffice', '--headless', '--convert-to', 'pdf',file_path])
        except subprocess.CalledProcessError:
            return open(file_path, 'r').read()
            raise RuntimeError(f'Failure to OCR file {file_path}')        
        out_path = f'./{file_name}.pdf'
        txt = OCR_PDF(out_path,remove=remove_mid,quiet=quiet)
        if remove_mid:
            os.remove(out_path)
        else:
            subprocess.run(['mv',out_path,file_real + '.pdf'])
        return txt
        
        
def OCR(file_path:str,remove_mid=True,quiet=True):
    """Do OCR for all files. Return the text string"""
    if not os.path.exists(TMP_DIR):
        os.makedirs(TMP_DIR)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'Cannot locate file {file_path}')
    return _replace_space(_raw_OCR(file_path,remove_mid,quiet=quiet))

