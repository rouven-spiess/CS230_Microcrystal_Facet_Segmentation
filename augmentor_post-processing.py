from PIL import Image
import numpy as np
import os, sys
import re

path = "/Path/to/dataset/"

dirs = os.listdir( path )

#for data distribution
dist = np.zeros(4)

def rgb_ortho():
    for item in dirs:
        if item == '.DS_Store' or item == 'distribution.txt':
            continue
        if os.path.isfile(path+item):
            im = Image.open(path+item)
            item_s = re.sub("_(.+)_", '', item) #performs sanitization of item name
            f, e = os.path.splitext(path+item_s)
            
            im = im.convert('RGBA')
            
            global dist

            data = np.array(im)   # "data" is a height x width x 4 numpy array
            red, green, blue, alpha = data.T # Temporarily unpack the bands for readability
            
            black_areas = (red < 70) & (green < 70) & (blue < 70)
            red_areas = (red > 70) & np.logical_not(black_areas)
            green_areas = (green > 70) & np.logical_not(black_areas)
            
            #update the total surfaces for pixel distribution
            #dist = np.add(dist, [np.count_nonzero(black_areas), np.count_nonzero(red_areas), np.count_nonzero(green_areas), np.count_nonzero(yellow_areas)])

            data[..., :-1][black_areas.T] = (0, 0, 0) # Blue channel as class index
            data[..., :-1][red_areas.T] = (255, 0, 1) # Blue channel as class index
            data[..., :-1][green_areas.T] = (0, 255, 2) # Blue channel as class index

            im2 = Image.fromarray(data)
            im2 = im2.convert('RGB')
            
            print(f)
            im2.save(f + '.png')
    
    pixels = np.sum(dist)
    #distribution = (dist[0]/pixels, dist[1]/pixels, dist[2]/pixels, dist[3]/pixels, pixels)
    #print(distribution)
    #with open(path + "distribution.txt", "w") as text_file:
        #text_file.write("black: %f red: %f green: %f yellow: %f other: %f pixels: %d" % distribution)
        
rgb_ortho()
