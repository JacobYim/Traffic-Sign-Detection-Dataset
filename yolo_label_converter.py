import os 
import json
import pandas as pd
from functools import *
print(os.listdir())
if 'yolo_label' in os.listdir() :
    os.rmdir('yolo_label')
os.mkdir('yolo_label')
os.mkdir('yolo_label/annotaion')

yolo_labels = ['speed_limit','stop']
mapilary_labels_list = [[
    'regulatory--maximum-speed-limit-40--g3','regulatory--maximum-speed-limit-50--g1'
],[
    'regulatory--stop--g1','regulatory--stop--g10','regulatory--stop-signals--g1'
]]
lisa_labels_list = [['rampSpeedAdvisory50','speedLimit15','speedLimit35'],['stop']]

def load_lisa(dataset='total') :
    dfs = []
    if dataset == 'total' or dataset == 'aiua' :    
        df = pd.read_csv ('./organized_lisa_dataset/aiua/annotations.csv')
        dfs.append(df)

    if dataset == 'total' or dataset == 'vid' :
        df = pd.read_csv ('./organized_lisa_dataset/aiua/annotations.csv')
        dfs.append(df)
    if len(dfs) == 2:
        df = dfs[0].append(dfs[1], ignore_index=True)
    return df

def load_mapilary(dataset='total') :
    json_datas = []
    if dataset == 'total' or dataset == 'fully' : 
        for label_json in os.listdir('./organized_mapilary_dataset/fully/annotations') :
            with open('./organized_mapilary_dataset/fully/annotations/'+label_json) as json_stream:
                json_data = json_stream.read()
                json_data = json.loads(json_data)
                json_data['dataset'] = 'fully'
                json_data['filename'] = label_json.split('.')[0]
                json_datas.append(json_data)

    if dataset == 'total' or dataset == 'partially' :
        for label_json in os.listdir('./organized_mapilary_dataset/partially/annotations') :
            with open('./organized_mapilary_dataset/partially/annotations/'+label_json) as json_stream:
                json_data = json_stream.read()
                json_data = json.loads(json_data)
                json_data['dataset'] = 'partially'
                json_data['filename'] = label_json.split('.')[0]
                json_datas.append(json_data)
    return json_datas

# def lisa_to_yolo(lisa_dataframe, yolo_labels, lisa_labels_list) :
#     lisa_labels = list(reduce(lambda x, y : x+y, lisa_labels_list))
#     valid_dataset = lisa_dataframe[lisa_dataframe['Annotation tag'].isin(lisa_labels)]
#     for data in valid_dataset.values.tolist() :
#         if data[1] in 


# def mapilary_to_yolo(mapilary_json_list) :



# for yolo_label, lisa_labels, mapilary_labels in zip(yolo_labels, lisa_labels_list, mapilary_labels_list) :

#     for lisa_label in lisa_labels :
#         pass

#     for mapilary_label in mapilary_labels :
#         pass