import math
class Ride(object):
    def __init__(self, startR , startC,finishR,finishC, earliestStart,latestFinish):
        self.startR = startR
        self.startC = startC
        self.finishR = finishR
        self.finishC = finishC
        self.earliestStart = earliestStart
        self.latestFinish = latestFinish

class Car(object):
    def __init__(self, id,row=None,col=None):
        self.id = id
        self.row = row
        self.col = col
        self.actions = []
        self.moving = 0
        self.actualAction = 0
        self.rewardToTake = False
        self.eventualReward = 0
        self.startRide = 0
    def setRoute(self,listOfdestinations):
        self.actions = listOfdestinations
    def estimateTime(self,destRow,destCol):
        height = math.fabs(destRow-self.row)
        width = math.fabs(destCol-self.col)
        # print("distance "+str(height+width))
        return height + width
    def takeAction(self):
        self.moving = self.moving - 1
        if self.moving<=0:
            if self.rewardToTake:
                table.addScore(self.actions[self.actualAction],self.startRide,self.eventualReward)
                self.rewardToTake = False
                self.eventualReward = 0
                self.actualAction = self.actualAction + 1

            if self.actualAction < len(self.actions):

                ride = Rides[self.actions[self.actualAction]]
                if (self.row==ride.startR)&(self.col==ride.startC):
                    if table.time>=ride.earliestStart:
                        self.moving = self.estimateTime(ride.finishR,ride.finishC)
                        self.eventualReward = self.estimateTime(ride.finishR,ride.finishC)
                        self.startRide = table.time
                        self.row = ride.finishR
                        self.col = ride.finishC
                        self.rewardToTake = True
                    else:
                        self.moving = ride.earliestStart - table.time
                else:
                    self.moving = self.estimateTime(ride.startR, ride.startC)
                    self.row = ride.startR
                    self.col = ride.startC

class Ticker(object):
    def __init__(self):
        self.T = 0
        self.score = 0
        self.time = 0
    def setT(self, T):
        self.T = T
    def next(self):
        self.time = self.time +1
    def addScore(self,rideId,startTime,timeToTravel):
        ride = Rides[rideId]
        bonus = 0
        if ride.earliestStart==startTime:
            bonus = B
        if startTime+timeToTravel<=ride.latestFinish:
            self.score = self.score + bonus + timeToTravel
    def getScore(self):
        return self.score

class Manager(object):
    def __init__(self,T):
        self.T = T
    def start(self):
        for x in range(self.T):
            global R, C, F, Cars, N, B, T, Rides
            print("turn: ", x)
            for car in Cars:
                car.takeAction()
            table.next()

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
            global R,C,F,Cars,N,B,T,Rides
            R = int(nLine[0])
            C = int(nLine[1])
            F = int(nLine[2])
            global Cars
            Cars = []
            for i in range(F):
                car = Car(i,0,0)
                Cars.append(car)
            N = int(nLine[3])
            B = int(nLine[4])
            T = int(nLine[5])
            global Rides
            Rides = []
            for x in range(N):
                line = line + 1
                nLine = content[line].split(" ")
                rid = Ride(int(nLine[0]),int(nLine[1]),int(nLine[2]),int(nLine[3]),int(nLine[4]),int(nLine[5]))
                Rides.append(rid)
        with open(submissionF) as f:
            content = f.readlines()
            line = 0
            for i in range(F):
                nLine = content[line].split(" ")
                numRides = int(nLine[0])
                ridesToAdd = []
                for rideCar in range(1,numRides+1):
                    ridesToAdd.append(int(nLine[rideCar]))
                Cars[i].setRoute(ridesToAdd)
                line = line + 1
            manager = Manager(T)
            manager.start()
            self.score = table.getScore()

j = JudgeSystem("input_example", "submission_example")
print("Score: ", j.score)