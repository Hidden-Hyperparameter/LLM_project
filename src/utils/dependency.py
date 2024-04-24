def _check_package(package:str,url:str,additional:str=''):
    import subprocess
    try:
        # Run the apt command to check if ocrmypdf is installed
        subprocess.check_output([package,'--help'])
        print(f"Check dependencies: {package} installed")
    except:
        raise RuntimeError(f'You have not installed the {package} package yet, use apt(or pip) to install {package}, download from {url}, or check our `README.md`. {additional}')
def CheckDependencies():
    """ Make sure that the user has installed the `ocrmypdf` software packages using apt"""
    _check_package('tesseract','https://github.com/tesseract-ocr/tesseract','Notice: use apt install tesseract-ocr, instead of tesseract')
    _check_package('ocrmypdf','https://github.com/ocrmypdf/OCRmyPDF')
    _check_package('soffice','https://www.libreoffice.org/download/download-libreoffice','Notice: use apt install libreoffice, instead of soffice')
    # check that chinese package is installed
    import os
    l = None
    dirs = ['/usr/share/tesseract-ocr/5/tessdata','/usr/share/tesseract-ocr/4.00/tessdata']
    for directory in dirs:
        try:
            l = os.listdir(directory)
        except FileNotFoundError:
            continue
        else:
            break
    if l is None:
        raise RuntimeError('cannot find tesseract trained data')
    if not 'chi_sim.traineddata' in l:
        raise RuntimeError(f'Tesseract Chinese Simplified language not downloaded. Go to https://github.com/tesseract-ocr/tessdata to download chi_sim.traineddata and place it in the directory {directory}. Alternatively, check for the `package` folder and place in that directory.')
    print('Check dependencies: chinese trained data installed')