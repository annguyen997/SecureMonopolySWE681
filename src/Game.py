import util
import TwoDice, Player, Board, Card, Bank
from Title import Title, Property, Utility, Transports

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
        self.dice.resetDoubleStatus()

    #Determine winner of the game   
    def determineWinner(self, timerExpired = false):
        pass

    #Run the game 
    def run(self): 
        #Determine who plays first 
        self.determineFirstPlayer()
        
        #Add money to each player before starting the first round
        for player in self.players: 
            player.changeMonetaryValue(Bank.STARTING_AMOUNT)
            bank.subtract(Bank.STARTING_AMOUNT)

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
        #Check if player is in jail, and if so process the options
        if (player.getInJailStatus()):
            returnedCard = player.escapeJailOptions(bank, dice)

            #If card is returned, do the following actions to return card to deck
            if (returnedCard != None): 
                if (returnedCard.getCardType() == "Chance"):
                    self.chancePile.returnJailFreeCard(returnedCard)
                elif (returnedCard.getCardType() == "Community"):
                    self.communityPile.returnJailFreeCard(returnedCard) 
        else: 
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
        if (player.getInJailStatus() and (player.getJailTurns() == 0)): 
            player.setPosition(Board.TILES_JAIL[0])
            player.setJailTurns(3)
            return #End the turn here - do not do any other action

        #Get property card if player landed on property, utility, or transports tile
        if boardTile in ("Property", "Utility", "Transports"):
            self.checkTitleDeed(player, boardTile)
        
        #User pays the tax indicated on the board
        elif boardTile == "Tax":
            player.payTax(bank)
            
        #Get chance card if player landed on chance tile
        elif boardTile == "Chance Card":
            player.doChanceCard(self.chancePile.pullCard(), bank)

            #May need to check the new position of the player for a including a property/utility/transport
            newBoardTile = self.board.getTileType(player.getPosition())
            if newBoardTile in ("Property", "Utility", "Transports"):
                self.checkTitleDeed(player, boardTile)
            elif newBoardTile == "Go to Jail":
                player.setJailTurns(3)
                return #End turn right here

        #Get community card if player landed on community chest tile
        elif boardTile == "Community Card":
            player.doCommunityCard(self.communityPile.pullCard(), bank)

            #May need to check the new position of the player for a including a property/utility/transport
            newBoardTile = self.board.getTileType(player.getPosition())
            if newBoardTile in ("Property", "Utility", "Transports"):
                self.checkTitleDeed(player, boardTile)
            elif newBoardTile == "Go to Jail":
                player.setJailTurns(3)
                return #End turn right here

        #Log that the player has landed on a tile after all movements/actions are complete
        self.board.hit(player.getPosition())

        #If player has properties, check if the user would wish to purchase additional houses/hotels before ending turn as well as sell properties 
        #This statement also runs in player lands on Free Parking space 
        self.handleExistingTitleDeeds(player) 

        #Check if user is bankrupt 

        #Go again if not on jail and has thrown double
        if (not player.getInJailStatus() and dice.getDoubleStatus()):
            turn(player) 

    #Get the title deed card and do the following actions based on the information provided.
    def checkTitleDeed(self, player, boardTile = "None"): 
        titleDeedName = Board.TILE_LIST[player.getPosition()]
        
        owner = None
        ownerExisting = False
        
        #Check for owner information of a property
        for player in self.players: 
            user_titleDeeds = player.getTitleDeeds()
            if (titleDeedName == user_titleDeeds["Title Deed"].getName()):
                ownerExisting = True
                owner = player
        
        #Check if this property is already owned by some player
        if (ownerExisting):
            if (owner.getuserID() == player.getuserID()):
                #Player lands on their own property; can do any property handlings back in the caller turn() function 
                return
            else: #If another player owns the property; pay rent or mortgage
                player.payRent(owner, titleDeedName, boardTile, dice)
        else: 
            #This is when this property is not yet owned by some player 

            titleDeed = self.bank.getTitleDeedCard(titleDeedName, boardTile)
            if (titleDeed == None): 
                print("Invalid title deed requested or bank does not have this card.")
                return #End immediately 

            #Get the printed value price, print card's information, and request user input
            printedValue = titleDeed.getPrintedValue()
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
                player.acquireTitleDeed(titleDeed, printedValue, self.bank)
            elif (value == "Auction"):   #Get the starting value
                #Validate the starting value - ensure value is not too high 
                startingPrice = input("Please supply the starting price for auction: ")
                self.auctionProperty(startingPrice, titleDeed, player.getName())
            else: 
                print("Invalid response was provided.")
    
    #If auctioning property, there will be two rounds to do auction from all players - this is a modified change from the actual game for simplicity purposes
    #A timer may be needed for each user to input a value; if runs out user does not play. - 1 minute max
    def auctionProperty(self, startingPrice, titleDeed, playerName):
        auctionAmounts = [0] * len(self.players)
        self.bank.startAuction(startingPrice)

        #First Round - Skipping the starting bid player
        print("An auction has started for " + titleDeed.getName() + ", started by " + playerName + ".\n" + 
            "The starting bid for this auction is: " + str(startingPrice))

        numberAuctioned = 0
        for player in self.player: 
            if (playerName == player.getName()):
                auctionAmounts[numberAuctioned] = startingPrice
                numberAuctioned += 1
                continue #Skip that player since they inputted starting bid.

            #Validate input here - including price must be higher than auction bid. To skip auction, user enters "zero".
            #If user types in invalid value, re-enter. If time expires, player forfeits this round.
            biddingPrice = player.provideAmount("Auction", titleDeed.getName(), startingPrice)
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

            #Validate input here - including price must be higher than auction bid. To skip auction, user enters "zero".
            biddingPrice = player.provideAmount("Auction", titleDeed.getName(), newBidAmount)
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
        playerAuctionWinner.acquireTitleDeed(titleDeed, highestAmount, self.bank)

        #Reset bank's auction amount
        self.bank.resetAuctionPrice()

    #Handle all existing deeds of a player 
    def handleExistingTitleDeeds(self, player): 
        #Get player's title deeds
        titleDeedsOwned = player.getTitleDeeds()
        titleDeedsNames = [titleDeed["Title Deed"].getName() for titleDeed in titleDeedsOwned]

        displayOptions = "Type in one of the following options exactly as shown: "
        + "\n 1. Mortgage a Property"  
        + "\n 2. Repay a Mortgaged Property" 
        + "\n 3. Purchase a House"
        + "\n 4. Purchase a Hotel"
        + "\n 5. Sell a House"
        + "\n 6. Sell a Hotel" 
        + "\n 7. Sell a Property"
        + "\n 8. Sell a Utility"
        + "\n 9. Sell a Transport"
        + "\n 11. End Turn \n\n" 
        + "Note for options 7, 8, and 9 - you can also sell mortgaged title deeds." 

        #May need a while loop to loop through options continuously until user wishes to end the round
        userHandling = True
        while (userHandling): 
            #Need to validate the input result
            optionSelection = input(displayOptions + "\n\n Enter your choice: ")

            #If user wishes to mortgage on a particular property - if so check if there are homes/hotels in any cards in group
            #Note other players cannot assist player on a mortgaged property, though can collect rent on other properties of that same color group.
            if (optionSelection == "Mortgage a Property"):
                util.getMortgage(player, titleDeedsNames, titleDeedsOwned, self.bank)

            #If user wishes to repay the mortgage on a particular property - pay 10% interest to the nearest 10
            elif (optionSelection == "Repay a Mortgaged Property"):
                util.repayMortgage(player, titleDeedsOwned, self.bank)

            #If user wishes to purchase a house - check if (1) player owns a monopoly on a color group, and then (2) homes are evenly purchased on other properties
            #The property also must not be mortgaged as well as others in color group
            elif (optionSelection == "Purchase a House"):
                util.purchaseHome(player, titleDeedsNames, titleDeedsOwned, self.bank)

            #If user wishes to purchase a hotel - check if (1) player owns a monopoly on a color group, and then (2) 4 homes are evenly purchased for each property
            #The property also must not be mortgaged as well as others in color group
            elif (optionSelection == "Purchase a Hotel"): 
                util.purchaseHotel(player, titleDeedsNames, titleDeedsOwned, self.bank) 

            #If user wishes to sell a house, get property name. Ensure homes are evenly available on other properties before selling
            elif (optionSelection == "Sell a House"): 
                util.sellHouse(player, titleDeedsNames, titleDeedsOwned, self.bank)

            #If user wishes to sell a hotel, get property name. Also get 4 homes back. 
            elif (optionSelection == "Sell a Hotel"): 
                util.sellHotel(player, titleDeedsNames, titleDeedsOwned, self.bank)

            #If user wishes to sell a property to another user - ensure there are no buildings
            elif (optionSelection == "Sell a Property"): 
                playerRequest = util.selectPlayerToSell(player, "property")
                util.sellProperty(player, playerRequest, titleDeedsNames, titleDeedsOwned, bank)
                        
            #If user wishes to sell a utility to another user
            elif (optionSelection == "Sell a Utility"):
               playerRequest = util.selectPlayerToSell(player, "utility")
               util.sellUtility(player, playerRequest, titleDeedsNames, titleDeedsOwned, bank)

            #If user wishes to sell a transports to another user
            elif (optionSelection == "Sell a Transport"): 
                playerRequest = util.selectPlayerToSell(player, "transport")
                util.sellTransport(player, playerRequest, titleDeedsNames, titleDeedsOwned, bank)

            #If user wishes to exit
            elif(optionSelection == "End Turn"): 
                userHandling = False
            
            #If user entered invalid choice
            else: 
                print("\nYou have entered an invalid choice. Please try again.\n")
        
        print("End processing of making changes to user's title deeds.")
                
        
