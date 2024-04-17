def CheckDependencies():
    """ Make sure that the user has installed the `ocrmypdf` software packages using apt"""
    import subprocess
    try:
        # Run the apt command to check if ocrmypdf is installed
        subprocess.check_output(['apt', 'list', '--installed', 'ocrmypdf'])
        print("Check dependencies: ocrmypdf installed")
    except subprocess.CalledProcessError:
        raise RuntimeError('You have not installed the ocrmypdf package yet, use `sudo apt install ocrmypdf` to finish the installation.')
    