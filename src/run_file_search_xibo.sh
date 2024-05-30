python ./file_search/gen_prompt.py $1 > /ssdshare/.it/file_search/prompt.txt
python /ssdshare/.db_project/src/file_search/cut.py
num=$?
tot=$num
echo $num
echo "-----------------------------"
echo "" > /ssdshare/.it/file_search/ans.txt
while [ $num -gt 0 ]; do
cat /ssdshare/.it/file_search/prompt.txt /ssdshare/.it/all_files_cutted$num.txt /ssdshare/.it/assistant.prompt | /share/ollama/ollama run llama3:70b-instruct >> /ssdshare/.it/file_search/ans.txt
cat /ssdshare/.it/file_search/prompt.txt /ssdshare/.it/all_files_cutted$num.txt /ssdshare/.it/assistant.prompt | /share/ollama/ollama run llama3:70b-instruct >> /ssdshare/.it/file_search/ans.txt
#   rm "/ssdshare/.it/all_files_cutted$num.txt"
    num=$((num-1))
    echo "$((tot-num))/$tot"
done

# python sublits.py > ans.txt
python ./file_search/sublist.py > /ssdshare/.it/file_search/prompt_final.txt 2> ./debug.log
cat /ssdshare/.it/file_search/prompt_final.txt | /share/ollama/ollama run llama3:70b-instruct > /ssdshare/.it/files.txt