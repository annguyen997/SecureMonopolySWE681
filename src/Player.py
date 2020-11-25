import Board, Bank
from Title import Title, Property, Utility, Transports

class Player():
    #Dual means both Regular and Banker, used only if there are less than 5 players; Bank can be automated
    #PLAYER_TITLES = ["Regular", "Banker/Auctioneer", "Dual"] 

    PLAYER_MINIMUM = 2
    PLAYER_MAXIMUM = 8
    
    def __init__(self, id, name):
        self.id = id                            #Identification Number
        self.name = name                        #Name of player
        self.money = 0                          #Cash on hand - starts with 1500
        self.position = 0                       #Position ranges from 0 - 40 (for game's 41 spaces) - Start at "Go" tile
        self.titleDeeds = []                    #Start with no properties
        self.jail_cards = []                    #Jail cards in posession 
        self.jail_turns = 0                     #Number of remaining turns in jail
        self.bankrupt = False                   #Bankrupt status
        self.inJail = False                     #Check if user is in jail 

        self.consecutiveDoubles = 0             #Start with no doubles 
        self.order = None                       #Determine the order of play in game - default is None. 

        self.num_homes = 0                      #Number of homes in total 
        self.num_hotels = 0                     #Number of hotels in total 

    #Get the id of user
    def getuserID(self): 
        return self.id 
    
    #Get the name of user
    def getName(self): 
        return self.name 

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
    
    #Get the list of properties of player
    def getTitleDeeds(self): 
        return self.titleDeeds
    
    #Add a title deed to the player's list of possessions
    def addTitleDeeds(self, titleDeed): 
        self.titleDeeds.append(titleDeed)

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
        if dice.getDoubleStatus(): 
            self.consecutiveDoubles += 1

            #Check if user goes to jail if 3 doubles in a row
            if self.consecutiveDoubles >= 3: 
                self.setInJailStatus(True)
                self.setPosition(Board.TILES_JAIL[0])
                self.consecutiveDoubles = 0 

                #Rese the dice's double status
                dice.resetDoubleStatus()

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
            #Record user was on this space first
            self.board.hit(position)

            #Read the values, and do the actions based on the vaue
            if cardValue == "Go": 
                self.setPosition(Board.TILES_GO[0])

                #Collect money
                self.changeMonetaryValue(Board.PASS_GO)
                bank.subtract(Board.PASS_GO)

            elif cardValue == "Utility":
                #Keep track if nearest utility is found 
                found = False 
                newPositionUtility = None

                #Go to the nearest utility
                for posUtil in Board.TILES_UTILITY: 
                    if position < posUtil: 
                        newPositionUtility = posUtil
                        found = True
                        break 
                
                #If not nearest utility found, go to first utility. 
                #Note it may be possible that user does not collect cash if passing Go
                if not found:
                    newPositionUtility = Board.TILES_UTILITY[0]

                #If player would cycle the board, re-calibrate the position number and collect 200 if necessary
                if (newPositionUtility < position):
                    #Collect more money by passing GO
                    self.changeMonetaryValue(Bank.PASS_GO)
                    bank.subtract(Bank.PASS_GO)

                self.setPosition(newPositionUtility)
            
            elif cardValue == "Transports":
                #Keep track if nearest transports is found 
                found = False 
                newPositionTransports = None

                #Go to the nearest transport
                for posTransports in Board.TILES_TRANSPORTS: 
                    if position < posTransports: 
                        newPositionTransports = posTransports
                        found = True
                        break 
                
                #If not nearest utility found, go to first transports. 
                #Note it may be possible that user does not collect cash if passing Go
                if not found:
                    newPositionTransports = Board.TILES_TRANSPORTS[0]
                
                #If player would cycle the board, re-calibrate the position number and collect 200 if necessary
                if (newPositionTransports < position):
                    #Collect more money by passing GO
                    self.changeMonetaryValue(Bank.PASS_GO)
                    bank.subtract(Bank.PASS_GO)

                self.setPosition(newPositionTransports)
            
            elif cardValue <= 0: 
                #If negative, this means player must go back
                newPosition = position + cardValue 
                self.setPosition(newPosition)

            elif cardValue == "Go to Jail": 
                #Player goes to jail directly, do not collect amount of passing GO
                self.setInJailStatus(True)
                self.setPosition(Board.TILES_JAIL[0])
            
            else: 
                #If player would cycle the board, re-calibrate the position number and collect 200 if necessary
                if (cardValue < position):
                    #Collect more money by passing GO
                    self.changeMonetaryValue(Bank.PASS_GO)
                    bank.subtract(Bank.PASS_GO)
                
                #Set new position
                self.setPosition(cardValue)

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

        #Do actions based on community card 
        if cardKind == "Advance": 
            #Record user was on this space first
            self.board.hit(position)

            #Read the values, and do the actions based on the vaue
            if cardValue == "Go": 
                self.setPosition(Board.TILES_GO[0])
                
                #Collect money
                self.changeMonetaryValue(Board.PASS_GO)
                bank.subtract(Board.PASS_GO)

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

    #Options to escape jail - Note player can collect rent, but cannot do any changes on title deeds at this time. 
    def escapeJailOptions(self): 
        print("You are currently in jail, and you have " + self.getJailTurns() + " left in jail." + 
              "\nYou do have three options if you wish to get out of jail early." + 
              "\nPay 50 dollar fine - Type 'Pay 50' to use this option." +
              "\nUse a get out of jail free card - Type 'Jail Free Card' to use this option." + 
              "\nRoll a double - Type 'Roll Dice' to use this option.")

        jailOption = input("Select an option based on the options listed.")
        
        #Pay 50 fine
        #Use get out of jail free card
        #Roll a double 

    #User pays the rent to the other player
    def payRent(self, owner, titleDeedName, boardTile, dice):
        titleDeedCard = None

        #Get the title deed information 
        titleDeedsList = owner.getTitleDeeds() 
        for titleDeed in titleDeedsList: 
            if (titleDeedName == titleDeed.getName()):
                titleDeedCard = titleDeed

        #Check if the property is in mortgage, if so do not collect rent

        #Check if the owner owns a monopoly - that is owns all title deeds of that color group 
        #If so, check if that title deed is undeveloped

        #Check if that property contains homes or hotels

        #If utility, roll dice, and the value is 4x roll multiply by 10
        if (boardTile == "Utility"): 
            diceRoll = dice.rollDice()
            
            #if owner has both utilities - use 10 
            #Get the rent amount
            rentAmount = diceRoll * titleDeedCard.getRentCosts[Utility.UTILITY_ONE] * Bank.RENT_MULTIPLER

            #Make the rent payment
            self.changeMonetaryValue(-1 * rentAmount)
            owner.changeMonetaryValue(rentAmount) 

        #If transports... 
        if (boardTile == "Transports"):
            pass

    #Add a title deed to player's possession
    def addTitleDeed(self, titleDeed, purchaseValue, bank): 
        #Add title deed to posession
        self.addTitleDeeds(titleDeed)

        #Remove card from bank's possession
        bank.removeTitleDeed(titleDeed)

        #Set the owner to the title deed 
        titleDeed.setOwner(self.getName())

        #Make the purchase 
        self.changeMonetaryValue(-1 * purchaseValue)
        bank.add(purchaseValue)
    
    #Remove a title deed from player's possession 
    #For properties, this assumes the player does not have any buildings on that property
    def removeTitleDeed(self, titleDeed, bank): 
        pass 

    #def purchaseHome()
    #def purchaseHotel()
    #def sellHome()
    #def sellHotel() 

    def handleExistingTitleDeeds(self): 
        #May need a while loop to loop through options continuously until user wishes to end the round

        #If user wishes to mortgage on a particular property - if so check if there are homes/hotels in any cards in group
        #Note other players cannot assist player on a mortgaged property, though can collect rent on other properties of that smae color group.

        #If user wishes to repay the mortgage on a particular property - pay 10% interest to the nearest 10

        #If user wishes to purchase a house - check if (1) player owns a monopoly on a color group, and then (2) homes are evenly purchased on other properties
        #The property also must not be mortgaged as well as others in color group

        #If user wishes to purchase a hotel - check if (1) player owns a monopoly on a color group, and then (2) 4 homes are evenly purchased for each property
        #The property also must not be mortgaged as well as others in color group

        #Also add logic that a player cannot add any more houses or hotels once reach maximum limit

        #If user wishes to sell a house, get property name. Ensure homes are evenly available on other properties before selling
        #If user wishes to sell a hotel, get property name. Also get 4 homes back. 
        
        #If user wishes to sell a property to another user - ensure there are no buildings

        #If user wishes to sell a mortgaged property to another user - ensure there are no buildings

        #If user wishes to sell a utility or transports to another user


        pass

    #Check if user has run out of cash
    def runOutOfCash(self): 
        if (self.getMonetaryValue() <= 0): 
            return True #User does not have cash 
        return False 
    
    #If bankrupt, start the destruction process
    def declareBankruptcy(self): 
        pass 

            

            




