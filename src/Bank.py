from Title import Property, Utility, Transports

class Bank: 
    #Dollar Demoniations Avaiable - traditionally there are 30 bills each 
    #Typically about 20580, but this is not a hard number.  
    DOLLAR_AMOUNTS = [500, 100, 50, 20, 10, 5, 1]
    PASS_GO = 200
    STARTING_AMOUNT = 1500

    #Tax Amounts on Board
    INCOME_TAX = -200
    LUXURY_TAX = -100

    #Jail Fine Payment 
    JAIL_PAYMENT = 50

    #Interests
    MORTGAGE_INTEREST = 0.10

    #Utility/Transport Multipler
    RENT_MULTIPLER = 10

    #Numer of properties available
    HOMES_AVAILABLE = 4 * len(Property.PROPERTY_CARDS)
    HOTELS_AVAILABLE = 1 * len(Property.PROPERTY_CARDS)

    #TODO: May need to add logic regarding timing the auction 
    
    #Create a new bank
    def __init__(self): 
        self.moneyReserves = 20580

        #Create the title cards for possession 
        self.propertyCards = Property()
        self.utilityCards = Utility()
        self.transportsCards = Transports() 

        #Create the property quantities 
        self.homesAvailable = HOMES_AVAILABLE
        self.hotelsAvailable = HOTELS_AVAILABLE

        #Properties for auction
        self.auctionPrice = 0

    #Generate additional cash after each round - this is unique for this particular game implementation
    def generateCash(self): 
        self.moneyReserves *= 1.5
    
    #Get current money in bank 
    def getCurrentReserves(self):
        return self.moneyReserves

    #Add money to the bank 
    def add(self, amount): 
       self.moneyReserves += amount

    #Subtract money from the bank
    def subtract(self, amount):
        self.moneyReserves -= amount 

    #Retrieve the title deed. This assumes the bank has this card. 
    def getTitleDeedCard(self, titleName, boardTileName):
        if (boardTileName == "Property"):  
            for propertyCard in self.propertyCards: 
                if (propertyCard.getName() == titleName):
                    return propertyCard
            
            #Used if no property of name was found
            return None

        elif (boardTileName == "Utility"):
            for utilityCard in self.utilityCards: 
                if (utilityCard.getName() == titleName):
                    return utilityCard
            
            #Used if no utility of name was found
            return None

        elif (boardTileName == "Transports"):
            for transportsCard in self.transportsCards: 
                if (transportsCard.getName() == titleName):
                    return transportsCard

            #Used if no transports of name was found
            return None
        
        #Invalid item is used
        return None 

    #Remove a title deed from bank's possession 
    def removeTitleDeed(self, titleDeed): 
        titleType = titleDeed.getTitleType()
        titleName = titleDeed.getName() 

        if (titleType == "Property"):  
            for propertyCard in self.propertyCards: 
                if (propertyCard.getName() == titleName):
                    self.propertyCards.remove(propertyCard) 
                    return 
        
        elif (titleType == "Utility"):
            for utilityCard in self.utilityCards: 
                if (utilityCard.getName() == titleName):
                    self.utilityCards.remove(utilityCard) 
                    return 

        elif (titleType == "Transports"):
            for transportsCard in self.transportsCards: 
                if (transportsCard.getName() == titleName):
                    self.transportsCards.remove(transportsCard) 
                    return 
    
    #Add a title deed to bank's possession (e.g. player sells the card)
    def addTitleDeed(self, titleDeed): 
        titleType = titleDeed.getTitleType()

        if (titleType == "Property"):  
            self.propertyCards.append(titleDeed)
        elif (titleType == "Utility"):
           self.utilityCards.append(titleDeed)
        elif (titleType == "Transports"):
            self.transportsCards.append(titleDeed)

    def purchaseHome(self, paymentAmount): 
        self.homesAvailable -= 1
        self.add(paymentAmount)

    def purchaseHotel(self, paymentAmount):
        self.hotelsAvailable -= 1
        self.add(paymentAmount)

    def sellHome(self, refundAmount):
        self.homesAvailable += 1
        self.subtract(refundAmount)
    
    def sellHotel(self, refundAmount): 
        self.hotelsAvailable += 1 
        self.subtract(refundAmount)

    def returnHomesWithHotel(self): 
        self.homesAvailable += Property.HOMES_MAX
    
    def getHomesWithHotel(self): 
        self.homesAvailable -= Property.HOMES_MAX

    """ MORTGAGE methods """
    def giveMortgageLoan(self, mortgageValue):
        self.subtract(mortgageValue)
    
    def creditMortgagePayment(self, repayAmount): 
        self.add(repayAmount)

    """ AUCTION methods """
    def startAuction(self, startingPrice):
        self.auctionPrice = startingPrice

    def getAuctionPrice(self): 
        return self.auctionPrice
    
    def setAuctionPrice(self, auctionPrice):
        self.auctionPrice = auctionPrice
    
    def resetAuctionPrice(self):
        self.setAuctionPrice(0)
    