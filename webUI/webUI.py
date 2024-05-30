import gradio as gr
import requests
import json
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
         
from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn

import gradio as gr

def FIND(query, max_p,filter):
    os.system(f'sh /ssdshare/.db_project/src/run_all.sh "{query}" "{filter}"> /ssdshare/.db_project/src/putput.txt')
    with open('/ssdshare/.db_project/src/putput.txt', 'r') as f:
        data = f.read()
    return data

demo = gr.Interface(
    fn=FIND,
    inputs=["text", "slider",'filter'],
    #output:markdown
    outputs="markdown",
    title="File Search",
    description="Search for files based on a query."
)
demo.launch(share=True)

## sh /ssdshare/.db_project/src/run_all.sh prompt