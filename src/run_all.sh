echo $1 > /ssdshare/.it/query.txt
python inits.py
sh run_file_search_xibo.sh $2
# sh format_query.sh
sh run_final_query.sh