
def get_index(lst=None, item=''): ##获取全部索引
    return [i for i in range(len(lst)) if lst[i] == item]
def cut_max(num=10,alist=[2,8,19,30]): ##相减取绝对值最大索引
    cutlist=[abs(i-num) for i in alist]
    # print(cutlist.index(max(cutlist)))
    return  alist[cutlist.index(min(cutlist))]

#
# text_eat='三箱西瓜苹果五十斤,一瓶来自天山呼伦贝尔妈妈带的矿泉水'
# label_eat=['S-NUM', 'S-UNI', 'B-EAT', 'E-EAT','B-EAT', 'E-EAT', 'S-NUM','S-NUM', 'S-UNI',  'O', 'O', 'S-UNI', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'B-EAT', 'I-EAT', 'E-EAT']
# text_bad='抽了三根烟,喝了五十瓶呼伦贝尔来的啤酒'
# label_bad=['B-BAD', 'E-BAD', 'S-NUM', 'S-UNI', 'O', 'O', 'B-BAD', 'E-BAD', 'S-NUM', 'S-NUM', 'S-UNI', 'O', 'O', 'O', 'O', 'O', 'O', 'S-BAD', 'O']
#
# dicti={'-EAT':[{'entity':'','uni':'','num':''},{'entity':'','uni':'','num':''}],'-BAD':[{'entity':'','uni':'','num':''},{'entity':'','uni':'','num':''}]}


def get_char_list(text_eat,label,inde,uni_or_num):  #输入i,输出标点内的所有uni索引
    def in_char(test=text_eat,indexd=inde):
        import re
        pattern = r',|，|。|\.|!|！|？'
        result_list=re.split(pattern,test)
        count=0
        for i in result_list:
            count=count+len(i)+1
            if indexd < count:
                break
        return i

    char_uni_list=[]
    char_num_list=[]
    for i,ele in enumerate(label):  #抓uni
        if ele[1:] =='-UNI':
            # print(i)
            # print(text_bad[i])
            if text_eat[i] in in_char(text_eat):
                char_uni_list.append(i)
        if ele[1:] =='-NUM':
            # print(i)
            # print(text_bad[i])
            if text_eat[i] in in_char(text_eat):
                char_num_list.append(i)
    if uni_or_num =='UNI':
        print(char_uni_list)
        return char_uni_list

    if uni_or_num == 'NUM':
        print(char_num_list)
        return char_num_list
# get_char_list(text_eat=text_eat,label=label_eat,inde=2,uni_or_num='UNI')




aa={'-HEIGHT': '  2.5  公斤', '-WEIGHT': '  90公斤'}

chnumber=['零''一','二','三','四','五','六','七','八','九','十','点']

# def hw_to_nor(aa):
#
#     import re
#
#     if aa['-HEIGHT']!='':
#         number = re.findall(r"\d+\.?\d*",aa['-HEIGHT'])
#         number_start=aa['-HEIGHT'].find(''.join(str(s) for s in number))
#         uni=aa['-HEIGHT'][number_start+len(''.join(str(s) for s in number)):]
#         aa['-HEIGHT']=[{"NUM":''.join(str(s) for s in number),"UNI":uni}]
#
#     if aa['-WEIGHT']!='':
#         number = re.findall(r"\d+\.?\d*", aa['-WEIGHT'])
#         number_start = aa['-WEIGHT'].find(''.join(str(s) for s in number))
#         uni = aa['-WEIGHT'][number_start + len(''.join(str(s) for s in number)):]
#         aa['-WEIGHT'] = [{"NUM": ''.join(str(s) for s in number), "UNI": uni}]
#
#
#     print(aa)
#     return aa
# hw_to_nor(aa=aa)




# super=[{'-HEIGHT': [], '-WEIGHT': [], '-EAT': [{'B-EAT': '西瓜', 'NUM': '[]', 'UNI': '[]'}], '-BAD': [{'B-BAD': '抽了', 'NUM': '三', 'UNI': '根'}, {'B-BAD': '喝了', 'NUM': '五', 'UNI': '瓶'}], '-EMO': ['|', '焦', '虑']}, {'-HEIGHT': ['|', '9', '0', '公', '分'], '-WEIGHT': [], '-EAT': [], '-BAD': [], '-EMO': []}, {'-HEIGHT': [], '-WEIGHT': ['|', '1', '0', '0', '斤'], '-EAT': [], '-BAD': [], '-EMO': []}]
#
# for i in super:
#     print(i)

def timee(final_dii,time):
    for i in final_dii:

        for j in final_dii[i]:
            if i != 'EMO':
                j['TIME'] = dt.strftime(time)

    print(final_dii)
    return final_dii

