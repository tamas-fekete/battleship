from AI.AI import AIClass
from gameLogic.GameLogic import GameLogic


class GameVsAI:
    def __init__(self, playerCommunicator):
        self.gameLogic = GameLogic(self)
        self.gameLogicAI = GameLogic(self)
        self.AI = AIClass()
        self.playerCommunicator = playerCommunicator
        self.initialization()
        self.isEnd = False
        self.winner = None

    def initialization(self):
        self.gameLogicAI.readInAIShips(self.AI.initShips())
        print("AI has placed its ships.")

        self.playerCommunicator.setGameVsAI(self)
        #self.gameLogic.readIn()

    def game(self):
        responseAI = None

        while(not self.isEnd):
            response = self.gameLogicAI.responseOfMissile(self.gameLogic.shoot())
            self.gameLogic.updateOpponentState(response)
            if(len(self.gameLogicAI.playerOneShips) == 0):
                self.isEnd = True
                self.winner = "You"

            AInextshot = self.AI.nextStep(responseAI)
            self.printStateForMe("AI shoot: ")  #TODO az indexet vissza kell alakítani koordinátává
            responseAI = self.gameLogic.responseOfMissile(AInextshot)
            #print(responseAI)
            self.gameLogicAI.setPreviousShot(AInextshot)
            self.gameLogicAI.updateOpponentState(responseAI)
            if (len(self.gameLogic.playerOneShips) == 0):
                self.isEnd = True
                self.winner = "AI"


            self.playerCommunicator.printState(self.gameLogic.printState())

        self.playerCommunicator.printState("The winner is " + self.winner)



    def printStateForMe(self, state):
        self.playerCommunicator.printState(state)


