import tkinter as tk
from PIL import Image, ImageTk
from helper import helper as hl
from gameLogic.GameLogic import GameLogic

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

        self.myInput = None     # az elejen ebben a valtozoban lesz elmentve a letenni kivant hajo, aztan pedig a loves koordinataja
        self.shipSprites = []
        self.gameLogic = GameLogic(None, self)

        self.loadImages()
        # put a few sprites on the canvas:

        # self.boardShips.putImageOnCanvas(self.green, 31, 31, "green")
        # self.boardShips.putImageOnCanvas(self.ship3vertical, 93,93, "ship3vertical")
        # self.radarShips.putImageOnCanvas(self.red, 62, 62, "red")
        # self.radarShips.putImageOnCanvas(self.hit, 93, 93, "hit")

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
            self.igreen = Image.open("sprites/green.png")
            self.green = ImageTk.PhotoImage(self.igreen)

            self.ired = Image.open("sprites/red.png")
            self.red = ImageTk.PhotoImage(self.ired)

            self.ihit = Image.open("sprites/hit.png")
            self.hit = ImageTk.PhotoImage(self.ihit)

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

    def onEnter(self, event):
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
            else: pass #notify user that ship placement was unsuccessful


    def getInput(self):
        return self.myInput

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
    BattleGui()
    root.mainloop()


if __name__ == '__main__':
    main()
