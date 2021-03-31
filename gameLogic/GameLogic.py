from helper import helper as hl

# GameLogic osztaly: sorfolytonos repr. allapot, jatekosok hajoinak tarolasa, szukseges hajok
class GameLogic():
    def __init__(self):
        self.state = [hl.States.WATER]*100
        # [number, size]
        # minden hajó egy list ebben a list-ben, a hajo altal felvett koordinatakat tartalmazza
        self.ships = [[2, 1], [2,2]] #, [3,3], [2,4], [1,5]]
        # minden hajo egy list ebben a list-ben, a hajo altal felvett koordinatakat tartalmazza
        self.playerOneShips = []

#allapot kiirasa
    def printState(self):
        letters = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        counter = 0
        stateStr = "  1 2 3 4 5 6 7 8 9 10\nA "
        for i in range(0,len(self.state)):
            stateStr += str(self.state[i].value) + " "
            if ((i+1)%10 == 0) and (i != 99):
                stateStr += "\n" + letters[counter] + " "
                counter += 1
        print(stateStr)

# TODO amikor elsullyedt az osszes, akkor mindet sink-re kell allitani
    def step(self, coord):
        if self.state[coord] == hl.States.SHIP:
            for ships in self.playerOneShips:
                if coord in ships and len(ships) >= 2:
                    ships.remove(coord)
                    self.state[coord] = hl.States.HIT
                    return hl.States.HIT
                elif coord in ships and len(ships) < 2:
                    ships.remove(coord)
                    gl.playerOneShips.remove(ships)
                    self.state[coord] = hl.States.SINK

                    for i in range(0, 100):
                        # TODO ez lehet, hogy nem kosher igy
                        if self.state[i] == hl.States.HIT and [elem != hl.States.SHIP for elem in hl.getNeighbours(i)]:
                            self.state[i] = hl.States.SINK
                    return hl.States.SINK
        else:
            self.state[coord] = hl.States.MISSED
            return hl.States.MISSED


#beolvasas, hajok elhelyezese
def readIn(gl):
    forbiddenSpaces = set([])
    for i in gl.ships:
        size = i[1]
        for j in range(1, i[0]+1):
            print("Position the " + str(j) + ". ship of size " + str(size) + "!")
            coordinates = input().lower().split('-')
            if hl.validateStringCoordinate(coordinates[0]) & hl.validateStringCoordinate(coordinates[1]):
                coordOne = hl.stringToCoordinate(coordinates[0])
                coordTwo = hl.stringToCoordinate(coordinates[1])
            else: break

            tempShips = []
            if(coordOne%10 == coordTwo%10) and (int(abs(coordTwo - coordOne) / 10 + 1) == size):
                coordinates = [k for k in range(min(coordOne, coordTwo), max(coordOne, coordTwo)+10, 10)]
            elif (abs(coordTwo - coordOne) + 1 == size):
                coordinates = [k for k in range(min(coordOne, coordTwo), max(coordOne, coordTwo)+1)]
            else:
                print("Rossz koordinatak, vagy nem sorban/oszlopban van a hajo, vagy nem jo meretu!")
                break

            neighbours = set([])
            for coord in coordinates:
                neighbours.update(hl.getNeighbours(coord))
            print(forbiddenSpaces)
            #[neighbours.remove(coord) for coord in coordinates]
            if len(forbiddenSpaces.intersection(set(coordinates))) == 0:
                for k in coordinates:
                    gl.state[k] = hl.States.SHIP
                forbiddenSpaces.update(neighbours)
                forbiddenSpaces.update(coordinates)
                gl.playerOneShips.append(coordinates)
            else:
                print("Rossz koordinatak, nem lehet ilyen kozel helyezni hajot egy masikhoz!")
                break

            print(forbiddenSpaces)
            gl.playerOneShips.append(tempShips)
            gl.printState()

gl = GameLogic()
readIn(gl)
print(gl.playerOneShips)
gl.printState()
print("Lojj kettot\n")
gl.step(0)
gl.printState()
print(gl.playerOneShips)
print("\n")
gl.step(15)
gl.printState()
print("\n")
gl.step(14)
gl.printState()


