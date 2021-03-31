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
        self.glAI.readInAIShips(self.AI.placeShips())
        print("AI has placed its ships.")
        self.gl1.readIn()

    def game(self):
        print("Player shoot: ")
        response = self.glAI.responseOfMissile(self.gl1.shoot())
        self.gl1.updateOpponentState(response)
        print("AI shoot: ")
        responseAI = self.gl1.responseOfMissile(self.AI.nextStep())
        self.glAI.setPreviousShot(self.AI.nextStep())
        self.glAI.updateOpponentState(responseAI)

        self.gl1.printState()

        while(not self.isEnd):
            print("Player shoot: ")
            response = self.glAI.responseOfMissile(self.gl1.shoot())
            self.gl1.updateOpponentState(response)
            if(len(self.glAI.playerOneShips) == 0): self.isEnd = True


            print("AI shoot: ")
            # AI lo
            responseAI = self.gl1.responseOfMissile(self.AI.nextStep(responseAI))
            self.glAI.updateOpponentState(responseAI)
            if (len(self.gl1.playerOneShips) == 0): self.isEnd = True


            self.gl1.printState()




asd = GameVsAI()
asd.game()

