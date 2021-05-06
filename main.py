from UserInterface import BattleGui as bg
import argparse
import logging

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("-D", "--DEBUG", help="print out debug information",
                        action="store_true")
    args = parser.parse_args()
    if args.DEBUG:
        logging.basicConfig(level=logging.DEBUG)
    gui = bg.MainGuiApp()
    gui.mainloop()
