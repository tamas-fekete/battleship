from helper import helper as hl
from gameLogic.PlayerState import PlayerState
import random
import logging


class AIClass(PlayerState):
    def __init__(self):
        super().__init__(None, False)
        self.lastShot = None
        self.myShots = []
        self.possibleShots = list(range(0, 100))
        random.shuffle(self.possibleShots)
        # print(self.possibleShots)
        logging.debug(self.possibleShots)

        self.nextStepGenerator = self.calculateNextStep()
        self.nextStepGeneratorRandom = self.calculateNextStepRandom()
        self.replyFromServer = hl.States.MISSED
        self.myShotsReplies = []
        self.possibleDeleteindicesHorizontal = []
        self.possibleDeleteindicesVertical = []
        self.sinkremove = []
        self.memo = None
        self.myShips = None  # = [[0], [15], [26, 27], [45, 55]]
        # self.initShips()

    def nextStep(self, replyfromserver=hl.States.MISSED):
        self.replyFromServer = replyfromserver
        return next(self.nextStepGenerator)

        # minden hajó egy list ebben a list-ben, a hajo altal felvett koordinatakat tartalmazza

    def calculateNextStepRandom(self):
        for i in self.possibleShots:
            yield i

    def calculateNextStep(self):
        nextstep = self.possibleShots[0]
        self.possibleShots.remove(self.possibleShots[0])
        self.myShots.append(nextstep)
        # print("LOVES", nextstep)
        logging.info("LOVES " + str(nextstep))
        yield nextstep
        while True:
            skip = False
            self.myShotsReplies.append(self.replyFromServer)
            prev_hits = []
            for i in range(1, len(self.myShots) + 1):  # fontos emléket keresve
                # print(self.myShots[-i], self.myShotsReplies[-i])
                if self.myShotsReplies[-i] == hl.States.HIT:
                    prev_hits.append(self.myShots[-i])
                if self.myShotsReplies[-i] == hl.States.SINK:
                    break
            if len(prev_hits) >= 2:
                # print("HOPHOP")
                logging.debug("HOPHOP")
                bigger = max(prev_hits)
                smaller = min(prev_hits)
                difference_between_two_hits = bigger - smaller
                # print(bigger, smaller)
                # print(difference_between_two_hits)
                logging.debug(str(bigger) + " " + str(smaller))
                logging.debug(str(difference_between_two_hits))
                if difference_between_two_hits < 10:
                    self.memo = {bigger: bigger + 1,
                                 smaller: smaller - 1
                                 }
                else:
                    self.memo = {bigger: bigger + 10,
                                 smaller: smaller - 10
                                 }
                logging.debug("MEMO MOST " + str(self.memo))
                for key, i in self.memo.items():
                    logging.debug("keresem, hogy ez jó " + str(i))
                    logging.debug("i in poss " + str(i) in self.possibleShots)
                    logging.debug("i in possibleship " + str(i) in hl.getPossibleShipPositions(key))

                    if i in self.possibleShots and i in hl.getPossibleShipPositions(key):
                        self.possibleShots.remove(i)
                        logging.debug("FURA LOVES " + str(i))
                        self.myShots.append(i)
                        nextstep = i
                        skip = True
                        break
            if skip:
                logging.debug("okosan ez lett " + str(nextstep))
                yield nextstep

            else:
                if self.replyFromServer == hl.States.MISSED:
                    logging.debug(str(self.myShots[-1]) + " NEM TALÁLT")
                    nextstep = self.possibleShots[0]
                    self.possibleShots.remove(self.possibleShots[0])
                    # print("LOVES", nextstep)
                    logging.debug("LOVES " + str(nextstep))
                    self.myShots.append(nextstep)
                    yield nextstep
                elif self.replyFromServer == hl.States.HIT:
                    logging.debug(str(self.myShots[-1]) +  " TALÁLT")
                    preferred_indeces = hl.getPossibleShipPositions(self.myShots[-1])
                    random.shuffle(preferred_indeces)
                    logging.debug(str(self.possibleShots))
                    delete = []
                    for i in preferred_indeces:
                        if i not in self.possibleShots:
                            delete.append(i)
                        else:
                            self.possibleShots.remove(i)

                    for i in delete:
                        preferred_indeces.remove(i)
                    logging.debug(str(preferred_indeces))
                    self.possibleShots = preferred_indeces + self.possibleShots
                    # for i in range(len(preferred_indeces)):
                    #     if preferred_indeces[i] in self.possibleShots:
                    #         tmp = self.possibleShots[i]
                    #         self.possibleShots.remove(preferred_indeces[i])
                    #         self.possibleShots[i] = preferred_indeces[i]
                    #         self.possibleShots.append(tmp)
                    logging.debug(str(self.possibleShots))
                    nextstep = self.possibleShots[0]
                    self.possibleShots.remove(self.possibleShots[0])  # amit lövök azt kiveszem
                    # print("LOVES", nextstep)
                    logging.info("LOVES " + str(nextstep))
                    self.myShots.append(nextstep)
                    yield nextstep

                elif self.replyFromServer == hl.States.SINK:

                    need_to_be_deleted = []
                    need_to_be_deleted.append(self.myShots[-1])
                    for i in range(2, len(self.myShots) + 1):  # fontos emléket keresve
                        logging.debug(str(self.myShots[-i]) + " " +str(self.myShotsReplies[-i]))
                        if self.myShotsReplies[-i] == hl.States.HIT:
                            need_to_be_deleted.append(self.myShots[-i])
                        if self.myShotsReplies[-i] == hl.States.SINK:
                            break
                    logging.debug("HOPHOPppppsink")
                    for i in need_to_be_deleted:
                        for d in hl.getNeighbours(i):
                            if d in self.possibleShots:
                                logging.debug("törlöm " + str(d))
                                self.possibleShots.remove(d)

                    nextstep = self.possibleShots[0]
                    self.possibleShots.remove(nextstep)
                    logging.debug("SINK LOVES " + str(nextstep))
                    self.myShots.append(nextstep)
                    yield nextstep

    def placeShips(self):
        return self.myShips
