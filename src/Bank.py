class Bank: 
    #Dollar Demoniations Avaiable - traditionally there are 30 bills each 
    #Typically about 20580, but this is not a hard number.  
    DOLLAR_AMOUNTS = [500, 100, 50, 20, 10, 5, 1]
    PASS_GO = 200

    #TODO: May need to add logic regarding timing the auction 
    
    #Create a new bank
    def __init__(self): 
        self.moneyReserves = 20580
    
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
    
    