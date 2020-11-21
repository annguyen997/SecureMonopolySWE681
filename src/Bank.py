from Title import Property, Utility, Transports

class Bank: 
    #Dollar Demoniations Avaiable - traditionally there are 30 bills each 
    #Typically about 20580, but this is not a hard number.  
    DOLLAR_AMOUNTS = [500, 100, 50, 20, 10, 5, 1]
    PASS_GO = 200

    #Tax Amounts on Board
    INCOME_TAX = -200
    LUXURY_TAX = -100

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

    #Perform a transaction between two accounts
    def transaction(self, amount, receiver): 
        pass

    """ PROPERTIES """
    def getPropertyCard(self, titleName): 
        for propertyCard in self.propertyCards: 
            if (propertyCard.getName() == titleName):
                return propertyCard
        
        #Used if an invalid property was returned
        return "Invalid Property"

    def purchaseHome(self): 
        pass

    def purchaseHotel(self):
        pass

    def sellHome(self):
        pass
    
    def sellHotel(self): 
        pass 
    
    
    