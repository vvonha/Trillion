import cv2
import pytesseract
from pytesseract import *
import numpy as np

img = cv2.imread('./test.png')

# 회색 변환(channel 수 감소)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 이진수 변환(흑 / 백)
img_binary = cv2.threshold(img_gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# 모폴로지 연산(Opening)
kernel = np.ones((5, 5), np.uint8)
img_open = cv2.morphologyEx(img_binary, cv2.MORPH_OPEN, kernel)

# tesseract 설정
custom_config = '--oem 3' # LSTM 버전
text = pytesseract.image_to_string(img_binary, 'eng+Hangul') # 한글은 kor이 아닌 Hangul

with open('file.txt', mode='w') as f:
    f.write(text)
