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
    result=str(coordinate)

class States(Enum):
    WATER = 0
    SHIP = 1
    MISSED = 2
    HIT = 3

# this function will check if the string is a valid coordinate
# input: string
# return value: boolen, true if the string is a valid coordinate and false if it is not

def validateStringCoordinate(strCoord):
    if re.search("^[a-j][1-9]$|^[a-j]10$", strCoord) is None:
        return False
    else:
        return True
