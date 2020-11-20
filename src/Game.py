import TwoDice, utility
import Player, Board, Card

class Game:

    #Instiates a new game
    def __init__(self):
        self.players = []
        self.currentPlayer = None
        self.board = Board() 
        self.chancePile = Card.ChanceCards() 

    #Return first player of game based on the rolling
    def firstPlayer(self): 
        return self.players[0]
    
    #Return current player in game
    def currentPlayer(self):
        return self.currentPlayer
    
    #Go to the next player in game, or set first player if new game
    def goToNextPlayer(self, newGame = False): 
        if ((newGame) or self.currentPlayer["Index"] == len(self.players)):
            #Go to first player if new game or complete round 
            self.currentPlayer = {"Player": firstPlayer(), "Index": 1}
        else: 
            #If game in progress and no need to begin new round, set next player via indexing
            newIndex = self.currentPlayer["Index"] + 1 
            self.currentPlayer["Player"] = self.currentPlayer[newIndex-1]
            self.currentPlayer["Index"] = newIndex

    #Add player to the game - if players are added post-roll, they are included at the end
    def addPlayer(self, id, name): 
        if (len(self.player) < Player.PLAYER_MAXIMUM):
            self.players.append(Player(id, name))

    #Remove player from game - due to bankruptcy, connection timeout, quit, or etc. 
    #This would not affect the ordering of other players.
    def removePlayer(self, id): 
        pass

    #Determine the player as banker
    def setBanker(self, player):
        if (len(self.players) <= Player.PLAYER_BANKER_LIMIT):
            player.setTitle("Dual")
        else: 
            player.setTitle("Banker/Auctioneer")

    #Determine the player who gets to go first in the game
    def determineFirstPlayer(self): 
        playerListOrder = [] #Temporary list to order players by highest roller
        playerNotEligible = None

        #Set the order by rolling dice 
        for player in self.players: 

            #If player is banker/auctioneer (non-dual role), player's order is not calculated. 
            if (player.getTitle() == "Banker/Auctioneer"):
                playerNotEligible = player
                continue 

            userID = player.getuserID()
            rollNumber = TwoDice.rollDice() 
            playerListOrder.append({'userID': userID, 'order' : rollNumber})

        #Order the players by the set order
        playerListOrder.sort(key=utility.rollOrder)

        #Check if list order has ties based on the new order
        playerListOrder = utility.checkTies(playerListOrder)

        #Order the main players list (self.players) based on player order 
        newPlayersList = [] #Temporary list

        for player in playerListOrder: #Insert players into temp list by order presented in sorted list
            
            for playerObject in self.player:
                if (playerObject.getuserID == player['userID']):
                    newPlayersList.append(playerObject)
                    break
        
        if(playerNotEligible): #If there was a banker, add the player back to list
            newPlayersList.append(playerNotEligible)
        
        #Replace player list with temp list 
        self.playerList = newPlayersList

        #Reset double class variable should value have changed 
        TwoDice.double = False

    #Determine winner of the game   
    def determineWinner(self, timerExpired = false):
        pass

    #Conduct the turn of a player
    def turn(self, player): 
        
        #Get the number of eyes on dice for movement
        moveNum = TwoDice.rollDice()

        #Move the player to new position 
        player.move(moveNum)

        #Get the tile based on player position 

        #Check if player went to jail 
        if (player.getInJail()):
            player.pos

        #Get chance card if player landed on chance tile

        #Get community card if player landed on community chest tile

        #Go again if not on jail and has thrown double
        if (not player.getInJail() and TwoDice.double):
            turn(player) 
        


    
        
         