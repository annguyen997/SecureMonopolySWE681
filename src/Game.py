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

        #Set the order by rolling dice 
        for player in self.players: 
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

        #Get property card if player landed on property, utility, or transports tile
        if boardTile in ("Property", "Utility", "Transports"):
            self.checkTitleDeed(player, boardTile)
        
        #User pays the tax indicated on the board
        if boardTile == "Tax":
            player.payTax(bank)
            
        #Get chance card if player landed on chance tile
        if boardTile == "Chance Card":
            player.doChanceCard(self.chancePile.pullCard(), bank)

            #May need to check the new position of the player for a property/utility/transport

        #Get community card if player landed on community chest tile
        if boardTile == "Community Card":
            player.doCommunityCard(self.communityPile.pullCard(), bank)

            #May need to check the new position of the player for a including a property/utility/transport

        #Log that the player has landed on a tile after all movements/actions are complete
        self.board.hit(player.getPosition())

        #If player has properties, check if the user would wish to purchase additional houses/hotels before ending turn
        #User can also wish to sell properties 
        #This statement also runs in player lands on Free Parking space 

        #Go again if not on jail and has thrown double
        if (not player.getInJailStatus() and dice.double):
            turn(player) 

    #Get the title deed card and do the following actions based on the information provided.
    def checkTitleDeed(self, player, boardTile = "None"): 
        titleDeedName = Board.TILE_LIST[player.getPosition()]
        
        owner = None
        ownerExisting = False
        
        #Check for owner information of a property
        for player in self.players: 
            user_properties = player.getProperties()
            if (titleDeedName in user_properties):
                ownerExisting = True
                owner = player
        
        #Check if this property is already in a user's possession
        if (ownerExisting):
            if (owner.getuserID() == player.getuserID()):
                #If the current player owns this property
                pass
            else: #If another player owns the property; pay rent or mortgage
                player.payRent(owner, titleDeedName, boardTile)
        else: 
            titleDeed = self.bank.getTitleDeedCard(titleDeedName, boardTile)
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
                player.addProperty(titleDeed, printedValue, self.bank)
            elif (value == "Auction"):   #Get the starting value
                #Validate the starting value - ensure value is not too high 
                startingPrice = input("Please supply the starting price for auction: ")
                self.auctionProperty(startingPrice, titleDeed, player.getName())
            else: 
                print("Invalid response was provided.")
    
    #If auctioning property, there will be two rounds to do auction from all players - this is a modified change from the actual game for simplicity purposes
    #A timer may be needed for each user to input a value; if runs out user does not play. - 1 minute max
    def auctionProperty(self, startingPrice, titleDeed, name):
        auctionAmounts = [0] * len(self.players)
        self.bank.startAuction(startingPrice)

        #First Round - Skipping the starting bid player
        print("An auction has started for " + titleDeed.getName() + ", started by " + name + ".\n" + 
            "The starting bid for this auction is: " + str(startingPrice))

        numberAuctioned = 0
        for player in self.player: 
            if (name == player.getName()):
                auctionAmounts[numberAuctioned] = startingPrice
                numberAuctioned += 1
                continue #Skip that player since they inputted starting bid.

            print("Please enter your bidding bid.")

            #Validate input here - including price must be higher than auction bid. To skip auction, user enters "zero".
            #If user types in invalid value, re-enter. If time expires, player forfeits this round.
            biddingPrice = input("Enter bid here: ") 
            self.auctionAmounts[numberAuctioned] = biddingPrice
            numberAuctioned += 1

        #Process the amounts of first round - highest one is the new auction price
        newBidAmount = max(auctionAmounts)
        self.bank.setAuctionPrice(newBidAmount)

        #Second round
        print("The second round of this auction has started for " + titleDeed.getName() + ".\n" + 
            "The new starting bid for this round is: " + str(newBidAmount))
            
        numberAuctioned = 0
        for player in self.player: 
            print("Please enter your bidding bid.")

            #Validate input here - including price must be higher than auction bid. To skip auction, user enters "zero".
            biddingPrice = input("Enter bid here: ") 
            auctionAmounts[numberAuctioned] = biddingPrice
            numberAuctioned += 1

        #Process the amounts of second round - highest one is the winner auction price
        highestAmount = max(auctionAmounts)

        #Check if highest amount occurs more than once (i.e. at least two players entered same value)
        tieAmountExist = False
        occurrences = auctionAmounts.count(highestAmount)
        if (occurrences > 1): 
            tieAmountExist = True 
              
        #Need the name of player to get the title deed. If there is a tie, one with higher order value wins. 
        indexHighest = auctionAmounts.index(highestAmount)
        playerAuctionWinner = self.player[indexHighest]

        winnerAnnounce = ""
        if (tieAmountExist): 
            winnerAnnounce += "There is a tie in the highest amount bidder.\n"
        
        winnerAnnounce += "The winner of this auction is " + playerAuctionWinner.getName() + ", who bid for " + highestAmount + ". Congratulations!"
        winnerAnnounce += "That player now owns this property, paying the specified amount."

        print(winnerAnnounce)

        #Conduct the purchase of property
        playerAuctionWinner.addProperty(titleDeed, highestAmount, self.bank)

        #Reset bank's auction amount
        self.bank.resetAuctionPrice()


