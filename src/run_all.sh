echo $1 > /ssdshare/.it/query.txt
python inits.py
sh run_file_search.xibo
# sh format_query.sh
sh run_final_query.sh