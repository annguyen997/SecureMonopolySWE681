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
    
    #Determine the player as banker
    def setBanker(self, player):
        if (len(self.players) <= Player.PLAYER_BANKER_LIMIT):
            player.setTitle("Dual")
        else: 
            player.setTitle("Banker/Auctioneer")

    #Determine the player who gets to go first in the game
    def determineFirstPlayer(self): 
        playerListOrder = [] #Temporary list to order players by highest roller

        #Set the order by rolling dice 
        for player in self.players: 

            #If player is banker/auctioneer (non-dual role), player's order is not calculated. 
            if (player.gettitle == "Banker/Auctioneer"):
                continue 

            userID = player.getuserID()
            rollNumber = TwoDice.rollDice() 
            playerListOrder.append({'userID': userID, 'order' : rollNumber})

        #Order the players by the set order
        playerListOrder.sort(key=utility.rollOrder)

        #Check if list order has ties
        playerListOrder = utility.checkTies(playerListOrder)

        #Order the main players list based on player order 
        #TODO: Organize main player list based on order in playerListOrder
        
        #Reset double class variable should value have changed 
        TwoDice.double = False

        


        


    
        
         