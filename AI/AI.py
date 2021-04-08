from helper import helper as hl
from random import randrange
import random


class AIClass:
    def __init__(self):
        self.lastShot=None
        self.myShots=[]
        self.possibleShots=list(range(0,100))
        random.shuffle(self.possibleShots)
        #print(self.possibleShots)
        self.nextStepGenerator=self.calculateNextStep()
        self.nextStepGeneratorRandom = self.calculateNextStepRandom()
        self.replyFromServer=hl.States.MISSED
        self.myShotsReplies=[]
        self.possibleDeleteindicesHorizontal=[]
        self.possibleDeleteindicesVertical=[]
        self.sinkremove=[]
        self.memo=None
        self.myShips = None #= [[0], [15], [26, 27], [45, 55]]
        #self.initShips()

    def nextStep(self,replyfromserver=hl.States.MISSED):
        self.replyFromServer=replyfromserver
        return next(self.nextStepGenerator)

    def initShips(self):
        self.myShips=[]
        possiblePositions= [i for i in range(100)]
        sizes = [5, 2, 1, 1]  # sizes=[5,4,4,3,3,3,2,2,1,1]
        for i in range(len(sizes)):
            pos_good=False
            pos=None
            good_dirs=[]
            while not pos_good:
                pos = random.randint(0, 99)
                #print(pos)
                for size in range(sizes[i]):
                    if pos+size not in possiblePositions :
                        break
                    else:
                        if size==sizes[i]-1:
                            good_dirs.append(1)
                            pos_good=True
                for size in range(sizes[i]):
                    if pos-size not in possiblePositions :
                        break
                    else:
                        if size==sizes[i]-1:
                            good_dirs.append(-1)
                            pos_good=True
                for size in range(sizes[i]):
                    if pos+(size*10) not in possiblePositions :
                        break
                    else:
                        if size==sizes[i]-1:
                            good_dirs.append(10)
                            pos_good=True
                for size in range(sizes[i]):
                    if pos-(size*10) not in possiblePositions :
                        break
                    else:
                        if size==sizes[i]-1:
                            good_dirs.append(-10)
                            pos_good=True

            if sizes[i]==111:
                need_to_be_deleted= hl.getNeighbours(pos)
                #print(need_to_be_deleted,pos)
                for j in need_to_be_deleted:
                    if j in possiblePositions:
                        possiblePositions.remove(j)
                #print(possiblePositions)
                nextship=[pos]
                self.myShips.append(nextship)
            else:
                nextship=[pos]
                random.shuffle(good_dirs)
                for h in range(1,sizes[i]):
                    nextship.append(pos+good_dirs[0]*h)
                for coord in nextship:
                    need_to_be_deleted=hl.getNeighbours(coord)
                    for d in need_to_be_deleted:
                        if d in possiblePositions:
                            possiblePositions.remove(d)
                self.myShips.append(nextship)

        #print(self.myShips)
        return self.myShips








        # minden hajó egy list ebben a list-ben, a hajo altal felvett koordinatakat tartalmazza

    def calculateNextStepRandom(self):
        for i in self.possibleShots:
            yield i
    def calculateNextStep(self):
        nextstep = self.possibleShots[0]
        self.possibleShots.remove(self.possibleShots[0])
        self.myShots.append(nextstep)
        print("LOVES",nextstep)
        yield nextstep
        while True:
            skip=False
            self.myShotsReplies.append(self.replyFromServer)
            prev_hits=[]
            for i in range(1,len(self.myShots)+1):#fontos emléket keresve
                #print(self.myShots[-i], self.myShotsReplies[-i])
                if self.myShotsReplies[-i]==hl.States.HIT:
                    prev_hits.append(self.myShots[-i])
                if self.myShotsReplies[-i]==hl.States.SINK:
                    break
            if len(prev_hits)>=2:
                print("HOPHOP")
                bigger=max(prev_hits)
                smaller=min(prev_hits)
                difference_between_two_hits=bigger-smaller
                print(bigger, smaller)
                print(difference_between_two_hits)
                if difference_between_two_hits<10:
                    self.memo ={bigger:bigger+1,
                                smaller:smaller-1
                   }
                else:
                    self.memo = {bigger: bigger + 10,
                                 smaller: smaller - 10
                                 }
                print("MEMO MOST",self.memo)
                for key,i in self.memo.items():
                    print("keresem, hogy ez jó",i)
                    print("i in poss",i in self.possibleShots)
                    print("i in possibleship", i in hl.getPossibleShipPositions(key))
                    if i in self.possibleShots and i in hl.getPossibleShipPositions(key):
                        self.possibleShots.remove(i)
                        print("FURA LOVEs",i)
                        self.myShots.append(i)
                        nextstep=i
                        skip=True
                        break
            if skip:
                print("okosan ez lett",nextstep)
                yield nextstep

            else:
                if self.replyFromServer==hl.States.MISSED:
                    print(self.myShots[-1], "NEM TALÁLT")
                    nextstep=self.possibleShots[0]
                    self.possibleShots.remove(self.possibleShots[0])
                    print("LOVES",nextstep)
                    self.myShots.append(nextstep)
                    yield nextstep
                elif self.replyFromServer==hl.States.HIT:
                    print(self.myShots[-1], "TALÁLT")
                    preferred_indeces= hl.getPossibleShipPositions(self.myShots[-1])
                    random.shuffle(preferred_indeces)
                    print(self.possibleShots)
                    delete=[]
                    for i in preferred_indeces:
                        if i not in self.possibleShots:
                            delete.append(i)
                        else:
                            self.possibleShots.remove(i)

                    for i in delete:
                        preferred_indeces.remove(i)
                    print(preferred_indeces)
                    self.possibleShots=preferred_indeces+self.possibleShots
                    # for i in range(len(preferred_indeces)):
                    #     if preferred_indeces[i] in self.possibleShots:
                    #         tmp = self.possibleShots[i]
                    #         self.possibleShots.remove(preferred_indeces[i])
                    #         self.possibleShots[i] = preferred_indeces[i]
                    #         self.possibleShots.append(tmp)
                    print(self.possibleShots)
                    nextstep = self.possibleShots[0]
                    self.possibleShots.remove(self.possibleShots[0])#amit lövök azt kiveszem
                    print("LOVES",nextstep)
                    self.myShots.append(nextstep)
                    yield nextstep

                elif self.replyFromServer==hl.States.SINK:

                    print(self.myShots[-1], "SINK")
                    need_to_be_deleted=[]
                    need_to_be_deleted.append(self.myShots[-1])
                    for i in range(2, len(self.myShots) + 1):  # fontos emléket keresve
                        print(self.myShots[-i], self.myShotsReplies[-i])
                        if self.myShotsReplies[-i] == hl.States.HIT:
                            need_to_be_deleted.append(self.myShots[-i])
                        if self.myShotsReplies[-i] == hl.States.SINK:
                            break
                    print("HOPHOPppppsink")
                    for i in need_to_be_deleted:
                        for d in hl.getNeighbours(i):
                            if d in self.possibleShots:
                                print("törlöm",d)
                                self.possibleShots.remove(d)

                    nextstep=self.possibleShots[0]
                    self.possibleShots.remove(nextstep)
                    print("SINK LOVES", nextstep)
                    self.myShots.append(nextstep)
                    yield nextstep


    def placeShips(self):
        return self.myShips








