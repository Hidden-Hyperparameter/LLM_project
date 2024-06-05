import os
if not os.path.exists('/ssdshare/.it/final_query/related.txt'):
    raise RuntimeError('[FINAL_QUERY/GEN_PROMPT.PY]: cannot find final_query/related.txt')
# if not os.path.exists('/ssdshare/.it/query_formatted.txt'):
#     raise RuntimeError('[FINAL_QUERY/GEN_PROMPT.PY]: cannot find query_formatted.txt')

with open('/ssdshare/.it/final_query/related.txt', 'r') as file:
    context = file.read()

with open('/ssdshare/.it/query.txt', 'r') as query_file:
    query = query_file.read()

print(f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are an information integrator. You will be asked a question.
Answer the question based on the given context.
Aggregate all the non-trivial answers together to form a complete one.
Write in MARKDOWN FORMAT.
ALWAYS CITE THE SOURCES LIKE THE EXAMPLE! (FILES' DIRECTORY)
If you cannot give an answer from the context, just say you haven't found any related information to answer this question.

# Example Answer
A quotient group is obtained by collapsing or “dividing out” by a normal subgroup $K$, resulting in the set $G/K$.

*Sources:*
* /ssdshare/.it/test/data/test.pdf
<|eot_id|>
<|start_header_id|>user<|end_header_id|>

# Context
{context}

# Question
{query}
<|eot_id|>
<|start_header_id|>assistant<|end_header_id|>
""")

# # Context
# {context}

# # Instruction
# You are an information integrator. You will be asked a question.
# Answer the question based on the given context.
# Aggregate all the non-trivial answers together to form a complete one.
# Write in MARKDOWN FORMAT.
# ALWAYS CITE THE SOURCES LIKE THE EXAMPLE! (FILES' DIRECTORY)
# If you cannot give an answer from the context, just say you haven't found any related information to answer this question.

# # Example Answer
# A quotient group is obtained by collapsing or “dividing out” by a normal subgroup $K$, resulting in the set $G/K$.

# *Sources:*
# * /ssdshare/.it/test/data/test.pdf

# # Question
# {query}

# # Answer Based on Given Context