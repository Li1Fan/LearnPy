import ddddocr

# im = Image.open(r'code.png')
# text = pytesseract.image_to_string(im)
# print(text)

# import ddddocr
ocr = ddddocr.DdddOcr(old=True, show_ad=False)
with open(r"D:\PycharmProjects\LearnPy\10-浏览器\browser_control\ocr\code.png", 'rb') as f:
    image = f.read()
res = ocr.classification(image)
print(res)
