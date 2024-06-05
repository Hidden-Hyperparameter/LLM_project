python ./scripts/sim_search.py
num=$?
tot=$num
echo '---------------------------'
echo Number of similarty search results: $num
echo '---------------------------'

# format prompt
cat /ssdshare/.it/query.txt > /ssdshare/.it/formatted.qry
# NOTE: this code is no longer used!!!
# python ./final_query/rephrase.py > /ssdshare/.it/format_query.prompt
# cat /ssdshare/.it/format_query.prompt | /share/ollama/ollama run llama3:70b-instruct > /ssdshare/.it/formatted.qry

python ./final_query/gen_prompt.py $num 

echo '' > /ssdshare/.it/lots.txt
while [ $num -gt 0 ]; do
    echo "--- text $((tot-num))" >> /ssdshare/.it/lots.txt
    cat /ssdshare/.it/final_query/prompt$num.txt | /share/ollama/ollama run llama3:70b-instruct >> /ssdshare/.it/lots.txt 
    num=$((num-1))
    echo "$((tot-num))/$tot"
done

cat ./final_query/MUST-NOT-DELETE-header.txt /ssdshare/.it/formatted.qry ./final_query/MUST-NOT-DELETE-middle.txt /ssdshare/.it/lots.txt ./final_query/MUST-NOT-DELETE-tail.txt | tee /ssdshare/.it/tuptup.txt |  /share/ollama/ollama run llama3:70b-instruct > /ssdshare/.it/putput.txt