def emoori(final_dii):
    def trans(lis,entity):
        # c=['a','b','c']
        all=[]
        for i in lis:
            all=all+[{entity:i}]
        # print(all)
        return all

    for i in final_dii:

            if i=='-EMO':
                final_dii[i]=trans(lis=final_dii[i],entity='MOOD')
            if i=='-ORI':
                final_dii[i] = trans(lis=final_dii[i], entity='TEXT')
    # print(final_dii)
    return final_dii
def emoori2(final_dii,senta):   #加入分数（建议后面做）
    def trans(lis,entity):
        all=[]
        for i in lis:
            all=all+[{entity:i}]
        return all
    def trans1(lis, entity):
        if lis!=[ ]: ####
            all_value = []
            input_dict = {"text": lis}
            results = senta.sentiment_classify(data=input_dict)
            for result in results:
                for i in result:
                    if i == 'positive_probs':
                        all_value.append(result[i])
            value_dic = dict(zip(lis, all_value))
            all = []
            for i in lis:
                all = all + [{entity: i, 'value': value_dic[i]}]
            return all
        else:
            all = []
            for i in lis:
                all = all + [{entity: i}]
            return all
    for i in final_dii:

        if final_dii[i] != [] or final_dii[i] != [''] or final_dii[i] != '':  # 可能报错
            if i == '-EMO':
                print('buggggggggggggggg22', final_dii[i])
                final_dii[i] = trans1(lis=final_dii[i], entity='mood')
            if i == '-ORI':
                final_dii[i] = trans(lis=final_dii[i], entity='text')
    print(final_dii)
    return final_dii

def onlyone(final_dii):         #身高体重唯一
    def remo(list1):
        count = -1
        for i in list1:
            count = count + 1
            if i == "|":
                cc = count

        index_to_delete = [i for i in range(cc)]
        list2 = [list1[i] for i in range(0, len(list1), 1) if i not in index_to_delete]
        # print(list2)
        return list2

    for i in final_dii:
        if i == '-HEIGHT' or i == '-WEIGHT':
            if final_dii[i].count('|') > 1:
                final_dii[i] = remo(final_dii[i])
    return final_dii
import pymongo
from datetime import datetime
client = pymongo.MongoClient(host='localhost', port=27017)
db = client.test
collection=db.students
dt=datetime.now() #创建一个datetime类对象

def deal_final(final_dii):          #字和字结合
    for i in final_dii:  # suo的子function
        if i != '-EAT' and i != '-BAD':
            final_dii[i] = "".join('%s' %id for id in final_dii[i]).replace("|", " ")
        if i == '-EMO':
            final_dii[i]=[c for c in final_dii[i].strip().split(' ')]
    final_diii = hw_to_nor(aa=final_dii)
    return final_diii



def hw_to_nor(aa):

    import re

    if  aa['-HEIGHT']!='':
        number = re.findall(r"\d+\.?\d*",aa['-HEIGHT'])
        number_start=aa['-HEIGHT'].find(''.join(str(s) for s in number))
        uni=aa['-HEIGHT'][number_start+len(''.join(str(s) for s in number)):]
        aa['-HEIGHT']=[{"NUM":''.join(str(s) for s in number),"UNI":uni}]

    if  aa['-WEIGHT']!='':
        number = re.findall(r"\d+\.?\d*", aa['-WEIGHT'])
        number_start = aa['-WEIGHT'].find(''.join(str(s) for s in number))
        uni = aa['-WEIGHT'][number_start + len(''.join(str(s) for s in number)):]
        aa['-WEIGHT'] = [{"NUM": ''.join(str(s) for s in number), "UNI": uni}]



    print(aa)
    return aa

def suo(dii,input_id,collection):
    # for i in dii:
    #     if i != '-EAT' and i != '-BAD':
    #         dii[i] = "".join(dii[i]).replace("|", "  ")
    # dii = hw_to_nor(aa=dii)
    # dii['-TIME'] = dt.strftime('%y-%m-%d %I:%M:%S %p')
    NAME = collection.find({input_id: {'$exists': 'true'}})

    if len([i for i in NAME]) == 0:  ##
        print('id不存在')
        ins = collection.insert(      {input_id: [dii]}     )
    else:
        print('id存在')
        NAME = collection.find({input_id: {'$exists': 'true'}})
        p1 = dict((key, value) for key, value in NAME[0].items() if key == input_id)
        new_list = NAME[0][input_id] + [dii]
        new_dict = {input_id: new_list}
        print(p1)
        print(new_dict)
        up = collection.update(p1, {'$set': new_dict})
    return dii
