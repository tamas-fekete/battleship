import tkinter as tk
from PIL import Image, ImageTk

class Cons:

    BOARD_WIDTH = 342
    BOARD_HEIGHT = 342

class Board(tk.Canvas):

    def __init__(self, imageBackground):
        super().__init__(width=Cons.BOARD_WIDTH, height=Cons.BOARD_HEIGHT,
            background="black", highlightthickness=0)

        self.initBoard(imageBackground)


    def initBoard(self,imageBackground):
        '''initializes game'''

        self.loadImages(imageBackground)
        self.createObjects()
   


    def loadImages(self, imageBackground):
        '''loads images from the disk'''

        try:
            
            self.background = ImageTk.PhotoImage(imageBackground)

        except IOError as e:

            print(e)
            sys.exit(1)
            
            
    def createObjects(self):
        '''creates objects on Canvas'''
        self.create_image(0, 0, image=self.background, anchor=tk.NW,  tag="background")
          
        


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
        
        self.boardShips.pack(side=tk.LEFT, expand="true")
        self.radarShips.pack(side=tk.RIGHT, expand="true")
        
        self.gameInfo = tk.Label(text="Game Information:")
        self.gameInfo.pack()
        self.textBox = tk.Text(width=40, height=1)
        self.textBox.pack()
        
        #creating menus:
        menu = tk.Menu(self.master)
        self.master.config(menu=menu)
        
        file = tk.Menu(menu)
        file.add_command(label="play on network")
        file.add_command(label="play against AI")
        file.add_command(label="Exit", command=self.clientExit)
        menu.add_cascade(label="File", menu=file)
        
        
        self.pack()
        
        
    def onEnter(self, event):
        myInput = self.entry.get()
        self.entry.delete(0, tk.END)
        self.textBox.delete("1.0",tk.END)
        self.textBox.insert(tk.END, myInput+"\n")
        
    def clientExit(self):
        exit()


def main():

    root = tk.Tk()
    BattleGui()
    root.mainloop()


if __name__ == '__main__':
    main()