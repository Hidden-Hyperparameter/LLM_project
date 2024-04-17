from dependency import CheckDependencies
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

def OCR(file_path):
    """Use terminal command ` ocrmypdf --force-ocr <input path> <output path>` to generate ocr pdf """
    if not os.path.isfile(file_path) or not file_path.endswith('.pdf'):
        raise ValueError('Can only do OCR with pdf')
    out_path = file_path.replace('.pdf','')+'_ocr.pdf'
    try:
        subprocess.run(['ocrmypdf', '--force-ocr', file_path, out_path])
    except Exception as e:
        print(f"An error occurred during OCR: {e}")
    return extract_text_from_pdf(out_path)
