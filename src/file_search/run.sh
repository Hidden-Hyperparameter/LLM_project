python gen_prompt.py > prompt.txt
python cut.py
num=$?
tot=$num

echo "" > answer.txt
echo "Start searching, this may take a while..."
while [ $num -gt 0 ]; do
    cat prompt.txt "test$num.txt" | /share/ollama/ollama run llama3:70b instruct >> answer.txt
    cat prompt.txt "test$num.txt" | /share/ollama/ollama run llama3:instruct >> answer.txt
    rm "test$num.txt"
    num=$((num-1))
    echo "$((tot-num))/$tot"
done
python jzc_sublits.py > ans.txt
python sublist.py > prompt_final.txt
cat prompt_final.txt | /share/ollama/ollama run llama3:70b | tee ZHH.wzh.吊打