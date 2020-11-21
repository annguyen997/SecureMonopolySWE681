import Board, Bank

class Player():

    PLAYER_TITLES = ["Regular", "Banker/Auctioneer", "Dual"]  #Dual means both Regular and Banker, used only if there are less than 5 players
    PLAYER_MINIMUM = 2
    PLAYER_MAXIMUM = 8 
    PLAYER_BANKER_LIMIT = 5 #If there are more than 5 players in game, one person must be Banker/Auctioneer only 
    
    def __init__(self, id, name):
        self.id = id                            #Identification Number
        self.name = name                        #Name of player
        self.money = 0                          #Cash on hand - starts with 1500
        self.position = 0                       #Position ranges from 0 - 40 (for game's 41 spaces) - Start at "Go" tile
        self.properties = []                    #Start with no properties
        self.jail_cards_Num = 0                 #Number of "Get Out of Jail Free" cards
        self.jail_cards = []                    #Jail cards in posession 
        self.jail_turns = 0                     #Number of remaining turns in jail
        self.bankrupt = False                   #Bankrupt status
        self.title = PLAYER_TITLES["Regular"]   #Title of player - Default is Regular
        self.inJail = False                     #Check if user is in jail 

        self.consecutiveDoubles = 0             #Start with no doubles 
        self.order = None                       #Determine the order of play in game - default is None. 

        self.num_homes = 0                      #Number of homes in total 
        self.num_hotels = 0                     #Number of hotels in total 

    #Get the id of user
    def getuserID(self): 
        return self.id 

    #Get the monetary value of the player
    def getMonetaryValue(self): 
        return self.money 
    
    #Add money to or subtract money from player
    def changeMonetaryValue(self, amount): 
        self.money += amount
    
    #Get the position of the player on the board
    def getPosition(self): 
        return self.position 

    #Set the position of player on board
    def setPosition (self, position): 
        self.position = position 

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
    def getInJailStatus(self):
        return self.inJail
    
    def setInJailStatus(self, status): 
        self.inJail = status
    
    #Move the player across the board when it is their turn 
    def move(self, moveNum, dice, bank):

        #Check if the user is in jail 
        #TODO: Add logic regarding if user has jail-free cards or has money to self-bail 
        if (self.jail_turns > 0):
            return 0

        #Check if player rolled doubles 
        if dice.double: 
            self.consecutiveDoubles += 1

            #Check if user goes to jail if 3 doubles in a row
            if self.consecutiveDoubles >= 3: 
                self.setInJailStatus(True)
                self.setPosition(Board.TILES_JAIL[0])
                self.consecutiveDoubles = 0 
                return #If going to jail, end the turn right here

        else: 
            #Reset consecutive doubles if different numbers are rolled
            self.consecutiveDoubles = 0 
        
        #Calculate new position of player
        newPosition = self.getPosition() + moveNum 

        #Check if player has cycled through the board
        if (newPosition > len(Board.TILES_LIST)):
            newPosition -= len(Board.TILES_LIST)
                
            #Collect more money
        
        #Add one to position if went past jail, assuming player was either starting next to jail 
        #Number 35 is the highest possible new position if user rolled doubles twice and was closest to jail by one spot
        if (newPosition >= Board.TILES_JAIL[0] and newPosition < 35) and (self.getPosition() < Board.TILES_JAIL[0] or self.getPosition() > 35):
            newPosition += 1
        
        #Apply new position 
        self.setPosition(newPosition)
    
    #Read and do the chance card 
    def doChanceCard(self, card, bank): 
        #Get user's position 
        position = self.getPosition() 

        #Get the type of chance card and the associated value
        cardKind = card.getKind()
        cardValue = card.getValue() 

        #Do actions based on chance card 
        if cardKind == "Advance": 
            #Read the values, and do the actions based on the vaue
            if cardValue == "Go": 
                self.setPosition(Board.TILES_GO[0])
                #Collect money

            elif cardValue == "Utility":
                #Keep track if nearest utility is found 
                found = False 

                #Go to the nearest utility
                for posUtil in Board.TILES_UTILITY: 
                    if position < posUtil: 
                        self.setPosition(posUtil)
                        found = True
                        break 
                
                #If not nearest utility found, go to first utility. 
                #Note it may be possible that user does not collect cash if passing Go
                if not found:
                    self.setPosition(Board.TILES_UTILITY[0])
            
            elif cardValue == "Transports":
                #Keep track if nearest transports is found 
                found = False 

                #Go to the nearest utility
                for posUtil in Board.TILES_TRANSPORTS: 
                    if position < posUtil: 
                        self.setPosition(posUtil)
                        found = True
                        break 
                
                #If not nearest utility found, go to first transports. 
                #Note it may be possible that user does not collect cash if passing Go
                if not found:
                    self.setPosition(Board.TILES_TRANSPORTS[0])
            
            elif cardValue <= 0: 
                #If negative, this means player must go back
                newPosition = position + cardValue 
                self.setPosition(newPosition)

            elif cardValue == "Go to Jail": 
                pass
        
        elif cardKind == "Credit": 
            bank.subtract(cardValue)
            self.changeMonetaryValue(cardValue)
        elif cardKind == "Debit": 
            if (len(cardValue) > 1): 
                pass
                #debit from each home and hotel 
            else: 
                self.changeMonetaryValue(cardValue)
                bank.add(cardValue) 
        elif cardKind == "Escape Jail":
            pass
            #TODO: Get possession of the card for user to hold
    
     #Read and do the chance card 
    def doCommunityCard(self, card, bank): 
        #Get user's position 
        position = self.getPosition() 

        #Get the type of chance card and the associated value
        cardKind = card.getKind()
        cardValue = card.getValue() 

        #Do actions based on chance card 
        if cardKind == "Advance": 
            #Read the values, and do the actions based on the vaue
            if cardValue == "Go": 
                self.setPosition(Board.TILES_GO[0])
                #Collect money
            
            elif cardValue == "Go to Jail": 
                pass
            
        elif cardKind == "Credit": 
            bank.subtract(cardValue)
            self.changeMonetaryValue(cardValue)
        elif cardKind == "Debit":
            if (len(cardValue) > 1): 
                pass
                #debit from each home and hotel 
            else: 
                self.changeMonetaryValue(cardValue)
                bank.add(cardValue) 
        elif cardKind == "Escape Jail":
            pass
            #TODO: Get possession of the card for user to hold
    
    #User pays tax if lands on a tax tile
    def payTax(self, bank): 
        #Get position of player to get tax type, and create value to hold tax amount
        position = self.getPosition()
        taxCharged = 0 
        
        #Get the type of tax 
        if (Board.TILES_LIST[position] == "Income Tax"):
            taxCharged = Bank.INCOME_TAX
        elif (Board.TILES_LIST[position] == "Luxury Tax"):
            taxCharged = Bank.LUXURY_TAX

        #Tax the player, and add the money to bank
        self.changeMonetaryValue(taxCharged)
        bank.add(abs(taxCharged))

    #Add a property/title deed to player's possession
    def addProperty(self, titleDeed): 
        self.properties.append(titleDeed)
    

    

        

            

            




