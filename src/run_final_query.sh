python ./sim_search.py
python ./final_query/gen_prompt.py > ./final_query/prompt.txt
cat ./final_query/prompt.txt | /share/ollama/ollama run llama3:70b