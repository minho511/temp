from re import L
import matplotlib.pyplot as plt
import cv2
from skimage import data
from skimage import exposure
from skimage.exposure import match_histograms
import numpy as np
import glob
import os
import time
from time import ctime
import ProcessingTools as pt
from ProcessingTools.functions import multi_func
import torch
market_files = []
for (root, dirs, files) in os.walk('/data/min/minho/MetaBIN/datasets/Market-1501-v15.09.15/bounding_box_train/'):
    for f in files:
        market_files.append(os.path.join(root, f))

celeb_files = []
for (root, dirs, files) in os.walk('/home/vcl/Desktop/min/minho/MetaBIN/datasets/TOCELEB-tolast/query_ori'):
    for f in files:
        celeb_files.append(os.path.join(root, f))

# size = len(celeb_files)
# def list_chunk(lst, n):
#     return [list[i:i+n] for i in range(0, len(lst), n)]

# splited_files = list_chunk(celeb_files, len(celeb_files)//7)


def histo_match(files, market_files, channel, num = 10000):


    histo_sum_result_name = 'market_histo_sum.npy'
    if not os.path.isfile(f'{histo_sum_result_name}'):
        # market 10000장
        sample10000 = np.random.choice(market_files, num, replace = False)
        hsv_files = []    
        for i in pt.ProgressBar(range(0,num)):
            img_bgr = cv2.imread(sample10000[i])
            img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
            h, w = img_hsv.shape[:2]
            img_hsv = cv2.resize(img_hsv, (1, h*w))
            hsv_files.append(img_hsv)
        result = cv2.vconcat(hsv_files)
        np.save(f'market_histo_sum', result)
    result = np.load(histo_sum_result_name)
    # exit()
    # result = cv2.cvtColor(result, cv2.COLOR_HSV2RGB)
    result_h = result[:,:,0] # H
    result_s = result[:,:,1] # S
    result_v = result[:,:,2] # V
    #######
    ####### convert
    
    for i in pt.ProgressBar(range(len(files))):
    # for i in range(len(files)):
        f = files[i]
        if f.split('/')[-1][0:2] == '._':
            f=f.replace('._',"")
        img_bgr = cv2.imread(f)
        # img_hsv = cv2.cuda_GpuMat()
        # img_hsv.upload(img_bgr)
        img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
        # plt.subplot(1, 2, 1)
        # plt.title('source')
        # plt.imshow(img_bgr[:,:,::-1])

        temp = img_hsv.copy()
        if channel == "sv":
            img_hsv[:,:,1] = match_histograms(temp[:,:,1], result_s)
            img_hsv[:,:,2] = match_histograms(temp[:,:,2], result_v)
        elif channel == 'h':
            img_hsv[:,:,0] = match_histograms(temp[:,:,0], result_h)
        
        # print(os.path.join('./histo_matched',f.split('/')[-1]))
        img_rgb = cv2.cvtColor(img_hsv, cv2.COLOR_HSV2RGB)
        # plt.subplot(1, 2, 2)
        # plt.title('matched')
        # plt.imshow(img_rgb)
        # plt.savefig(os.path.join('/home/vcl/Desktop/min/minho/MetaBIN/datasets/TOCELEB-toceleb/histo_matched_refer',f.split('/')[-1]))
        plt.imsave(os.path.join(f'/home/vcl/Desktop/min/minho/MetaBIN/datasets/TOCELEB-tolast/query_h',f.split('/')[-1]), img_rgb)

histo_match(celeb_files,market_files, channel = 'h', num = 10000)

