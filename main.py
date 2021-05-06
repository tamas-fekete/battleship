from UserInterface import BattleGui as bg
import logging
logging.basicConfig(level=logging.DEBUG)

if __name__ == '__main__':
    gui = bg.MainGuiApp()
    gui.mainloop()
