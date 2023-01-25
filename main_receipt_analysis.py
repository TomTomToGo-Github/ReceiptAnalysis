"""
Receipt Analysis.

This code is the first step towards a full grown app
for android with which one can make pictures of shopping receipts.
The images will be analysed and the shopping items categorized into
important and not-important items.


Remark: only pip isnstall pytesseract is not enough!
#1. Install tesseract using windows installer available at: https://github.com/UB-Mannheim/tesseract/wiki

#2. Note the tesseract path from the installation.Default installation path at the time the time of this edit was: C:\Users\USER\AppData\Local\Tesseract-OCR. It may change so please check the installation path.

#3. pip install pytesseract

#4. Set the tesseract path in the script before calling image_to_string:

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\USER\AppData\Local\Tesseract-OCR\tesseract.exe'

REMARK2: cv2 -> pip install opencv-python
"""


import os
import pytesseract as pt


# See how to deal with bad quality and mirroring

# Get the local path where receipts .png can be found
path_receipt_img = r"{}\\Receipts".format(os.getcwd())
pt.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\tesseract'

receipts_list = [r"Bipa_mirrored_bad_quality.jpg", r"Cewe_mirrored_bad_quality.jpg"]
for receipt_str in receipts_list:
    receipt_pathfile = os.path.join(path_receipt_img, receipt_str)
    print(pt.image_to_string(receipt_pathfile))

import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\USER\\AppData\\Local\\Tesseract-OCR\\tesseract.exe'
text = pytesseract.image_to_string(Image.open(receipt_pathfile), lang='eng',
                        config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

print(text)




import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Grayscale, Gaussian blur, Otsu's threshold
image = cv2.imread(receipt_pathfile)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (3,3), 0)
thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

# Morph open to remove noise and invert image
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
invert = 255 - opening

# Perform text extraction
data = pytesseract.image_to_string(Image.fromarray(invert), lang='eng', config='--psm 10')
print(data)

cv2.imshow('thresh', thresh)
cv2.imshow('opening', opening)
cv2.imshow('invert', invert)
cv2.waitKey()