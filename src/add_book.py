from run_process import GenerateTagsFromPath,MakeDBFromPath

if __name__ == '__main__':
    file_path = './test.pdf'
    GenerateTagsFromPath(file_path,quiet=True)
    MakeDBFromPath(file_path,quiet=True)