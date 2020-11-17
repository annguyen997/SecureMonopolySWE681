class Bank: 
    TOTAL_MONETARY = 20580

    #Dollar amounts available 

    #Create a new bank
    def __init__(self): 
        self.currentAmount = TOTAL_MONETARY
    
    #Add money to the bank 
    def add(self, amount): 
        
        #Check if added amount exceeds total monetary value available
        if (amount + self.currentAmount > TOTAL_MONETARY):
            return "Invalid amount reported. No changes." 

        self.currentAmount += amount

    #Subtract money from the bank
    def subtract(self, amount):
        #Check if requested amount results in insufficient funds in bank
        if (amount + self.currentAmount < 0):
            return "Supplied amount results in insufficient funds. No changes." 

        self.currentAmount -= amount
    
    
    