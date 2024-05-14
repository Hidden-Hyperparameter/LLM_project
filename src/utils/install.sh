apt update
source activate base
echo "Installing Packages"
apt install tesseract-ocr
apt install ocrmypdf
apt install libreoffice
echo "Package Installation complete"

echo "Installing Data"
cp package/chi_sim.traineddata /usr/share/tesseract-ocr/4.00/tessdata
cp package/chi_sim.traineddata /usr/share/tesseract-ocr/5/tessdata
echo "Data Installation complete"

echo "Installing Python Packages"
source activate base
pip install PyPDF2
pip install PyMuPDF
pip install argparse
echo "Installing Python Packages Complete"

echo "Finished!"
