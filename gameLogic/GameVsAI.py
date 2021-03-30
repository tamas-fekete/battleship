from AI.AI import AIClass
from gameLogic.GameLogic import GameLogic


class GameVsAI:
    def __init__(self):
        self.gl1 = GameLogic()
        self.gl2 = GameLogic()
        self.AI = AIClass()


