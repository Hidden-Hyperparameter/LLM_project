from langchain.agents import AgentType, Tool
import os

def list_files(str):
    os.system("sh ./run_file_search_final.sh " + str)
    with open("/ssdshare/.it/files.txt", 'r') as file:
        return file.read()

def search(str):
    os.system("sh ./run_all.sh " + str)
    with open("/ssdshare/.it/result.txt", 'r') as file:
        return file.read()

tools = [
    Tool(
        name="list files",
        func=list_files,
        description="List all files related to the given query."
    ), 
    Tool(
        name="search in files",
        func=search, 
        description="Search the query automatically in all files."
    )
]

from langchain.agents import initialize_agent
from langchain.llms import LlamaCpp

# Construct the agent. We will use the default agent type here.
# See documentation for a full list of options.

llm = LlamaCpp(
    model_path=r"/share/ollama/models/blobs/sha256-4fe022a8902336d3c452c88f7aca5590f5b5b02ccfd06320fdefab02412e1f0b",
#     n_gpu_layers=n_gpu_layers,
#     n_batch=n_batch,
#     n_ctx=4000,
#     f16_kv=True,  # MUST set to True, otherwise you will run into problem after a couple of calls
#     callback_manager=callback_manager,
# #     verbose=False,
#     temperature=0.1,
#     device=0,
    streaming=False
)


agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

import multiprocessing

if __name__ == '__main__':
    process = multiprocessing.Process(target=run_agent)
    process.start()
