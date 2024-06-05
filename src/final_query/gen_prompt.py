import os,sys
# if not os.path.exists('/ssdshare/.it/final_query/related.txt'):
#     raise RuntimeError('[FINAL_QUERY/GEN_PROMPT.PY]: cannot find final_query/related.txt')
# # if not os.path.exists('/ssdshare/.it/query_formatted.txt'):
# #     raise RuntimeError('[FINAL_QUERY/GEN_PROMPT.PY]: cannot find query_formatted.txt')

for i in range(int(sys.argv[1])):
    with open(f'/ssdshare/.it/final_query/related{i}.txt', 'r') as file:
        context = file.read()

    with open('/ssdshare/.it/query.txt', 'r') as query_file:
        query = query_file.read()

    with open(f'/ssdshare/.it/final_query/prompt{i+1}.txt','w') as f:
        f.write(f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

Imagine that you do not have any knowledge in specific fields, but you are very strong at summarizing informations. Please only use the `Context` provided below to answer the question. You should aggregate all the non-trivial answers together to form a complete one.
                
If the `Context` provided is not closely related with the `Question` at all, you MUST answer "None.". Otherwise, you should ALWAYS try to answer by making connections between the `Question` and the `Context`. However, in ANY case, do NOT use your OWN knowledge to answer.

# Requirements:
1. If you can answer, the you MUST cite THE SOURCES (file directories) like the example. Otherwise, you should directly say "None".
2. For texts and formulas, use MARKDOWN FORMAT; for SOURCE CITATION, use the FOLLOWING format in the `Example Answer` part. 

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
<|start_header_id|>assistant<|end_header_id|>\n""")

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