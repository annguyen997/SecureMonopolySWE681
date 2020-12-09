import socket 
import os 
from _thread import *
import uuid 
import base64
import json

from Driver import Driver

import util
import Board
import Bank
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
        self.gameMessages = None

    #Return the game messages
    def getGameMessages(self): 
        return self.gameMessages 
        
    #Return first player of game based on the rolling
    def firstPlayer(self): 
        return self.players[0]
    
    #Return current player in game
    def getCurrentPlayer(self):
        return self.currentPlayer

    #Set the current player in round
    def setCurrentPlayer(self, player):
        self.currentPlayer = player

    #Get the number of players in game
    def getNumberOfPlayers(self): 
        return len(self.players)

    #Add player to the game - if players are added post-roll, they are included at the end
    def addPlayer(self, id, name): 
        if (len(self.players) < Player.PLAYER_MAXIMUM):
            self.players.append(Player(id, name))

    #The controller can call this to add the players already available
    """ 
        def addPlayers(self, listPlayers): 
        playerNumber = 1

        for playerUsername in listPlayers:   #List of the username IDs
            self.addPlayer(self, playerUsername, "Player " + playerNumber)
    """ 

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

    #Forfeit the game 
    def forfeitGame(self, id): 
        removePlayer(id) 
    
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
                #value = input("Do you wish to purchase to this property at the printed value of " + str(printedValue) +
                           # " or do you wish to auction? \n" +
                           # "If you want to purchase, please type the word 'Purchase'. \n" +
                           # "If you wish to auction, please type 'Auction'.")
                
                message = self.printPlayerStats(player) + \
                        "Do you wish to purchase to this property at the printed value of " + str(printedValue) + \
                        " or do you wish to auction? \n" + \
                        "If you want to purchase, please type the word 'Purchase'. \n" + \
                        "If you wish to auction, please type 'Auction'."
                self.gameMessages = message

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

    #Print all the statistics of the player
    def printPlayerStats(self, player): 
        playerStats = "" 

        playerStats += "Current Net Worth: " + str(player.getMonetaryValue()) + "\n"                #This gets the current amount of the player
        playerStats += "Current Position: " + str(Board.TILES_LIST[player.getPosition()]) + "\n"    #This gets the current location of player on the board 

        return playerStats

