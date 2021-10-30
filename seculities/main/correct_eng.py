# coding: utf_8
import queue
import re
import cv2
import argparse
import numpy as np
from PIL import Image
import pyocr
import pyocr.builders



def minor_adjustmenteng(imgcv):
    tools = pyocr.get_available_tools()
    tool = tools[0]
    #文字の認識方法
    builder = pyocr.builders.TextBuilder(tesseract_layout=6)
    #数字のみを認識する
    #builder.tesseract_configs.append("digits")
    # 文字を認識する
    check = tool.image_to_string(Image.fromarray(imgcv), lang="eng",builder=builder)

    # 空白以外を認識する
    result = re.findall(r'\S+', check)
    # 配列を宣言
    l = list()
    # ,を繋げるためのキュー
    connect_comma  = queue.Queue()

    # resultの配列を繋げる
    # 最後の文字が","や"."になっていれば前後を繋げる
    for i in result:
        #chr.isdigit()は少なくとも一つ以上数字が入っているとTrueを返す。
        # if(any(chr.isdigit() for chr in i)):
            if(i[len(i)-1]==',' or i[len(i)-1]=='.'):
                connect_comma.put(i)
            elif(connect_comma):
                # 新しくできる数字
                new_num = ''
                while not connect_comma.empty():
                    comma = connect_comma.get()
                    comma = comma[:len(comma)-1] + ','
                    new_num = new_num + comma
                new_num = new_num+ i
                l.append(new_num)
            else:
                l.appned(i)


    # 数字のみを取り出す
    only_number = list()
    for j in l:
        if(j[0]=='ム' or j[0] == 'A' or j[0] == '人'):
            m =  re.findall(r'\d+',j)
            if(m):
                only_number.append(-int(''.join(m)))
        elif(j[0]=='る'):
            j = '2' + j[1:]
            m =  re.findall(r'\d+',j)
            only_number.append(int(''.join(m)))
        elif(j[0]=='ー' or j[0] == '一' or j[0]=='_'):
            only_number.append('-')
        elif(j[0]==']'):
            only_number.append(1)
        else:
            m =  re.findall(r'\d+',j)
            if(m):
                only_number.append(int(''.join(m)))


    return  only_number
