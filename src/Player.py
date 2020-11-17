import TwoDice 
import Board

class Player():

    PLAYER_TITLES = ["Regular", "Banker/Auctioneer"]
    PLAYER_MINIMUM = 2
    PLAYER_MAXIMUM = 8 
    PLAYER_BANKER_LIMIT = 5 #If there are more than 5 players in game, one person must be Banker/Auctioneer only 

    def __init__(self, id, name):
        self.id = id
        self.name = name
        self.money = 0  #Revision for later - each player gets $1500
        self.position = 0 #Start at "Go" tile
        self.double = 0 #Start with no doubles 
        self.cards = [] #Start with no cards

    #Get the monetary value of the player
    def getMonetaryValue(self): 
        return self.money 
    
    #Get the position of the player on the board
    def getPosition(self): 
        return self.position 
    
    #Move the player across the board when it is their turn 
    def move(self):
        #Roll the dice to move the player 
        self.position += TwoDice.rollDice() 

        #Check if player rolled doubles 
        while TwoDice.double:
            self.double += 1
            add_total = TwoDice.rolledDouble() 

            #Check if the return total is zero, indicating player needs to go to jail
            if (add_total == 0): 
                self.position = Board.TILES_JAIL[0]
                break
            else: 
                self.position += add_total

        #Check if player has cycled through the board
        if (self.position > len(Board.TILES_LIST)):
            self.position = self.position - len(Board.TILES_LIST)
                
            #Collect more money 
        

    

        

            

            




