from UserInterface.TextUI import TextUI
from helper import helper as hl
from gameLogic.GameLogic import GameLogic

class PlayerCommunicator:
    def __init__(self):
        self.gameLogic = GameLogic()
        self.textUI = TextUI()
        self.previousShot = None

    def updateOpponentState(self, response):
        self.textUI.updateOpponentStateUI(response)

    def updateMyState(self, coord, response):
        self.textUI.updateMyState(coord, response)

    def shoot(self):
        self.gameLogic.responseOfMissile(self.textUI.shootUI())

    def getShips(self):
        return self.gameLogic.ships

    def setMyShips(self, coordinates):
        self.gameLogic.playerOneShips.append(coordinates)

    def readIn(self):
        self.textUI.readInUI()