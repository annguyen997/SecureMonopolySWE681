#import statements
from random import randint

class TwoDice:
    dice1 = -1
    dice2 = -1
    total = 0
    double = False
    doubleOccurrence = 0

    """
    def __init__(self):
        self.dice1 = -1
        self.dice2 = -1
        self.total = 0
        self.double = False
    """
    
    def rollDice(self):
        #Reset the total to zero
        total = 0 

        #Roll the two dice  
        dice1 = randint(1,7)
        dice2 = randint(1,7)
        
        #Calculate the total 
        total = dice1 + dice2

        #Check if double have occurred
        if (dice1 == dice2): 
            double = True 

        #Return the total for the player to move
        return total 
    
    #Get the value of first die
    def getFirstDice(self): 
        return dice1
    
    #Get the value of the second die
    def getSecondDice(self): 
        return dice2

    #Get the value of both dice 
    def getTotal(self):
        return total 

    #Calculate mechanism if player gets a double
    def rolledDouble(self): 
        if TwoDice.double:
            TwoDice.doubleOccurrence += 1
            total = rollDice()

            if dice1 != dice2: 
                TwoDice.double = False
                TwoDice.doubleOccurrence = 0

            if TwoDice.doubleOccurrence == 3:
                TwoDice.double = False
                TwoDice.doubleOccurrence = 0

                #Return value indicating go to JAIL
                return 0
        
        return total 

            
            
