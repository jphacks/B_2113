import requests
import base64
import json
import re
import queue
from .find_bs import bs
import os
from .google_ocr_num import number_array
def japanese_array():

        UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + '/jpg_uploads/'  # アップロードしたファイルを保存するディレクトリ

        answer,images = bs()


        image = f"{UPLOAD_DIR}\{images}"

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
        img_base64 = img_to_base64(f'{image}')
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

        # 配列の中身を勘定のみにする
        only_number = list()
        for j in sp:
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
        only_jap = list()
        for j in before_list:
            if(j==''):
                continue
            else:
                only_jap.append(j)
        co = 0
        last_only_jap = list()
        for i in only_jap:
            if(i=='その他'):
                co += 1
                i  = i+ str(co)
                last_only_jap.append(i)
            else:
                last_only_jap.append(i)




        for i in range(len(last_only_jap)):
            for j in range(len(last_only_jap[i])):
                if(last_only_jap[i][j]=="產"):
                    last_only_jap[i] = last_only_jap[i][:j]+"産"+last_only_jap[i][j+1:]

        only_num = number_array(images)

        return last_only_jap,only_num
