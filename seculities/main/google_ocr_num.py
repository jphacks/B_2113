import requests
import base64
import json
import re
import cv2
import argparse
import numpy as np
import os
from .correct_eng import minor_adjustmenteng
from .resizing import only_resize

def number_array(image):
        name = "yuuka"
        UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + '/jpg_uploads/'

        image = f"{UPLOAD_DIR}\{image}"

        #画像の読み込み
        imgcv = cv2.imread(image)

        #画像のサイズを調整する
        imgcv = only_resize(imgcv)

        cv2.imwrite(f"1_{name}_gray.jpg",imgcv)
        adjustmenteng = minor_adjustmenteng(imgcv)

        GOOGLE_CLOUD_VISION_API_URL = 'https://vision.googleapis.com/v1/images:annotate?key='
        API_KEY = ''

        
        # APIを呼び、認識結果をjson型で返す
        def request_cloud_vison_api(image_base64):
            api_url = GOOGLE_CLOUD_VISION_API_URL + API_KEY
            req_body = json.dumps({
                'requests': [{
                    'image': {
                        # jsonに変換するためにstring型に変換する
                        'content': image_base64.decode('utf-8')
                    },
                    'features': [{
                        # ここを変更することで分析内容を変更できる
                        'type': 'TEXT_DETECTION',
                        'maxResults': 10,
                    }]
                }]
            })
            res = requests.post(api_url, data=req_body)
            return res.json()

        # 画像読み込み
        def img_to_base64(filepath):
            with open(filepath, 'rb') as img:
                img_byte = img.read()
            return base64.b64encode(img_byte)

        # 文字認識させたい画像を設定
        img_base64 = img_to_base64(f"1_{name}_gray.jpg")
        result = request_cloud_vison_api(img_base64)
        # 認識した文字を出力
        text_r = result["responses"][0]["textAnnotations"][0]["description"]


        # 一文字ずつ文字を抽出する
        by_character = list()
        for i in text_r:
            m = ''.join(i)
            by_character.append(m)

        # 配列に入っている全ての文字列を繋げる
        m = ''.join(by_character)
        new_num = list()
        new_num.append(m)

        sp = list()
        # '\n'で配列を区切る
        for j in new_num:
            sp = j.split('\n')


        # 配列の中身を数字のみにする
        only_number = list()
        for j in sp:
            #　空白を削除する
            if(j==''):
                continue
            elif(j[0]=='Д' or j[0] == 'Δ' or j[0] == 'A'):
                m =  re.findall(r'\d+',j)
                if(m):
                    only_number.append(int(''.join(m)))
            else:
                m =  re.findall(r'\d+',j)
                if(m):
                    only_number.append(int(''.join(m)))

        flag = 1
        subtraction = adjustmenteng.count("-")
        if(abs(len(adjustmenteng)-len(only_number)-subtraction)>4):
            flag = 0
        co = 0
        mark_index = list()
        if(flag):
            for k in adjustmenteng:
                if(k=="-"):
                    mark_index.append(co)
                    co+= 1
                else:
                    co+=1

            for k in mark_index:
                only_number.insert(k,"-")


        return only_number
