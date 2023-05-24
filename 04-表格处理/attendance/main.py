import os

from cal_data2 import create_table
from util.cut_pic import split_image
from util.ocr_baiduApi import baiduApi_ocr


def rename_pic(dir):
    for root, dirs, files in os.walk(dir):
        if root == dir:
            for name in files:
                if name.endswith('.jpeg'):
                    print(name)
                    old_name = os.path.join(root, name)
                    new_name = os.path.join(root, name.split('.')[0] + '.jpg')
                    os.rename(old_name, new_name)


def get_ocr_data(dir):
    ocr_data = ''
    for root, dirs, files in os.walk(dir):
        if root == dir:
            for name in files:
                if name.endswith('.jpg'):
                    print(name)
                    data = baiduApi_ocr(os.path.join(root, name))
                    # print(data)
                    for i in data:
                        ocr_data += i['words']
                        ocr_data += '\n'
        return ocr_data


if __name__ == "__main__":
    pic_path = r'C:\Users\10262\Desktop\4月.jpg'
    cut_pic_path = r'C:\Users\10262\Desktop\contact\attend\cutPic\4'

    split_image(pic_path, 10, 1, cut_pic_path)
    rename_pic(cut_pic_path)
    data = get_ocr_data(cut_pic_path)
    print(data)
    with open('data.txt', 'w', encoding='utf-8') as f:
        f.write(data)
    create_table(data)