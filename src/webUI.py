import gradio as gr
import os,sys
# sys.path.append('..')
# sys.path.append('.')
from utils.dependency import CheckDependencies
CheckDependencies()
os.environ['HTTP_PROXY']=''
os.environ['HTTPS_PROXY']=''
os.environ['ALL_PROXY']=''

def FIND(query, max_p,filters):
    """filters: the filename must contain the given {filters}."""
    print('UI recieve')
    os.system(f'sh /ssdshare/.db_project/src/run_all.sh "{query}" "{filters}"')
    with open('/ssdshare/.it/putput.txt', 'r') as f:
        data = f.readlines()
    if 'student' in data[0]:
        data = data[1:]
    data = '\n'.join(data)
    return data

demo = gr.Interface(
    fn=FIND,
    inputs=["text", "slider",'text'],
    #output:markdown
    outputs="markdown",
    title="File Search",
    description="Search for files based on a query."
)

demo.launch(server_port=1145)

## sh /ssdshare/.db_project/src/run_all.sh prompt