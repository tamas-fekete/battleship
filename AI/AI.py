from helper import helper as hl


class AIClass:
    def __init__(self):
        self.state = [hl.States.WATER] * 100
        # [number, size]
        self.ships = [[2, 1]]  # , [2,2], [3,3], [2,4], [1,5]]
        # minden hajó egy list ebben a list-ben, a hajo altal felvett koordinatakat tartalmazza
        self.playerOneShips = []
        self.playerTwoShips = []


print("Ez a merge próba")