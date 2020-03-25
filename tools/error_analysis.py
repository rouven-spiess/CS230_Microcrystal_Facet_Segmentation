from PIL import Image, ImageDraw, ImageFont
import numpy as np
import os, sys
import re

#prediction and ground truth paths
pr_path = "/path/to/predictions/"
gt_path = "/path/to/ground_truth/"
out_path = "/path/to/output/images"

pr_dirs = os.listdir( pr_path )
gt_dirs = os.listdir( gt_path )

def compute_IoU_mPA(pr, gt):
    
    EPS = 1e-12
    n_classes = 4

    #Classwise Intersection over Union IoU
    class_wise_IoU = np.zeros(n_classes)
    for cl in range(n_classes):
        intersection = np.sum((gt == cl)*(pr == cl))
        union = np.sum(np.maximum((gt == cl), (pr == cl)))
        iou = float(intersection)/(union + EPS)
        class_wise_IoU[cl] = iou
            
    #Classwise Pixel Accuracy mPA
    class_wise_mPA = np.zeros(n_classes)
    for cl in range(n_classes):
        intersection = np.sum((gt == cl)*(pr == cl))
        total = np.sum((gt == cl))
        mpa = float(intersection)/(total + EPS)
        class_wise_mPA[cl] = mpa
    
    return class_wise_IoU, class_wise_mPA
    

def convert_and_annotate():
    
    IoU = np.empty(4)
    mPA = np.empty(4)
    
    for item in pr_dirs:
        if item == '.DS_Store' or item == 'distribution.txt':
            continue
        if os.path.isfile(pr_path+item):
            f, e = os.path.splitext(out_path+item)
            pr = Image.open(pr_path+item)
            gt = Image.open(gt_path+item)
            pr = pr.convert('RGBA')
            gt = gt.convert('RGBA')

            #Get RGB values from predictions
            pr_data = np.array(pr)   # "data" is a height x width x 3 numpy array
            red, green, blue, alpha = pr_data.T # Temporarily unpack the bands for readability
            background = (red == 20) & (green == 215) & (blue == 197) 
            facet_100 = (red == 207) & (green == 248) & (blue == 132)
            facet_111 = (red == 183) & (green == 244) & (blue == 155)
            facet_110 = (red == 144) & (green == 71) & (blue == 111)
            #rest = (np.logical_not(background) & np.logical_not(facet_100) & np.logical_not(facet_111) & np.logical_not(facet_110))
            
            #Convert to decimal
            pr_data[..., :-1][rest.T] = 0
            pr_data[..., :-1][background.T] = 0 
            pr_data[..., :-1][facet_100.T] = 1 
            pr_data[..., :-1][facet_111.T] = 2 
            pr_data[..., :-1][facet_110.T] = 3 
            
            #Get RGB values from ground truth
            gt_data = np.array(gt)   # "data" is a height x width x 3 numpy array
            red, green, blue, alpha = gt_data.T # Temporarily unpack the bands for readability
            facet_100 = (red == 255) & (green == 0) & (blue == 1) 
            facet_111 = (red == 0) & (green == 255) & (blue == 2)
            facet_110 = (red == 255) & (green == 255) & (blue == 3)
            background = (red == 0) & (green == 0) & (blue == 0)
            #rest = (np.logical_not(background) & np.logical_not(facet_100) & np.logical_not(facet_111) & np.logical_not(facet_110))
            
            #Convert to decimal
            gt_data[..., :-1][background.T] = 0 
            gt_data[..., :-1][facet_100.T] = 1 
            gt_data[..., :-1][facet_111.T] = 2 
            gt_data[..., :-1][facet_110.T] = 3       
            
            #Classwise IoU computation
            pr = pr_data
            gt = gt_data
 
            class_wise_IoU, class_wise_mPA = compute_IoU_mPA(pr, gt)
            #print(item, class_wise_IoU, class_wise_mPA)
    
            IoU = np.vstack((IoU, class_wise_IoU))
            mPA = np.vstack((mPA, class_wise_mPA))
               
            IoU.astype('float')
            IoU[IoU == 0] = np.nan
            #IoU = np.delete(IoU, (0), axis=0)
            #print(np.nanmean(IoU, axis=0))
    
            mPA.astype('float')
            mPA[mPA == 0] = np.nan
            #mPA = np.delete(mPA, (0), axis=0)
            #print(np.nanmean(mPA, axis=0))
            #print(mPA)
            
            #Image conversion and annotation
            out = Image.open(pr_path+item)
            out = out.convert('RGBA')
            out_data = np.array(out)   # "data" is a height x width x 4 numpy array
            red, green, blue, alpha = out_data.T # Temporarily unpack the bands for readability
            background = (red == 20) & (green == 215) & (blue == 197) 
            facet_100 = (red == 207) & (green == 248) & (blue == 132)
            facet_111 = (red == 183) & (green == 244) & (blue == 155)
            facet_110 = (red == 144) & (green == 71) & (blue == 111)
            
            #Convert predictions to RGBA
            out_data[..., :-1][background.T] = (128, 128, 128)
            out_data[..., :-1][facet_100.T] = (255, 0, 86)
            out_data[..., :-1][facet_111.T] = (0, 255, 2)
            out_data[..., :-1][facet_110.T] = (0, 102, 255)
            
            im2 = Image.fromarray(out_data)
            im2 = im2.convert('RGB') #Rouven
            perf = np.round(class_wise_IoU*100, decimals=0)
            ImageDraw.Draw(
                im2  # Image
                ).text(
                    (0, 0),  # Coordinates
                str(perf),  # Text
                (0, 0, 0)  # Color
                )
            im2.save(f + 'new.png')
    print(np.nanmean(IoU, axis=0))
    print(np.nanmean(mPA, axis=0))

convert_and_annotate()