class Controller:
    game_sessions = [] 

    #Controller instance (for each user)
    def __init__(self): 
        self.driver = Driver() 
        self.user = None
        self.gameSession = None 
        self.game = None
        #Should there be a group of session IDs stored per Controller? 

    #Check if the number of players in that game session enough to play
    @classmethod
    def sufficientNumberPlayers(cls, gameID): 
        print("Get to sufficient number player")
        gamePlayers = None 
        print("Get to sufficient number player2")
        for gameSession in cls.game_sessions: 
            if (str(gameID) == str(gameSession["Session"]) and len(gameSession["Player"]) >= 2):
                print(len(gameSession["Player"]))
                return True
        
        return False
    
    #Print the current game session IDs and number of players
    @classmethod
    def printCurrentGameSessionIDs(cls): 
        #Print each game session avaiable in the system
        gameInfo=""
        print("entering printCurrentGameSessionIDs FOR loop")
        print(cls.game_sessions)
        for gameSession in cls.game_sessions: 
            gameInfo += "Session ID: " + gameSession["Session"] + "\t# of Players: " + str(len(gameSession["Player"]))+"\n"
            print(gameSession["Active"])
            if (gameSession["Active"]):
                print("Active Yes!")
                gameInfo += " Game Active: Yes\n"
            else:
                print("Active No!") 
                gameInfo += " Game Active: No\n"
            
            print(gameInfo)
        
        return(gameInfo+"\nGame Active indicates if there is a game available for this session. A game session with sufficient number of players may not have a game active.\n")
    
    #Get the set of usernames from the game session IDs list
    def getUsernamesOfGameSessionID(cls, gameID): 
        for gameSession in cls.game_sessions: 
            if (str(gameID) == str(gameSession["Session"])):
                return gameSession["Usernames"]

    #Return the number of players of that game session 
    @classmethod
    def numberOfPlayers(cls, gameID): 
        for gameSession in cls.game_sessions: 
            if (str(gameID) == str(gameSession["Session"])):
                return len(gameSession["Player"])

    #Add session ID to an existing game session
    @classmethod
    def joinExistingSession(cls, playerID, gameID, username):
        for game in cls.game_sessions: 
            if str(gameID) == str(game["Session"]): 
                print("please help")

                #Check if the player's ID is not in the list for this session.
                #If player's ID is already in list, user just needs to join the game
                if (playerID in game["Player"]):
                    return #Player already in list, exit to previous caller
                elif (len(game["Player"]) <= 8): #If player in game is less than 8 players available 
                    game["Player"].append(playerID)
                    game["Usernames"].append(username)
                
    #Check if the game is active 
    @classmethod
    def checkGameActive(cls, gameID): 
        for gameSession in cls.game_sessions: 
            if (str(gameID) == str(gameSession["Session"]) and gameSession["Active"]):
                return True
        
        return False

    #Create a new game once there is sufficient number of players - asynchronous 
    @classmethod
    def createNewGame(cls, gameID, driver): 
        gamePlayers = None 
        
        for gameSession in cls.game_sessions: 
            if (str(gameID) == str(gameSession["Session"]) and Controller.numberOfPlayers(gameID) >= 2):
                gamePlayers = gameSession["Player"]
                gameSession["Active"] = True #This means enough players are available to start playing new game
                gameSession["Game Instance"] = driver.createNewGame() 

    #Get the game instance to controller
    @classmethod
    def getGameInstance(cls, gameID): 
        for gameSession in cls.game_sessions: 
            if (str(gameID) == str(gameSession["Session"]) and gameSession["Game Instance"]):
                return gameSession["Game Instance"]
        
        return None

    #Game information would need to be displayed to web client.... 
    def __incomingUser(self, username, password, mode):
        print("Incoming...")
        
        if (mode == "Authenticate"): 
            #session Ids will be returned as base-64
            generatedSessionID = self.driver.authUser(username, password)

            #It should return a new line with the returned byte/float value automatically 
            #Stripping new line may be needed 
            if (generatedSessionID == 0): 
                return 
            self.user = username 
            return generatedSessionID

        if (mode == "Create"): 
            userCreated = self.driver.createUser(username, password)

            if userCreated: 
                #Once created user, authenticate to generate session ID
                #session Ids will be returned as base-64
                generatedSessionID = self.driver.authUser(username, password)
                #It should return a new line with the returned byte/float value automatically 
                #Stripping new line may be needed 
                if (generatedSessionID == 0): 
                    return 
                #self.id = str(generatedSessionID).strip("\n")
                self.user = username
                return generatedSessionID
            
    #Asynchronous call
    def __checkSessionID(self, user, sessionID):
        #Call Driver's check session ID 
        sessionExist = self.driver.checkSession(user, sessionID) 

        #If session does not exist, end player's connection
        if (not sessionExist): 
            print("Ending the session.")

            for game in game_sessions: 
                if self.sessionID in game["Player"]: 
                    game["Player"].remove(self.sessionID)
        return sessionExist
        #random.urandom(32)....

    #Create a game session - requires at least two players to play
    def __createGameSession(self, sessionID):
        #Generate game session ID
        gameID = str(uuid.uuid4())

        #Add session ID with player 
        players = [sessionID]
        Controller.game_sessions.append({"Session": gameID, "Player": players, "Usernames": [self.user],  "Active": False, "Game Instance": None})
        
        self.gameSession = gameID  #Is this needed? 
        print(gameID)

        return gameID

    #Join an existing game 
    def __joinExistingGame(self, playerID, gameID): 
        print("You got here congrats.1@#!@#!@")
        Controller.joinExistingSession(playerID, gameID, self.user)
        self.gameSession = gameID
        print("Joining Existing Game")

        #if (Controller.checkGameActive()): 
            #self.setGameInstance(Controller.getGameInstance(self.gameSession))

    #Check if game can be created
    def __startGame(self, gameID): 
        print("entering __startGame")
        #print(Controller.sufficientNumberPlayers(gameID))

        #Check if there is a game instance already, and if not create one. 
        if (Controller.getGameInstance(self.gameSession) == None): 
            run = Controller.sufficientNumberPlayers(gameID)
            print("asdasdqw")
            if (run):
                Controller.createNewGame(gameID, self.driver) 
                print("after __startGame")
        #else: 
            #If there is a game instance already, simply join the game

        self.__setGameInstance(Controller.getGameInstance(self.gameSession))
        self.game.addPlayer(self.user, "Player #" + str(self.game.getNumberOfPlayers() + 1))

        #Run the game automatically once the sufficient number of players join 
        if (self.game.getNumberOfPlayers() == Controller.numberOfPlayers(self.gameSession)): 
            self.game.run() 

        #self.game.addPlayers(Controller.getUsernamesOfGameSessionID(self.gameSession))
    
    #Get all game instances available for viewing
    def __getGameInstancesAvailable(self): 
        Controller.printCurrentGameSessionIDs() 

    #Set the game variable to controller (of each client)
    def __setGameInstance(self, game): 
        self.game = game
    
    #Validate the input of the player 
    #ResponseType corresponds to the context of the input in relation to the game
    def parseInput(self, inp):
        #assert isinstance (inp, dict)
        #Regex parts here 

        # this will see what to call and interpret the api calls
        # i think it is best to devide up to 3 catergories
        # user stuff
        # management
        # and game

        # so I will interpret the data as so
        # dict {'user_': [data]} - user stuff
        # dict {'mana_': [data], 'username_': username, 'sessionID_': data} - management stuff such as sessionID
        # dict {'game_': [data], 'username_': username, 'sessionID_': data} - game data
        # 

        #user stuff
        # within [data] -> FIRST FIELD ALWAYS BE WHAT TO DO aka Authenticate/Create
        # [data] [1] = user, [data] [2] = password 
        if 'user_' in inp:
            inp=json.loads(inp)
            # __incomingUser(self, username, password, mode):
            return self.__incomingUser(str(inp['user_'][1]),    # username offset in 'user_' valueprint("We in parse Input")
                                        str(inp['user_'][2]),   # passwd offset in 'user_' value
                                        str(inp['user_'][0]))   # mode

        # management stuff
        if 'mana_' in inp:
            inp=json.loads(inp)
        # check session id if before anything
        # __checkSessionID(self, user, sessionID)
            if not (self.__checkSessionID(  str(inp['username_']),
                                            str(inp['sessionID_'])
                                            )):
                print("[!] LOG: Session for user %s has expired"
                        % (str(inp['username_'])) )
                return False

            ###############
            #   joinExistingGame
            ###############
            if (str(inp['mana_'][0]) == 'joinExistingGame'):
                # __joinExistingGame(self, playerID, gameID): 
                return self.__joinExistingGame(str(inp['username_']),   # playerID or username
                                        inp['mana_'][1])        # game session id
                


            ###############
            #   createGame
            ###############
            if (str(inp['mana_'][0]) == 'createGame'):
                # __createGame(self, sessionID): 
                print("creating game")
                return self.__createGameSession(inp['sessionID_'])        # player session id
            if (str(inp['mana_'][0]) == 'startGame'):
                # __createGame(self, sessionID): 
                print("starting game")
                return self.__startGame(inp['mana_'][1])   
                
        # game data stuff
        if 'game_' in inp:
            inp=json.loads(inp)
            print("Got to game_")
            if not (self.__checkSessionID( str(inp['username_']),
                                           str(inp['sessionID_'])
                                           )):
                print("[!] LOG: Session for user %s has expired"
                        % (str(inp['username_'])) )
                return False
            if (str(inp['game_'][0]) == 'listExistingGame'):
                print("Got to list")
                return Controller.printCurrentGameSessionIDs()        # game session id

            #If player is in the session and in the game itself, then call the game 
            #if 
                
        

        
        #Use the current instance of game to send user input to the game instance
        #A remote-controller function would be added to route the input to the appropriate location in the game. 

#???
def main(): 
    ServerSideSocket = socket.socket()
    host = '127.0.0.1'
    port = 2004
    ThreadCount = 0 

    controllerClient = None
    
    print("Waiting for the connection response.")
    try: 
         ServerSideSocket.bind((host, port))
    except socket.error as e:
        print(str(e))

    print('Socket is listening for a connection')
    ServerSideSocket.listen(5)

    def multi_threaded_client(connection):
        #connection.send(str.encode('Server is working:'))

        controllerClient = Controller()
        while True:
            try: 
                data = connection.recv(2048)

                # REGEX PARTS HERE

                # handle data 
                # can you parse input and stuff and save it as a data structure or something
                # HOA

                '''
                if data is not valid:
                    connection.send("data contains invalid input")
                '''
                print(data.decode('utf-8'))
                response=controllerClient.parseInput(data.decode('utf-8'))



                print("response..2")
                print(response)


                if not data:
                    print("Did i break?")
                    break
                else: 
                    print("Received: ", data)
                    print("Sending: ", response) 
            
                print(connection.sendall(response))
            except: 
                break
        
        connection.close()

    while True:
        Client, address = ServerSideSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(multi_threaded_client, (Client, ))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    ServerSideSocket.close()


if __name__ == "__main__":
    main() 