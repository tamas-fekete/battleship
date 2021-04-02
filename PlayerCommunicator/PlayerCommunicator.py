class PlayerCommunicator:
    def __init__(self, textUI):
        self.textUI = textUI
        self.gameVsAI = None
        self.previousShot = None

    def shoot(self):
        return self.textUI.shootUI()

    def readIn(self):
        return self.textUI.readInUI()

    def printState(self, state):
        self.textUI.printState(state)

    def setGameVsAI(self, gameVsAI):
        self.gameVsAI = gameVsAI