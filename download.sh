#!/bin/bash

# LISA Dataset
wget -O LISA_Data.zip http://cvrr.ucsd.edu/LISA/Datasets/signDatabasePublicFramesOnly.zip
unzip LISA_Data.zip -d LISA_Data

# Google Open Dataset
# git clone https://github.com/EscVM/OIDv4_ToolKit.git
# mkdir dataset/google
# cd OIDv4_ToolKit
# virtualenv venv --py=python3
# source venv/bin/activate
# pip3 install -r requirements.txt
# python3 main.py downloader --classes Traffic_sign --type_csv validation --Dataset ../../google/ -y
# python3 main.py downloader --classes Traffic_sign --type_csv test  --Dataset ../../google/ -y
# python3 main.py downloader --classes Traffic_sign --type_csv train --Dataset ../../google/ -y
# deactivate
mkdir mapillary_data
virtualenv venv --py=python3
source venv/bin/activate
pip install -r requirements.txt
python downloader/mapilary_downloader.py
deactivate
