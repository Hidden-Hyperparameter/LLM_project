import os

with open('/ssdshare/.it/query.txt', 'r') as query_file:
    query = query_file.read()

print(f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>

You are a smart question rephraser. You will be given a question.
You need to rephrase the question so that I can use it to text search.
Only add specific keywords that are likely to appear in the context.
You just need to output the revised question and I will do the searching.
You need to do your best to make the question closer to the original text (answer).
If the question is already specific, you do not have to make any changes, just output the original question.
ONLY OUTPUT THE REPHRASED VERSION.

# Example
Input question: What is a splitting field?
Output rephrased version:
What is the definition and properties of splitting field?

[CAUTION: in the example, you might want to add "in abstract algebra" at the end. DON'T DO THIS since the phrase "abstract algebra" is unlikely to appear in the definition context of splitting field.]

Input question: What is a normal subgroup?
Output rephrased version:
What is the definition and properties of normal subfield?

[CAUTION: in the example, you might want to add "in group theory" at the end. DON'T DO THIS since the phrase "group theory" is unlikely to appear in the definition context of normal subfield.]

<|eot_id|>
<|start_header_id|>user<|end_header_id|>
{query}
<|start_header_id|>assistant<|end_header_id|>
""")