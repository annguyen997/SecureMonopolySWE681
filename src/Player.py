import Board, Bank

class Player():

    #It is possible to remove the titles; the bank itself can act as a player in an automated environment 
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
    def setPosition(self, position): 
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

    #Get the list of properties of player
    def getProperties(self): 
        return self.properties
    
    #Add a property to the player's list of possessions
    def addProperties(self, propertyCard): 
        self.properties.append(propertyCard)

    def getNumHomes(self): 
        return self.num_homes

    def getNumHotels(self): 
        return self.num_hotels 

    #Get the status of player in jail
    def getInJailStatus(self):
        return self.inJail
    
    #Set the in jail status
    def setInJailStatus(self, status): 
        self.inJail = status

    #Add a jail-free card to player's possesssion 
    def addEscapeJailCard(self, card): 
        self.jail_cards.append(card)

    #Remove a jail-free card from player's possession, starting with the most recent card first
    def removeEscapeJailCard(self):
        card = self.jail_cards.pop()
        return card

    def getJailTurns(self): 
        return self.jail_turns
    
    def setJailTurns(self, turns): 
        self.jail_turns = turns

    #Move the player across the board when it is their turn 
    def move(self, moveNum, dice, bank):
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
        
        #Add one to position if went past jail, assuming player was starting next to jail at minimum.
        #Number 35 is the highest possible new position if user rolled doubles twice and was closest to jail by one spot
        if (newPosition >= Board.TILES_JAIL[0] and newPosition < 35) and (self.getPosition() < Board.TILES_JAIL[0] or self.getPosition() > 35):
            newPosition += 1

        #Check if player has cycled through the board, assuming player does not go to jail directly
        if (newPosition > len(Board.TILES_LIST)):
            newPosition -= len(Board.TILES_LIST)
                
            #Collect more money by passing GO
            self.changeMonetaryValue(Bank.PASS_GO)
            bank.subtract(Bank.PASS_GO)
        
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
                #Player goes to jail directly, do not collect amount of passing GO
                self.setInJailStatus(True)
                self.setPosition(Board.TILES_JAIL[0])
            
            else: 
                #Advance to the spot on the board; collect 200 if necessary
                newPosition = cardValue + self.getPosition()

                #If player cycles through the board, re-calibrate the position number
                if (newPosition > len(Board.TILES_LIST)):
                    newPosition -= len(Board.TILES_LIST)
                
                    #Collect more money by passing GO
                    self.changeMonetaryValue(Bank.PASS_GO)
                    bank.subtract(Bank.PASS_GO)
                
                #Set new position
                self.setPosition(newPosition)

        elif cardKind == "Credit": 
            bank.subtract(cardValue)
            self.changeMonetaryValue(cardValue)
        elif cardKind == "Debit": 
            self.changeMonetaryValue(cardValue) 
            bank.add(abs(cardValue))
        elif cardKind == "Debit Complex": 
            #debit from each home and hotel 
            numHomePay = cardValue[0] * self.getNumHomes()
            numHotelPay = cardValue[1] * self.getNumHotels() 
            
            #Debit the amount from player 
            self.changeMonetaryValue(numHomePay + numHotelPay)

            #Add the amount to the bank 
            bank.add(abs(numHomePay + numHotelPay))
        elif cardKind == "Escape Jail":
            self.addEscapeJailCard(card)
    
    #Read and do the community card 
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
                self.setInJailStatus(True)
                self.setPosition(Board.TILES_JAIL[0])
            
        elif cardKind == "Credit": 
            bank.subtract(cardValue)
            self.changeMonetaryValue(cardValue)
        elif cardKind == "Debit": 
            self.changeMonetaryValue(cardValue) 
            bank.add(abs(cardValue))
        elif cardKind == "Debit Complex": 
            #debit from each home and hotel 
            numHomePay = cardValue[0] * self.getNumHomes()
            numHotelPay = cardValue[1] * self.getNumHotels() 
            
            #Debit the amount from player 
            self.changeMonetaryValue(numHomePay + numHotelPay)

            #Add the amount to the bank 
            bank.add(abs(numHomePay + numHotelPay)) 
        elif cardKind == "Escape Jail":
            self.addEscapeJailCard(card)

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

    #Options to escape jail 
    def escapeJailOptions(self): 
        print("You are currently in jail, and you have " + self.getJailTurns() + " left in jail." + 
              "\nYou do have three options if you wish to get out of jail early.")
        
        #Pay 50 fine
        #Use get out of jail free card
        #Roll a double 

    #Add a property/title deed to player's possession
    def addProperty(self, titleDeed): 
        self.properties.append(titleDeed)
    
    #Add money to auction - this requires inputting valid dollar amount



    

        

            

            




