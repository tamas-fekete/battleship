from UserInterface.PlayerCommunicator import PlayerCommunicator
from helper import helper as hl

class TextUI:
    def __init__(self):
        self.state = [hl.States.WATER]*100
        self.opponentState = [hl.States.WATER]*100
        self.playerCommunicator = PlayerCommunicator()
        self.ships = self.playerCommunicator.getShips()

    def readInUI(self):
        sizes = [[k[1] for _ in range(k[0])] for k in self.ships]
        sizes = [item for sublist in sizes for item in sublist]
        forbiddenSpaces = set([])
        for i in sizes:
            while True:
                    print("Position a " + str(i) + " sized ship!")
                    try:
                        coordinates = input("Type the coordinates of the endpoints of your ship like this: \'A1-A1\'!\n").lower().split('-')
                        if not (hl.validateStringCoordinate(coordinates[0]) & hl.validateStringCoordinate(coordinates[1])):
                            raise ValueError("Not valid coordinates.")
                        else:
                            coordOne = hl.stringToCoordinate(coordinates[0])
                            coordTwo = hl.stringToCoordinate(coordinates[1])
                    except  ValueError as e:
                        print("exc1")
                        continue
                    except IndexError as e2:
                        print("exc2")
                        continue

                    try:
                        if(coordOne%10 == coordTwo%10) and (int(abs(coordTwo - coordOne) / 10 + 1) == i):
                            coordinates = [k for k in range(min(coordOne, coordTwo), max(coordOne, coordTwo)+10, 10)]
                        elif (abs(coordTwo - coordOne) + 1 == i):
                            coordinates = [k for k in range(min(coordOne, coordTwo), max(coordOne, coordTwo)+1)]
                        else:
                            raise ValueError("message")
                    except ValueError:
                        print("exc3")
                        continue
                            #raise ValueError("Wrong coordinates, the ship is not in a row neither in a column or has not its right size!")

                    neighbours = set([])
                    for coord in coordinates:
                        neighbours.update(hl.getNeighbours(coord))
                        #[neighbours.remove(coord) for coord in coordinates]

                    try:
                        if len(forbiddenSpaces.intersection(set(coordinates))) == 0:
                            for k in coordinates:
                                self.state[k] = hl.States.SHIP
                            forbiddenSpaces.update(neighbours)
                            forbiddenSpaces.update(coordinates)
                            #self.playerOneShips.append(coordinates)
                            self.playerCommunicator.setMyShips(coordinates)
                        else:
                            raise ValueError("msg2")
                    except ValueError:
                        print("exc4")
                        continue
                            #raise ValueError("Wrong coordinates, you can't place ships this close to each other!")

                    self.printState()
                    # print(forbiddenSpaces)

                    # print(self.playerOneShips)
                    break
    def printState(self):
        letters = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        counter = 0
        stateStr = "Opponent board\n"
        stateStr += "  1 2 3 4 5 6 7 8 9 10\nA "
        for i in range(0,len(self.opponentState)):
            stateStr += str(self.opponentState[i].value) + " "
            if ((i+1)%10 == 0) and (i != 99):
                stateStr += "\n" + letters[counter] + " "
                counter += 1
        stateStr += "\nMy board\n"
        counter = 0
        stateStr += "  1 2 3 4 5 6 7 8 9 10\nA "
        for i in range(0, len(self.state)):
            stateStr += str(self.state[i].value) + " "
            if ((i + 1) % 10 == 0) and (i != 99):
                stateStr += "\n" + letters[counter] + " "
                counter += 1
        print(stateStr+"\n")

    def shootUI(self):
        while True:
            try:
                coordinate = input().lower()
                if not hl.validateStringCoordinate(coordinate):
                    raise ValueError
            except ValueError:
                print("exc5")
                continue

            else:
                self.previousShot = hl.stringToCoordinate(coordinate)
                return hl.stringToCoordinate(coordinate)

    def updateOpponentStateUI(self, response):
        self.opponentState[self.previousShot] = response
        if response == hl.States.SINK:
            for i in range(0, 100):
                if self.opponentState[i] == hl.States.HIT and [elem != hl.States.SHIP for elem in hl.getNeighbours(i)]:
                    self.opponentState[i] = hl.States.SINK

    def updateMyState(self, coord, response):
        self.state[coord] = response