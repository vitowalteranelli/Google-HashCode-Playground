class Lat(object):
    def passPoles(x):
        if ((x >= -324000) & (x <= 324000)):
            return 1
        else:
            return -1
    def or2or(x):
        if ((x >= -324000) & (x <= 324000)):
            return x
        elif  (x<-324000):
            return -324000-(x+324000)
        else:
            return 324000-(x-324000)
    def or2ind(x):
        if ((x>=-324000)&(x<=324000)):
            return  (324000+x)
        elif  (x<-324000):
            return -(324000 + x)
        else:
            return -x+3*324000
    def ind2or(x):
        if ((x>=0)&(x<=2*324000)):
            return  (-324000+x)
        elif  (x<0):
            return Lat.ind2or(-x)
        else:
            return -x+3*324000

class Lon(object):
    def or2or(x):
        if ((x>=-648000)&(x<=647999)):
            return x
        elif  (x<-648000):
            return (647999) + (x+648000 +1)
        else:
            return (x-648000 ) -648000
    def or2ind(x):
        if ((x>=-648000)&(x<=647999)):
            return  (648000+x)
        elif  (x<-648000):
            return (2*648000 - 1) - (-x-648000)
        else:
            return (x-648000 )
    def ind2or(x):
        if ((x>=0)&(x<=2*648000-1)):
            return  (-648000+x)
        elif  (x<0):
            return 648000 +x
        else:
            return x - (3*648000)

class Ticker(object):
    def __init__(self):
        self.T = 0
        self.score = 0
        self.time = 0
    def setT(self, T):
        self.T = T
    def next(self):
        self.time = self.time +1
    def addScore(self,val):
        # partialScore = (self.T - self.time) * 100 / self.T
        self.score = self.score +val
    def getScore(self):
        return self.score

class Image(object):
    def __init__(self,lat,lon):
        self.lat = lat
        self.lon = lon
class Range(object):
    def __init__(self,start,stop):
        self.start = start
        self.stop = stop

class Collection(object):
    def __init__(self,V,L,R):
        self.V = V
        self.L = L
        self.R = R
        self.images = []
        self.ranges = []
        self.completed = False
    def addImage(self,lat,lon):
        im = [lat,lon]
        self.images.append(im)
    def addRange(self, start, stop):
        ra = [start, stop]
        self.ranges.append(ra)
    def checkImageByTurn(self,lat,lon,turn):
        turnCheck = False
        for start,stop in self.ranges:
            if((turn>=start)&(turn<=stop)):
                turnCheck = True
        if(turnCheck):
            if([lat,lon]in self.images):
                self.images.remove([lat,lon])
        if not self.images:
            self.completed = True

class Satellite(object):
    def __init__(self,id,phi,lam,v,w,d):
        self.id = id
        self.phi = phi
        self.lam = lam
        self.v = v
        self.w = w
        self.d = d
        self.cam = Camera(self.w,self.d)
        self.cam.setPosition(self.phi,self.lam,self.phi,self.lam)
    def move(self):
        self.v = self.v * Lat.passPoles(self.phi+self.v)
        self.phi = Lat.or2or(self.phi+self.v)
        self.lam = Lon.or2or(self.lam - 15)
    def takePhoto(self,photoPhi,photoLam):
        self.cam.setPosition(self.phi, self.lam, photoPhi, photoLam)
    def playTurn1phase(self):
        self.cam.expandByW()
    def playTurn2phase(self):
        self.move()
    def getCamView(self):
        return self.cam.getLocations(self.phi,self.lam)


class Snaps(object):
    def __init__(self):
        self.NoP =0
        self.snapList = []
    def addSnap(self,snap):
        self.snapList.append(snap)
    def getSnapsByTurn(self,turn):
        temp = []
        for snap in self.snapList:
            if (snap[2]==turn):
                temp.append(snap)
        return temp

