import mimetypes

def filetype(filename):
    """
    Input: file name optionally with path
    Output: file type: 'text', 'image', 'audio', 'video', 'application' (binary file)
    """
    kind, _ = mimetypes.guess_type(filename)
    if kind == None:
        return 'text'
    return kind.split('/')[0]

if __name__ == '__main__':
    print(filetype('r.json'))