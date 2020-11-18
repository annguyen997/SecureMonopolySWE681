import TwoDice, utility
import Player 

class Game:

    #Instiates a new game
    def __init__(self):
        self.players = []
        self.currentPlayer = None 

    #Add Player to the game 
    def addPlayer(self, newPlayer): 
        self.players.append(newPlayer) 
        
        #May need to generate the Player object here 

    #Determine the player who gets to go first in the game
    def determineFirstPlayer(self): 
        playerListOrder = [] #Temporary list to order players by highest roller

        #Set the order by rolling dice 
        for player in self.players: 
            userID = player.getuserID()
            rollNumber = TwoDice.rollDice() 
            playerListOrder.append({'userID': userID, 'order' : rollNumber})

        #Order the players by the set order
        playerListOrder.sort(key=utility.rollOrder)

        #Check if list order has ties
        playerListOrder = utility.checkTies(playerListOrder)

        TwoDice.double = False #Reset double class variable should value have changed 

        


        


    
        
         