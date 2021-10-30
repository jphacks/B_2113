import os
from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from .forms import UploadFileForm
from pathlib import Path
from pdf2image import convert_from_path
from .google_ocr_jap import japanese_array
from .google_ocr_num import number_array
from .creation_excel import cre_ex

#語句の辞書
dic_account = {'流動資産' : '短い期間で現金にすることが可能な資産','現金及び預金' : '企業が所有している現金や、銀行に預けている預金',
'受取手形及び売掛金' : '売上代金の未回収分' ,'有価証券' : '財産的価値のある権利を表彰する証券','棚卸資産' : '企業が販売する目的で一時的に保有している商品・製品・原材料・仕掛品の総称',
'貸倒引当金' : '貸倒損失によるリスクに備え、損失になるかもしれない金額を予想して、あらかじめ計上しておく引当金', '流動資産合計' : '流動資産の合計','固定資産' : '会社が長期間にわたり保有するものや１年を超えて現金化・費用かされる資産',
'有形固定資産' : '実体を持つ固定資産' , '無形固定資産':'実体を持たない固定資産','投資その他の資産':'固定資産のひとつで、有形固定資産、無形固定資産に入らない資産',
'投資有価証券':'満期保有目的の有価証券など','投資その他の資産合計':'固定資産の中で、有形固定資産、無形固定資産に入らない資産','固定資産合計':'固定資産の合計','資産合計':'会社が運用している財産の総額すなわち資産の合計',
'負債の部':'株主・会社以外の外部からの調達資金','流動負債':'原則として１年以内に返済しなくてはならない債務','支払手形及び買掛金':'仕入先との取引に基づいた手形上の債務と仕入先との取引によって発生した営業上の未払金',
'引当金':'将来の支出に備えてあらかじめ準備しておく見積金額','未払法人税等':'納付すべき法人税、住民税および事業税の未払い額','流動負債合計':'流動負債の合計','固定負債':'１年以内に支払い義務が発生しない負債',
'退職給付に係る負債':'連結財務諸表上、退職給付から年金資産の額を控除した貸方残高（積立状況を示す額）を負債として計上したもの','固定負債合計':'固定負債の合計','負債合計':'流動負債と固定負債の合計',
'純資産の部':'資産から負債を差し引いた金額','株主資本':'株主が出資した資本と資本を使って生じた利益のこと','資本金':'事業を円滑に進めるために、株主が会社に出資した金額のこと','資本剩余金':'設立後新たに株式を発行した時など資本取引によって発生する余剰金',
'利益剩余金':'会社の活動によって得た利益のうち、社内に留保している額','自己株式':'株式会社が発行する株式のうち、自社で取得した上で保有している株式のこと','株主資本合計':'株主資本の合計',
'その他の包括利益累計額':'これまでに公表された会計基準等で使用されている純資産の部の「評価・換算差額等」を読み替えたもの','その他有価証券評価差額金':'その他有価証券を毎期末に時価評価した場合の、相手勘定を表す勘定科目',
'為替換算調整勘定':'連結財務諸表を作成する手続で発生する換算差額を調整する勘定科目','その他の包括利益累計額合計':'その他の包括利益累計額の合計','非支配株主持分':'連結子会社の資本のうち連結親会社の持分に属しない部分',
'純資産合計':'純資産の合計','負債純資産合計':'負債と純資産の合計','その他1':'','その他2':'','その他3':'','その他4':'','その他5':'',
}

# Create your views here.
def top(request):
    return render(request,'top.html')


UPLOAD_DIR = os.path.dirname(os.path.abspath(__file__)) + '/uploads/' # アップロードしたファイルを保存するディレクトリ
UPLOADS_DIR = os.path.dirname(os.path.abspath(__file__)) + '/jpg_uploads/'
# アップロードされたファイルのハンドル
def handle_uploaded_file(f):
    path = os.path.join(UPLOAD_DIR, f.name)
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    # PDFファイルのパス
    pdf_path = Path(f"{UPLOAD_DIR}\{f.name}")
    #outputのファイルパス
    img_path=Path(f"{UPLOADS_DIR}")
    #この1文で変換されたjpegファイルが、imageホルダー内に作られます。
    convert_from_path(pdf_path, output_folder=img_path,fmt='jpeg',output_file=pdf_path.stem)



