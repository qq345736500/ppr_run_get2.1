def add_datetime(all_dict , time_list):   #给字典list和时间list 打上时间日期,合并date
    new_dic={}
    for i,ele in enumerate(all_dict):
        for small_key in ele :
            # print('字字典：；',ele[small_key])    #允许[]和''
            for smallll_dic in ele[small_key]:
                # print('子子字典',smallll_dic)
                smallll_dic['TIME']=time_list[i].split(' ')[1]  #time


        if time_list[i].split(' ')[0] not in new_dic:
            new_dic[time_list[i].split(' ')[0] ] = [ele]                 #  date
        else:
            new_dic[time_list[i].split(' ')[0]]=new_dic[time_list[i].split(' ')[0]]+[ele]

    # print(new_dic)
    return new_dic

def sametime_combine(diccc):   #接add_datetime，相同时间和并 （最好是用[]）
    import re                       #asdASASDsSAS
    new_diccc={}
    for i in diccc:
        savv_dic={}
        for small_dic in diccc[i]:
            aa=re.search(r"\d\d:\d\d[AP]M",str(small_dic))
            if aa.group(0) in savv_dic:
                for k,v in small_dic.items():
                    savv_dic[aa.group(0)][k]+=v
            else:
                savv_dic[aa.group(0)]=small_dic
        savv_lis=[]                 #最外层
        for j in savv_dic:
            savv_lis=savv_lis+[savv_dic[j]]
        new_diccc[i]=savv_lis
    # print(new_diccc)
    return new_diccc

def ios_time_nor(a):
    a = a.replace('年','-').replace('月','-').replace('日','')
    if '下午' in a:
        a=a.replace('下午','')+'PM'
    if '上午' in a:
        a=a.replace('上午','') + 'AM'
    import re
    long_moon = re.search(r"-\d+-", a).group()
    long_day = re.search(r"-\d+ ", a).group()

    if len(long_moon) < 4:
        lis = list(long_moon)
        lis.insert(1, '0')
        aa = ''.join(lis)
        a = a.replace(long_moon, aa)
    if len(long_day) < 4:
        lis = list(long_day)
        lis.insert(1, '0')
        aa = ''.join(lis)
        a = a.replace(long_day, aa)

    print(a)


    # print(a)
    return a


def cut_max(num=10,alist=[2,8,19,30]): ##相减取绝对值最大索引
    cutlist=[abs(i-num) for i in alist]
    # print(alist[cutlist.index(min(cutlist))])
    return  alist[cutlist.index(min(cutlist))]

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
        return char_uni_list
    if uni_or_num == 'NUM':
        return char_num_list

def dictionary(label_list,mytext):          #变成字典
    dicti = {'-HEIGHT': [], '-WEIGHT': [], '-EAT': [], '-BAD': [], '-EMO': []}

    for i ,ele in enumerate(label_list):
        if 'B-BAD'== ele or 'B-EAT'== ele:
            name=mytext[i]                               ###到break都是加多字的名字
            for shu,x in enumerate(label_list[i:]):
                try:
                    if label_list[i:][shu][1:]==label_list[i:][shu+1][1:]:
                        name=name+mytext[i+shu+1]
                    else:
                        break
                except IndexError:
                    break
            evert_dic={ele:name,'NUM':'','UNI':''}

            all_uni_inchar = get_char_list(mytext, label_list, i, uni_or_num='UNI')
            all_num_inchar = get_char_list(mytext, label_list, i, uni_or_num='NUM')
            # print('\n'+mytext[i])

            print('\n')
            print(i)
            if all_uni_inchar !=[]:
                print('UNI:',cut_max(i,all_uni_inchar),all_uni_inchar,mytext[cut_max(i,all_uni_inchar)])  #算和uni距离最小的               ##记得抓双数

                name_uni=mytext[cut_max(i,all_uni_inchar)]                ###到break都是加多字的名字
                for x in range(1,3):
                    # print(label_list[cut_max(i,all_uni_inchar)+x][1:])
                    try:
                        if label_list[cut_max(i,all_uni_inchar)][1:]==label_list[cut_max(i,all_uni_inchar)+x][1:]:
                            name_uni=name_uni+mytext[cut_max(i,all_uni_inchar)+x]

                        if label_list[cut_max(i,all_uni_inchar)][1:]==label_list[cut_max(i,all_uni_inchar)-x][1:]:
                            name_uni = mytext[cut_max(i,all_uni_inchar)-x]+name_uni
                    except IndexError:
                        print('超过了')

                # for shu, x in enumerate(label_list[cut_max(i,all_uni_inchar):]):
                #     print('222222222222222',label_list[cut_max(i,all_uni_inchar)][shu - 1][1:])
                #     if label_list[1:][shu][1:]==label_list[1:][shu+1][1:]:
                #         name_uni = name_uni + mytext[cut_max(i,all_uni_inchar)+ shu + 1]
                #     else:
                #         break
                evert_dic['UNI']=name_uni
            else:
                print('UNI:[]')
                evert_dic['UNI'] = '[]'
            if all_num_inchar != []:
                print('NUM:',cut_max(i,all_num_inchar),mytext[cut_max(i,all_num_inchar)])  #算和uni距离最小的
                name_num=mytext[cut_max(i,all_num_inchar)]
                for x in range(1,3):
                    # print(label_list[cut_max(i,all_uni_inchar)+x][1:])
                    try:
                        if label_list[cut_max(i,all_num_inchar)][1:]==label_list[cut_max(i,all_num_inchar)+x][1:]:
                            name_num=name_num+mytext[cut_max(i,all_num_inchar)+x]
                        if label_list[cut_max(i,all_num_inchar)][1:]==label_list[cut_max(i,all_num_inchar)-x][1:]:
                            name_num = mytext[cut_max(i,all_num_inchar)-x]+name_num
                    except IndexError:
                        print('超过了')

                # for shu, x in enumerate(label_list[cut_max(i, all_num_inchar):]):
                #     if label_list[1:][shu][1:] == label_list[1:][shu + 1][1:]:
                #         name_num=name_num + mytext[cut_max(i,all_num_inchar)+ shu + 1]
                #     else:
                #         break
                evert_dic['NUM'] = name_num
            else:
                print('NUM: []')
                evert_dic['NUM'] = '[]'
            print(evert_dic)

            if 'B-BAD' in evert_dic:
                dicti['-BAD'].append(evert_dic)
            if 'B-EAT' in evert_dic:
                dicti['-EAT'].append(evert_dic)
        elif ele[1:]!='-EAT' and ele[1:]!='-BAD' and ele[1:] in dicti:
            if label_list[i - 1] == 'O':
                dicti[label_list[i][1:]].append('|')
                dicti[label_list[i][1:]].append(mytext[i])
            else:
                dicti[label_list[i][1:]].append(mytext[i])
    print('222222222222',dicti)

    return dicti

