echo $1 > /ssdshare/.it/query.txt
python scripts/inits.py
sh run_file_search_final.sh $2 #> /dev/null 2>&1
# sh format_query.sh
sh run_final_query.sh # > /ssdshare/.it/result.txt