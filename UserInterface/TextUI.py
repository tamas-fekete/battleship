from PlayerCommunicator.PlayerCommunicator import PlayerCommunicator
from gameLogic.GameVsAI import GameVsAI

class TextUI:
    def __init__(self):
        self.playerCommunicator = PlayerCommunicator(self)
        self.state = None

    def readInUI(self):
            return input("Type the coordinates of the endpoints of your ship like this: \'A1-A1\'!\n").lower().split('-')


    def printState(self, state):
        self.state = state
        print(self.state)

    def shootUI(self):
        return input("Player shoot: ")

    def start(self):
        gameType = input("For local game type \'L\', for network game type \'N\'!\n").lower()
        if gameType == 'l':
            gameVsAI = GameVsAI(self.playerCommunicator)
            gameVsAI.game()

textUI = TextUI()
textUI.start()
