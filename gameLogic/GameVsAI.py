from AI.AI import AIClass
from gameLogic.GameLogic import GameLogic


class GameVsAI:
    def __init__(self):
        self.gl1 = GameLogic()
        self.glAI = GameLogic()
        self.AI = AIClass()
        self.initialization()
        self.isEnd = False

    def initialization(self):
        self.glAI.readInAIShips(self.AI.initShips())
        print("AI has placed its ships.")

        self.gl1.readIn()

    def game(self):
        responseAI = None

        while(not self.isEnd):
            #self.gl1.printStateForMe()
            print("Player shoot: ")
            response = self.glAI.responseOfMissile(self.gl1.shoot())
            self.gl1.updateOpponentState(response)
            if(len(self.glAI.playerOneShips) == 0): self.isEnd = True


            print("AI shoot: ")
            AInextshot = self.AI.nextStep(responseAI)
            responseAI = self.gl1.responseOfMissile(AInextshot)
            print(responseAI)
            self.glAI.setPreviousShot(AInextshot)
            self.glAI.updateOpponentState(responseAI)
            if (len(self.gl1.playerOneShips) == 0): self.isEnd = True


            self.gl1.printState()



asd = GameVsAI()
asd.game()

