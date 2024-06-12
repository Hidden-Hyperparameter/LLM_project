apt update
source activate base
echo "Installing Packages"
apt install -y tesseract-ocr
apt install -y ocrmypdf
apt install -y libreoffice
apt install -y ffmpeg
source activate
conda install poppler
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
pip install av
pip install gradio
pip install librosa
pip install pillow_heif
echo "Installing Python Packages Complete"

echo "Final check"
python utils/dependency.py
echo "Final check finished"

echo "All Finished!"

