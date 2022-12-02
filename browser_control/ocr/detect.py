import ddddocr
from PIL import Image
from pytesseract import pytesseract

# im = Image.open(r'code.png')
# text = pytesseract.image_to_string(im)
# print(text)

# import ddddocr
ocr = ddddocr.DdddOcr(old=True,show_ad=False)
with open(r"C:\Users\10262\Desktop\da.jpg", 'rb') as f:
    image = f.read()
res = ocr.classification(image)
print(res)