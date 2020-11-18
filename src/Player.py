import TwoDice 
import Board

class Player():

    PLAYER_TITLES = ["Regular", "Banker/Auctioneer", "Dual"]  #Dual means both Regular and Banker, used only if there are less than 5 players
    PLAYER_MINIMUM = 2
    PLAYER_MAXIMUM = 8 
    PLAYER_BANKER_LIMIT = 5 #If there are more than 5 players in game, one person must be Banker/Auctioneer only 
    
    def __init__(self, id, name):
        self.id = id                            #Identification Number
        self.name = name                        #Name of player
        self.money = 0                          #Cash on hand - starts with 1500
        self.position = 0                       #Start at "Go" tile
        self.properties = []                    #Start with no properties
        self.jail_cards = 0                     #Number of "Get Out of Jail Free" cards
        self.jail_turns = 0                     #Number of remaining turns in jail
        self.bankrupt = False                   #Bankrupt status
        self.title = PLAYER_TITLES["Regular"]   #Title of player - Default is Regular

        self.double = 0         #Start with no doubles 
        self.order = None       #Determine the order of play in game - default is None. 

    #Get the id of user
    def getuserID(self): 
        return self.id 

    #Get the monetary value of the player
    def getMonetaryValue(self): 
        return self.money 
    
    #Get the position of the player on the board
    def getPosition(self): 
        return self.position 

    #Get the order of play of player
    def getOrder(self):
        return self.order 

    #Set the order of play for player
    def setOrder(self, order): 
        self.order = order 
    
    #Get the title of the player
    def getTitle(self):
        return self.title
    
    #Set the title of the player
    def setTitle(self, title):
        self.title = PLAYER_TITLES[title] 

        if (self.getTitle() == "Banker/Auctioneer"):
            self.setOrder(0)
    
    #Move the player across the board when it is their turn 
    def move(self):

        #Check if the user is in jail 
        #TODO: Add logic regarding if user has jail-free cards or has money to self-bail 
        if (self.jail_turns > 0):
            return 0
        
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
        

    

        

            

            




