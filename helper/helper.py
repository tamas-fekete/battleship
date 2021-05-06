import re
from enum import Enum
# helper functions
from enum import IntEnum


def stringToCoordinate(strCoord):
    """
    This function will convert a string to coordinates
    :param strCoord: string coordinate
    :return: a list with two elements, first element: x coordinate, second element: y coordinate
    """

    y = ord(strCoord[0]) - ord('a')
    x = int(strCoord[1:]) - 1

    return y * 10 + x


def coordinateToString(coordinate):
    """
    Converts coordinates to strings
    :param coordinate: linear coordinate
    :return: string coordinate
    """
    if coordinate < 0 or coordinate > 99:
        return None
    result = str(coordinate)
    if len(result) == 1:
        return "A" + str(coordinate + 1)
    else:
        if result[0] == "1":
            return "B" + str(int(result[1]) + 1)
        elif result[0] == "2":
            return "C" + str(int(result[1]) + 1)
        elif result[0] == "3":
            return "D" + str(int(result[1]) + 1)
        elif result[0] == "4":
            return "E" + str(int(result[1]) + 1)
        elif result[0] == "5":
            return "F" + str(int(result[1]) + 1)
        elif result[0] == "6":
            return "G" + str(int(result[1]) + 1)
        elif result[0] == "7":
            return "H" + str(int(result[1]) + 1)
        elif result[0] == "8":
            return "I" + str(int(result[1]) + 1)
        elif result[0] == "9":
            return "J" + str(int(result[1]) + 1)


def getNeighbours(coordinate):
    """
    Returns a set containing the neighbouring coordinates
    :param coordinate: linear coordinate
    :return: a set containing the neighbouring coordinates
    """
    lis = []
    x = coordinate % 10
    y = int(coordinate / 10)
    # print(x,y)
    for i in range(max(0, x - 1), min(9, x + 1) + 1):
        for j in range(max(0, y - 1), min(9, y + 1) + 1):
            lis.append(j * 10 + i)

    # print(range(max(0,x-1),min(9,x+1)+1))
    # print(range(max(0,y-1),min(9,y+1)+1))
    return set(lis)


def getPossibleShipPositions(coordinate):
    """
    Returns a list of possible ship positions neighbouring the input parameter coordinate
    :param coordinate: linear coordinate
    :return: a list of possible ship positions
    """
    lis = []
    x = coordinate % 10
    y = int(coordinate / 10)
    if y != 0:
        lis.append(coordinate - 10)
    if x != 0:
        lis.append(coordinate - 1)
    if x != 9:
        lis.append(coordinate + 1)
    if y != 9:
        lis.append(coordinate + 10)
    return lis


class States(IntEnum):
    """
    The possible states of the playing field
    """
    WATER = 0
    SHIP = 1
    MISSED = 2
    HIT = 3
    SINK = 4


class shipOrientation(IntEnum):
    """
    This is for the GUI, so it will know the orientation of a ship
    """
    HORIZONTAl = 0
    VERTICAL = 1


class guiShip():
    """
    The GUI will use this class to draw a ship on the screen
    """
    def __init__(self):
        self.size = 0
        self.startingCoordinate = 0
        self.orientation = None
        self.successful = False


def validateStringCoordinate(strCoord):
    """
    This function will check if the string is a valid coordinate
    :param strCoord: string coordinate
    :return: boolean, true if the string is a valid coordinate and false if it is not
    """
    if re.search("^[a-j][1-9]$|^[a-j]10$", strCoord) is None:
        return False
    else:
        return True
