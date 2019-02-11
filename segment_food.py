# -*- coding: utf-8 -*-

from sklearn.cluster import KMeans
import numpy as np
from skimage.morphology import disk
from skimage.filters.rank import median

def segment_food (img_rgbb, food):
    
    img_rgb = img_rgbb * 1.0
    for k in range(0,3):
        img_rgb[:,:,k] = median(img_rgbb[:,:,k], disk(3)) / 255
           
    sum = 0;
    for i in range(0, food.shape[0]):
        for j in range(0, food.shape[1]):
            if (food[i][j] == 1):
                sum = sum+1
    
    data = np.zeros((sum,5))
    idx = 0
    for i in range(0, food.shape[0]):
        for j in range(0, food.shape[1]):
            if (food[i][j] == 1):
                data[idx][0] = i * 2
                data[idx][1] = j
                data[idx][2] = img_rgb[i][j][0] * 50
                data[idx][3] = img_rgb[i][j][1] * 50
                data[idx][4] = img_rgb[i][j][2] * 50
                idx = idx + 1
    # print(data)
    kmeans = KMeans(n_clusters=2, random_state=0).fit(data)
    
    labels = food * 0 
    centers = kmeans.cluster_centers_
    l = [0, 1]
    if centers[0][0] > centers[1][0] :
        l = [1, 0]
    # print(centers)
    for i in range(0, kmeans.labels_.shape[0]):
        x = data[i][0]//2
        y = data[i][1]
        la = kmeans.labels_[i]
        # print(x, y, la)
        labels[int(x)][int(y)]= (l[la]+1)*0.5
    
    labels2 = median(labels, disk(3))
    
    return labels, labels2


def get_height_and_area(labels):      
    area = 0
    for i in range(labels.shape[0]):
        for j in range(labels.shape[1]):
            if (0 < labels[i][j] and labels[i][j] <= 128):
                area = area+1
    
    heights = []
    for j in range(labels.shape[1]):
        a = 0
        for i in range(labels.shape[0]):
            if (labels[i][j] > 128):
                a = a+1
        if a != 0:
            heights.append(a)
    
    idx1 = int(len(heights)*0.2)
    idx2 = int(len(heights)*0.8)
    height = sum(heights[idx1: idx2]) / (idx2 - idx1)
    
    return area, height