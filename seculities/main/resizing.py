import re
import cv2
import argparse
import numpy as np




def only_resize(imgcv):
    # 画像から数字だけを取得するために初期画像を分割する
    name = "yuuka"
    h, w, ch = imgcv.shape
    # 縦横幅の初期値
    h_start = 350
    h_end = h-125
    w_start = round(w/2)
    w_end = w-92
    # 分割する
    imgcv = imgcv[h_start:h_end, w_start:w_end, :ch]

    #現在の縦横幅
    height = h_end - h_start
    width = w_end - w_start
    # n倍
    n = 3
    width = round(width *n)
    height = round(height *n)
    imgcv = cv2.resize(imgcv,(width,height))
    return imgcv
