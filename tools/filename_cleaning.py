from PIL import Image
import numpy as np
import os, sys
import re

path = "/Path/to/dataset/"

dirs = os.listdir( path )

def filename_cleaning():
    for item in dirs:
        if item == '.DS_Store' or item == 'distribution.txt':
            continue
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            item_s = re.sub("train_(.+)_", '', item)
            f, e = os.path.splitext(path+item_s)
            print(item_s)
            im.save(f + '.png')
        
filename_cleaning()
