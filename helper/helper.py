import re
from enum import Enum
# helper functions


# this function will convert a string to coordinates
# input: string
# return value: a list with two elements, first element: x coordinate, second element: y coordinate

def stringToCoordinate(strCoord):
    coordinates = []
    
    y = ord(strCoord[0]) - ord('a')
    x = int(strCoord[1:])-1

    return y*10+x


def coordinateToString(coordinate):
    if coordinate<0 or coordinate >99:
        return None
    result=str(coordinate)
    if len(result)==1:
        return "A"+str(coordinate+1)
    else:
        if result[0]=="1":
            return "B"+str(int(result[1])+1)
        elif result[0]=="2":
            return "C"+str(int(result[1])+1)
        elif result[0]=="3":
            return "D"+str(int(result[1])+1)
        elif result[0]=="4":
            return "E"+str(int(result[1])+1)
        elif result[0]=="5":
            return "F"+str(int(result[1])+1)
        elif result[0]=="6":
            return "G"+str(int(result[1])+1)
        elif result[0]=="7":
            return "H"+str(int(result[1])+1)
        elif result[0]=="8":
            return "I"+str(int(result[1])+1)
        elif result[0]=="9":
            return "J"+str(int(result[1])+1)

def getNeighbours(coordinate):
    lis=[]
    x= coordinate%10
    y= int(coordinate/10)
    #print(x,y)
    for i in range(max(0,x-1),min(9,x+1)+1):
        for j in range(max(0,y-1),min(9,y+1)+1):
            lis.append(j*10+i)

    #print(range(max(0,x-1),min(9,x+1)+1))
    #print(range(max(0,y-1),min(9,y+1)+1))
    return set(lis)

def getPossibleShipPositions(coordinate):
    lis=[]
    x= coordinate%10
    y= int(coordinate/10)
    if y!=0:
        lis.append(coordinate-10)
    if x!=0:
        lis.append(coordinate-1)
    if x!=9:
        lis.append(coordinate+1)
    if y!=9:
        lis.append(coordinate+10)
    return lis


class States(Enum):
    WATER = 0
    SHIP = 1
    MISSED = 2
    HIT = 3
    SINK = 4

class shipOrientation(Enum):
    HORIZONTAl = 0
    VERTICAL = 1

class guiShip():
    def __init__(self):
        self.size=0
        self.startingCoordinate=0
        self.orientation=None
        self.successful = False
    



# this function will check if the string is a valid coordinate
# input: string
# return value: boolen, true if the string is a valid coordinate and false if it is not

def validateStringCoordinate(strCoord):
    if re.search("^[a-j][1-9]$|^[a-j]10$", strCoord) is None:
        return False
    else:
        return True