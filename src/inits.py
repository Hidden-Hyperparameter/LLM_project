import os
PATHES_REQUIRED = [
    '/ssdshare/.it/file_search',
    '/ssdshare/.it/final_query',
]
for path in PATHES_REQUIRED:
    os.makedirs(path,exist_ok=True)
    assert os.path.exists(path),'[INIT.PY] mkdir failed'