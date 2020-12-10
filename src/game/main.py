# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


#def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    #print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

import Game
from Card import *

def main():
    #print(Game.Games)
    monopoly_instance = Game.Games()
    monopoly_instance.addPlayer('anguy03', 'Anh Nguyen')
    monopoly_instance.addPlayer('knguye15', 'Khanh Nguyen')
    monopoly_instance.run()

    #cardDeck = CommunityCards()
    #print(cardDeck.pile)
    #for i in range(25):
        #print(cardDeck.pullCard())

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    #print_hi('PyCharm')
    main()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
