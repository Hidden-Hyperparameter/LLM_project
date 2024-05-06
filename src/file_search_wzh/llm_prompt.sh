python gen_prompt.py > prompt.txt
cat prompt.txt test.txt | /share/ollama/ollama run llama3:70b > ans.txt
cat prompt.txt test.txt | /share/ollama/ollama run llama3:70b >> ans.txt
python sublist.py > prompt_final.txt
cat prompt_final.txt | /share/ollama/ollama run llama3:70b