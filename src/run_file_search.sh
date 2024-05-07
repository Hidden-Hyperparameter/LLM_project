python ./file_search/gen_prompt.py > ./file_search/prompt.txt
cat ./file_search/prompt.txt ./all_files.txt | /share/ollama/ollama run llama3:70b > ./file_search/ans.txt
cat ./file_search/prompt.txt ./all_files.txt | /share/ollama/ollama run llama3:70b >> ./file_search/ans.txt
# python sublits.py > ans.txt
python ./file_search/sublist.py > ./file_search/prompt_final.txt
cat ./file_search/prompt_final.txt | /share/ollama/ollama run llama3:70b > ./files.txt