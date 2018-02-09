import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
class Endpoint(object):
    def __init__(self, Ld,K):
        self.Ld = int(Ld)
        self.K = K
        self.cs = []
        self.Lcs = []
    def add_c(self, c, Lc):
        self.cs.append(int(c))
        self.Lcs.append(int(Lc))
    def getLcFromC(self,C):
        return self.Lcs[self.cs.index(C)]
    def getCs(self):
        return self.cs
    def getLd(self):
        return self.Ld

class Request(object):
    def __init__(self, Rv,Re,Rn):
        self.Rv = int(Rv)
        self.Re = int(Re)
        self.Rn = int(Rn)
    def getValues(self):
        return [self.Rv , self.Re , self.Rn]

class CacheServer(object):
    def __init__(self, id):
        self.id = id
        self.videos = []
    def addVideo(self,v):
        self.videos.append(int(v))
    def getId(self):
        return self.id
    def getValues(self):
        return self.videos

def score(inputF, submissionF):
    with open(inputF) as f:
        content = f.readlines()

    firstLine = content[0].split(" ")
    V = int(firstLine[0])
    E = int(firstLine[1])
    R = int(firstLine[2])
    C = int(firstLine[3])
    X = int(firstLine[4])
    S = content[1].split(" ")
    line = 2
    endPoints = []
    for endpoint in range(0, E):
        endPsummary = content[line].split(" ")
        endP = Endpoint(int(endPsummary[0]), int(endPsummary[1]))
        line = line + 1
        for x in range(0, int(endPsummary[1])):
            cacheS = content[line].split(" ")
            endP.add_c(cacheS[0], cacheS[1])
            line = line + 1
        endPoints.append(endP)
    requests = []
    for req in range(0, R):
        reqsummary = content[line].split(" ")
        request = Request(int(reqsummary[0]), int(reqsummary[1]), int(reqsummary[2]))
        requests.append(request)
        line = line + 1

    with open(submissionF) as f:
        content = f.readlines()
    N = int(content[0])
    cacheServers = []
    line = 1
    for x in range(0, N):
        cacheSsummary = content[line].split(" ")
        Cs = CacheServer(int(cacheSsummary[0]))
        cacheSsummary = cacheSsummary[1:]
        for y in cacheSsummary:
            Cs.addVideo(int(y))
        cacheServers.append(Cs)
        line = line + 1
    num = 0
    den = 0

    for each in requests:
        firstReq = each.getValues()
        firstVideo = int(firstReq[0])
        firstendpoint = endPoints[firstReq[1]]
        dataCenterLatency = firstendpoint.getLd()
        cacheWithVideo = []
        for cacheserver in cacheServers:
            if (firstVideo in cacheserver.getValues()):
                cacheWithVideo.append(cacheserver.getId())
        latencies = []
        latencies.append(dataCenterLatency)
        cachesEndpoint = firstendpoint.getCs()
        for cache in cachesEndpoint:
            if (cache in cacheWithVideo):
                latencies.append(firstendpoint.getLcFromC(cache))
        minlat = min(latencies)
        saved = dataCenterLatency - minlat
        den = den + int(firstReq[2])
        num = num + int(firstReq[2]) * saved

    total = int(1000 * num / den)
    return total

listResults =[]
listResults.append(score("input_example", "submission_example"))
print("Score: ",sum(listResults))




