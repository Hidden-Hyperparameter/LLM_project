with open('./final_query/related.txt', 'r') as file:
    context = file.read()

with open('./query.txt', 'r') as query_file:
    query = query_file.read()

print(f"""# Context
{context}

# Instruction
You are an information integrator. You will be asked a question.
Answer the question based on the given context.
Aggregate all the non-trivial answers together to form a complete one.
ALWAYS CITE THE SOURCES LIKE THE EXAMPLE! (FILES' DIRECTORY)
If you cannot give an answer from the context, just say you haven't found any related information to answer this question.

# Example Answer
A quotient group is obtained by collapsing or “dividing out” by a normal subgroup K, resulting in the set G/K.

Sources:
1. ./test/data/test.pdf

# Question
{query}

# Answer Based on Given Context
""")