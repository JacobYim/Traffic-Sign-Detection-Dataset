import zipfile
import os 

for i in os.listdir() :
	if i.endswith(".zip") :
		os.mkdir(i.split(".")[0])
		with zipfile.ZipFile(i, 'r') as ref:
			ref.extractall(i.split(".")[0])
