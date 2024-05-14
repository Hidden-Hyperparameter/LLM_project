python ./sim_search.py
python ./final_query/gen_prompt.py > /ssdshare/.it/final_query/prompt.txt
cat /ssdshare/.it/final_query/prompt.txt | /share/ollama/ollama run llama3:70b