def suo2(dii,input_id,collection,datee):
    # for i in dii:
    #     if i != '-EAT' and i != '-BAD':
    #         dii[i] = "".join(dii[i]).replace("|", "  ")
    # dii = hw_to_nor(aa=dii)
    # dii['-TIME'] = dt.strftime('%y-%m-%d %I:%M:%S %p')
    NAME = collection.find({input_id: {'$exists': 'true'}})
    if len([i for i in NAME]) == 0:  ##
        print('id不存在')
        ins = collection.insert( {input_id:[{dt.strftime(datee): [dii]}]}   )
    else:
        print('id存在')
        NAME = collection.find({input_id: {'$exists': 'true'}})
        name_result = NAME[0][input_id]
        original = NAME[0][input_id]
        timelis = []
        for i in name_result:
            # print(12,i)   ##所有日期的结果
            timelis = timelis + [j for j in i]

        if dt.strftime(datee) in timelis:  # 如果时间存在
            for i in name_result:
                try:
                    i[dt.strftime(datee)] = i[dt.strftime(datee)] + [dii]  # 加新的
                    print('coo', i[dt.strftime(datee)])
                except KeyError:
                    pass

        if dt.strftime(datee) not in timelis:
            name_result = name_result + [{dt.strftime(datee): [dii]}]

        print('ooooooooooooooooooo',original)
        print('nnnnnnnnnnnnnnnnnnn',name_result)

        up = collection.update({input_id:original}, {'$set': {input_id:name_result}})
    return dii
def text_text2(aa):
    result=''
    for i in aa:
        # print(i)
        result=result+'<br/>'+i+'<br/>'
        for small_dic in aa[i]:
            result = result + '<br/>'
            for small_key in small_dic:
                if small_dic[small_key]!=[]:
                    result=result+small_key
                    result=result+str(small_dic[small_key])
                    # print(small_key,small_dic[small_key])
    result=result.replace('-ORI','原句：').replace('-WEIGHT','体重：').replace('-HEIGHT','身高：').replace('B-EAT','食物：')\
        .replace('B-BAD','抽烟喝酒：').replace('-EMO','情绪：').replace('TIME','时间：').replace('TEXT','文本：')\
        .replace('NUM', '数值：').replace('UNI', '单位：').replace('-EAT', '饮食：').replace('-BAD', '坏习惯：')
    return result

def text_text(final_dii,last=True):

    if final_dii['-HEIGHT'] == [] or final_dii['-HEIGHT'] == '':
        text_hei = ''
    else:
        if final_dii['-HEIGHT'][0]["UNI"] == '':
            text_hei = "身高为: " + final_dii['-HEIGHT'][0]["NUM"]
        else:
            text_hei = "身高为: " + final_dii['-HEIGHT'][0]["NUM"] + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;单位: " + \
                       final_dii['-HEIGHT'][0]["UNI"] + '<br/>'

    if final_dii['-WEIGHT'] == [] or final_dii['-WEIGHT'] == '':
        text_wei = ''
    else:
        if final_dii['-WEIGHT'][0]["UNI"] == '':
            text_wei = "体重为: " + final_dii['-WEIGHT'][0]["NUM"]
        else:
            text_wei = "体重为: " + final_dii['-WEIGHT'][0]["NUM"] + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;单位: " + \
                       final_dii['-WEIGHT'][0]["UNI"] + '<br/>'

    if final_dii['-EAT'] == [] or final_dii['-EAT'] == '':
        text_eat = ''
    else:
        te_eat = [final_dii['-EAT'][i]['B-EAT'] + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;数量: " + final_dii['-EAT'][i][
            "NUM"] + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;单位: " + final_dii['-EAT'][i][
                      "UNI"] + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                  for i in range(len(final_dii['-EAT']))]
        text_eat = [i.replace('数量: []&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;', '').replace(
            '单位: []&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;', '') for i in te_eat]
        text_eat = "吃了:&nbsp" + str(text_eat) + '<br/>'

    if final_dii['-BAD'] == [] or final_dii['-BAD'] == '':
        text_bad = ''
    else:
        te_bad = [final_dii['-BAD'][i]['B-BAD'] + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;数量: " + final_dii['-BAD'][i][
            "NUM"] + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;单位: " + final_dii['-BAD'][i][
                      "UNI"] + "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                  for i in range(len(final_dii['-BAD']))]
        text_bad = [i.replace('数量: []&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;', '').replace(
            '单位: []&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;', '') for i in te_bad]
        text_bad = "抽烟喝酒状况为:&nbsp" + str(text_bad) + '<br/>'

    if final_dii['-EMO'] == [''] or final_dii['-EMO'] ==[] :
        text_emo = ''
    else:
        print('wwwwwwwwwwwwwwwwwwwwwww',final_dii['-EMO'])
        saave=''
        for i in final_dii['-EMO']:
            saave=saave+' '+i
        text_emo = "情绪为： " + saave
    if last==True:
        say='确认请说“确认”,需要修改请说“有误”'
    if last == False:
        say = '您可以说：“删除XX”来修改记录；或继续聊点别的来记录其它。'
    a =  text_hei  + text_wei + text_eat + text_bad + text_emo + '<br/>' + '<br/>' + say

    return '<table border="0" cellpadding="0" cellspacing="0" width="100%">'+a

