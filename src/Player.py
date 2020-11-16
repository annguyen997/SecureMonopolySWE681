import TwoDice 
from Board import TILES_LIST 

class Player():

    PLAYER_TITLES = ["Regular", "Banker", "Accountant"]

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.moneyAmount = 0 
        self.position = 0
        self.double = 0

    def move(self):
        self.position += TwoDice.rollDice() 

        #Check if player rolled doubles 
        while TwoDice.double:
            self.double += 1
            add_total = TwoDice.rolledDouble() 

            #Check if the return total is zero, indicating player needs to go to jail
            if (add_total == 0): 
                #TODO: Go to jail logic here
                self.position = 11
            else: 
                self.position += add_total

            #Check if player has cycled through the board
            if (self.position > len(TILES_LIST)):
                self.position = self.position - len(TILES_LIST)
    

        

            

            




