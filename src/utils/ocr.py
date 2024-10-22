import PyPDF2
from langchain.document_loaders import PDFMinerLoader
import subprocess
import os
import fitz
from .others import encode,filetype
from transformers import pipeline

import av
import numpy as np
from transformers import AutoProcessor, AutoModelForCausalLM, LlavaForConditionalGeneration
import librosa
from transformers import Wav2Vec2ForCTC, Wav2Vec2Processor
import torch

from PIL import Image


VIDEO_MODEL = '/ssdshare/LLMs/git-base/'


TMP_DIR = '/ssdshare/.it/ocr'

DEVICE = 'cuda:3' if torch.cuda.is_available() else 'cpu'

class MyDataParallel(torch.nn.DataParallel):
    def __getattr__(self, name):
        try:
            return super().__getattr__(name)
        except AttributeError:
            return getattr(self.module, name)


def extract_text_from_pdf(file_path):
    """return text from one text-pdf"""
    with open(file_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = ''
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def _ocr_pdf(file_path:str,remove_mid=True):
    """directly run ocrmypdf on the file_path, return the text string"""
    out_path = file_path.replace('.pdf','')+'_ocr.pdf'
    try:
        subprocess.check_output(['ocrmypdf','-l','eng+chi_sim', '--force-ocr', file_path, out_path])
    except Exception as e:
        raise RuntimeError(f"An error occurred during OCR: {e}")
    tfile = extract_text_from_pdf(out_path)
    if remove_mid:
        os.remove(out_path)
    return tfile

def load_image_model():
    model_id = "/ssdshare/LLMs/llava-1.5-7b-hf/"
    processor = AutoProcessor.from_pretrained(model_id)
    model = LlavaForConditionalGeneration.from_pretrained(
        model_id, 
        torch_dtype=torch.float16, 
        low_cpu_mem_usage=True, 
    )
    model = MyDataParallel(model,device_ids=[3,2,1,0])
    model.to('cuda:3')
    return processor,model

def match_image_model_outouts(text:str):
    results = []
    lines = text.split('\n')
    for line in lines:
        if line.find('ASSISTANT:') != -1:
            results.append(line.removeprefix('ASSISTANT: '))
    return results

def Describe_PNG(file_path:str,suffix:str,remove_mid=True):
    prompt = "USER: <image>\nWhat is in this image\nASSISTANT:"
    image_file = file_path
    processor,model = load_image_model()
    raw_image = Image.open(image_file)
    x,y = (raw_image.size)
    raw_image = raw_image.resize((min(x,1350),min(y,1350)))
    inputs = processor(prompt, raw_image, return_tensors='pt').to(DEVICE, torch.float16)
    output = model.generate(**inputs, max_new_tokens=200, do_sample=False)
    texts = processor.decode(output[0][2:], skip_special_tokens=True)
    del model,inputs
    torch.cuda.empty_cache()
    return_values = ' '.join(match_image_model_outouts(texts))
    # print(return_values)
    return return_values

def read_video_pyav(container, indices):
    frames = []
    container.seek(0)
    start_index = indices[0]
    end_index = indices[-1]
    for i, frame in enumerate(container.decode(video=0)):
        if i > end_index:
            break
        if i >= start_index and i in indices:
            ratio = (frame.width * frame.height / 5e4)**0.5
            if ratio < 1:
                ratio = 1
            new_width = int(frame.width/ratio)
            new_height = int(frame.height/ratio)
            img = frame.to_image()
            img = img.resize((new_width, new_height))
            new_frame = av.VideoFrame.from_image(img)
            new_frame.pts = frame.pts
            frames.append(new_frame)
    return np.stack([x.to_ndarray(format="rgb24") for x in frames])

def sample_frame_indices( stop, num,start=0):
    indices = np.linspace(1,stop,num)
    indices = [int(x) for x in indices]
    return indices

def Describe_Video(file_path:str,remove_mid=True):
    processor,model = load_image_model()
    container = av.open(file_path)
    num_frames = container.streams.video[0].frames
    prompt = "USER: <image>\nWhat is in this image\nASSISTANT:"
    NUM_FRAMES_PICK = 25
    indices = sample_frame_indices(
        num=min(num_frames//5,NUM_FRAMES_PICK), stop=num_frames
    )
    frames = read_video_pyav(container, indices)
    texts = ''
    for i in range(NUM_FRAMES_PICK-1):
        inputs = processor([prompt], list(frames[i:i+1]), return_tensors='pt').to('cuda:3', torch.float16)
        output = model.generate(**inputs, max_new_tokens=100, do_sample=False)
        texts += ((processor.decode(output[0][2:], skip_special_tokens=True))+'\n')
        del inputs,output
        torch.cuda.empty_cache()
    return_values =  'This is a video. The contents in images are:'+'\n'.join(match_image_model_outouts(texts))
    # print(return_values)
    return return_values

def OCR_VIDEO(file_path:str,suffix:str,remove_mid=True):
    print('[OCR.PY] running ocr for video files...')
    out_path = os.path.join(TMP_DIR,encode(file_path.removesuffix(suffix))+'.mp4')
    if suffix != '.mp4':
        try:
            subprocess.run(['ffmpeg','-i',file_path,out_path])
        except Exception as e:
            print(f'[OCR.PY]: Unhandled Video Type: {file_path}. Exception raised: {e}')
            if os.path.exists(out_path) and remove_mid:
                os.remove(out_path)
            return
    texts = Describe_Video(file_path,remove_mid)
    audio_texts = get_audio_description(file_path,suffix,remove_mid)
    if remove_mid and suffix!='.mp4':
        os.remove(out_path)
    return texts+f"""

Additionaly, there is some audio information: {audio_texts}
"""

def OCR_AUDIO(file_path:str,suffix:str,remove_mid=True):
    texts = dict()
    for lang in ['english','chinese']:
        MODEL_ID = f"/ssdshare/LLMs/wav2vec/wav2vec2-{lang}"

        audio_processor = Wav2Vec2Processor.from_pretrained(MODEL_ID)
        audio_model = Wav2Vec2ForCTC.from_pretrained(MODEL_ID)
        audio_model.to(DEVICE)

        y,fps = librosa.load(file_path)
        ten_seconds = 10 * fps
        cutted = [y[i:i+ten_seconds] for i in range(0,len(y),ten_seconds)]
        cutted[-1] = np.concatenate((cutted[-1],np.zeros(ten_seconds-len(cutted[-1]))),axis=0)
        audio = np.stack(cutted,axis=0)
        inputs = audio_processor(audio, sampling_rate=16_000, return_tensors="pt", padding=True).to(DEVICE)

        with torch.no_grad():
            logits = audio_model(inputs.input_values, attention_mask=inputs.attention_mask).logits

        predicted_ids = torch.argmax(logits, dim=-1)
        predicted_sentences = audio_processor.batch_decode(predicted_ids)
        texts[lang]=' '.join(predicted_sentences)
        del audio_processor,audio_model
        torch.cuda.empty_cache()
    text_chn = texts['chinese']
    text_eng = texts['english']
    return f"""This is a audio with both Chinese and English Language. Please note that the audio contains some noise, so the text provided below may not be accurate. If you find some texts being non-sense, please ignore it.
In Chinese, this audio contains the following text:
{text_chn}

In English, this audio contains the following text:
{text_eng}
"""


def get_audio_description(video_path:str,suffix:str,remove_mid=True):
    out_path = os.path.join(TMP_DIR,encode(video_path.removesuffix(suffix))+'_audio.mp3')
    try:
        subprocess.check_output(['ffmpeg','-i',video_path,'-vn',out_path])
    except subprocess.CalledProcessError: # this video may not have audio, or not supported
        return ''
    texts = OCR_AUDIO(video_path,'.mp3',remove_mid)
    if remove_mid:
        os.remove(out_path)
    return texts

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
    description = Describe_PNG(file_path,suffix,remove_mid)
    return f"""This is a image, the description of the image is: "{description}". 
    Additionaly, there is some texts in the image: '{tfile}'"""

def ocrmypdf_ocr(page_start,page_end,py_pdf_reader:PyPDF2.PdfReader,output_folder,remove=True,quiet=True):
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

def ocr_image_based_pdf(input_pdf:str,max_step:int=20,quiet=True,remove=True):
    # print('[INFO] ocr_image_based_pdf')
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
                text += ocrmypdf_ocr(i,i+step,py_pdf_reader,output_folder=output_folder,quiet=quiet,remove=remove)
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
        if step==max_step:
            max_step += 2
        # elif max_step > 4:
        #     max_step //=2 
    if remove:
        # forcely remove output_folder, since it isn't empty
        subprocess.run(['rm','-rf',output_folder])
    return '\n'.join(text)

def ocr_text_based_pdf(input_pdf:str,quiet=True,remove=True):
    # print('[INFO] oce_text_based_pdf')
    data = PDFMinerLoader(input_pdf).load()
    if sum([len(d.page_content) for d in data])/len(data) < 300:
        return False
    return '\n'.join([d.page_content for d in data])

def OCR_PDF(input_pdf:str,quiet=True,remove=True):
    # print('[INFO] OCR_PDF')
    ans = ocr_text_based_pdf(input_pdf,quiet=quiet,remove=remove)
    if ans != False:
        return ans
    return ocr_image_based_pdf(input_pdf,quiet=quiet,remove=remove)

def _replace_space(s:str):
    # print('----------input---------\n\n',s)
    l = [c for c in s]
    lc = l.copy()
    import string
    alls = string.ascii_lowercase+string.ascii_uppercase
    j = 0
    for i,c in enumerate(lc):
        if c==' ' and (i==0 or not lc[i-1] in alls) and (i+1==len(lc) or not lc[i+1] in alls):
            l = l[:j]+l[j+1:]
        else:
            j += 1
    output = ''.join(l)
    # print('----------output---------\n\n',output)
    return output

def _raw_OCR(file_path:str,remove_mid=True,quiet=True):
    # first convert path to absolute path
    file_path = os.path.abspath(file_path)
    if not quiet:
        print(f'[OCR.PY]: running ocr for {file_path}')
    file_real,file_suffix = os.path.splitext(file_path)[:2]
    file_name = os.path.basename(file_real)
    
    file_type = filetype(file_path)
    # print('[OCR.PY] the file type is',file_type)
    if os.path.isdir(file_path):
        raise NotImplementedError(f'have not implemented ocr on file type as {file_path}')    
    elif file_suffix=='.pdf':
        print('[OCR.PY]:Running ocr for pdf files')
        return OCR_PDF(file_path,quiet=quiet,remove=remove_mid)
    elif file_type == 'image':
        return OCR_PNG(file_path,file_suffix,remove_mid)
    elif file_type == 'video':
        return OCR_VIDEO(file_path,file_suffix,remove_mid=remove_mid)
    elif filetype(file_path)=='text':
        return open(file_path, 'r').read()
    else:
        try:
            subprocess.check_output(['soffice', '--headless', '--convert-to', 'pdf',file_path])
        except subprocess.CalledProcessError:
            return file_path+"(Could not be OCR'ed, maybe a binary file or other unsupported file type)"     
        out_path = f'./{file_name}.pdf'
        if not os.path.exists(out_path):
            raise RuntimeError(f'[OCR]: ocr for {file_path} failed')
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

