import cv2
import os
import re
import numpy as np

class_list = []
color_dic = dict()
flag = 0

def color_gen():
    '''
    Generate a new color. As first color generates (0, 255, 0)
    '''
    global flag
  
    if flag == 0:
        color = (0, 255, 0)
        flag += 1
    else:
        np.random.seed()
        color = tuple(255 * np.random.rand(3))
    return color


def show(download_dir, index=0, file= None, window_name="aaaa", class_name=None) :
    
    
    if file : 
        if file.endswith('.txt'):
            expect_img_file = str('.'.join(file.split('.')[:-1])) + '.jpg'
            if expect_img_file in os.listdir(download_dir) :
                text_file = file
                file_name = expect_img_file
            else :
                print('[ERROR] {} NOT exist'.format(expect_img_file))
        elif file.endswith('.jpg'):
            expect_txt_file = str('.'.join(file.split('.')[:-1])) + '.txt'
            if expect_txt_file in os.listdir(download_dir) :
                text_file = expect_txt_file
                file_name = file
            else :
                print('[ERROR] {} NOT exist'.format(expect_txt_file))
        else :
            if file+'.txt' in os.listdir(download_dir) and file+'.jpg' in os.listdir(download_dir) :
                text_file = file+'.txt'
                file_name = file+'.jpg'
            else :
                print('[ERROR] {} or {} NOT exist'.format(file+'.txt', file+'.jpg'))
                return 0 
    else :
    
        txt_filtered = filter(lambda x : x.endswith('.txt'), os.listdir(download_dir)) 

        if class_name :
            def check_class_name(file_name, class_name) :
                f = open(file_name, 'r')
                return f.readlines()[0].split(' ')[0] == class_name
            txt_list = list(txt_filtered)
            txt_filtered = filter(lambda x : check_class_name(x), txt_list)

        filtered_list = list(txt_filtered)
        filtered_list.sort()

        text_file = filtered_list[index]
        file_name = str('.'.join(text_file.split('.')[:-1])) + '.jpg'
        
    file_path = os.path.join(download_dir, text_file)
    print(file_path)
    f = open(file_path, 'r')
    
    current_image_path = str(os.path.join(download_dir, file_name))
    print(current_image_path)
    img = cv2.imread(current_image_path)
    
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    width = 500
    height = int((img.shape[0] * width) / img.shape[1])
    cv2.resizeWindow(window_name, width, height)

    for line in f:        
        # each row in a file is class_name, XMin, YMix, XMax, YMax
        match_class_name = re.compile('^[a-zA-Z]+(\s+[a-zA-Z]+)*').match(line)
        class_name = line[:match_class_name.span()[1]]
        ax = line[match_class_name.span()[1]:].lstrip().rstrip().split(' ')
	# opencv top left bottom right

        if class_name not in class_list:
            class_list.append(class_name)
            color = color_gen()     
            color_dic[class_name] = color  

        font = cv2.FONT_HERSHEY_SIMPLEX
        r ,g, b = color_dic[class_name]
        # cv2.putText(img,class_name,(int(float(ax[0]))+5,int(float(ax[1]))-7), font, 0.8,(b, g, r), 2,cv2.LINE_AA)
        cv2.rectangle(img, (int(float(ax[-2])), int(float(ax[-1]))),
                      (int(float(ax[-4])),
                       int(float(ax[-3]))), (b, g, r), 3)

    print('show')
    cv2.imshow(window_name, img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
if __name__ == "__main__" :   
    show(file='stop_1331867195.avi_image3', download_dir='yolo_label')