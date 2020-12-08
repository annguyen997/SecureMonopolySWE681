import util
import Board
import Bank
#import Title
from TwoDice import *
from Player import *
from Card import *

class Game:
    #Instiates a new game
    def __init__(self):
        self.players = []
        self.currentPlayer = None
        self.board = Board() 
        self.chancePile = ChanceCards()
        self.communityPile = CommunityCards()
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
            playerListOrder.append({'userID': userID, 'order': rollNumber})

        #Order the players by the set order
        #playerListOrder.sort(key=util.rollOrder())
        playerListOrder = sorted(playerListOrder, key=lambda item: item.get('order'))

        #Check if list order has ties based on the new order
        playerListOrder = util.checkTies(playerListOrder, self.dice)

        #Order the main players list (self.players) based on player order 
        newPlayersList = [] #Temporary list

        for player in playerListOrder: #Insert players into temp list by order presented in sorted list
            for playerObject in self.players:
                if (playerObject.getuserID() == player.get('userID')):
                    newPlayersList.append(playerObject)
                    break
                
        #Replace player list with temp list 
        self.playerList = newPlayersList

        #Reset double class variable should value have changed 
        self.dice.resetDoubleStatus()

    #Determine winner of the game   
    def determineWinner(self, timerExpired = False):
        if (len(self.players) == 1): 
            winner = self.players[0]
            print(winner.getName() + " wins the game!")
        else:
            print("No winner at this time.")

    #Run the game
    def run(self): 
        if (len(self.players) < Player.PLAYER_MINIMUM): 
            print("Game must have at least two players")
            return #Do not run game 
            
        #Determine who plays first 
        self.determineFirstPlayer()
        
        #Add money to each player before starting the first round
        for player in self.players: 
            player.changeMonetaryValue(Bank.STARTING_AMOUNT)
            self.bank.subtract(Bank.STARTING_AMOUNT)

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
        
        #Report the winner of the game
        self.determineWinner()
    
    #Go through all players in round
    def round(self): 
        for player in self.players: 
            self.setCurrentPlayer(player)
            self.turn(player)

    #Conduct the turn of a player
    def turn(self, player):
        #Print current player
        print("It is now " + player.getName() + "'s turn.\n")

        #Check if player is in jail, and if so process the options
        if (player.getInJailStatus()):
            returnedCard = player.escapeJailOptions(self.bank, self.dice)

            #If card is returned, do the following actions to return card to deck
            if (returnedCard != None): 
                if (returnedCard.getCardType() == "Chance"):
                    self.chancePile.returnJailFreeCard(returnedCard)
                elif (returnedCard.getCardType() == "Community"):
                    self.communityPile.returnJailFreeCard(returnedCard) 
        else: 
            #Get the number of eyes on dice for movement
            moveNum = self.dice.rollDice()

            #Inform the dice roll
            print("Dice 1: " + str(self.dice.getFirstDice()))
            print("Dice 2: " + str(self.dice.getSecondDice()))
            print("Dice Roll Total: " + str(moveNum))

            #Move the player to new position 
            player.move(moveNum, self.dice, self.bank)

        #Print current tile position
        print("\nPlayer " + player.getName() + " is now at " + Board.TILES_LIST[player.getPosition()] + ".\n")

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
            player.payTax(self.bank)
            
        #Get chance card if player landed on chance tile
        elif boardTile == "Chance Card":
            player.doChanceCard(self.chancePile.pullCard(), self.board, self.bank)

            #May need to check the new position of the player for a including a property/utility/transport
            newBoardTile = self.board.getTileType(player.getPosition())
            if newBoardTile in ("Property", "Utility", "Transports"):
                self.checkTitleDeed(player, boardTile)
            elif newBoardTile == "Go to Jail":
                player.setJailTurns(3)
                return #End turn right here

        #Get community card if player landed on community chest tile
        elif boardTile == "Community Card":
            player.doCommunityCard(self.communityPile.pullCard(), self.board, self.bank)

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

        #Check if player has no cash left after this round, and if so if has assets
        noCashStatus = player.runOutOfCash() 
        if (noCashStatus): 
            self.checkForAssets(player) 
            
        #Check if the player is bankrupt (due to no cash and/or insufficient asset amounts)
        if (player.getBankruptStatus()):
            self.declareBankruptcy(player, self.players, self.bank)
            return #Player has left the game, stop turn here 
            
        #Go again if not on jail and has thrown double
        if (not player.getInJailStatus() and (self.dice.getDoubleStatus())):
            self.turn(player)

    #Get the title deed card and do the following actions based on the information provided.
    def checkTitleDeed(self, player, boardTile = "None"): 
        titleDeedName = Board.TILES_LIST[player.getPosition()]
        
        owner = None
        ownerExisting = False
        
        #Check for owner information of a property
        for player in self.players: 
            user_titleDeeds = player.getTitleDeeds()
            for titleDeed in user_titleDeeds:
                if (titleDeedName == titleDeed["Title Deed"].getName()):
                    ownerExisting = True
                    owner = player
        
        #Check if this property is already owned by some player
        if (ownerExisting):
            if (owner.getuserID() == player.getuserID()):
                #Player lands on their own property; can handle any title deeds back in the caller turn() function
                return
            else: #If another player owns the title deeds; pay rent or mortgage
                player.payRent(owner, titleDeedName, boardTile, self.dice)
        else: 
            #This is when this property is not yet owned by some player 

            titleDeed = self.bank.getTitleDeedCard(titleDeedName, boardTile)
            if (titleDeed == None): 
                print("Invalid title deed requested or bank does not have this card.")
                return #End immediately 

            #Get the printed value price, print card's information, and request user input
            printedValue = titleDeed.getPrintedValue()
            print(titleDeed)

            # User types either "Purchase" or "Auction"
            newTitleDeedDecided = False
            while (not newTitleDeedDecided):
                #Validate the input here
                value = input("Do you wish to purchase to this property at the printed value of " + str(printedValue) +
                            " or do you wish to auction? \n" +
                            "If you want to purchase, please type the word 'Purchase'. \n" +
                            "If you wish to auction, please type 'Auction'.")

                if (value == "Purchase"):
                    player.acquireTitleDeed(titleDeed, printedValue, self.bank)
                    newTitleDeedDecided = True
                elif (value == "Auction"):   #Get the starting value
                    #Validate the starting value - ensure value is not too high
                    startingPrice = input("Please supply the starting price for auction: ")
                    self.auctionProperty(startingPrice, titleDeed, player.getName())
                    newTitleDeedDecided = True
                else:
                    print("Invalid response was provided.")
    
    #Check if player has assets if run out of cash. If no sufficient assets, declare bankruptcy 
    def checkForAssets(self, player):
        #Check if user has title deeds (having mortgages or buildings means title deeds) 
        titleDeedsNum = player.getTitleDeeds()
        
        #If user has no title deeds, user has no income sources and thus must declare bankruptcy 
        if (titleDeedsNum <= 0):
            player.setBankruptStatus(True) 
        else: 
            #Note that having title deeds by themselves have no inherit value 
            #Possible rent is not considered when calculating assets as those are not realized and not guaranteed

            #Get the title deed and debt records of player
            titleDeedRecords = player.getTitleDeeds() 
            debtRecords = player.getDebtRecord()

            #Set the variables to calculate the assets and possible mortgaged values
            buildingAssetsValue = 0 
            potentialMortgagedValue = 0 

            #Calculate the value of the buildings owned and possible mortgages 
            for titleDeedRecord in titleDeedRecords: 
                #If the title deed contains buildings, get the building values (at selling price)
                if (titleDeedRecord["Houses"] or titleDeedRecord["Hotels"]):
                    housesValue = titleDeedRecord["Houses"] * (titleDeedRecord["Title Deed"].getBuildingCosts(Property.HOMES_COST) * 0.50)
                    hotelsValue = titleDeedRecord["Hotels"] * (titleDeedRecord["Title Deed"].getBuildingCosts(Property.HOTELS_COST) * 0.50)
                    
                    buildingAssetsValue = buildingAssetsValue + housesValue + hotelsValue
                
                #If title deed has no properties but can be mortgaged, get the possible mortgage amount
                #Skip if mortgages are already set
                if (titleDeedRecord["Mortgaged"] == False):
                    potentialMortgagedValue += titleDeedRecord["Title Deed"].getMortgageValue() 
            
            #Get the total amount of debts from each player (or bank)
            debtAmount = 0 
            for debtRecord in debtRecords: 
                debtAmount += debtRecord["Debt Owned"]
            
            #Determine if player is bankrupt
            if ((debtAmount > buildingAssetsValue) and (debtAmount > potentialMortgagedValue)): 
                #If debt amount is higher than building and potential mortgages separately
                #Check if debt is higher than building and mortgages combined 
                if (debtAmount > buildingAssetsValue + potentialMortgagedValue): 
                    #If debt amount is higher than assets and potential mortgages combined, set bankruptcy 
                    player.setBankruptStatus(True) 
                else: 
                    #This means the debt amount is lower than the assets and potential mortgages combined
                    player.setBankruptStatus(False) 
            else: 
                #Debt amount is lower than assets, or the possible mortgages, or both 
                player.setBankruptStatus(False)

    #If auctioning property, there will be two rounds to do auction from all players - this is a modified change from the actual game for simplicity purposes
    def auctionProperty(self, startingPrice, titleDeed, playerName):
        auctionAmounts = [0] * len(self.players)
        self.bank.startAuction(startingPrice)

        #First Round - Skipping the starting bid player
        print("An auction has started for " + titleDeed.getName() + ", started by " + playerName + ".\n" + 
            "The starting bid for this auction is: " + str(startingPrice))

        numberAuctioned = 0
        for player in self.players:
            if (playerName == player.getName()):
                auctionAmounts[numberAuctioned] = startingPrice
                numberAuctioned += 1
                continue #Skip that player since they inputted starting bid.

            #Validate input here - including price must be higher than auction bid. To skip auction, user enters "zero".
            #If user types in invalid value, re-enter.
            biddingPrice = player.provideAmount("Auction", titleDeed.getName(), startingPrice)
            auctionAmounts[numberAuctioned] = biddingPrice
            numberAuctioned += 1

        #Process the amounts of first round - highest one is the new auction price
        newBidAmount = max(auctionAmounts)
        self.bank.setAuctionPrice(newBidAmount)

        #Second round
        print("The second round of this auction has started for " + titleDeed.getName() + ".\n" + 
            "The new starting bid for this round is: " + str(newBidAmount))
            
        numberAuctioned = 0
        for player in self.players:

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
        playerAuctionWinner = self.players[indexHighest]

        winnerAnnounce = ""
        if (tieAmountExist): 
            winnerAnnounce += "There is a tie in the highest amount bidder.\n"
        
        winnerAnnounce += "The winner of this auction is " + playerAuctionWinner.getName() + ", who bid for " + str(highestAmount) + ". Congratulations!"
        winnerAnnounce += "That player now owns this property, paying the specified amount."

        print(winnerAnnounce)

        #Conduct the purchase of property
        playerAuctionWinner.acquireTitleDeed(titleDeed, highestAmount, self.bank)

        #Reset bank's auction amount
        self.bank.resetAuctionPrice()
   
    #If auctioning property, there will be two rounds to do auction from all players - this is a modified change from the actual game for simplicity purposes
    #Auction the title deed as a result of a bankruptcy of owner
    def bankruptAuction(self, titleDeed, mortgaged, bankruptedPlayer):
        auctionAmounts = [0] * (len(self.players) - 1)
        self.bank.startAuction(0)

        #First Round - Skipping the starting bid player
        print("An auction has started for " + titleDeed.getName() + ".\n")

        numberAuctioned = 0
        for player in self.players:
            if (bankruptedPlayer == player.getName()):
                continue #Skip that player since bankrupted

            #Validate input here - including price must be higher than auction bid. To skip auction, user enters "zero".
            #If user types in invalid value, re-enter. 
            biddingPrice = player.provideAmount("Auction", titleDeed.getName(), 0)
            auctionAmounts[numberAuctioned] = biddingPrice
            numberAuctioned += 1

        #Process the amounts of first round - highest one is the new auction price
        newBidAmount = max(auctionAmounts)
        self.bank.setAuctionPrice(newBidAmount)

        #Second round
        print("The second round of this auction has started for " + titleDeed.getName() + ".\n" + 
            "The new starting bid for this round is: " + str(newBidAmount))
            
        numberAuctioned = 0
        for player in self.players:
            if (bankruptedPlayer == player.getName()):
                continue #Skip that player since bankrupted

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
        playerAuctionWinner = self.players[indexHighest]

        winnerAnnounce = ""
        if (tieAmountExist): 
            winnerAnnounce += "There is a tie in the highest amount bidder.\n"
        
        winnerAnnounce += "The winner of this auction is " + playerAuctionWinner.getName() + ", who bid for " + str(highestAmount) + ". Congratulations!"
        winnerAnnounce += "That player now owns this property, paying the auction amount."

        print(winnerAnnounce)

        #Conduct the purchase of property via inheritance
        playerAuctionWinner.inheritTitle(titleDeed, highestAmount, mortgaged, self.bank)

        #Reset bank's auction amount
        self.bank.resetAuctionPrice()

    #Handle all existing deeds of a player 
    def handleExistingTitleDeeds(self, player): 
        #Get player's title deeds
        titleDeedsOwned = player.getTitleDeeds()
        titleDeedsNames = [titleDeed["Title Deed"].getName() for titleDeed in titleDeedsOwned]

        displayOptions = "Type in one of the following options exactly as shown: " + "\n 1. Mortgage a Property" + "\n 2. Repay a Mortgaged Property" + "\n 3. Purchase a House" + "\n 4. Purchase a Hotel" + "\n 5. Sell a House" + "\n 6. Sell a Hotel" + "\n 7. Sell a Property" + "\n 8. Sell a Utility" + "\n 9. Sell a Transport" + "\n 10. End Turn \n\n" + "Note for options 7, 8, and 9 - you can also sell mortgaged title deeds."

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
                util.sellHome(player, titleDeedsNames, titleDeedsOwned, self.bank)

            #If user wishes to sell a hotel, get property name. Also get 4 homes back. 
            elif (optionSelection == "Sell a Hotel"): 
                util.sellHotel(player, titleDeedsNames, titleDeedsOwned, self.bank)

            #If user wishes to sell a property to another user - ensure there are no buildings
            elif (optionSelection == "Sell a Property"): 
                playerRequest = util.selectPlayerToSell(player, "property")
                util.sellProperty(player, playerRequest, titleDeedsNames, titleDeedsOwned, self.bank)
                        
            #If user wishes to sell a utility to another user
            elif (optionSelection == "Sell a Utility"):
               playerRequest = util.selectPlayerToSell(player, "utility")
               util.sellUtility(player, playerRequest, titleDeedsNames, titleDeedsOwned, self.bank)

            #If user wishes to sell a transports to another user
            elif (optionSelection == "Sell a Transport"): 
                playerRequest = util.selectPlayerToSell(player, "transport")
                util.sellTransport(player, playerRequest, titleDeedsNames, titleDeedsOwned, self.bank)

            #If user wishes to exit
            elif(optionSelection == "End Turn"): 
                userHandling = False
            
            #If user entered invalid choice
            else: 
                print("\nYou have entered an invalid choice. Please try again.\n")
        
        print("End processing of making changes to user's title deeds.")
                
    #Do bankruptcy process if bankrupt
    def declareBankruptcy(self, player, playersList, bank): 
        #Get the list of debts and title deeds
        debtItems = player.getDebtRecord()
        titleDeedRecords = player.getTitleDeeds() 

        #Sell all buildings first to the bank, then add amount to the current monetary value of player
        monetaryBuildingValue = 0 
        for titleDeed in titleDeedRecords: 
            #If the title deed is a property, sell any buildings
            if (titleDeed["Title Deed"].getTitleType() == "Property"): 
                propertyName = titleDeed["Title Deed"].getName()

                #If there is a hotel, sell hotel first
                if (titleDeed["Hotels"] > 0):
                    sellHotelAmount = titleDeed["Title Deed"].getBuildingCosts(Property.HOTELS_COST) * 0.50 
                    player.sellHotel(propertyName, sellHotelAmount, bank)
                    monetaryBuildingValue += sellHotelAmount

                #Then sell each house of that property
                if (titleDeed["Houses"] > 0):
                    #Get the number of houses of that property; needs constant value
                    numberHouses = titleDeed["Houses"]

                    #For each house, make the sell back to bank
                    for i in range(numberHouses):
                        sellHouseAmount = titleDeed["Title Deed"].getBuildingCosts(Property.HOMES_COST) * 0.50 
                        player.sellHome(propertyName, sellHouseAmount, bank)
                        monetaryBuildingValue += sellHouseAmount
        
        player.changeMonetaryValue(monetaryBuildingValue)
        
        #Pay all remaining debts to players - least amount of debt first
        debtAmounts = []
        for debtItem in debtItems: 
            #If player owes debt to bank, skip that for as bank is least priority 
            if (debtItem["Player"] == "Bank"): 
                continue
            debtAmounts.append(debtItem["Debt Owned"])
        debtAmounts.sort(reverse=True)

        #Pay debts until player has insufficient funds 
        for debtAmount in debtAmounts: 
            repayPlayerName = None

            #If player has enough funds to clear debt, clear the debt
            possibleNewAmount = player.getMonetaryValue() - debtAmount

            if (possibleNewAmount > 0): 
                #Find player of that debt amount
                for debtItem in debtItems: 
                    if (debtItem["Debt Owned"] == debtAmount):
                        repayPlayerName = debtItem["Player"]
                        break
            
                #Search for that player in player list (of the game), and pay the debts
                for indebitedPlayer in playersList: 
                    if (indebitedPlayer.getName() == repayPlayerName): 
                        player.changeMonetaryValue(-1 * debtAmount)
                        indebitedPlayer.changeMonetaryValue(debtAmount)
                        player.reduceDebt(repayPlayerName, debtAmount)
            else: 
                break #End the for loop to pay the debts
          
        #If you owe debt to another player (most debt first), sell the title deeds and any jail free cards to that player
        #Any other players which bankrupted player had payables dues must accept losses
        #Any cash generated by selling the buildings is credited to the new owner
        #This option is used even if the bankrupt player owns money to the bank (e.g. repaying a mortgage payment)
        debtAmounts.sort()
        maxDebtAmount = max(debtAmounts) 
        secondDebtAmount = debtAmounts[1]

        maxPlayer = None
        secondHighestPlayer = None

        #Find players of highest and second highest debt amounts
        for debtItem in debtItems: 
            if (debtItem["Debt Owned"] == maxDebtAmount):
                maxPlayer = debtItem["Player"]
            elif (debtItem["Debt Owned"] == secondDebtAmount):
                secondHighestPlayer = debtItem["Player"]

        #If highest debt amount is another player, or the highest is bank but there are more than two debt items
        if (maxPlayer != "Bank" or (maxPlayer == "Bank" and (len(debtAmounts) > 1))): 
            playerToSellAllItems = None
            if (maxPlayer == "Bank"):
                playerToSellAllItems = secondHighestPlayer
            else: 
                playerToSellAllItems = maxPlayer 

            #Find the player in the list of the game
            newOwner = None
            for playerReceiver in playersList: 
                if (playerReceiver.getName() == playerToSellAllItems): 
                    newOwner = playerReceiver
                
            #Sell all deeds to the player
            for titleDeedRecord in titleDeedRecords: 
                deedMortgaged = titleDeedRecord["Mortgaged"]
                titleDeedInTransit = player.sellTitle(titleDeedRecord["Title Deed"].getName(), 0)
                newOwner.inheritTitle(titleDeedInTransit, 0, deedMortgaged, bank)

            #Give away any jail cards
            while (player.jailCardsAvailable()): 
                jailCard = player.removeEscapeJailCard() 
                newOwner.addEscapeJailCard(jailCard)
            
            #Give any cash (from selling properties) remaining to that player, assuming it is greater than zero 
            if (player.getMonetaryValue() > 0): 
                cashAmount = player.getMonetaryValue() 
                player.changeMonetaryValue(-1 * cashAmount) 
                newOwner.changeMonetaryValue(cashAmount) 

        #If there is just the bank, bank must auction the properties and receive any cash     
        else: 
            #Auction all deeds to other players via bank
            for titleDeedRecord in titleDeedRecords: 
                titleDeedCard = player.sellTitle(titleDeedRecord["Title Deed"].getName(), 0)
                deedMortgaged = titleDeedRecord["Mortgaged"]
                self.bankruptAuction(titleDeedCard, deedMortgaged, player.getName())

            #Give away any jail cards back to the game piles
            while (player.jailCardsAvailable()): 
                jailCard = player.removeEscapeJailCard() 

                #Return card to deck based on the card Type
                if (jailCard.getCardType() == "Chance"):
                    self.chancePile.returnJailFreeCard(jailCard)
                elif (jailCard.getCardType() == "Community"):
                    self.communityPile.returnJailFreeCard(jailCard) 
            
            #Give any cash (from selling properties) remaining to the bank, assuming it is greater than zero 
            if (player.getMonetaryValue() > 0): 
                cashAmount = player.getMonetaryValue() 
                player.changeMonetaryValue(-1 * cashAmount) 
                bank.changeMonetaryValue(cashAmount) 
    
        #Remove player from the game
        playerID = player.getuserID()
        self.removePlayer(playerID)
