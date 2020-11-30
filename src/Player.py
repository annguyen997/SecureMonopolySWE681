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
        self.bankrupt = False                   #Bankrupt status
        
        self.inJail = False                     #Check if user is in jail 
        self.jail_cards = []                    #Jail cards in posession 
        self.jail_turns = 0                     #Number of remaining turns in jail

        self.consecutiveDoubles = 0             #Start with no doubles 
        self.order = None                       #Determine the order of play in game - default is None. 

        self.titleDeeds = []                    #Start with no title deeds owned
        self.propertyOwned = 0                  #Number of properties owned 
        self.colorMonopoly = []                 #List of color group monopolies owned 
        self.utilityOwned = 0                   #Number of utilities owned
        self.transportsOwned = 0                #Number of transports owned

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
        titleType = titleDeed.getTitleType() 

        if (titleType == "Property"): 
            self.titleDeeds.append({"Title Deed": titleDeed, "Mortgaged": False, "Houses": 0, "Hotels": 0, "Color Group": titleDeed.getColorGroup()})
            self.propertyOwned += 1
            
            #Check if adding the property means the player has a monopoly
            colorGroupName = titleDeed.getColorGroup() 
            colorGroupList = Property.getColorGroup(colorGroupName)

            createMonopoly = True
            for propertyItem in colorGroupList:
                if (propertyItem == titleDeed.getName()): 
                    #Property item refers to the title deed being added 
                    continue
                elif (not propertyItem in self.titleDeeds):
                    #If given property item is not part of the owner's list of title deeds
                    createMonopoly = False 
                    break 

            if (createMonopoly): 
                self.colorMonopoly.append({"Color Group": colorGroupName, "Number Houses Built": 0, "Number Hotels Built": 0})

        elif (titleType == "Utility"):
            self.titleDeeds.append({"Title Deed": titleDeed, "Mortgaged": False, "Houses": None, "Hotels": None, "Color Group": None}) 
            self.utilityOwned += 1
        elif(titleType == "Transports"): 
            self.titleDeeds.append({"Title Deed": titleDeed, "Mortgaged": False, "Houses": None, "Hotels": None, "Color Group": None}) 
            self.transportsOwned += 1
    
    #Remove a title deed from a player's list of possessions 
    def removeTitleDeed(self, titleDeedName): 
        pass
        #Check if removing property would result in player to lose monopoly
    
    def getPropertyOwned(self): 
        return self.propertyOwned
    
    def getColorMonopoly(self):
        return self.colorMonopoly
    
    def getUtilityOwned(self):
        return self.utilityOwned
    
    def getTransportsOwned(self):
        return self.transportsOwned

    #Get total number of homes owned
    def getNumHomes(self): 
        return self.num_homes
    
    #Get total number of hotels owned 
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
    
    #Check if there are jail cards available 
    def jailCardsAvailable(self): 
        if (len(self.jail_cards) > 0): 
            return True
        return False

    #Get the current number of jail turns
    def getJailTurns(self): 
        return self.jail_turns
    
    #Set the number of jail turns
    def setJailTurns(self, turns): 
        self.jail_turns = turns
    
    #Subtract the number of jail turns
    def subtractJailTurns(self): 
        self.jail_turns -= 1

    #Get the bankrupt status
    def getBankruptStatus(self):
        return self.bankrupt
    
    #Set the bankrupt status
    def setBankruptStatus(self, status = False): 
        self.bankrupt = status

    """Methods associated with the player interacting in the game """
    #Move the player across the board when it is their turn 
    def move(self, moveNum, dice, bank = None):
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
                print("You have been sent to jail.")
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

    #Options to escape jail - Note player can collect rent (provided not mortgaged) or make changes to the title deeds
    def escapeJailOptions(self, bank, dice): 
        #Return the Get Out of Jail Free card to the deck in game if used 
        card = None
        validOptionSelected = False

        jailMessage = "You are currently in jail, and you have " + self.getJailTurns() + " left in jail."
        + "\nYou do have the following options if you wish to get out of jail early." 
        + "\n1. Pay 50 dollar fine - Type 'Pay 50' to use this option." 
        + "\n2. Roll a double - Type 'Roll Dice' to use this option."
        
        if (self.jailCardsAvailable()): 
            jailMessage += "\n3. Use a get out of jail free card - Type 'Jail Free Card' to use this option."
        
        while (not validOptionSelected): 
            print(jailMessage)
            jailOption = input("Select an option based on the options listed.") #This needs to be validated
        
            #Pay 50 fine, user may not go forward until the next turn
            if (jailOption == "Pay 50"): 
                self.changeMonetaryValue(-1 * Bank.JAIL_PAYMENT)
                bank.add(Bank.JAIL_PAYMENT)

                #Reset the statuses 
                self.setInJailStatus(False)
                self.setJailTurns(0)

                #Player goes to just visiting jail 
                self.setPosition(Board.TILES_LIST["Just Visiting"])

                validOptionSelected = True

            #Use get out of jail free card
            elif (jailOption == "Jail Free Card" and self.jailCardsAvailable()): 
                card = self.removeEscapeJailCard() 

                #Reset the statuses 
                self.setInJailStatus(False)
                self.setJailTurns(0)

                #Player goes to just visiting jail 
                self.setPosition(Board.TILES_LIST["Just Visiting"])

                validOptionSelected = True
            
            #Roll a double
            elif (jailOption == "Roll Dice"):
                total = dice.rollDice()

                #If player rolls a double 
                if (dice.getDoubleStatus()):
                    #Advance to the tile according to your roll
                    #Calculate new position of player
                    newPosition = self.getPosition() + total

                    #Apply new position 
                    self.setPosition(newPosition)

                    #Reset the statuses 
                    self.setInJailStatus(False)
                    self.setJailTurns(0)

                    #Reset the double status - user does not do another dice roll
                    dice.resetDoubleStatus()

                    validOptionSelected = True
                else: 
                    print("You did not roll a double, and thus you must remain in jail.") 

                    #Reduce one jail turn 
                    self.subtractJailTurns()

                    #If this results in no more jail turns left, player must pay 50. If so reset statuses. 
                    if (self.getJailStatus == 0): 
                        print("You may now escape jail as a result, but you must pay 50 to the bank.")
                        self.changeMonetaryValue(-1 * Bank.JAIL_PAYMENT)
                        bank.add(Bank.JAIL_PAYMENT)
                        #Reset the statuses 
                        self.setInJailStatus(False)
                        self.setJailTurns(0)
                        self.setPosition(Board.TILES_LIST["Just Visiting"])
                        
                        #By virtue, valid option does not need to be selected
                        validOptionSelected = True
            else:
                if (jailOption == "Jail Free Card"): 
                    print("You do not have any jail free cards you can use at this time.")
                
                #Print message reporting user did not type in a valid response. 
                print("You did not select a valid option to escape jail. Please try again.")
        
        return card 

    #User pays the rent to the other player
    #Check if the current player has run out of money but still has property - i.e. owes debt
    def payRent(self, owner, titleDeedName, boardTile, dice):
        titleDeedCard = None
        titleDeedRecord = None
        rentAmount = 0

        #Get the title deed information 
        titleDeedsList = owner.getTitleDeeds() 
        for titleDeedItem in titleDeedsList: 
            if (titleDeedName == titleDeedItem["Title Deed"].getName()):
                titleDeedRecord = titleDeedItem
                titleDeedCard = titleDeedItem["Title Deed"]
        
        #No payment can be made given no information is available 
        if (titleDeedCard == None): 
            print("There is no title deed card information available for " + titleDeedName)
            return 

        #Check if the title deed is in mortgages, if so do not collect rent
        if (titleDeedRecord["Mortgaged"]):
            print("This property " + titleDeedCard.getName() + " is currently mortgaged, and rent cannot be collected at this time.") 
            return #Go back to the caller function; do not collect rent

        #If title deed is a property, additional checking is needed to determine the rent value.
        if (boardTile == "Property"): 
            #Check if the owner owns a monopoly - that is owns all title deeds of that color group 
            colorGroup = titleDeedCard.getColorGroup() 

            #If the owner has a monopoly on that color group
            if (colorGroup in owner.getColorMonopoly()): 
                #Get the number of houses and hotels of that property
                num_Houses = titleDeedRecord["Houses"]
                num_Hotels = titleDeedRecord["Hotels"]

                if (num_Houses): 
                    #There is at least one house on the property
                    rentAmount = titleDeedCard.getRentCosts(Property.HOMES_RENT[num_Houses - 1])
                elif (num_Hotels): 
                    #There may be no homes on the property, but there is a hotel 
                    rentAmount = titleDeedCard.getRentCosts(Property.HOTELS_RENT)
                else: 
                    #This is an undeveloped site 
                    rentAmount = titleDeedCard.getRentValue() * Property.DOUBLE_RENT
            else: 
                #There is no monopoly on the color group associated for that property
                rentAmount = titleDeedCard.getRentValue() 

        #If utility, roll dice, and the rental amount based on number of utilities owned
        elif (boardTile == "Utility"): 
            #Roll the dice
            diceRoll = dice.rollDice()
            
            #If owner has both utilities - use 10 
            if (owner.getUtilityOwned() == Utility.UTILITY_BOTH):
                rentAmount = diceRoll * titleDeedCard.getRentCosts[Utility.UTILITY_BOTH - 1] * Bank.RENT_MULTIPLER
            else: #If owner owns this utility only - use 4
                rentAmount = diceRoll * titleDeedCard.getRentCosts[Utility.UTILITY_ONE - 1] * Bank.RENT_MULTIPLER

        #If transports, calculate the rent amount based on number of transports title deeds owned by owner
        elif (boardTile == "Transports"):
            #Get the number of transports owned by the owner
            transportsOwned = owner.getTransportsOwned() 

            #Calculate the rental payment
            rentAmount = titleDeedCard.getRentCosts[transportsOwned - 1] 

        #Make the rental payment to owner        
        self.changeMonetaryValue(-1 * rentAmount)
        owner.changeMonetaryValue(rentAmount) 
            
        #Reset the dice's doubles
        dice.resetDoubleStatus() 

    #Add a title deed to player's possession
    def addTitleDeed(self, titleDeed, purchaseValue, bank): 
        #Add title deed to possession
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

    #Purchase a home for the property
    def purchaseHome(self, propertyName, buildingCost, bank):
        propertyFound = False
        colorGroup = None
        propertyRecord = None

        #Search for the property 
        for titleDeed in self.titleDeeds: 
            if (titleDeed["Title Deed"].getName() == propertyName):
                propertyFound = True
                colorGroup = titleDeed["Title Deed"].getColorGroup()
                propertyRecord = titleDeed
        
        #Add the house to the property name if found
        if (propertyFound): 
            propertyRecord["Houses"] = propertyRecord["Houses"] + 1
            self.num_homes += 1
        
        #Add the number of houses built for that monopoly
        for monopolyColor in self.colorMonopoly:
            if (colorGroup == monopolyColor["Color Group"]):
                monopolyColor["Number of Houses Built"] = monopolyColor["Number of Houses Built"] + 1
        
        #Make the purchase
        self.changeMonetaryValue(-1 * buildingCost) 
        bank.purchaseHome(buildingCost)
    
    #Purchase a hotel for the property, and return four houses to the bank
    def purchaseHotel(self, propertyName, buildingCost, bank): 
        propertyFound = False
        colorGroup = None
        propertyRecord = None

        #Search for the property 
        for titleDeed in self.titleDeeds: 
            if (titleDeed["Title Deed"].getName() == propertyName):
                propertyFound = True
                colorGroup = titleDeed["Title Deed"].getColorGroup()
                propertyRecord = titleDeed
        
        #Add the hotel to the property name if found, return four houses
        if (propertyFound): 
            propertyRecord["Hotels"] = propertyRecord["Hotels"] + 1
            self.num_hotels += 1

            propertyRecord["Houses"] = 0
            self.num_homes -= Property.HOMES_MAX

        #Add the number of hotels built for that monopoly, and reflect four houses returned
        for monopolyColor in self.colorMonopoly:
            if (colorGroup == monopolyColor["Color Group"]):
                monopolyColor["Number of Hotels Built"] = monopolyColor["Number of Hotels Built"] + 1
                monopolyColor["Number of Houses Built"] = monopolyColor["Number of Hotels Built"] - Property.HOMES_MAX
        
        #Make the purchase
        self.changeMonetaryValue(-1 * buildingCost) 
        bank.purchaseHotel(buildingCost)
        
        #Return four houses back to the bank
        bank.returnHomesWithHotel()
    
    #Sell a home from the property
    def sellHome(self, propertyName, sellingAmount, bank): 
        propertyFound = False
        colorGroup = None
        propertyRecord = None

        #Search for the property 
        for titleDeed in self.titleDeeds: 
            if (titleDeed["Title Deed"].getName() == propertyName):
                propertyFound = True 
                colorGroup = titleDeed["Title Deed"].getColorGroup()
                propertyRecord = titleDeed
        
        #Remove the house to the property name if found
        if (propertyFound): 
            propertyRecord["Houses"] = propertyRecord["Houses"] - 1
            self.num_homes -= 1
        
        #Add the number of houses built for that monopoly
        for monopolyColor in self.colorMonopoly:
            if (colorGroup == monopolyColor["Color Group"]):
                monopolyColor["Number of Houses Built"] = monopolyColor["Number of Houses Built"] - 1
        
        #Make the purchase
        self.changeMonetaryValue(sellingAmount) 
        bank.sellHome(sellingAmount)
    
    #Sell a hotel from the property, and get four houses back from the bank
    def sellHotel(self): 
        pass

    #Add a mortgage to a property
    def addMortgage(self, propertyName, mortgageValue, bank): 
        for titleDeed in self.titleDeeds: 
            if (titleDeed["Title Deed"].getName() == propertyName): 
                titleDeed["Mortgaged"] = True
        
        bank.giveMortgageLoan(mortgageValue)
        self.changeMonetaryValue(mortgageValue)

    #Remove and repay a mortgage from a property
    def removeMortgage(self, propertyName, repayAmount, bank): 
        for titleDeed in self.titleDeeds: 
            if (titleDeed["Title Deed"].getName() == propertyName): 
                titleDeed["Mortgaged"] = False
    
        self.changeMonetaryValue(-1 * repayAmount)
        bank.creditMortgagePayment(repayAmount)

    #Check if user has run out of cash
    def runOutOfCash(self): 
        if (self.getMonetaryValue() <= 0): 
            return True #User does not have cash 
        return False 
    
    #If bankrupt, start the destruction process
    def declareBankruptcy(self): 
        pass 

    
            

            




