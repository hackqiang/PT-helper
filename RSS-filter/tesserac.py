'''
http://www.liaoxuefeng.com/wiki/001374738125095c955c1e6d8bb493182103fac9270762a000/00140767171357714f87a053a824ffd811d98a83b58ec13000
http://www.jianshu.com/p/4a7bba756192

apt-get install tesseract-ocr python-imaging
pip install pytesseract

'''

import pytesseract



from PIL import Image

image = Image.open('image.png')

vcode = pytesseract.image_to_string(image)

print vcode