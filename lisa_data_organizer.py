import os
from shutil import copyfile, rmtree
import pandas as pd
import matplotlib.pyplot as plt

home_dir = os.getcwd()
lisa_dir = home_dir+'/LISA_Data'
new_lisa_dir = home_dir+'/organized_lisa_dataset'
new_vid_lisa_dir = new_lisa_dir+'/vid'
new_aiua_lisa_dir = new_lisa_dir+'/aiua'
new_vid_img_lisa_dir = new_vid_lisa_dir+'/img'
new_aiua_img_lisa_dir = new_aiua_lisa_dir+'/img'

if not 'LISA_Data' in os.listdir() :
    assert Exception
if 'organized_lisa_dataset' in os.listdir() :
    rmtree(new_lisa_dir)
    print('OVERWRITTING to "organized_lisa_dataset" directory. organized_lisa_dataset is already exist.')
os.mkdir(new_lisa_dir)
os.mkdir(new_vid_lisa_dir)
os.mkdir(new_aiua_lisa_dir)
os.mkdir(new_vid_img_lisa_dir)
os.mkdir(new_aiua_img_lisa_dir)

# vid
vid_dirs = list(filter(lambda x : "vid" in x and not "." in x, os.listdir(lisa_dir)))
csv_filenames = []
for vid_dir in vid_dirs :
    inner_vid_dir = lisa_dir+'/'+vid_dir+'/'+os.listdir(lisa_dir+'/'+vid_dir)[0]
    for i in os.listdir(inner_vid_dir) :
        if '.csv' in i :
            csv_filenames.append(inner_vid_dir+'/'+i)  
        elif '.png' in i :
            classname = i.split('_')[0]
            if not classname in os.listdir(new_vid_img_lisa_dir) :
                os.mkdir(new_vid_img_lisa_dir+'/'+classname)
            copyfile(inner_vid_dir+'/'+i, new_vid_img_lisa_dir+'/'+classname+'/'+i)
        else : 
            pass
combined_csv = pd.concat([pd.read_csv(f, sep=';') for f in csv_filenames ])
combined_csv.to_csv(new_vid_lisa_dir+"/annotations.csv", index=False, encoding='utf-8-sig')

fig, ax = plt.subplots()
vid_df = combined_csv['Annotation tag']
vid_hist = vid_df.hist(ax=ax)
ax.tick_params(labelrotation=90)
fig.savefig(new_lisa_dir+'/vid_annotation.png')

vid_list = vid_df.to_list()
f = open(new_lisa_dir+'/vid_labels.txt', 'a') 
for l in list(set(vid_list)) :
    f.write(l+'\t'+str(vid_list.count(l))+'\n')
f.close()

# aiua
aiua_dirs = list(filter(lambda x : "aiua" in x and not "." in x, os.listdir(lisa_dir)))
csv_filenames = []
for aiua_dir in aiua_dirs :
    inner_aiua_dir = lisa_dir+'/'+aiua_dir+'/'+os.listdir(lisa_dir+'/'+aiua_dir)[0]
    for i in os.listdir(inner_aiua_dir) :
        if '.csv' in i :
            csv_filenames.append(inner_aiua_dir+'/'+i)  
        elif '.png' in i :
            classname = i.split('_')[0]
            if not classname in os.listdir(new_aiua_img_lisa_dir) :
                os.mkdir(new_aiua_img_lisa_dir+'/'+classname)
            copyfile(inner_aiua_dir+'/'+i, new_aiua_img_lisa_dir+'/'+classname+'/'+i)
        else : 
            pass
combined_csv = pd.concat([pd.read_csv(f, sep=';') for f in csv_filenames ])
combined_csv.to_csv(new_aiua_lisa_dir+"/annotations.csv", index=False, encoding='utf-8-sig')

fig, ax = plt.subplots()
aiua_df = combined_csv['Annotation tag']
aiua_hist = aiua_df.hist(ax=ax)
ax.tick_params(labelrotation=90)
fig.savefig(new_lisa_dir+'/aiua_annotation.png')

aiua_list = aiua_df.to_list()
f = open(new_lisa_dir+'/aiua_labels.txt', 'a') 
for l in list(set(aiua_list)) :
    f.write(l+'\t'+str(aiua_list.count(l))+'\n')
f.close()

###

fig, ax = plt.subplots()
total_df = aiua_df.append(vid_df)
total_hist = total_df.hist(ax=ax)
ax.tick_params(labelrotation=90)
fig.savefig(new_lisa_dir+'/total_annotation.png')

total_list = total_df.to_list()
f = open(new_lisa_dir+'/labels.txt', 'a') 
for l in list(set(total_list)) :
    f.write(l+'\t'+str(total_list.count(l))+'\n')
f.close()
