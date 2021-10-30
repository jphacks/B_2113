# coding: utf_8
import os
import queue
import re
import cv2
import argparse
import numpy as np
from PIL import Image
import pyocr
import pyocr.builders

def bs():
    tools = pyocr.get_available_tools()
    tool = tools[0]
    UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + '/jpg_uploads/'  # アップロードしたファイルを保存するディレクトリ
    files = os.listdir(f"{UPLOAD_DIR}")
    t = 0
    answer =0
    img_name = ''


    for image in files:
        #画像の読み込み
        imgcv = cv2.imread(f"{UPLOAD_DIR}\{image}")
        # get grayscale image

        tools = pyocr.get_available_tools()
        tool = tools[0]
        #文字の認識方法
        builder = pyocr.builders.TextBuilder(tesseract_layout=6)
        #数字のみを認識する
        #builder.tesseract_configs.append("digits")
        # 文字を認識する
        check = tool.image_to_string(Image.fromarray(imgcv), lang="jpn",builder=builder)

        # 空白以外を認識する
        result = re.findall(r'\S+', check)
        t+=1
        # 配列の中身を勘定のみにする
        only_number = list()
        for j in result:
            #　空白を削除する
            if(j==''):
                continue
            else:
                # 日本語だけ抽出
                m =  re.findall(r'[一-龥 ぁ-ん ァ-ン]',j)
                if(m):
                    only_number.append(''.join(m))

        #　配列の要素の空白を連結させる
        before_list = list()
        for j in only_number:
            if(j):
                m = re.findall(r'\S+', j)
                m = ''.join(m)
                before_list.append(m)
        # 配列の''を省く
        last_list = list()
        for j in before_list:
            if(j==''):
                continue
            else:
                last_list.append(j)
        for i in range(1):
            if("四半期連結財務諸表"==last_list[i]):
                answer = t
                img_name = image
            elif("要約四半期連結財務諸表"==last_list[i]):
                answer = t
                img_name = image
        print(t)
        #ファイルの削除
        #os.remove('sample.txt')

    return answer,img_name