# ファイルアップロード
def upload(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        pdf_name = request.FILES['yuuka']
        handle_uploaded_file(request.FILES['yuuka'])
    return render(request, 'upload.html', {'form': form,'pdf_name':pdf_name})
# ファイルアップロード完了
def upload_complete(request):
    jap_ar,num_ar = japanese_array()
    asset = list()
    liability = list()
    net_asset = list()
    flag = 0
    asset_num = list()
    liability_num = list()
    net_asset_num = list()
    co = 0



    for i in jap_ar:
        if(i=='資産の部'):
            flag = 1
        elif(i=='負債の部'):
            flag = 2
        elif(i=='純資産の部'):
            flag = 3
        elif(flag ==1):
            asset.append(i)
        elif(flag ==2):
            liability.append(i)
        elif(flag==3):
            net_asset.append(i)


    all = list()

    for i in asset:
        all.append(i)

    for j in liability:
        all.append(j)

    for k in net_asset:
        all.append(k)

    asset_num = list()
    liability_num = list()
    net_asset_num = list()

    num_before = list()
    num_current = list()
    for j in num_ar:
        if(co%2==0):
            co += 1
            num_before.append(j)
        else:
            co += 1
            num_current.append(j)

    co = 0
    ad = 0
    #判定方法は辞書型に変えられそう
    for k in all:
        if(k=='資産の部'):
            continue
        elif(k=='負債の部'):
            continue
        elif(k=='純資産の部'):
            continue
        elif('流動資産' == k):
            ad += 1
            asset_num.append(' ')
            continue
        elif('固定資産' == k):
            ad += 1
            asset_num.append(' ')
            continue
        elif('投資その他の資産' ==k):
            ad += 1
            asset_num.append(' ')
            continue
        elif('流動負債' == k):
            ad += 1
            liability_num.append(' ')
            continue
        elif('固定負債' == k):
            ad += 1
            liability_num.append(' ')
            continue
        elif('株主資本' == k):
            ad += 1
            net_asset_num.append(' ')
            continue
        elif('その他の包括利益累計額' == k):
            ad += 1
            net_asset_num.append(' ')
            continue
        elif(ad<len(asset)):
            ad += 1
            asset_num.append(num_current[co])
            co += 1
            continue
        elif(len(asset)<=ad and ad <len(liability)+len(asset)):
            liability_num.append(num_current[co])
            ad += 1
            co += 1
            continue
        elif(len(liability)+len(asset)<=ad):
            net_asset_num.append(num_current[co])
            ad += 1
            co += 1
            continue
    co = 0
    ad = 0
    asset_num_before = list()
    liability_num_before = list()
    net_asset_num_before = list()
    for k in all:
        if(k=='資産の部'):
            continue
        elif(k=='負債の部'):
            continue
        elif(k=='純資産の部'):
            continue
        elif('流動資産' == k):
            ad += 1
            asset_num_before.append(' ')
            continue
        elif('固定資産' == k):
            ad += 1
            asset_num_before.append(' ')
            continue
        elif('投資その他の資産' ==k):
            ad += 1
            asset_num_before.append(' ')
            continue
        elif('流動負債' == k):
            ad += 1
            liability_num_before.append(' ')
            continue
        elif('固定負債' == k):
            ad += 1
            liability_num_before.append(' ')
            continue
        elif('株主資本' == k):
            ad += 1
            net_asset_num_before.append(' ')
            continue
        elif('その他の包括利益累計額' == k):
            ad += 1
            net_asset_num_before.append(' ')
            continue
        elif(ad<len(asset)):
            ad += 1
            asset_num_before.append(num_before[co])
            co += 1
            continue
        elif(len(asset)<=ad and ad <len(liability)+len(asset)):
            liability_num_before.append(num_before[co])
            ad += 1
            co += 1
            continue
        elif(len(liability)+len(asset)<=ad):
            net_asset_num_before.append(num_before[co])
            ad += 1
            co += 1
            continue

    current = list()

    ex_temp0 = list()
    ex_temp1 = list()
    for i in asset_num:
        ex_temp0.append(i)
    for j in liability_num:
        ex_temp0.append(j)
    for k in net_asset_num:
        ex_temp0.append(k)
    for i in asset_num_before:
        ex_temp1.append(i)
    for j in liability_num_before:
        ex_temp1.append(j)
    for k in net_asset_num_before:
        ex_temp1.append(k)

    all_new = list()

    for i in asset:
        all_new.append(i)

    for j in liability:
        all_new.append(j)

    for k in net_asset:
        all_new.append(k)


    cre_ex(all_new,ex_temp0,ex_temp1)


    dic = {key:val for key,val in zip(asset,asset_num)}
    dic_lia = {key:val for key,val in zip(liability,liability_num)}
    dic_net = {key:val for key,val in zip(net_asset,net_asset_num)}

    #語句の説明
    phrase_description = list()
    for k in all:
        val =dic_account[k]
        phrase_description.append(val)

    dic_phrase_description = {key:val for key,val in zip(all,phrase_description)}
    co = 0

    #流動比率
    # 流動比率 ＝ 流動資産／流動負債 × 100
    #もし流動資産合計という語句があれば
    flow_rate = dic['流動資産合計']/dic_lia['流動負債合計']*100
    flow_rate = round(flow_rate)


    #当座比率
    # 当座比率 ＝ 当座資産／流動負債 × 100
    flag = 0
    current_term_asset = 0
    for i in asset:
        if(flag):
            break
        elif(i=='流動資産'):
            continue
        elif(i=='棚卸資産' ):
            flag = 1
        elif(i=='その他1'):
            flag =1
        else:
            current_term_asset+=dic[i]

    flag = 0
    current_liabilities = 0
    for j in liability:
        if(flag):
            break
        elif(j=='流動負債'):
            continue
        elif(j=='その他3'):
            flag = 1
        else:
            current_liabilities+=dic_lia[j]

    current_rate = current_term_asset/current_liabilities*100
    current_rate = round(current_rate)


    #長期的な安全性を示す固定比率
    #固定比率 ＝ 固定資産／自己資本 × 100
    fixed_rate = dic['固定資産合計']/dic_net['純資産合計']*100
    fixed_rate = round(fixed_rate)


    #自己資本比率
    #自己資本比率 ＝ 純資産／総資本 × 100
    capital_adequacy_ratio = dic_net['純資産合計']/dic['資産合計']*100
    capital_adequacy_ratio = round(capital_adequacy_ratio)


    return render( request, 'upload_complete.html',context={
    'liability' : liability,
    'net_asset' : net_asset,
    'liability_num_current' : liability_num,
    'net_asset_num_current' : net_asset_num,
    'dic_current' : dic,
    'dic_current_lia' : dic_lia,
    'dic_current_net' : dic_net,
    'dic_phrase_description' : dic_phrase_description,
    'flow_rate' : flow_rate,
    'current_rate' : current_rate,
    'fixed_rate' : fixed_rate,
    'capital_adequacy_ratio' : capital_adequacy_ratio,

    })
