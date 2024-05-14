import gradio as gr
import requests
import json
import os
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
         
from fastapi import FastAPI, Request
from pydantic import BaseModel
import uvicorn

import gradio as gr

def FIND(query, max_p):
    os.system(f'sh /ssdshare/.2024040125_2023040165_2023040163_project/src/run_all.sh "{query}"> /ssdshare/.2024040125_2023040165_2023040163_project/src/putput.txt')
    with open('/ssdshare/.2024040125_2023040165_2023040163_project/src/putput.txt', 'r') as f:
        data = f.read()
    return data

demo = gr.Interface(
    fn=FIND,
    inputs=["text", "slider"],
    #output:markdown
    outputs="text",
    title="File Search",
    description="Search for files based on a query."
)
demo.launch(share=True)

## sh /ssdshare/.2024040125_2023040165_2023040163_project/src/run_all.sh prompt