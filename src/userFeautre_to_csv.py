import pandas as pd
import numpy as np

def readline(line):
    current_line_list=[]
    for tuple_str in line.split('|'):
        name_value = tuple_str.split()
        if len(name_value)==1:
            current_line_list.append((name_value[0],None))
        elif len(name_value)==2:
            current_line_list.append((name_value[0],name_value[1]))
        else:
            index = tuple_str.find(name_value[1])
            current_line_list.append((name_value[0],tuple_str[index:]))
    return current_line_list       

def generate_df(line_lists):
    datas=[]
    for i in range(len(line_lists)):
        row=[np.NAN]*len(columns)
        for j in range(len(line_lists[i])):
            key = line_lists[i][j][0]
            column_num =  columns_map[key]
            row[column_num] = line_lists[i][j][1]
        datas.append(row)
    return datas

def save(filename,datas):
    user_feature_df = pd.DataFrame(datas,columns=columns)
    user_feature_df.to_csv(filename,sep=',',index=False)

columns_map={}
columns=['uid','age','gender','LBS','consumptionAbility', 'education','topic1', 'topic2', 'topic3', 'kw1', 'kw2','kw3','carrier', 'ct',  'marriageStatus', 'interest1', 'interest2','interest3','interest4','interest5','house', 'os','appIdAction','appIdInstall']
for i in range(len(columns)):
    columns_map[columns[i]]=i


# 如果想全部保存到一个文件,也很简单,那么只要把MAX_NUM设置为>userFeature.data的行数即可
MAX_NUM=1000000
line_lists=[]
import os
if not os.path.exists("../tmp/"):
    os.mkdir("../tmp/")

with open('../data/userFeature.data') as f:
    count=0
    for line in f:
        current_line_list=readline(line)
        line_lists.append(current_line_list)
        count +=1
        if count%MAX_NUM==0:
            datas = generate_df(line_lists)
            file_index = (count//MAX_NUM)
            filename = "../tmp/MyUserFeature"+str(file_index)+".csv"
            save(filename,datas)
            line_lists=[]
    if count%MAX_NUM!=0:
        datas = generate_df(line_lists)
        file_index = (count//MAX_NUM)+1
        filename = "../tmp/MyUserFeature"+str(file_index)+".csv"
        save(filename,datas)
    f.close()

del line_lists, datas
user_feature=pd.concat([pd.read_csv('MyUserFeature' + str(i) + '.csv') for i in range(1,13)]).reset_index(drop=True)
user_feature.to_csv('../data/MyUserFeature.csv', index=False)

