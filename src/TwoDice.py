#import statements
from random import randint

class TwoDice:
    dice1 = -1
    dice2 = -1
    total = 0
    double = False

    """
    def __init__(self):
        self.dice1 = -1
        self.dice2 = -1
        self.total = 0
        self.double = False
    """
    
    #Roll dice to move in the game or to determine player order
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
        else: 
            double = False 

        #Return the total for the player to move
        return total

    #Roll dice to break ties in player order 
    def rollDiceBreakTie(self):
        round1 = rollDice()
        round2 = rollDice()
        
        #If rolling dice second time is same as the first, roll again 
        while (round1 == round2):
            round2 = rollDice() 
        
        #Return the sum of two dice rounds
        return round1 + round2

    #Get the value of first die
    def getFirstDice(self): 
        return dice1
    
    #Get the value of the second die
    def getSecondDice(self): 
        return dice2

    #Get the value of both dice 
    def getTotal(self):
        return total 
            
            
