from helper import helper as hl
from random import randrange
import random


class AIClass:
    def __init__(self):
        self.state = [hl.States.WATER] * 100
        self.ships = [[2, 1], [2,2]] #, [3,3], [2,4], [1,5]]
        self.lastShot=None
        self.myShots=[]
        self.possibleShots=list(range(0,100))
        random.shuffle(self.possibleShots)
        #print(self.possibleShots)
        self.nextSetepGenerator=self.calculateNextStep()
        self.replyFromServer=hl.States.MISSED
        self.myShotsReplies=[]
        self.possibleDeleteindicesHorizontal=[]
        self.possibleDeleteindicesVertical=[]
        self.sinkremove=[]
        self.memo=None
        self.myShips = [[0], [15], [26, 27], [45, 55]]
        self.initShips()

    def nextStep(self,replyfromserver=hl.States.MISSED):
        self.replyFromServer=replyfromserver
        return next(self.nextSetepGenerator)
    def initShips(self):
        self.myShips=[]
        possiblePositions= [i for i in range(100)]
        sizes=[5,4,4,3,3,3,2,2,1,1]
        for i in range(10):
            pos_good=False
            pos=None
            good_dirs=[]
            while not pos_good:
                pos = random.randint(0, 99)
                print(pos)
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
                print(need_to_be_deleted,pos)
                for j in need_to_be_deleted:
                    if j in possiblePositions:
                        possiblePositions.remove(j)
                print(possiblePositions)
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

        print(self.myShips)








        # minden hajó egy list ebben a list-ben, a hajo altal felvett koordinatakat tartalmazza

    def calculateNextStep(self):
        nextstep = self.possibleShots[0]
        self.possibleShots.remove(self.possibleShots[0])
      #  print(self.possibleShots)
        self.myShots.append(nextstep)
        print("LOVES",nextstep)
        #print(self.possibleShots)
        yield nextstep
        while True:

            self.myShotsReplies.append(self.replyFromServer)
            if self.replyFromServer==hl.States.MISSED:
                print(self.myShots[-1], "NEM TALÁLT")
                nextstep= None
                if self.memo is None:
                    nextstep=self.possibleShots[0]
                    self.possibleShots.remove(self.possibleShots[0])
                else:
                    nextstep=self.memo
                    self.possibleShots.remove(self.memo)
                    self.memo=None

                print("LOVES",nextstep)
                #print(self.possibleShots)
                self.myShots.append(nextstep)
                yield nextstep
            elif self.replyFromServer==hl.States.HIT:
                print(self.myShots[-1], "TALÁLT")
             #   print(len(self.myShots))
                if len(self.myShotsReplies)>=2 and self.myShotsReplies[-2]==hl.States.HIT:
                    if self.myShotsReplies[-2]!=hl.States.HIT:
                        self.memo=self.possibleShots[0]

                    print("EDDIGI LOVESEK",self.myShots[-1], self.myShots[-2])
                    #print(len(self.myShotsReplies), self.myShotsReplies[-2])
                    if self.myShots[-1] in self.possibleDeleteindicesVertical:
                        for i in self.possibleDeleteindicesHorizontal:
                            print("remove",i)
                            self.possibleShots.remove(i)
                    else:
                        for i in self.possibleDeleteindicesVertical:
                            print("remove", i)
                            self.possibleShots.remove(i)

                preferred_indeces= hl.getPossibleShipPositions(self.myShots[-1])
                for i in preferred_indeces:
                    self.sinkremove.append(i)
                random.shuffle(preferred_indeces)



                print(preferred_indeces)
                #print(self.possibleShots)
                need_to_be_deleted=[]
                for i in range (len(preferred_indeces)):#change positions
                    Need= True
                    if preferred_indeces[i] in self.possibleShots:
                        if len(self.myShotsReplies) >= 2 and self.myShotsReplies[-2] == hl.States.HIT:
                            #print(self.myShots[-1],self.myShots[-2])
                            print(
                                "elozo loves " + str(self.myShots[-1]) + " vizsgalt elem " + str(preferred_indeces[i]))
                            if abs(self.myShots[-1]-self.myShots[-2])>=10:
                                if abs(preferred_indeces[i] - self.myShots[-1]) < 10:
                                    print("ez most horizontalis szomszéd ezért torlom.", preferred_indeces[i])
                                    need_to_be_deleted.append(preferred_indeces[i])
                                 #   preferred_indeces.remove(preferred_indeces[i])
                                    continue
                            else:
                                if abs(preferred_indeces[i] - self.myShots[-1]) >= 10:
                                    print("ez most vertikalis szomszéd ezért torlom.", preferred_indeces[i])
                                    need_to_be_deleted.append(preferred_indeces[i])
                                  #  preferred_indeces.remove(preferred_indeces[i])
                                    continue








                for i in need_to_be_deleted:
                    preferred_indeces.remove(i)
                    print("remove",i)
                    self.possibleShots.remove(i)
                #ha lenne emlékben valami fontos:
               # mem = self.possibleShots[0]
                #self.possibleShots[0] = self.possibleShots[1]
                #self.possibleShots[1] = mem

                for i in range(len(preferred_indeces)):
                    if preferred_indeces[i] in self.possibleShots:
                        #tmpind = self.possibleShots.index(preferred_indeces[i])
                        tmp = self.possibleShots[i]
                        self.possibleShots.remove(preferred_indeces[i])


                        self.possibleShots[i] = preferred_indeces[i]
                        self.possibleShots.append(tmp)

                nextstep = self.possibleShots[0]
                #print(self.possibleShots)
                self.possibleShots.remove(self.possibleShots[0])#amit lövök azt kiveszem

                print("LOVES",nextstep)
                #print(self.possibleShots)
                print(self.myShots[-1],nextstep)
                self.possibleDeleteindicesVertical.clear()
                self.possibleDeleteindicesHorizontal.clear()
                for i in range(len(preferred_indeces)):  # change positions
                    if abs(preferred_indeces[i] - self.myShots[-1]) >= 10:
                        self.possibleDeleteindicesHorizontal.append(preferred_indeces[i])
                    else:
                        self.possibleDeleteindicesVertical.append(preferred_indeces[i])

                print(self.possibleDeleteindicesVertical,self.possibleDeleteindicesHorizontal)
                self.myShots.append(nextstep)
                yield nextstep





            elif self.replyFromServer==hl.States.SINK:
                print(self.myShots[-1], "SINK")
                preferred_indeces = hl.getPossibleShipPositions(self.myShots[-1])
                for i in preferred_indeces:
                    if i in self.possibleShots:
                        print("torlom",i)
                        self.possibleShots.remove(i)
                for i in self.sinkremove:
                    if i in self.possibleShots:
                        print("torlom",i)
                        self.possibleShots.remove(i)
                nextstep = self.possibleShots[0]
                print(self.possibleShots)
                self.possibleShots.remove(self.possibleShots[0])  # amit lövök azt kiveszem
                print("LOVES", nextstep)
                yield nextstep

    def placeShips(self):
        return self.myShips




ai =AIClass()
ai.initShips()

# a = AIClass()
# print("nulladik")
# a.nextStep()
# print("ELSő")
# a.nextStep(hl.States.MISSED)
# print("masodik")
# a.nextStep(hl.States.HIT)
# print("harmadik")
# a.nextStep(hl.States.HIT)
# print("negyedik")
# a.nextStep(hl.States.MISSED)
# print("otodik")
# a.nextStep(hl.States.HIT)
# print("hatodik")
# a.nextStep(hl.States.SINK)
# print("hetedik")
# a.nextStep(hl.States.MISSED)
# print("nyolcadik")
# a.nextStep(hl.States.MISSED)





