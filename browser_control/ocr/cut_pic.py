# -*- coding: utf-8 -*-
import cv2


def split_image(path, row_num, col_num):
    img = cv2.imread(path)
    size = img.shape[0:2]
    w = size[1]
    h = size[0]
    # 每行的高度和每列的宽度
    row_height = h // row_num
    col_width = w // row_num
    for i in range(row_num):
        for j in range(col_num):
            # 保存切割好的图片的路径，记得要填上后缀，以及名字要处理一下
            save_path = path.split('.')[0] + '_' + str((i + 1) * (j + 1)) + '.jpg'
            # print(save_path)
            row_start = j * col_width
            row_end = (j + 1) * col_width
            col_start = i * row_height
            col_end = (i + 1) * row_height
            # print(row_start, row_end, col_start, col_end)
            child_img = img[col_start:col_end, row_start:row_end]
            cv2.imwrite(save_path, child_img)


if __name__ == '__main__':
    src_path = 'code.png'
    row = 1
    col = 2
    split_image(src_path, row, col, src_path.split('.')[0])
