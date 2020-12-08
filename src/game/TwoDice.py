#import statements
import random
import sys

class TwoDice:

    def __init__(self):
        self.dice1 = -1
        self.dice2 = -1
        self.total = 0
        self.double = False
    
    #Roll dice to move in the game or to determine player order
    def rollDice(self):
        #Reset the total to zero
        total = 0 

        #Create a seed, and them seed the random number generator
        seedValue = random.randrange(sys.maxsize)
        random.seed(seedValue)

        #Roll the two dice   - Add a seed to the the random; don't hard code seed - true randomness of the seed  
        self.dice1 = random.randint(1,6)
        self.dice2 = random.randint(1,6)
        
        #Calculate the total 
        total = self.dice1 + self.dice2

        #Check if double have occurred
        if (self.dice1 == self.dice2):
            self.double = True
        else: 
            self.double = False

        #Return the total for the player to move
        return total

    #Roll dice to break ties in player order 
    def rollDiceBreakTie(self):
        round1 = self.rollDice()
        round2 = self.rollDice()
        
        #If rolling dice second time is same as the first, roll again 
        while (round1 == round2):
            round2 = self.rollDice()

        # Reset any double status if necessary
        self.resetDoubleStatus()

        #Return the sum of two dice rounds
        return round1 + round2

    #Get the value of first die
    def getFirstDice(self): 
        return self.dice1
    
    #Get the value of the second die
    def getSecondDice(self): 
        return self.dice2

    #Get the value of both dice 
    def getTotal(self):
        return self.total

    #Get the double status
    def getDoubleStatus(self): 
        return self.double

    #Reset the double status
    def resetDoubleStatus(self):
        self.double = False
