import numpy as np
import pandas as pd
import os
import random
import shutil

def iterateTextfile(path, savepath, datasetSize):


    file = open(path, 'r')
    lines = file.readlines()

    px_x = 1600
    px_y = 900
    px_bb = 160
    bb_w = px_bb / px_x
    bb_h = px_bb / px_y

    labels = ['FracturePlate_1x_MedScrewCut1', 'FracturePlate_1x_MedScrewCut2', 'FracturePlate_1x_LatScrewCut1', 'FracturePlate_1x_LatScrewCut2']
    added = set()


    for line in lines[1:]:
        tokens = line.split()
        labelstr = tokens[-1]
        label = -1
        for i in range(len(labels)):
            if labels[i] == labelstr:
                label = str(i//2)
                break
        index_str = tokens[0]
        index = int(index_str[:-1])
        added.add(index)
        posx = float(tokens[1][1:-1])
        posy = float(tokens[2][:-1])
        posx = (posx + 8) / 16
        posy = (posy + 4.5) / 9
        posy = 1 - posy
        scale = tokens[-2][:-1]
        bb_wi = str(float(scale) * bb_w)
        bb_hi = str(float(scale) * bb_h)

        printline = str(label) + " " + str(posx) + " " + str(posy) + " " + bb_wi + " " + bb_hi + "\n"
        f = open(savepath + "Data Point "+ str(index) + ".txt", "a")
        #f.truncate()
        f.write(printline)
        f.close()
    
    for i in range(datasetSize):
        if i not in added:
            f = open(savepath + "Data Point "+ str(i) + ".txt", "w")
            f.close()


def trainTestSplit(stablepath, targetpath, datasetSize, ratio = 0.85):
    noTrain = int(datasetSize * ratio)
    noVal = datasetSize - noTrain
    valIndex = set(random.sample(range(0, 5000), noVal))
    targetTrainImg = targetpath + "images/train/"
    targetValImg = targetpath + "images/val/"
    targetTrainLabel = targetpath + "labels/train/"
    targetValLabel = targetpath + "labels/val/"
    for i in range(5000):
        pathImg = "Data Point " + str(i) +".png"
        pathTxt = "Data Point " + str(i) +".txt"
        if i in valIndex:
            shutil.copyfile(stablepath + pathImg, targetValImg + pathImg)
            shutil.copyfile(stablepath + pathTxt, targetValLabel + pathTxt)
        else:
            shutil.copyfile(stablepath + pathImg, targetTrainImg + pathImg)
            shutil.copyfile(stablepath + pathTxt, targetTrainLabel + pathTxt)
    return
        

textpath = 'imagefile.txt'
stablepath = './DataPointsStable.nosync/'
targetpath = './DataPoints.nosync/'
datasetSize = 5000

#iterateTextfile(textpath, stablepath, datasetSize)
trainTestSplit(stablepath, targetpath, datasetSize, 0.85)

#print(os.listdir(folderpath))

