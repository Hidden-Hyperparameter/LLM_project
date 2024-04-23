def CheckPackage(package:str):
    import subprocess
    try:
        # Run the apt command to check if ocrmypdf is installed
        subprocess.check_output(['apt', 'list', '--installed', package])
        print(f"Check dependencies: {package} installed")
    except subprocess.CalledProcessError:
        raise RuntimeError(f'You have not installed the {package} package yet, use `sudo apt install {package}` to finish the installation.')
def CheckDependencies():
    """ Make sure that the user has installed the `ocrmypdf` software packages using apt"""
    CheckPackage('ocrmypdf')
    CheckPackage('tesseract')
    CheckPackage('soffice')
    # check that chinese package is installed
    directory = '/usr/share/tesseract-ocr/5/tessdata'
    import os
    if not 'chi_sim.traineddata' in os.listdir(directory):
        raise RuntimeError('Tesseract Chinese Simplified language not downloaded. Go to https://github.com/tesseract-ocr/tessdata to download chi_sim.traineddata and place it in the directory.')
    