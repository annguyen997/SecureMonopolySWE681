#import statements
from random import randint

class TwoDice:

    def __init__(self):
        self.dice1 = -1
        self.dice2 = -1
        self.total = 0 
    

    def rollDice(self):
        #Roll the two dice  
        self.dice1 = randint(1,6)
        self.dice2 = randint(1,6)
        
        #Calculate the total 
        total = dice1 + dice2

        #Return the total for the game
        return total 
    
    #Get the value of first die
    def getFirstDice(self): 
        return self.dice1
    
    #Get the value of the second die
    def getSecondDice(self): 
        return self.dice2

    #Get the value of both dice 
    def getTotal(self):
        return self.total 
