from collections import deque
import math

class Drone(object):
    def __init__(self, id,row=None,col=None):
        self.id = id
        self.row = row
        self.col = col
        self.actions = deque()
        self.flying = 0
        self.payload = []
        self.NumOfActions = 0
    def initializeNumOfActions(self):
        self.NumOfActions = len(self.actions)
    def initializePayload(self,P):
        self.payload = [0]*P
    def addAction(self,action):
        self.NumOfActions = self.NumOfActions + 1
        self.actions.appendleft(action)
    def getNextActionType(self):
        return self.actions[len(self.actions) - 1].command
    def act(self,Grid,Warehouses,Orders):
        action = self.actions.pop()
        if(action.command=='L'):
            row,col = Warehouses[action.param1].getLoc()
            if (self.checkPosition(action,row,col)):
                for ware in Grid[row][col]:
                    if ware.id==action.param1 :
                        if ware.availability[action.param2]>=action.param3:
                            ware.availability[action.param2] = ware.availability[action.param2] - action.param3
                            self.payload[action.param2] = self.payload[action.param2] + action.param3
                self.NumOfActions = self.NumOfActions - 1
        elif(action.command=='U'):
            row,col = Warehouses[action.param1].getLoc()
            if (self.checkPosition(action,row,col)):
                for ware in Grid[row][col]:
                    if ware.id==action.param1 :
                        if self.payload[action.param2]>=action.param3:
                            ware.availability[action.param2] = ware.availability[action.param2] + action.param3
                            self.payload[action.param2] = self.payload[action.param2] - action.param3
                self.NumOfActions = self.NumOfActions - 1
        elif(action.command=='D'):
            row, col = Orders[action.param1].getLoc()
            if (self.checkPosition(action, row, col)):
                for ord in Grid[row][col]:
                    if ord.id == action.param1:
                        if (ord.completed!=True):
                            if self.payload[action.param2] >= action.param3:
                                ord.itemsbytype[action.param2] = ord.itemsbytype[action.param2] - action.param3
                                self.payload[action.param2] = self.payload[action.param2] - action.param3
                                ord.updateCompleted()

                self.NumOfActions = self.NumOfActions - 1
        else:
            self.flying = action.param1
        return Grid,Warehouses,Orders
    def checkPosition(self,action,row,col):
        if(self.row == row)&(self.col == col):
            return True
        else:
            rounds = math.ceil(math.sqrt(math.pow(math.fabs(self.row - row),2)+math.pow(math.fabs(self.col - col),2)))
            self.flying = rounds
            self.actions.append(action)
            self.row = row
            self.col = col
            return False
    def isBusy(self):
        if(self.flying>0):
            self.flying = self.flying - 1
        return self.flying

class Action(object):
    def __init__(self, id, command, param1, param2=None, param3=None):
        self.id = id
        self.command = command
        self.param1 = param1
        self.param2 = param2
        self.param3 = param3

class Warehouse(object):
    def __init__(self, id,row,col):
        self.id = id
        self.row = row
        self.col = col
        self.availability = []
    def setAval(self, intlist):
        self.availability = intlist
    def getAval(self):
        return self.availability
    def getLoc(self):
        return self.row,self.col

class Order(object):
    def __init__(self, id,row,col):
        self.id = id
        self.row = row
        self.col = col
        self.itemsbytype = []
        self.completed = False
    def setLi(self, Li):
        self.Li = Li
    def setItemsbytypes(self,itemsByType):
        self.itemsbytype = itemsByType
    def getItemsbytype(self):
        return self.itemsbytype
    def getLoc(self):
        return self.row,self.col
    def updateCompleted(self):
        tempCompleted = True
        for x in self.itemsbytype:
            if x>0:
                tempCompleted = False
        self.completed = tempCompleted
        if(self.completed):
            global table
            table.addScore()

