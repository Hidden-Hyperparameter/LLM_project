python ./sim_search.py
python ./final_query/rephrase.py > /ssdshare/.it/format_query.prompt
cat /ssdshare/.it/format_query.prompt | /share/ollama/ollama run llama3:70b-instruct > /ssdshare/.it/formatted.qry
python ./final_query/gen_prompt.py > /ssdshare/.it/final_query/prompt.txt
cat /ssdshare/.it/final_query/prompt.txt | /share/ollama/ollama run llama3:70b-instruct