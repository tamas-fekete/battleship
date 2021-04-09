import tkinter as tk
from PIL import Image, ImageTk
from helper import helper as hl
from gameLogic.GameLogic import GameLogic
from AI.AI import AIClass

class Cons:
    BOARD_WIDTH = 342
    BOARD_HEIGHT = 342
    TILE_HEIGHT = 32
    TILE_WIDTH = 32


class Board(tk.Canvas):

    def __init__(self, imageBackground):
        super().__init__(width=Cons.BOARD_WIDTH, height=Cons.BOARD_HEIGHT,
                         background="black", highlightthickness=0)

        self.initBoard(imageBackground)

    def initBoard(self, imageBackground):

        try:
            self.background = ImageTk.PhotoImage(imageBackground)
        except IOError as e:
            print(e)
            exit(1)

        self.create_image(0, 0, image=self.background, anchor=tk.NW, tag="background")

    def putImageOnCanvas(self, image, x, y, tagName):

        self.create_image(x, y, image=image, anchor=tk.NW, tag=tagName)


class BattleGui(tk.Frame):

    def __init__(self):
        super().__init__()
        self.bind_all("<Return>", self.onEnter)

        self.master.title("BattleShip")

        self.inputText = tk.Label(text="Attack coordinates:")
        self.inputText.pack()

        self.entry = tk.Entry()
        self.entry.pack()

        self.boardShips = Board(Image.open("sprites/oceangrid_final.png"))
        self.radarShips = Board(Image.open("sprites/radargrid_final.png"))

        self.winner = None
        self.myInput = None     # az elejen ebben a valtozoban lesz elmentve a letenni kivant hajo, aztan pedig a loves koordinataja
        self.shipSprites = []
        self.radarSprites = []
        self.oceanSprites = []
        self.gameLogic = GameLogic(None, self)
        self.gameLogicAI = GameLogic(None, self)
        self.AI = AIClass()
        self.gameLogicAI.readInAIShips(self.AI.initShips())
        self.responseAI = None
        self.loadImages()

        self.boardShips.pack(side=tk.LEFT, expand="true")
        self.radarShips.pack(side=tk.RIGHT, expand="true")

        self.gameInfo = tk.Label(text="Game Information:")
        self.gameInfo.pack()
        self.textBox = tk.Text(width=40, height=1)
        self.textBox.pack()

        # creating menus:
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)

        file = tk.Menu(menu)
        file.add_command(label="play on network")
        file.add_command(label="play against AI")
        file.add_command(label="Exit", command=self.clientExit)
        menu.add_cascade(label="File", menu=file)

        self.pack()

    def loadImages(self):

        try:
            self.ihit = Image.open("sprites/hit.png")
            self.hit = ImageTk.PhotoImage(self.ihit)

            self.imiss = Image.open("sprites/miss.png")
            self.miss = ImageTk.PhotoImage(self.imiss)

            self.imiss2 = Image.open("sprites/miss2.png")
            self.miss2 = ImageTk.PhotoImage(self.imiss2)

            self.isink = Image.open("sprites/sink.png")
            self.sink = ImageTk.PhotoImage(self.isink)

            self.isink2 = Image.open("sprites/sink2.png")
            self.sink2 = ImageTk.PhotoImage(self.isink2)

            self.iship1vertical = Image.open("sprites/1vertical.png")
            self.ship1vertical = ImageTk.PhotoImage(self.iship1vertical)

            self.iship2vertical = Image.open("sprites/2vertical.png")
            self.ship2vertical = ImageTk.PhotoImage(self.iship2vertical)

            self.iship3vertical = Image.open("sprites/3vertical.png")
            self.ship3vertical = ImageTk.PhotoImage(self.iship3vertical)

            self.iship4vertical = Image.open("sprites/4vertical.png")
            self.ship4vertical = ImageTk.PhotoImage(self.iship4vertical)

            self.iship5vertical = Image.open("sprites/5vertical.png")
            self.ship5vertical = ImageTk.PhotoImage(self.iship5vertical)

            self.iship1horizontal = Image.open("sprites/1horizontal.png")
            self.ship1horizontal = ImageTk.PhotoImage(self.iship1horizontal)

            self.iship2horizontal = Image.open("sprites/2horizontal.png")
            self.ship2horizontal = ImageTk.PhotoImage(self.iship2horizontal)

            self.iship3horizontal = Image.open("sprites/3horizontal.png")
            self.ship3horizontal = ImageTk.PhotoImage(self.iship3horizontal)

            self.iship4horizontal = Image.open("sprites/4horizontal.png")
            self.ship4horizontal = ImageTk.PhotoImage(self.iship4horizontal)

            self.iship5horizontal = Image.open("sprites/5horizontal.png")
            self.ship5horizontal = ImageTk.PhotoImage(self.iship5horizontal)

        except IOError as e:
            print(e)
            exit(1)

        # create a list of dictionaries from the ships:
        dict1 = {hl.shipOrientation.HORIZONTAl: self.ship1horizontal, hl.shipOrientation.VERTICAL: self.ship1vertical}
        dict2 = {hl.shipOrientation.HORIZONTAl: self.ship2horizontal, hl.shipOrientation.VERTICAL: self.ship2vertical}
        dict3 = {hl.shipOrientation.HORIZONTAl: self.ship3horizontal, hl.shipOrientation.VERTICAL: self.ship3vertical}
        dict4 = {hl.shipOrientation.HORIZONTAl: self.ship4horizontal, hl.shipOrientation.VERTICAL: self.ship4vertical}
        dict5 = {hl.shipOrientation.HORIZONTAl: self.ship5horizontal, hl.shipOrientation.VERTICAL: self.ship5vertical}
        self.shipSprites.extend([dict1, dict2, dict3, dict4, dict5])
        self.radarSprites.extend([0, 1, self.miss, self.hit, self.sink])
        self.oceanSprites.extend([0, 1, self.miss2, self.sink2, self.sink2])

    def onEnter(self, event):
        self.gameAI()

    def gameAI(self):
        self.myInput = self.entry.get()
        self.entry.delete(0, tk.END)
        self.textBox.delete("1.0", tk.END)
        self.textBox.insert(tk.END, self.myInput + "\n")

        if self.gameLogic.gameState == 0:  # init state
            ship = self.gameLogic.readIn()
            if ship.successful:
                pixelCoords = self.coordinateToPixel(ship.startingCoordinate)

                self.boardShips.putImageOnCanvas(self.shipSprites[ship.size-1][ship.orientation], pixelCoords[0], pixelCoords[1],
                                                 "ship"+str(ship.size)+str(ship.orientation))
            else:
                pass  # notify user that ship placement was unsuccessful

        elif self.gameLogic.gameState == 1:   # game started against opponent

            # jatekos lo az AI-ra es az AI megmondja, hogy hit, miss vagy sink:
            response = self.gameLogicAI.responseOfMissile(self.gameLogic.shoot(self.myInput))
            self.gameLogic.updateOpponentState(response)
            self.updateRadar(self.gameLogic.opponentState)
            # csalas:
            print(self.gameLogicAI.printState())

            # ha az AI-nak elfogytak a hajoi, akkor nyert a jatekos
            if len(self.gameLogicAI.playerOneShips) == 0:
                self.gameLogic.gameState = 2
                self.winner = "You"
                self.textBox.delete("1.0", tk.END)
                self.textBox.insert(tk.END, "You win, congrats!" + "\n")

            # a deepmind klon kiszamolja a kovetkezo lepeset
            AInextshot = self.AI.nextStep(self.responseAI)
            # self.printStateForMe("AI shoot: ")  # TODO az indexet vissza kell alakítani koordinátává

            # az AI lovesere reagal a jatekos
            self.responseAI = self.gameLogic.responseOfMissile(AInextshot)

            # updatelni kell az ocean grid-et:
            self.updateOcean(self.gameLogic.state)

            self.gameLogicAI.setPreviousShot(AInextshot)  # lementeni az AI-nak az AI elozo loveset
            self.gameLogicAI.updateOpponentState(self.responseAI)  # az AI radarjat updatelni

            # ha elfogytak a jatekos hajoi, akkor az AI nyert
            if len(self.gameLogic.playerOneShips) == 0:
                self.gameLogic.gameState = 2
                self.winner = "AI"
                self.textBox.delete("1.0", tk.END)
                self.textBox.insert(tk.END, "The AI owned you, you lose!" + "\n")

        elif self.gameLogic.gameState == 2:
            self.textBox.delete("1.0", tk.END)
            if self.winner == "AI":
                self.textBox.insert(tk.END, "The AI owned you, you lose!" + "\n")
            elif self.winner == "You":
                self.textBox.insert(tk.END, "You win, congrats!" + "\n")

    def getInput(self):
        return self.myInput

    def updateOcean(self, states):
        for coordinate, state in enumerate(states):
            if state == hl.States.MISSED or state == hl.States.HIT or state == hl.States.SINK:
                pixelCoords = self.coordinateToPixel(coordinate)
                self.boardShips.putImageOnCanvas(self.oceanSprites[state], pixelCoords[0], pixelCoords[1],
                                                 "sprite" + str(pixelCoords[0]) + str(pixelCoords[1]))

    def updateRadar(self, opponentState):
        for coordinate, state in enumerate(opponentState):
            if state == hl.States.MISSED or state == hl.States.HIT or state == hl.States.SINK:
                pixelCoords = self.coordinateToPixel(coordinate)
                self.radarShips.putImageOnCanvas(self.radarSprites[state], pixelCoords[0], pixelCoords[1],
                                                 "sprite"+str(pixelCoords[0])+str(pixelCoords[1]))

    def coordinateToPixel(self, coordinate):
        pixelCoords = []
        x = coordinate % 10
        y = int(coordinate / 10)

        x = (Cons.TILE_WIDTH-1)*x + (Cons.TILE_WIDTH-1)
        y = (Cons.TILE_HEIGHT-1)*y + (Cons.TILE_HEIGHT-1)
        pixelCoords.extend([x, y])
        return pixelCoords

    def returnWithShip(self):  # ez csak teszteleshez kellett
        ship = hl.guiShip()
        ship.size = 5
        ship.startingCoordinate = 12
        ship.orientation = hl.shipOrientation.HORIZONTAl
        return ship

    def clientExit(self):
        exit()


def main():
    root = tk.Tk()
    root.iconbitmap("sprites/sonar.ico")
    BattleGui()
    root.mainloop()


if __name__ == '__main__':
    main()
