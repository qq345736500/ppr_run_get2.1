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
num_str_start_symbol = ['一', '二', '两', '三', '四', '五', '六', '七', '八', '九','十']
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
# import sys
# import codecs
# sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
from main import evaluate_line3    #不能删！！！
import tensorflow as tf
FLAGS = tf.app.flags.FLAGS
from model import Model
from utils import load_config,get_logger,create_model
from data_utils import load_word2vec,input_from_line
import pickle
from mainto_diction import dictionary

config = load_config(FLAGS.config_file)
logger = get_logger(FLAGS.log_file)
tf_config = tf.ConfigProto()
tf_config.gpu_options.allow_growth = True
with open(FLAGS.map_file, "rb") as f:
    char_to_id, id_to_char, tag_to_id, id_to_tag = pickle.load(f)
# sess=tf.Session(config=tf_config)
sess=tf.InteractiveSession(config=tf_config)
model = create_model(session=sess, Model_class=Model,path=FLAGS.ckpt_path, load_vec=load_word2vec, config=config, id_to_char= id_to_char, logger=logger)
def evaluate2(line_lis,sess):
    all_dict = []
    print('buuuuuuuuuuuuuuuug1',line_lis)
    for i in line_lis:
        result = model.evaluate_line(sess, input_from_line(i, char_to_id), id_to_tag)
        mytext, label_list = result  ##三箱西瓜,苹果，身高180公分，体重90斤，酒一瓶不喝，心情很好
        dii = dictionary(label_list=label_list, mytext=mytext)
        all_dict.append(dii)
    print('debugggggggggggg1')
    return all_dict
####################################################################    tf
import paddlehub as hub
senta = hub.Module(name="senta_bilstm")
from random import choice
from datetime import datetime
dt = datetime.now()  # 创建一个datetime类对象
from main import evaluate_line2

from flask import Flask, request, render_template, Markup
app = Flask(__name__)
app.debug = True

app.config['JSON_AS_ASCII'] = False   #json output不会unicode
import pymongo
from my_ut import suo, text_text2, deal_final,onlyone,emoori2,timee,suo2

client = pymongo.MongoClient(host='localhost', port=27017)
db = client.test
collection = db.students
collection_check = db.check
look_up = ['身高', '体重', '吃的', '抽烟喝酒', '情绪', ]

from mainto_diction import add_datetime,sametime_combine,ios_time_nor

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
    # global all_text                                             # http://0.0.0.0:5000/first_ask?idtext=WUHAO&input_text=
    global saven     # 暂存all_text，每次eval 新的
    global ori
    global all_dict
    global final_dii
    global  final_lis
    global date_text

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
                for i in final_dii:
                    for j in final_dii[i]:
                        for k in j:
                            if k == hea_ut[dele]:
                                j[k] = []
                dele_text='删除'+dele+'成功，我们继续'
                return dele_text
            except KeyError:
                return '删除失败,请说删除（身高，体重，饮食，坏习惯，心情）'

        if input_text == '查看数据' or input_text == '查看数据。':
            if saven!={}:
                all_dict = evaluate2(line_lis=[i for i in saven],sess=sess)
                for num,i in enumerate(all_dict):
                    deal_final(i)
                    i['-ORI'] = [[j for j in saven][num]]
                # print('all_dict1', all_dict)
                for i in all_dict:                      #处理全部value为[]
                    for key in i:
                        if i[key]==''or i[key]==['']:
                            i[key]=[]
                for i in all_dict:
                    emoori2(i, senta=senta)
                # print('all_dict2', all_dict)
                # print('time_list',[saven[i] for i in saven])
                temporarydic=add_datetime(all_dict=all_dict,time_list=[saven[i] for i in saven])
                temporarydic=sametime_combine(temporarydic)     #合并时间日期后的saven
                final_lis=final_lis+[temporarydic]
                final_dii={}
                for i in final_lis:
                    for tim in i  : #tim是时间
                        if tim in final_dii:
                            final_dii[tim]=final_dii[tim]+i[tim]
                        else:
                            final_dii[tim]=i[tim]
                final_dii=sametime_combine(final_dii)
                print('why???????????????',final_dii)
                saven = {}
            # return final_dii
            resu=str(text_text2(final_dii)) + '<br/>'+'<br/>''您可以说：“删除XX”来修改记录；或继续聊点别的来记录其它。'
            return resu
            # return str(text_text2(final_dii))

        if input_text == '没有了' or input_text == '没有了。':
            if saven != {}:
                all_dict = evaluate2(line_lis=[i for i in saven],sess=sess)
                for num, i in enumerate(all_dict):
                    deal_final(i)
                    i['-ORI'] = [[j for j in saven][num]]
                # print('all_dict1', all_dict)
                for i in all_dict:  # 处理全部value为[]
                    for key in i:
                        if i[key] == '' or i[key] == ['']:
                            i[key] = []
                for i in all_dict:
                    emoori2(i, senta=senta)
                # print('all_dict2', all_dict)
                # print('time_list',[saven[i] for i in saven])
                temporarydic = add_datetime(all_dict=all_dict, time_list=[saven[i] for i in saven])
                temporarydic = sametime_combine(temporarydic)  # 合并时间日期后的saven
                final_lis = final_lis + [temporarydic]
                final_dii = {}
                for i in final_lis:
                    for tim in i:  # tim是时间
                        if tim in final_dii:
                            final_dii[tim] = final_dii[tim] + i[tim]
                        else:
                            final_dii[tim] = i[tim]
                final_dii = sametime_combine(final_dii)

                saven = {}
            resu2=str(text_text2(final_dii))+'***'+'确认请选择“确认”,需要修改请选择“有误”'
            return resu2

        if input_text == '确认' or input_text == '确认。':
            resu3='结束了'+'***'+str(final_dii).replace("'", '"')
            return resu3
        if input_text=='有误'or input_text=='有误。':

            saven={}
            all_dict = []
            ori=[]
            date_text = {}
            ran1 =choice(['记录什么内容', '说出你最近的一切', '最近如何'])
            # final_dii = {'-HEIGHT': [], '-WEIGHT': [], '-EAT': [], '-BAD': [], '-EMO': []}
            final_lis=[]
            final_dii={}
            return '好吧，我们重新来。'+ran1
        if input_text == '' :

            saven={}
            all_dict = []
            ori=[]
            date_text={}
            ran1 =choice(['记录什么内容', '说出你最近的一切', '最近如何'])
            final_lis=[]
            final_dii = {}
            return ran1

        if input_text != '' :  # 第二次询问
            print(input_text)
            if '|||' in input_text:
                print('havetime')
                real_text = input_text.split('|||')[0]
                real_sj = input_text.split('|||')[1]     #用户提供时间
                real_sj = ios_time_nor(a = real_sj)      #日期正规
                ori = ori + [real_text]
                date_text[real_text] = real_sj
                saven[real_text] = real_sj
            else:
                print('nottime')
                ori = ori + [input_text]
                date_text[input_text]='20'+datetime.now() .strftime('%y-%m-%d %I:%M%p')  #系统时间
                # all_text.append(input_text)
                saven[input_text]='20'+datetime.now() .strftime('%y-%m-%d %I:%M%p')
            ran2 = choice(['还有什么要记录吗', '继续说你想记录的吧', '还有啥呢'])
            return ran2

if __name__ == '__main__':
    app.run(threaded=True,host='0.0.0.0', port='5000')


