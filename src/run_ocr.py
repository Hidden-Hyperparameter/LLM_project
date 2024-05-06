from utils.ocr import OCR
from utils.dependency import CheckDependencies
CheckDependencies()
# texts = OCR('./tests/data/test.pdf',remove_mid=False)
texts1 = OCR('./tests/data/lec.pdf',quiet=False)
open('./tests/data/out.txt','w').write(texts1)