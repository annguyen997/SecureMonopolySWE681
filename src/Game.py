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
        #Determine who plays first 
        self.determineFirstPlayer()

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
    
    #Implement timer 

    #Conduct the turn of a player
    def turn(self, player): 
        #Check if player is in jail 
        if (player.getInJailStatus()):
            player.escapeJailOptions()
            return

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
            player.setJailTurns(3)
            return #End the turn here

        #Get property card if player landed on property tile
        if boardTile == "Property":
            self.checkProperty(player)
        
        #Get utility card if player landed on utility tile
        if boardTile =="Utility":
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

        #If player has properties, check if the user would wish to purchase additional houses/hotels before ending turn

        #Go again if not on jail and has thrown double
        if (not player.getInJailStatus() and dice.double):
            turn(player) 

    #Get the property card and do the following actions based on the information provided.
    def checkProperty(self, player): 
        propertyName = Board.TILE_LIST[player.getPosition()]
        
        ownerName = None
        ownerExisting = False
        
        for player in self.players: 
            user_properties = player.getProperties()
            if (propertyName in user_properties):
                ownerExisting = False
                ownerName = player
        
        #Check if this property is already in a user's possession
        if (ownerExisting):
            if (ownerName.getuserID() == player.getuserID()):
                #If the current player owns this property
                pass
            else: #If another player owns the property; Pay rent or mortgage
                player.payRent(ownerName, propertyName)
        else: 
            titleDeed = self.bank.getPropertyCard(propertyName)
            printedValue = titleDeed.getPrintedValue()

            #Print card's information and request user input
            print(titleDeed) 
            
            value = input("Do you wish to purchase to this property at the printed value of " + printedValue + 
                    "or do you wish to auction? \n" +
                    "If you want to purchase, please type the word 'Purchase'. \n" + 
                    "If you wish to auction, please type 'Auction'.")

            #User types either "Purchase" or "Auction" 
            """
            ok = validateInputforTitle(value)
            if (not ok): 
                revalidate input again 
                Use while loop here 
            """

            if (value == "Purchase"): 
                player.addProperty(titleDeed)
                player.changeMonetaryValue(-printedValue)
            elif (value == "Auction"):   #Get the starting value
                #Validate the starting value - ensure value is not too high 
                startingPrice = input("Please supply the starting price for auction: ")
                self.auctionProperty(startingPrice, titleDeed, player.getName())
            else: 
                print("Invald response was provided.")
    
    #If auctioning property, there will be two rounds to do auction from all players
    #This is a modified change from the actual game for simplicity purposes
    #A timer may be needed for each user to input a value; if runs out user does not play. - 1 minute max
    def auctionProperty(self, startingPrice, titleDeed, name):
        bank.startAuction(startingPrice)

        print("An auction has started for " + titleDeed.getName() + ", started by " + name + ".\n" + 
            "The starting bid for this auction is: " + startingPrice)

        #First Round - Skipping the starting bid player
        for player in self.player: 
            if (name == player.getName()):
                continue #Skip that player since they inputted starting bid.

            print("Please enter your bidding bid.")

            #Validate input here - including price must be higher than auction bid. To skip auction, user enters "zero".
            biddingPrice = input("Enter bid here: ") 

        #Process the amounts of first round - highest one is the new auction price

        #Second round
        for player in self.player: 
            print("Please enter your bidding bid.")

            #Validate input here - including price must be higher than auction bid. To skip auction, user enters "zero".
            biddingPrice = input("Enter bid here: ") 

        #Process the amounts of second round - highest one is the auction price
        #Need the name of player to get the title deed. 
        #If there is a tie, use tie breaker dice.
        
        #Determine the highest auction bidder to get the title deed. 


