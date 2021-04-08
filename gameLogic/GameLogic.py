from helper import helper as hl

# GameLogic osztaly: sorfolytonos repr. allapot, jatekosok hajoinak tarolasa, szukseges hajok
class GameLogic():
    def __init__(self, gameVsAI):
        self.previousShot = None
        self.state = [hl.States.WATER]*100
        self.opponentState = [hl.States.WATER] * 100
        self.gameVsAI = gameVsAI
        self.ships = [[2, 1], [2,2], [3,3], [2,4], [1,5]]
        self.playerOneShips = [[0], [2], [4,5], [7,8], [20,21,22], [24,25,26], [40,41,42], [44,45,46,47], [60,61,62,63], [80,81,82,83,84]]
        for sublist in self.playerOneShips:
            for k in sublist:
                self.state[k] = hl.States.SHIP

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
        #print(stateStr+"\n")
        return stateStr + "\n"

    def printStateForOpponent(self):
        letters = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        counter = 0
        stateStr = "  1 2 3 4 5 6 7 8 9 10\nA "
        for i in range(0,len(self.opponentState)):
            stateStr += str(self.opponentState[i]) + " "
            if ((i+1)%10 == 0) and (i != 99):
                stateStr += "\n" + letters[counter] + " "
                counter += 1
        print(stateStr)

    def printStateForMe(self):
        letters = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        counter = 0
        stateStr = "  1 2 3 4 5 6 7 8 9 10\nA "
        for i in range(0,len(self.state)):
            stateStr += str(self.state[i].value) + " "
            if ((i+1)%10 == 0) and (i != 99):
                stateStr += "\n" + letters[counter] + " "
                counter += 1
        #print(stateStr)
        return stateStr + '\n'

    def responseOfMissile(self, coord):
        if self.state[coord] == hl.States.SHIP:
            for ships in self.playerOneShips:
                if coord in ships and len(ships) >= 2:
                    ships.remove(coord)
                    self.state[coord] = hl.States.HIT
                    return hl.States.HIT
                elif coord in ships and len(ships) < 2:
                    ships.remove(coord)
                    self.playerOneShips.remove(ships)
                    self.state[coord] = hl.States.SINK

                    for i in range(0, 100):
                        # TODO ez lehet, hogy nem kosher igy
                        if self.state[i] == hl.States.HIT and [elem != hl.States.SHIP for elem in hl.getNeighbours(i)]:
                            self.state[i] = hl.States.SINK
                    return hl.States.SINK
        else:
            self.state[coord] = hl.States.MISSED
            return hl.States.MISSED

    def shoot(self):
        while True:
            try:
                coordinate = self.gameVsAI.playerCommunicator.shoot()
                if not hl.validateStringCoordinate(coordinate):
                    raise ValueError
            except ValueError:
                print("exc5")
                continue

            else:
                self.previousShot = hl.stringToCoordinate(coordinate)
                return hl.stringToCoordinate(coordinate)

    def updateOpponentState(self, response):
        self.opponentState[self.previousShot] = response
        if response == hl.States.SINK:
            for i in range(0, 100):
                # TODO ez lehet, hogy nem kosher igy
                if self.opponentState[i] == hl.States.HIT and [elem != hl.States.SHIP for elem in hl.getNeighbours(i)]:
                    self.opponentState[i] = hl.States.SINK

    def setPreviousShot(self, prev):
        self.previousShot = prev

    def readInAIShips(self, AIships):
        self.state = [hl.States.WATER] * 100
        self.playerOneShips = AIships
        ships = [item for sublist in AIships for item in sublist]
        for k in ships:
            self.state[k] = hl.States.SHIP

    def readIn(self):
        sizes = [[k[1] for _ in range(k[0])] for k in self.ships]
        sizes = [item for sublist in sizes for item in sublist]
        forbiddenSpaces = set([])
        for i in sizes:
            while True:
                    print("Position a " + str(i) + " sized ship!")
                    try:
                        coordinates = self.gameVsAI.playerCommunicator.readIn()
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
                        #check if ship is vertical:
                        if(coordOne%10 == coordTwo%10) and (int(abs(coordTwo - coordOne) / 10 + 1) == i): 
                            coordinates = [k for k in range(min(coordOne, coordTwo), max(coordOne, coordTwo)+10, 10)]
                        #check if ship is horizontal:
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
                            self.playerOneShips.append(coordinates)
                        else:
                            raise ValueError("msg2")
                    except ValueError:
                        print("exc4")
                        continue
                            #raise ValueError("Wrong coordinates, you can't place ships this close to each other!")

                    self.printState()
                    # print(forbiddenSpaces)

                    # print(self.playerOneShips)
                    self.gameVsAI.printStateForMe(self.printStateForMe())
                    break
            #if i == 5: break


# gl = GameLogic()
# gl.readIn()
# print(gl.playerOneShips)
# gl.printState()
# print("Lojj kettot\n")
# gl.step(0)
# gl.printState()
# print(gl.playerOneShips)
# print("\n")
# gl.step(15)
# gl.printState()
# print("\n")
# gl.step(14)
# gl.printState()