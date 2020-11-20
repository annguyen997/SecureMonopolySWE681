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
        self.inJail = False                     #Check if user is in jail 

        self.consecutiveDoubles = 0             #Start with no doubles 
        self.order = None                       #Determine the order of play in game - default is None. 

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

    #Get the status of player in jail
    def getInJail(self):
        return self.inJail
    
    #Move the player across the board when it is their turn 
    def move(self, moveNum):

        #Check if the user is in jail 
        #TODO: Add logic regarding if user has jail-free cards or has money to self-bail 
        if (self.jail_turns > 0):
            return 0

        #Check if player rolled doubles 
        if TwoDice.double: 
            self.consecutiveDoubles += 1

            #Check if user goes to jail if 3 doubles in a row
            if self.consecutiveDoubles >= 3: 
                self.inJail = True
                self.position = Board.TILES_JAIL[0]
                self.consecutiveDoubles = 0 
                return #If going to jail, end the turn right here

        else: 
            #Reset consecutive doubles if different numbers are rolled
            self.consecutiveDoubles = 0 
        
        #Calculate new position of player
        newPosition = self.position + moveNum 

        #Check if player has cycled through the board
        if (newPosition > len(Board.TILES_LIST)):
            newPosition -= len(Board.TILES_LIST)
                
            #Collect more money
        
        #Add one to position if went past jail, assuming player was either starting next to jail 
        #Number 35 is the highest possible new position if user rolled doubles twice and was closest to jail by one spot
        if (newPosition >= Board.TILES_JAIL[0] and newPosition < 35) and (self.position < Board.TILES_JAIL[0] or self.position > 35):
            newPosition += 1
        
        #Apply new position 
        self.position = newPosition

    #Add a property/title deed to player's possession
    def addProperty(self, titleDeed): 
        self.properties.append(titleDeed)
    

    

        

            

            




