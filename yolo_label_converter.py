import os 
import shutil
import cv2
import json
import pandas as pd
from PIL import Image
from functools import *

destination_dataset_dir_name = 'yolo_data'

with open('label_setting.json') as f:
    data = json.load(f)
yolo_labels =  list(data.keys())
mapilary_labels_list = list(map(lambda x : data[x]["mapilary_labels_list"], yolo_labels))
lisa_labels_list = list(map(lambda x : data[x]["lisa_labels_list"], yolo_labels))

def load_lisa(dataset='total') :
    dfs = []
    if dataset == 'total' or dataset == 'aiua' :    
        df = pd.read_csv ('./organized_lisa_dataset/aiua/annotations.csv')
        df['dataset'] = 'aiua'
        dfs.append(df)
    if dataset == 'total' or dataset == 'vid' :
        df = pd.read_csv ('./organized_lisa_dataset/vid/annotations.csv')
        df['dataset'] = 'vid'
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

def pick_lisa_data(lisa_dataframe, yolo_labels, lisa_labels_list) :
    lisa_labels = list(reduce(lambda x, y : x+y, lisa_labels_list))
    target_data_list = lisa_dataframe[lisa_dataframe['Annotation tag'].isin(lisa_labels)].values.tolist()
    for data in target_data_list :
        for yolo_label, lisa_labels in zip(yolo_labels, lisa_labels_list) :
            if data[1] in lisa_labels :
                try :
                    # copy image
                    # shutil.copy('./organized_lisa_dataset/'+data[-1]+'/img/'+data[1]+'/'+data[0], './'+destination_dataset_dir_name)
                    im1 = Image.open('./organized_lisa_dataset/'+data[-1]+'/img/'+data[1]+'/'+data[0])
                    im1.save('./'+destination_dataset_dir_name+'/'+data[0].replace('.png','.jpg'))
                    # save annotation at destination directory
                    f = open('./'+destination_dataset_dir_name+'/'+'.'.join(data[0].split('.')[0:-1]+['txt']), "a")
                    f.write( " ".join(map(lambda x : str(x), [yolo_label]+data[2:6]))+"\n")
                    f.close()
                except :
                    pass

def mapilary_to_yolo(mapilary_jsons, yolo_labels, mapilary_labels_list) :
    mapilary_labels = list(reduce(lambda x, y : x+y, mapilary_labels_list))
    target_data_jsons = list(filter(lambda map_jason : len(set(mapilary_labels) & set(map(lambda x : x['label'] , map_jason['objects']))) > 0, mapilary_jsons))

    for data in target_data_jsons :
        try :
            shutil.copy('./organized_mapilary_dataset/'+data['dataset']+'/img/'+data['filename']+'.jpg', './'+destination_dataset_dir_name)
            f = open('./'+destination_dataset_dir_name+'/'+data['filename']+'.txt', "a")
            for yolo_label, mapilary_labels in zip(yolo_labels, mapilary_labels_list) :
                for data_object in data['objects'] :
                    if data_object['label'] in mapilary_labels :
                        # save annotation at destination directory
                        content_txt = " ".join([yolo_label, str(data_object['bbox']['xmin']), str(data_object['bbox']['ymin']), str(data_object['bbox']['xmax']), str(data_object['bbox']['ymax'])])
                        f.write(content_txt+'\n')
            f.close()
        except :
            pass

def convert_coordinate() :
    print('convert_coordinate start')
    new_label_file_dir = "yolo_label"
    if new_label_file_dir in os.listdir() :
        shutil.rmtree(new_label_file_dir)
    os.mkdir(new_label_file_dir)

    filelist = os.listdir(destination_dataset_dir_name)
    textfilelist = list(filter(lambda x : '.txt' in x, filelist))
    for textfile in textfilelist :
        print('{} processing ...'.format(destination_dataset_dir_name+"/"+textfile))
        file = open(destination_dataset_dir_name+"/"+textfile,mode='r+')
        all_of_it = file.read()
        lines = all_of_it.split('\n')[:-1]  
        file.close()
        
        print(lines)

        im = cv2.imread(destination_dataset_dir_name+'/'+textfile.split('.txt')[0]+'.jpg')
        h, w, c = im.shape
        # print(h, w, c)

        new_file = open(new_label_file_dir+"/"+textfile, "w+")
        for line in lines :
            # print(line)
            content = line.split(' ')
            # print(content)
            min_x = float(content[1]) 
            min_y = float(content[2])
            max_x = float(content[3])
            max_y = float(content[4])
            content[1] = str(float(min_x/w))
            content[2] = str(float(min_y/h))
            content[3] = str(float(max_x/w))
            content[4] = str(float(max_y/h))
            print("print content : ", content)
            new_line = " ".join(content)+"\n"
            # print(new_line)
            new_file.write(new_line)
        new_file.close()

if __name__ == "__main__" :
    if destination_dataset_dir_name in os.listdir() :
        shutil.rmtree(destination_dataset_dir_name)

    os.mkdir(destination_dataset_dir_name)

    lisa_dataframe = load_lisa(dataset='total')
    mapilary_jsons = load_mapilary(dataset='total')
    pick_lisa_data(lisa_dataframe, yolo_labels, lisa_labels_list)
    mapilary_to_yolo(mapilary_jsons, yolo_labels, mapilary_labels_list)
    convert_coordinate()