class Camera(object):
    def __init__(self,w,d):
        self.w = w
        self.d = d
        self.W = 2*self.d
        self.H = 2*self.d
        self.rectangle = [[0 for x in range(self.W)] for y in range(self.H)]
    def setPosition(self,phi,lam,photoPhi,photoLam):
        self.rectangle = [[0 for x in range(2 * self.d + 1)] for y in range(2 * self.d + 1)]
        self.rectangle[self.d+photoPhi-phi][self.d+photoLam-lam] = 1
    def setLocalPosition(self,row,col):
        self.rectangle = [[0 for x in range(2 * self.d + 1)] for y in range(2 * self.d + 1)]
        self.rectangle[row][col] = 1
    def expandByW_old(self):
        listToUpdate = []
        for rowNumber in range(self.H+1):
            for colNumber in range(self.W+1):
                if(self.rectangle[rowNumber][colNumber]==1):
                    listToUpdate.append([rowNumber,colNumber])
        for row,col in listToUpdate:
            minH = row-self.w
            if(minH<0): minH = 0
            maxH = row+self.w
            if(maxH>self.H): maxH=self.H
            minW = col - self.w
            if (minW < 0): minW = 0
            maxW = col + self.w
            if (maxW > self.W): maxW = self.W
            for rowNumber in range(minH,maxH+1):
                for colNumber in range(minW,maxW+1):
                    self.rectangle[rowNumber][colNumber] = 1
    def expandByW(self):
        rowsToUpdate = []
        colsToUpdate = []
        for rowNumber in range(self.H):
            for colNumber in range(self.W):
                if(self.rectangle[rowNumber][colNumber]==1):
                    rowsToUpdate.append(rowNumber)
                    colsToUpdate.append(colNumber)
        if rowsToUpdate:
            minH = min(rowsToUpdate) - self.w
            if (minH < 0): minH = 0
            maxH = max(rowsToUpdate) + self.w
            if (maxH > self.H): maxH = self.H
            minW = min(colsToUpdate) - self.w
            if (minW < 0): minW = 0
            maxW = max(colsToUpdate) + self.w
            if (maxW > self.W): maxW = self.W
            for rowNumber in range(minH, maxH+1):
                for colNumber in range(minW, maxW+1):
                    self.rectangle[rowNumber][colNumber] = 1

    def getLocations(self,phi,lam):
        listOfLocations = []
        for rowNumber in range(self.H):
            for colNumber in range(self.W):
                if (self.rectangle[rowNumber][colNumber] == 1):
                    deltaPhi = rowNumber - self.d
                    deltaLam = colNumber - self.d
                    listOfLocations.append([Lat.or2or(phi+deltaPhi),Lon.or2or(lam+deltaLam)])
        return listOfLocations

class Manager(object):
    def __init__(self,T):
        self.T = T
    def start(self,table,Satellites,Collections,SnapList):
        for x in range(self.T):
            remainingSnaps = SnapList.snapList
            if remainingSnaps:
                print("turn: ",x)
                remainingSats = []
                for snap in remainingSnaps:
                    remainingSats.append(snap[3])
                for sat in Satellites:
                    if sat.id in remainingSats:
                        sat.playTurn1phase()

                        snapsThisTurn = SnapList.getSnapsByTurn(x)
                        onlyOnePhotoPerTurn = True
                        for snap in snapsThisTurn:
                            if (snap[3] == sat.id):
                                if (onlyOnePhotoPerTurn):
                                    views = sat.getCamView()
                                    if ([snap[0], snap[1]] in views):
                                        sat.takePhoto(snap[0], snap[1])
                                        for collection in Collections:
                                            collection.checkImageByTurn(snap[0], snap[1], x)
                                        SnapList.snapList.remove(snap)
                        sat.playTurn2phase()

                table.next()

        for collection in Collections:
            if (collection.completed):
                table.addScore(collection.V)

class JudgeSystem(object):
    def __init__(self, inputF, submissionF):
        global table
        table = Ticker()
        self.score(inputF, submissionF)
    def score(self, inputF, submissionF):
        with open(inputF) as f:
            content = f.readlines()
            line = 0
            nLine = content[line].split(" ")
            T = int(nLine[0])
            line = line + 1
            nLine = content[line].split(" ")
            S = int(nLine[0])
            global Satellites
            Satellites = []
            for x in range(S):
                line = line + 1
                nLine = content[line].split(" ")
                sat = Satellite(x,int(nLine[0]),int(nLine[1]),int(nLine[2]),int(nLine[3]),int(nLine[4]))
                Satellites.append(sat)
            line = line + 1
            nLine = content[line].split(" ")
            C = int(nLine[0])
            global Collections
            Collections = []
            for x in range(C):
                line = line + 1
                nLine = content[line].split(" ")
                V = int(nLine[0])
                L = int(nLine[1])
                R = int(nLine[2])
                col = Collection(V,L,R)
                for y in range(L):
                    line = line + 1
                    nLine = content[line].split(" ")
                    col.addImage(int(nLine[0]),int(nLine[1]))
                for z in range(R):
                    line = line + 1
                    nLine = content[line].split(" ")
                    col.addRange(int(nLine[0]),int(nLine[1]))
                Collections.append(col)

        with open(submissionF) as f:
            content = f.readlines()
            line = 0
            nLine = content[line].split(" ")
            global SnapList
            SnapList = Snaps()
            SnapList.NoP = int(nLine[0])
            line = line + 1
            for i in range(SnapList.NoP):
                nLine = content[line].split(" ")
                lat = int(nLine[0])
                long = int(nLine[1])
                turn = int(nLine[2])
                id = int(nLine[3])
                SnapList.addSnap([lat,long,turn,id])
                line = line + 1

            manager = Manager(T)
            manager.start(table,Satellites,Collections,SnapList)
            self.score = table.getScore()

j = JudgeSystem("input_example", "submission_example")
print("Score: ", j.score)

