common_used_numerals_tmp = {'零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9,
                            '十': 10, '百': 100, '千': 1000, '万': 10000, '亿': 100000000}
common_used_numerals = {}
for key in common_used_numerals_tmp:
    common_used_numerals[key] = common_used_numerals_tmp[key]
def chinese2digits(uchars_chinese):
    total = 0
    r = 1  # 表示单位：个十百千...
    for i in range(len(uchars_chinese) - 1, -1, -1):
        val = common_used_numerals.get(uchars_chinese[i])
        if val >= 10 and i == 0:  # 应对 十三 十四 十*之类
            if val > r:
                r = val
                total = total + val
            else:
                r = r * val
                # total =total + r * x
        elif val >= 10:
            if val > r:
                r = val
            else:
                r = r * val
        else:
            total = total + r * val
    return total
num_str_start_symbol = ['一', '二', '两', '三', '四', '五', '六', '七', '八', '九',
                        '十']
more_num_str_symbol = ['零', '一', '二', '两', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万', '亿']

def trans(oriStr):
    lenStr = len(oriStr);
    aProStr = ''
    if lenStr == 0:
        return aProStr;

    hasNumStart = False;
    numberStr = ''
    for idx in range(lenStr):
        if oriStr[idx] in num_str_start_symbol:
            if not hasNumStart:
                hasNumStart = True;

            numberStr += oriStr[idx]
        else:
            if hasNumStart:
                if oriStr[idx] in more_num_str_symbol:
                    numberStr += oriStr[idx]
                    continue
                else:
                    numResult = str(chinese2digits(numberStr))
                    numberStr = ''
                    hasNumStart = False;
                    aProStr += numResult

            aProStr += oriStr[idx]
            pass

    if len(numberStr) > 0:
        resultNum = chinese2digits(numberStr)
        aProStr += str(resultNum)

    return aProStr

# diction={'-HEIGHT': '', '-WEIGHT': [{'NUM': '100', 'UNI': '斤', 'TIME': '04:08:46 PM'}], '-EAT': [{'B-EAT': '苹果', 'NUM': '五', 'UNI': '个', 'TIME': '04:08:46 PM'}], '-BAD': [{'B-BAD': '抽了', 'NUM': '', 'UNI': '根', 'TIME': '04:08:46 PM'}], '-EMO': [{'mood': '', 'TIME': '04:08:46 PM'}], '-ORI': [{'text': '体重100斤，吃了五个苹果，抽了三根烟', 'TIME': '04:08:46 PM'}]}
def to_dig(diction):
    for i in diction:
        if diction[i]!=''or diction[i]!=[] or  diction[i]!= ['']:
            for big in diction[i]:
                for son in big:
                    if son == 'NUM' :
                        big[son]=trans(big[son])
    # print(diction)
    return diction

def final_deel(di):
    if di['-EMO'][0]['mood'] == '':
        del di['-EMO']
    for i in list(di):
        if di[i] == '' or di[i] == [] or di[i] == ['']:
            del di[i]

    for i in di:
        if i == '-WEIGHT' or i == '-HEIGHT':
            di[i] = di[i][0]
    return di

def dataset(name, collection):
    result = collection.find({name: {'$exists': 'true'}})
    # print(type(result))
    aa = list(result)
    # print(aa[0][name])
    return aa[0][name]


def hw_to_nor(aa):
    import re

    if aa['-HEIGHT'] != '':
        number = re.findall(r"\d+\.?\d*", aa['-HEIGHT'])
        number_start = aa['-HEIGHT'].find(''.join(str(s) for s in number))
        uni = aa['-HEIGHT'][number_start + len(''.join(str(s) for s in number)):]
        aa['-HEIGHT'] = [{"NUM": ''.join(str(s) for s in number), "UNI": uni}]

    if aa['-WEIGHT'] != '':
        number = re.findall(r"\d+\.?\d*", aa['-WEIGHT'])
        number_start = aa['-WEIGHT'].find(''.join(str(s) for s in number))
        uni = aa['-WEIGHT'][number_start + len(''.join(str(s) for s in number)):]
        aa['-WEIGHT'] = [{"NUM": ''.join(str(s) for s in number), "UNI": uni}]

    print(aa)
    return aa
import paddlehub as hub
senta = hub.Module(name="senta_bilstm")
from random import choice
from datetime import datetime

dt = datetime.now()  # 创建一个datetime类对象
from main import evaluate_line,evaluate_line2
import tensorflow as tf
import keras
# from tensorflow.python.platform import flags
import json
from flask import Flask, request, render_template, Markup

app = Flask(__name__)
app.debug = True

import pymongo
from datetime import datetime
from my_ut import suo, text_text, deal_final,onlyone,emoori2,timee,suo2

dt = datetime.now()  # 创建一个datetime类对象

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.test
collection = db.students
collection_check = db.check
FLAGS = tf.app.flags.FLAGS
look_up = ['身高', '体重', '吃的', '抽烟喝酒', '情绪', ]


from mainto_diction import cut_max, get_char_list, dictionary




@app.route('/input_id')
def input_id():
    return render_template('input_id.html')


@app.route('/submit', methods=['POST'])
def submit():
    iddd = request.form.get("haha")
    try:
        all_dic = dataset(name=iddd, collection=collection_check)
    except IndexError:
        return '无效的输入'
    alll = ''
    for i in all_dic:
        alll = alll + '<br/>'
        for l in i:
            if l == '-HEIGHT' or l == '-WEIGHT':
                try:
                    alll = alll + l + str(i[l][0]) + '<br/>'
                except IndexError:
                    print('error')
            else:
                alll = alll + l + str(i[l]) + '<br/>'
    return render_template('submit.html', name=iddd,
                           text=alll.replace('-HEIGHT', '身高： ').replace('[]', ' ').replace('-WEIGHT', '体重： ').replace(
                               'B-BAD', '坏习惯').replace('B-EAT', '吃了').replace('-EAT', '吃的情况： ').replace('-BAD',
                                                                                                        '坏习惯： ').replace(
                               '-EMO', '情绪： ').replace('-ORI', '原句： ').replace('-TIME', '时间： ').replace('NUM',
                                                                                                        '值').replace(
                               'UNI', '单位'))

@app.route('/first_ask', methods=['GET', 'POST'])
def first_ask():
    global idd
    global all_text  # http://0.0.0.0:5000/first_ask?idtext=WUHAO&input_text=
    global saven     # 暂存all_text
    global ori
    global all_dict
    global final_dii

    if request.method == 'GET':
        id1 = request.args.get("idtext")
        if id1 != '':
            idd = id1

        input_text = request.args.get("input_text")

        if '怎么用' in input_text:
            how_to_use='您可以说出发生在您身上任意时间和健康相关的状况 ' \
                       '<br/>***' \
                       '<br/>例如<br/>' \
                       '<br/>我3年前，身高90公分。' \
                       '<br/>我的体重很重啊180斤' \
                       '<br/>我昨天吃了三个西瓜，五个苹果' \
                       '<br/>我不抽烟，昨天倒是喝了三瓶酒' \
                       '<br/>昨天心情焦虑，今天的心情是迷茫的<br/>'\
                       '<br/>我3年前，身高90公分。我的体重很重啊180斤,我昨天吃了三个西瓜，五个苹果,我不抽烟，昨天倒是喝了三瓶酒,昨天心情焦虑，今天的心情是迷茫的'
            return how_to_use

        if '删除' in  input_text :
            hea_ut = {'身高': '-HEIGHT', '体重': '-WEIGHT', '饮食': '-EAT', '坏习惯': '-BAD', '心情': '-EMO'}
            dele = input_text.strip('删除').strip('。')
            try:
                final_dii[hea_ut[dele]]=[]
                dele_text='删除'+dele+'成功'
                return dele_text
            except KeyError:
                return '删除失败'

        if input_text == '查看数据' or input_text == '查看数据。':
            if saven!=[]:
                print('saven!=0')
                all_dict = evaluate_line2(if_ask=True, another_input=saven, save=FLAGS.ckpt_path)
                temporary_dic={'-HEIGHT': [], '-WEIGHT': [], '-EAT': [], '-BAD': [], '-EMO': []}
                try:
                    for diction in all_dict:
                        for i in diction:
                            temporary_dic[i] = temporary_dic[i] + diction[i]
                except TypeError:
                    print('unknown', diction[i], final_dii[i])

                temporary_dic=deal_final(onlyone(temporary_dic))
                print('wanttttttttttttttttttttto',temporary_dic)
                for i in final_dii:
                    if temporary_dic[i]==''or temporary_dic[i]==['']:
                        temporary_dic[i]=[]
                    if final_dii[i]=='':
                        final_dii[i]=[]
                    final_dii[i]=final_dii[i]+temporary_dic[i]
                    print('tooooooooooooooknow',final_dii)
                # final_dii=deal_final(onlyone(final_dii))
            check = text_text(final_dii=final_dii,last=False)
            saven=[]
            return check

        if input_text == '没有了' or input_text == '没有了。':
            if saven!=[]:
                all_dict=evaluate_line2(if_ask=True, another_input=saven, save=FLAGS.ckpt_path)
                try:
                    for diction in all_dict:
                        for i in diction:
                            final_dii[i] = final_dii[i] + diction[i]
                except TypeError:
                    print('unknown',diction[i],final_dii[i])

                final_dii=onlyone(final_dii)
                final_dii = deal_final(final_dii)
                final_dii['-ORI'] = ori
                  #############################
            check = text_text(final_dii=final_dii,last=True)  # 询问是否确定，（删除空值），，上面也要记得写噢（suo()里面要考虑是否改动）
            final_dii=timee(final_dii=emoori2(final_dii,senta=senta),time='%I:%M:%S %p')            #time
            to_dig(final_dii)
            return check

        if input_text == '确认' or input_text == '确认。':
            print('buggggggggggggg',final_dii)
            # print('buggggggggggggg1',final_deel(di=suo2(dii=final_dii, input_id=idd, collection=collection,datee='%y-%m-%d')))
            return '结束了'+'***'+str({dt.strftime('%y-%m-%d'):final_deel(di=suo2(dii=final_dii, input_id=idd, collection=collection,datee='%y-%m-%d'))}).replace("'", '"')
        if input_text=='有误'or input_text=='有误。':
            all_text = []
            saven=[]
            all_dict = []
            ori=[]
            ran1 =choice(['记录什么内容', '说出你最近的一切', '最近如何'])
            final_dii = {'-HEIGHT': [], '-WEIGHT': [], '-EAT': [], '-BAD': [], '-EMO': []}
            return '那咱重新来'
        if input_text == '' :
            all_text = []
            saven=[]
            all_dict = []
            ori=[]
            ran1 =choice(['记录什么内容', '说出你最近的一切', '最近如何'])
            final_dii = {'-HEIGHT': [], '-WEIGHT': [], '-EAT': [], '-BAD': [], '-EMO': []}
            return ran1

        if input_text != '' :  # 第二次询问
            ori = ori + [input_text]
            all_text.append(input_text)
            saven.append(input_text)
            ran2 = choice(['还有什么要记录吗', '继续说你想记录的吧', '还有啥呢'])
            return ran2

if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000')


