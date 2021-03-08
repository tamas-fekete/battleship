import helper
# GameLogic osztaly: sorfolytonos repr. allapot, jatekosok hajoinak tarolasa, szukseges hajok
class GameLogic():
    def __init__(self):
        self.state = [0]*100
        # [number, size]
        self.ships = [[2, 1], [2,2], [3,3], [2,4], [1,5]]
        # minden hajo egy list ebben a list-ben, a hajo altal felvett koordinatakat tartalmazza
        self.playerOneShips = []
        self.playerTwoShips = []

#allapot kiirasa
    def printState(self):
        letters = ['B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        counter = 0
        stateStr = "  1 2 3 4 5 6 7 8 9 10\nA "
        for i in range(0,len(self.state)):
            stateStr += str(self.state[i]) + " "
            if ((i+1)%10 == 0) and (i != 99):
                stateStr += "\n" + letters[counter] + " "
                counter += 1
        print(stateStr)

#beolvasas, hajok elhelyezese
def readIn(gl):
    for i in gl.ships:
        size = i[1]
        for j in range(1, i[0]+1):
            print("Position the " + str(j) + ". ship of size " + str(size) + "!")
            coordinates = input().lower().split('-')
            if helper.validateStringCoordinate(coordinates[0]) & helper.validateStringCoordinate(coordinates[1]):
                coordOne = helper.stringToCoordinate(coordinates[0])
                coordTwo = helper.stringToCoordinate(coordinates[1])
            else: break

            tempShips = []
            # a hajo oszlopban van, meret megfelelo
            if(coordOne%10 == coordTwo%10) and (int(abs(coordTwo - coordOne) / 10 + 1) == size):
                for i in range(min(coordOne, coordTwo), max(coordOne, coordTwo)+10, 10):
                    gl.state[i] = 1
                    tempShips.append(i)
            # a hajo sorban van, meret megfelelo
            elif(abs(coordTwo - coordOne)+1 == size):
                for i in range(min(coordOne, coordTwo), max(coordOne, coordTwo)+1):
                    gl.state[i] = 1
                    tempShips.append(i)
            else:
                print("Rossz koordinatak!")
                break
            gl.playerOneShips.append(tempShips)
            gl.printState()

gl = GameLogic()
readIn(gl)
print(gl.playerOneShips)
#gl.printState()
# TODO hajokat ne lehessen egymas melle helyezni
