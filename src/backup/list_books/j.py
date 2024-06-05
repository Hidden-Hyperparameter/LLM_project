from langchain_community.llms import LlamaCpp
from langchain_core.callbacks import CallbackManager, StreamingStdOutCallbackHandler
from langchain_core.prompts import PromptTemplate
import os

print(os.environ['DLLAMA_CUBLAS'])

template = """Question: {question}

Answer: Let's work this out in a step by step way to be sure we have the right answer."""

prompt = PromptTemplate.from_template(template)
# Callbacks support token-wise streaming
# callback_manager = CallbackManager([StreamingStdOutCallbackHandler()])

n_gpu_layers = -1  # The number of layers to put on the GPU. The rest will be on the CPU. If you don't know how many layers there are, you can use -1 to move all to GPU.
n_batch = 512  # Should be between 1 and n_ctx, consider the amount of VRAM in your GPU.

# Make sure the model path is correct for your system!
llm = LlamaCpp(
    model_path="/share/ollama/models/blobs/sha256-4fe022a8902336d3c452c88f7aca5590f5b5b02ccfd06320fdefab02412e1f0b",
    n_gpu_layers=n_gpu_layers,
    n_batch=n_batch,
    # callback_manager=callback_manager,
    verbose=True,  # Verbose is required to pass to the callback manager
)

print('LLm loaded')

llm_chain = prompt | llm
question = "What NFL team won the Super Bowl in the year Justin Bieber was born?"

print('!!!'*1000)
llm_chain.invoke({"question": question})