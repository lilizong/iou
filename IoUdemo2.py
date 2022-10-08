# -*- coding: utf-8 -*-
"""
Created on Sat Oct  8 13:31:52 2022
适用于：输入四个值都是坐标（传统可ne能为坐标、长度，需要转换）
框参数值：左上角坐标、右下角坐标
@author: lilizong
"""

import cv2
import random


def iou(gt_box, b_box):
    '''
    计算iou
    gt_box:ground true，实际框位置，使用左上、右下坐标表示
    b_box:bounding box，预测框位置，使用左上、右下坐标表示
    '''
    # 计算实际框大小
    widthA = abs(gt_box[2]-gt_box[0])
    heightA = abs(gt_box[3] - gt_box[1])
    # 计算预测框大小
    widthB = abs(b_box[2] - b_box[0])
    heightB = abs(b_box[3] - b_box[1])

    # 计算两个框最左x值、最右x值、两个框所占x长度
    min_x = min(gt_box[0], gt_box[2], b_box[0], b_box[2])
    max_x = max(gt_box[0], gt_box[2], b_box[0], b_box[2])
    x_length = max_x-min_x
    # 计算两个框最上y值、最下y值、两个框所占y长度
    min_y = min(gt_box[1], gt_box[3], b_box[1], b_box[3])
    max_y = max(gt_box[1], gt_box[3], b_box[1], b_box[3])
    y_length = max_y-min_y

    # 计算iou宽度
    # 具体为：width=两个框的宽度和-x方向的总长度
    # 如果两个框在x方向有交集，width>0；否则 ，width<0
    width = widthA + widthB - (x_length)
    # 两个框没有交集，iou宽度为负数，将其置零
    width = max(0, width)

    # 计算iou高度
    # 具体为：height=两个框的高度和-y方向的总长度
    # 如果两个框在y方向有交集，height>0；否则 ，height<0
    height = heightA + heightB - y_length
    height = max(0, height)

    interArea = width * height
    boxAArea = widthA * heightA
    boxBArea = widthB * heightB
    iou = interArea / (boxAArea + boxBArea - interArea)
    return iou


x0 = random.randint(0, 1152)
x1 = random.randint(0, 1152)
x2 = random.randint(0, 1152)
x3 = random.randint(0, 1152)
y0 = random.randint(0, 648)
y1 = random.randint(0, 648)
y2 = random.randint(0, 648)
y3 = random.randint(0, 648)

gtBox = [x0, y0, x1, y1]
bBox = [x2, y2, x3, y3]

print(iou(gtBox, bBox))

image = cv2.imread("image/x.jpg")

cv2.rectangle(image, tuple(gtBox[:2]),
              tuple(gtBox[2:]), (0, 255, 0), 2)
cv2.rectangle(image, tuple(bBox[:2]),
              tuple(bBox[2:]), (0, 0, 255), 2)
iouValue = iou(gtBox, bBox)
# cv2.putText(image, "IoU: {:.4f}".format(iou), (10, 30),cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)


# show the output image

# cv2.imshow("Image",image)
cv2.imshow("Image", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

# 说明：第7列到第9列，长度为3（第7列、第8列、第9列），通常计算：9-7=2
# 可以考虑在计算宽度时都加上1，得到正确值
# 例如上述：9-7+1=3
