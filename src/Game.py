import util
import TwoDice, Player, Board, Card, Bank

class Game:

    #Instiates a new game
    def __init__(self):
        self.players = []
        self.currentPlayer = None
        self.board = Board() 
        self.chancePile = Card.ChanceCards() 
        self.communityPile = Card.CommunityCards()
        self.dice = TwoDice() 
        self.bank = Bank() 

    #Return first player of game based on the rolling
    def firstPlayer(self): 
        return self.players[0]
    
    #Return current player in game
    def getCurrentPlayer(self):
        return self.currentPlayer

    #Set the current player in round
    def setCurrentPlayer(self, player):
        self.currentPlayer = player

    #Add player to the game - if players are added post-roll, they are included at the end
    def addPlayer(self, id, name): 
        if (len(self.players) < Player.PLAYER_MAXIMUM):
            self.players.append(Player(id, name))

    #Remove player from game - due to bankruptcy, connection timeout, quit, or etc. 
    #This would not affect the ordering of other players.
    def removePlayer(self, id): 
        for player in self.players: 
            if (player.getuserID() == id):
                self.players.remove(player)
                break
        
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
            rollNumber = self.dice.rollDice() 
            playerListOrder.append({'userID': userID, 'order' : rollNumber})

        #Order the players by the set order
        playerListOrder.sort(key=util.rollOrder)

        #Check if list order has ties based on the new order
        playerListOrder = util.checkTies(playerListOrder, self.dice)

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
        self.dice.double = False

    #Determine winner of the game   
    def determineWinner(self, timerExpired = false):
        pass

    #Run the game 
    def run(self): 
        #Play game until a winner is found 
        winner = False
        if (not winner): 
            self.round()

            #If after the round, there is only one player left or game terminates, game ends
            if (len(self.players) <= 1): 
                winner = True
            else: 
                #Generate more money in the bank, and start another round
                self.bank.generateCash() 
    
    #Go through all players in round
    def round(self): 
        for player in self.players: 
            self.setCurrentPlayer(player)
            self.turn(player)

    #Conduct the turn of a player
    def turn(self, player): 
        #Check if player is in jail 
        if (player.getInJailStatus()):
            pass 

        #Get the number of eyes on dice for movement
        moveNum = self.dice.rollDice()

        #Move the player to new position 
        player.move(moveNum, dice, bank)

        #Get the board tile based on player position 
        boardTile = self.board.getTileType(player.getPosition())

        #Set to go to jail if landed on 'Go To Jail' tile on board
        if boardTile == "Go to Jail": 
            player.setInJailStatus(True)

        #Check if player went to jail because of tile or rolling three doubles in a row
        if (player.getInJailStatus()):
            player.position = Board.TILES_JAIL[0]
            return #End the turn here

        #Get property card if player landed on property tile
        if boardTile == "Property":
            propertyName = Board.TILE_LIST[player.getPosition()]

            user_properties = player.getProperties() 
            
            #Check if this property is already in user's possession 
            if propertyName in 
            
            #Check if another player owns the property and pay any rent/mortgage.

            #If no player owns the property, see if player will purchase or auction

        #Get utility card if player landed on utility tile
        if boardTile == "Utility":
            utilityName = Board.TILE_LIST[player.getPosition()]

        #Get transports card if player landed on transports tile
        if boardTile == "Transports":
            transportsName = Board.TILE_LIST[player.getPosition()]

        #User pays the tax indicated on the board 
        if boardTile == "Tax":
            player.payTax(bank)

        #Get chance card if player landed on chance tile
        if boardTile == "Chance Card":
            player.doChanceCard(self.chancePile.pullCard(), bank)

        #Get community card if player landed on community chest tile
        if boardTile == "Community Card":
            player.doCommunityCard(self.communityPile.pullCard(), bank)

        #Log that the player has landed on a tile after all movements/actions are complete
        self.board.hit(player.getPosition())

        #Go again if not on jail and has thrown double
        if (not player.getInJailStatus() and dice.double):
            turn(player) 
        


    
        
         