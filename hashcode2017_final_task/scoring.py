import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

input_src = "input_example"
submission_src = "submission_example"

def writeCovered():
    for rowNumber in range(H):
        for colNumber in range(W):
            if(Routers[rowNumber][colNumber]==1):
                manageRouter(rowNumber,colNumber)
def manageRouter(rowNumber,colNumber):
    minCol = colNumber - R
    maxCol = colNumber + R +1
    minRow = rowNumber -R
    maxRow = rowNumber + R +1
    for row in range(minRow,maxRow):
        for col in range(minCol,maxCol):
            if(checkArea(rowNumber,colNumber,row,col)):
                CoveredCells[row][col] = 1


def checkArea(rowNumber,colNumber,row,col):
    if(
            (row<0)|(row>=H)|(col<0)|(col>=W)
    ):
        return False
    else:
        if((Grid[row][col]=='#')|(Grid[row][col]=='-')):
            return False
        else:
            value = True
            minRow = min([rowNumber,row])
            maxRow = max([rowNumber, row])
            minCol = min([colNumber, col])
            maxCol = max([colNumber, col])
            for nrow in range(minRow,maxRow):
                for ncol in range(minCol,maxCol):
                    if (Grid[row][col] == '#'):
                        value = False
            return value

with open(input_src) as f:
    content = f.readlines()
    firstLine = content[0].split(" ")
    H = int(firstLine[0])
    W = int(firstLine[1])
    R = int(firstLine[2])
    firstLine = content[1].split(" ")
    Pb = int(firstLine[0])
    Pr = int(firstLine[1])
    B = int(firstLine[2])
    firstLine = content[2].split(" ")
    Br = int(firstLine[0])
    Bc = int(firstLine[0])
    line=3
    Grid = [[0 for x in range(W)] for y in range(H)]
    for rowNumber in range(H):
        row = list(content[line])
        for colNumber in range(W):
            Grid[rowNumber][colNumber] = row[colNumber]
        line=line+1

with open(submission_src) as f:
    content = f.readlines()
    line = 0
    N = int(content[line])
    line = line + 1
    BackboneCells = [[0 for x in range(W)] for y in range(H)]
    for i in range(N):
        cellRC = content[line].split(" ")
        BackboneCells[int(cellRC[0])][int(cellRC[1])] = 1
        line = line + 1
    M = int(content[line])
    line = line + 1
    Routers = [[0 for x in range(W)] for y in range(H)]
    for i in range(M):
        cellR = content[line].split(" ")
        Routers[int(cellR[0])][int(cellR[1])] = 1
        line = line + 1
    CoveredCells = [[0 for x in range(W)] for y in range(H)]
    writeCovered()
    t= sum(sum(CoveredCells, []))
    score = 1000*t+(B-(N*Pb+M*Pr))
    print("Score: ",score)
