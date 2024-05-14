python ./file_search/gen_prompt.py > /ssdshare/.it/file_search/prompt.txt
cat /ssdshare/.it/file_search/prompt.txt /ssdshare/.it/all_files.txt | /share/ollama/ollama run llama3:70b > /ssdshare/.it/file_search/ans.txt
cat /ssdshare/.it/file_search/prompt.txt /ssdshare/.it/all_files.txt | /share/ollama/ollama run llama3:70b >> /ssdshare/.it/file_search/ans.txt
# python sublits.py > ans.txt
python ./file_search/sublist.py > /ssdshare/.it/file_search/prompt_final.txt
cat /ssdshare/.it/file_search/prompt_final.txt | /share/ollama/ollama run llama3:70b > /ssdshare/.it/files.txt