class Manager(object):
    def __init__(self,T):
        self.T = T
    def start(self, Drones,Grid,Warehouses,Orders):
        for x in range(self.T):
            DronesNotU = []
            for drone in Drones:
                if(drone.NumOfActions>0):
                    if (drone.isBusy() == False):
                        if (drone.getNextActionType()=="U"):
                            Grid, Warehouses, Orders = drone.act(Grid,Warehouses,Orders)
                        else:
                            DronesNotU.append(drone.id)
            for y in range(len(Drones)):
                if (Drones[y].id in DronesNotU):
                    Grid, Warehouses, Orders = Drones[y].act(Grid,Warehouses,Orders)
            global table
            table.next()

class Score(object):
    def __init__(self):
        self.T = 0
        self.score = 0
        self.time = 0
    def setT(self, T):
        self.T = T
    def next(self):
        self.time = self.time +1
    def addScore(self):
        partialScore = (self.T - self.time) * 100 / self.T
        self.score = self.score +partialScore
    def getScore(self):
        return self.score

class JudgeSystem(object):
    def __init__(self, inputF, submissionF):
        global table
        table = Score()
        self.score(inputF, submissionF)
    def score(self, inputF, submissionF):
        with open(inputF) as f:
            content = f.readlines()
            nLine = content[0].split(" ")
            NoR = int(nLine[0])
            NoC = int(nLine[1])
            D = int(nLine[2])
            Drones = []
            for x in range(D):
                drone = Drone(x)
                Drones.append(drone)
            DoS = int(nLine[3])
            global table
            table.setT(DoS)
            MloD = int(nLine[4])
            P = int(content[1])
            productsWeights = content[2].split(" ")
            W = int(content[3])
            line = 4
            Warehouses = []
            Grid = [[[] for x in range(NoC)] for y in range(NoR)]
            for x in range(W):
                nLine = content[line].split(" ")
                ware = Warehouse(x, int(nLine[0]), int(nLine[1]))
                rowWare = int(nLine[0])
                colWare = int(nLine[1])
                if (x == 0):
                    for y in range(len(Drones)):
                        Drones[y] = Drone(y, int(nLine[0]), int(nLine[1]))
                line = line + 1
                nLine = content[line].split(" ")
                intlist = []
                for st in nLine:
                    intlist.append(int(st))
                ware.setAval(intlist)
                Warehouses.append(ware)
                list = Grid[rowWare][colWare]
                list.append(ware)
                Grid[rowWare][colWare] = list
                line = line + 1
            x = 0
            C = int(content[line])
            line = line + 1
            Orders = []
            for x in range(C):
                nLine = content[line].split(" ")
                ord = Order(x, int(nLine[0]), int(nLine[1]))
                rowOrd = int(nLine[0])
                colOrd = int(nLine[1])
                line = line + 1
                Li = int(content[line])
                ord.setLi(Li)
                line = line + 1
                nLine = content[line].split(" ")
                intlist = []
                for st in nLine:
                    intlist.append(int(st))
                intemsByType = [0] * P
                for item in intlist:
                    intemsByType[item] = intemsByType[item] + 1
                ord.setItemsbytypes(intemsByType)
                Orders.append(ord)
                list = Grid[rowOrd][colOrd]
                list.append(ord)
                Grid[rowOrd][colOrd] = list
                line = line + 1
        with open(submissionF) as f:
            content = f.readlines()
            line = 0
            Q = int(content[line])
            line = line + 1
            for x in range(Q):
                nLine = content[line].split(" ")
                if (len(nLine) > 3):
                    action = Action(int(nLine[0]), nLine[1], int(nLine[2]), int(nLine[3]), int(nLine[4]))
                else:
                    action = Action(int(nLine[0]), nLine[1], int(nLine[2]))
                drone = Drones[int(nLine[0])]
                drone.addAction(action)
                Drones[int(nLine[0])] = drone
                line = line + 1
        for drone in Drones:
            drone.initializePayload(P)
        manager = Manager(DoS)
        manager.start(Drones, Grid, Warehouses, Orders)
        self.score = table.score

listResults =[]
listResults.append(JudgeSystem("input_example", "submission_example").score)
print("Score: ",sum(listResults))




