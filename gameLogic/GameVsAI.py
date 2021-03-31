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
        print("AI has placed its ships.\n")
        self.gl1.readIn()

    def game(self):
        print("Player shoot: ")
        self.glAI.responseOfMissile(self.gl1.shoot())
        self.glAI.printStateForOpponent()
        print("\n")
        print("AI shoot: ")
        # AI lo
        response = self.gl1.responseOfMissile(self.AI.nextStep())
        self.gl1.printStateForOpponent()

        print("\n")
        while(not self.isEnd):
            # jatekos lo
            print("Player shoot: ")
            self.glAI.responseOfMissile(self.gl1.shoot())
            self.glAI.printStateForOpponent()
            if(len(self.glAI.playerOneShips) == 0): self.isEnd = True
            print("\n")
            print("AI shoot: ")
            # AI lo
            response = self.gl1.responseOfMissile(self.AI.nextStep(response))
            self.gl1.printStateForOpponent()
            if (len(self.gl1.playerOneShips) == 0): self.isEnd = True

            print("\n")




asd = GameVsAI()
asd.game()

