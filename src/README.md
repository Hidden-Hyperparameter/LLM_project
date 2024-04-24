## Setting Up the environment
First run:
```bash
apt update
```

### Tesseract
The package `libtiff5_4.1.0+git191117-2ubuntu0.20.04.12_amd64.deb` is used when installing tesseract. First run
```bash
apt install tesseract-ocr
```
**If fail**, check the error indicates that what packages are not found. For myself, the package `libjbig0` and `libwebp6` are required, so I put them in the `./package` dir. Then you can run
```bash
apt install libjbig0 libwebp6
cd package
dpkg -i libtiff5_4.1.0+git191117-2ubuntu0.20.04.12_amd64.deb
apt install tesseract-ocr --fix-missing
```

### OCRMyPDF

# NOTE: this haven't been fixed yet, there are issues!

## issues for OCRMyPDF
when running on large files (e.g. 100 pages), this will emits an error
```
ERROR - SubprocessOutputError: Ghostscript text extraction failed
/tmp/com.github.ocrmypdf.3k1am01w/origin.pdf
```
see the [issue page](https://github.com/ocrmypdf/OCRmyPDF/issues/750), but I haven't currently figured out how to solve this.

---
**below is the original instructuons**

First run:
```bash
apt install ocrmypdf
```

Similarly, their will be missing packages. You can solve using the following code.
```bash
apt install libimagequant0 liblcms2-2 libwebpdemux2
cd package
dpkg -i libtiff5_4.1.0+git191117-2ubuntu0.20.04.12_amd64.deb
dpkg -i python3-pil_7.0.0-4ubuntu0.9_amd64.deb
apt install ocrmypdf --fix-missing
```
You may also have to run
```bash
pip install --user --upgrade ocrmypdf
```

see [url](https://github.com/ocrmypdf/OCRmyPDF/issues/750) for more info.

### Soffice (This works well)
simply do
```bash
apt update
apt install libreoffice
```