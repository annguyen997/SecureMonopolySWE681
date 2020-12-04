from Bank import *
from Title import Title, Property #, Utility, Transports
import math 

"""Utility methods regarding the order of the player list"""
#Determine the method of ordering of players in list
def rollOrder(self, element): 
    return element['order']

def checkTies(playerListOrder, dice): 
    #Check for ties in the rolling order of each player in game 

    playerTies = []         #List of players that are tied
    previous = None         #Previous object in list to compare
    value = 0               #Die value which there is a tie
    index = 0               #Current position in list
    tiedStartIndex = 0      #Starting index which ties first occur

    for current in playerListOrder:
        #If there is a tie with the current player with previous player in main list, add to PlayerTies list 
        if (current.get('order') == previous.get('order')):

            #Set the value to check for matches further in list, assuming value was not matched previously. 
            if (value == 0):
                value = current.get('order')
                tiedStartIndex = index - 1

            #Check if this element's ID already exists in ties list
            elementExists = False
            for player in playerTies: 
                if player['userID'] == previous['userID']:
                    elementExists = True
                    break
    
            #If previous element does not exist in list, add to list
            if (not elementExists): 
                playerTies.append(previous) 
            #Add the current object being compared to the list
            playerTies.append(current)
        
        #If there is no tie with current player with previous player of main list, start roll new dice values, and the set the new player positions in main list resolving the ties
        elif (value != 0): 
            value = 0  #Reset the value to zero
            
            #Check if there are at least two players tied - safety measure
            if (len(playerTies) > 1):
                tieBroken = False 

                #Keep rolling new dice values until tie is broken
                while (not tieBroken):
                    #Roll the dice again for each player with a tie
                    for player in playerTies: 
                        player['order'] = dice.rollDiceBreakTie()
                    
                    #Check if there are new unlikely ties in the new rolling
                    previous = None
                    secondTie = False
                    for player in playerTies: 
                        if player['order'] == previous['order']: 
                            secondTie = False
                        previous = player 
                    
                    #If there are no more ties, mark tie broken as True
                    if (not secondTie):
                        tieBroken = True

                #Sort the players in the players tie list
                playerTies.sort(key=rollOrder)

                #Once tie is broken, set new positions of players in main list, starting at index which tie begins
                indexToReplace = tiedStartIndex
                for player in playerTies: 
                    playerListOrder[indexToReplace] = player
                    indexToReplace += 1
                
                #Reset the starting index to zero, and clear out players in the ties list
                tiedStartIndex = 0 
                playerTies = []

        #Replace previous element with current element. That element would then be checked with the next element. This is the default set of code
        previous = current
        index += 1 
    
    #Return the list order to the caller
    return playerListOrder


""" Methods regarding user's processing of existing title deeds """ 
#Helper function to process player's interest to get mortgage on a title deed. 
def getMortgage(self, player, titleDeedsNames, titleDeedsOwned, bank = None):
    #Print all title deeds owned
    for titleDeed in titleDeedsNames: 
        print(titleDeed) 
    print("You may need to scroll if you own a large number of title deeds.")

    #User types in title deed to mortgage
    titleDeedToMortgage = input("Enter name of title deed you wish to mortgage: ")  #This needs validation

    #Search for the title deed, and get the card information
    titleDeedRecord = None 
    for titleDeed in titleDeedsOwned: 
        if (titleDeedToMortgage == titleDeed["Title Deed"].getName()): 
            titleDeedRecord  = titleDeed
    
    #If there is no title deed of such name, stop processing. 
    if (titleDeedRecord == None): 
        print("There is no title deed card with that name. Returning to previous menu.")
        return #Go to the previous caller function 
    
    #Check if there is any buildings on that title deed and other title deeds of that color group. 
    #If there are any buildings, player must sell all properties first. 
    if (titleDeedRecord["Title Deed"].getTitleType() == "Property"):

        #Get the color group information from card and player's current monopolies
        colorGroup = titleDeedRecord["Title Deed"].getColorGroup()
        playerColorMonopoly = player.getColorMonopoly()
        colorGroupStats = None 

        #Get the stats information on that monopoly
        for colorMonopoly in playerColorMonopoly: 
            if (colorMonopoly["Color Group"] == colorGroup):
                colorGroupStats = colorMonopoly
        
        #Check if there is any property, and if so inform player the property cannot be mortgaged 
        if (colorGroupStats["Number Buildings Built"] > 0):
            print("You cannot mortgage this property because there are buildings in at least one of properties in the color group " + colorGroup) 

            #List the title deeds in the color group with buildings
            propertiesList = Title.getColorGroup(colorGroup)
            for propertyItem in propertiesList:
                for titleDeed in titleDeedsOwned: 
                    if (titleDeed["Title Deed"].getName() == propertyItem): 
                        print("Property Name: " + propertyItem + 
                        "\nNumber of Houses: " + titleDeed["Houses"] + 
                        "\nNumber of Hotels: " + titleDeed["Hotels"] + "\n")
            
            print("If you wish to add a mortgage to " + titleDeedToMortgage + "please sell all buildings first in this color group first.")

            return  #Go to the previous caller function 

    #Get the mortgage value 
    mortgageValue = titleDeedRecord["Title Deed"].getMortgageValue()

    #Make the mortgage
    player.addMortgage(titleDeedRecord["Title Deed"], mortgageValue, bank)

    print(player.getName() + ", your mortgage request for " + titleDeedRecord["Title Deed"].getName() + " was successful.\n" + 
        "Returning to the previous menu.")
    
#Helper function to process player's request to repay a mortgaged property back to bank
def repayMortgage(self, player, titleDeedsOwned, bank = None):
    #Print all title deeds owned that are mortgaged
    for titleDeedRecord in titleDeedsOwned: 
        if (titleDeedRecord["Mortgaged"]): 
            print(titleDeedRecord["Title Deed"].getName())
    print("You may need to scroll if you have many title deeds mortgaged.")

    #User types in title deed to mortgage
    titleDeedToRepay = input("Enter name of mortgaged title deed you wish to repay: ")  #This needs validation

    #Check if title deed is in the list
    titleDeedOwned = False
    titleDeedStats = None
    for titleDeedRecord in titleDeedsOwned: 
        if (titleDeedToRepay == titleDeedRecord["Title Deed"].getName()): 
            titleDeedStats = titleDeedRecord
            titleDeedOwned = True
    
    #If player has that title deed, check if it is mortgaged
    repayAmount = 0
    if (titleDeedOwned):
        #Check if that title deed is mortgaged
        if (titleDeedStats["Mortgaged"]): 

            #Get the mortgage value
            mortgageValue = titleDeedStats["Title Deed"].getMortgageValue()

            #Calculate repayment amount with interest
            repayAmount = int(math.ceil((mortgageValue + (mortgageValue * Bank.MORTGAGE_INTEREST))/100.0) * 100)
        else: 
            print("This property is not mortgaged. Please enter a property that is mortgaged.")
            return #Stop processing, return to the caller function. 
    else: 
        print("This property is not in your list of owned title deeds. Please try again.")
        return #Stop processing, return to the caller function.

    #Make the repayment mortgage to the bank 
    player.removeMortgage(titleDeedStats["Title Deed"].getName(), repayAmount, bank)

    print(player.getName() + ", your repayment for " + titleDeedStats["Title Deed"].getName() + " was successful.\n" + 
        "Returning to the previous menu.")

#Helper function to process player's interest to get a house
def purchaseHome(player, titleDeedsNames, titleDeedsOwned, bank): 
    #Print all title deeds owned
    for titleDeed in titleDeedsNames: 
        print(titleDeed) 
    print("You may need to scroll if you own a large number of title deeds.")

    #User types in title deed to buy a hotel
    titleDeedToPurchaseHouse = input("Enter name of title deed you wish to buy a house: ")  #This needs validation

    #Search for the title deed, and get the card information
    titleDeedRecord = None 
    for titleDeed in titleDeedsOwned: 
        if (titleDeedToPurchaseHouse == titleDeed["Title Deed"].getName()): 
            titleDeedRecord = titleDeed
    
    #If there is no title deed of such name, stop processing. 
    if (titleDeedRecord == None): 
        print("There is no title deed card with that name. Returning to previous menu.")
        return #Go to the previous caller function 

    #Check if the property's color group is a monopoly.
    colorGroup = titleDeedRecord["Title Deed"].getColorGroup()
    monopolyList = player.getColorMonopoly()
    colorMonopoly = False 
    if (colorGroup in monopolyList):
        colorMonopoly = True 
    
    if (not colorMonopoly): 
        print("You cannot purchase a home at this time; you must own all properties of color group " + colorGroup + "first before you can purchase home.")
        return #Go to the previous caller function 

    #Check if the current property is mortgaged
    if (titleDeedRecord["Mortgaged"]): 
        print("This property is currently mortgaged. You cannot purchase any buildings.")
        return #Go to the previous caller function
    
    #Check if other properties of that color group are mortgaged
    if (colorMonopoly):
        propertiesList = Title.getColorGroup(colorGroup)

        otherPropertiesMortgaged = False 

        for propertyItem in propertiesList:
            for titleDeed in titleDeedsOwned: 
                if (titleDeed["Title Deed"].getName() == propertyItem):
                    if (titleDeed["Mortgaged"]): 
                        print("This property " + titleDeed["Title Deed"].getName() + " is mortgaged.")
                        otherPropertiesMortgaged = True
        
        if (otherPropertiesMortgaged): 
            print("Please repay the mortgages of the other properties first before purchasing buildings.")
            return #Go to the previous caller function
    
    #Check if other properties have the exactly same number as homes/hotels available for this property
    if (colorMonopoly):
        #Get current number of buildings of title deed player wishes to purchase another building
        getCurrentHouses = titleDeedRecord["Houses"]

        #Check other properties of the color group
        propertiesList = Title.getColorGroup(colorGroup)

        notEvenHouses = False 
        for propertyItem in propertiesList:
            for titleDeed in titleDeedsOwned: 
                if (titleDeed["Title Deed"].getName() == propertyItem):
                    #Get current number of buildings of that title deed
                    getCurrentHousesOther = titleDeed["Houses"]

                    print("Property Name: " + titleDeed["Title Deed"].getName() + "\tNumber of Houses: " + getCurrentHousesOther)
                    if (getCurrentHousesOther < getCurrentHouses):
                        notEvenHouses = True

        if (notEvenHouses): 
            print("You cannot build another house on this property " + titleDeedRecord["Title Deed"].getName() + " right now.\nPlease ensure all other properties of the color group " + colorGroup + " have exactly " + getCurrentHouses + " each before proceeding.")
            return #Go to the previous caller function.
    
    #Check if current property has four houses
    if (titleDeedRecord["Houses"] == 4): 
        print("You cannot purchase another house on this property. You may purchase a hotel instead.")
        return #Go to the previous caller function. 

    #If other requirements are passed, purchase the house 
    buildingCost = titleDeedRecord["Title Deed"].getBuildingCosts(Property.HOMES_COST)

    #Purchase the home by purchasing from bank and then get the home
    player.purchaseHouse(titleDeedToPurchaseHouse, buildingCost, bank)

    print(player.getName() + ", has purchased a house for " + titleDeedRecord["Title Deed"].getName() + 
        "Returning to the previous menu.")
    
#Helper function to process player's interest to get a hotel 
def purchaseHotel(player, titleDeedsNames, titleDeedsOwned, bank): 
    #Print all title deeds owned
    for titleDeed in titleDeedsNames: 
        print(titleDeed) 
    print("You may need to scroll if you own a large number of title deeds.")

    #User types in title deed to buy a hotel 
    titleDeedToPurchaseHotel = input("Enter name of title deed you wish to buy a hotel: ")  #This needs validation

    #Search for the title deed, and get the card information
    titleDeedRecord = None 
    for titleDeed in titleDeedsOwned: 
        if (titleDeedToPurchaseHotel == titleDeed["Title Deed"].getName()): 
            titleDeedRecord = titleDeed
    
    #If there is no title deed of such name, stop processing. 
    if (titleDeedRecord == None): 
        print("There is no title deed card with that name. Returning to previous menu.")
        return #Go to the previous caller function 

    #Check if the property's color group is a monopoly.
    colorGroup = titleDeedRecord["Title Deed"].getColorGroup()
    monopolyList = player.getColorMonopoly()
    colorMonopoly = False 
    if (colorGroup in monopolyList):
        colorMonopoly = True 
    
    if (not colorMonopoly): 
        print("You cannot purchase a hotel at this time; you must own all properties of color group " + colorGroup + "first before you can purchase a hotel, which requires building four houses first.")
        return #Go to the previous caller function 

    #Check if the current property is mortgaged
    if (titleDeedRecord["Mortgaged"]): 
        print("This property is currently mortgaged. You cannot purchase any buildings.")
        return #Go to the previous caller function
    
    #Check if other properties of that color group are mortgaged
    if (colorMonopoly):
        propertiesList = Title.getColorGroup(colorGroup)

        otherPropertiesMortgaged = False 

        for propertyItem in propertiesList:
            for titleDeed in titleDeedsOwned: 
                if (titleDeed["Title Deed"].getName() == propertyItem):
                    if (titleDeed["Mortgaged"]): 
                        print("This property " + titleDeed["Title Deed"].getName() + " is mortgaged.")
                        otherPropertiesMortgaged = True
        
        if (otherPropertiesMortgaged): 
            print("Please repay the mortgages of the other properties first before purchasing buildings.")
            return #Go to the previous caller function
    
    #Check if this building has already reached the limit for hotels 
    if (titleDeedRecord["Hotels"] == 1): 
        print("You cannot purchase any more hotels on this property. You have reached the limit.")
        
    #Check if other properties have the exactly same number as homes as this property, in this case four
    if (colorMonopoly):
        #Check other properties of the color group
        propertiesList = Title.getColorGroup(colorGroup)

        notEvenHouses = False 
        for propertyItem in propertiesList:
            for titleDeed in titleDeedsOwned: 
                if (titleDeed["Title Deed"].getName() == propertyItem):
                    #Get current number of buildings of that title deed
                    getCurrentHousesOther = titleDeed["Houses"]

                    print("Property Name: " + titleDeed["Title Deed"].getName() + "\tNumber of Houses: " + getCurrentHousesOther)
                    if (getCurrentHousesOther != 4):
                        notEvenHouses = True

        if (notEvenHouses): 
            print("You cannot build a hotel on this property " + titleDeedRecord["Title Deed"].getName() + " right now.\nPlease ensure all other properties of the color group " + colorGroup + " each have exactly 4 houses before proceeding.")
            return #Go to the previous caller function.
    
    #If other requirements are passed, purchase the hotel
    buildingCost = titleDeedRecord["Title Deed"].getBuildingCosts(Property.HOTELS_COST)

    #Purchase the hotel by purchasing from bank and then get the home
    player.purchaseHotel(titleDeedToPurchaseHotel, buildingCost, bank)

    print(player.getName() + ", has purchase a hotel for " + titleDeedRecord["Title Deed"].getName() + 
        "Returning to the previous menu.")
    
#Helper function to process player's interest to sell a house (assumes property not mortgaged)
def sellHome(player, titleDeedsNames, titleDeedsOwned, bank): 
    #Print all title deeds owned that have houses
    for titleDeedRecord in titleDeedsOwned: 
        if (titleDeedRecord["Houses"] != None and titleDeedRecord["Houses"] >= 1): 
            print(titleDeedRecord["Title Deed"].getName())
    print("You may need to scroll if you have many title deeds with houses.")

    #User types in title deed to sell the home
    titleDeedToSellHouse = input("Enter name of title deed you wish to sell a home: ")  #This needs validation

    #Search for the title deed, and get the card information
    titleDeedRecord = None 
    for titleDeed in titleDeedsOwned: 
        if (titleDeedToSellHouse == titleDeed["Title Deed"].getName()): 
            titleDeedRecord = titleDeed
    
    #If there is no title deed of such name, stop processing. 
    if (titleDeedRecord == None): 
        print("There is no title deed card with that name. Returning to previous menu.")
        return #Go to the previous caller function 

    #Check if other properties have the exactly same number as homes/hotels available for this property before selling. First current number of buildings of title deed player wishes to sell another building
    getCurrentHouses = titleDeedRecord["Houses"]

    #Check if current property has no homes to sell
    if (getCurrentHouses == 0): 
        print("You do not have any houses to sell.")
        return #Go to the previous caller function. 

    #Check other properties of the color group
    colorGroup = titleDeedRecord["Title Deed"].getColorGroup()
    propertiesList = Title.getColorGroup(colorGroup)

    notEvenHouses = False 
    for propertyItem in propertiesList:
        for titleDeed in titleDeedsOwned: 
            if (titleDeed["Title Deed"].getName() == propertyItem):
                getCurrentBuildingsOther = 0 

                #Get current number of buildings of that title deed
                getCurrentHousesOther = titleDeed["Houses"]

                #Get the number of hotels of that title deed
                getCurrentHotelsOther = titleDeed["Hotel"]
                if (getCurrentHotelsOther):
                    getCurrentBuildingsOther = getCurrentHousesOther + getCurrentHotelsOther 
                else: 
                    getCurrentBuildingsOther = getCurrentHousesOther

                print("Property Name: " + titleDeed["Title Deed"].getName() + "\tNumber of Houses: " + getCurrentHousesOther + "\tNumber of Hotels: " + getCurrentHotelsOther)

                if (getCurrentBuildingsOther > getCurrentHouses):
                    notEvenHouses = True

    if (notEvenHouses): 
        print("You cannot sell a house on this property " + titleDeedRecord["Title Deed"].getName() + " right now.\nPlease ensure all other properties of the color group " + colorGroup + " have exactly " + getCurrentHouses + " each before proceeding.")
        return #Go to the previous caller function.

    #If other requirements are passed, sell the home  
    sellBuildingAmount = titleDeedRecord["Title Deed"].getBuildingCosts(Property.HOMES_COST) * 0.50 

    #Purchase the home by purchasing from bank and then get the home
    player.sellHome(titleDeedToSellHouse, sellBuildingAmount, bank)

    print(player.getName() + ", has sold a house for " + titleDeedRecord["Title Deed"].getName() + 
        "Returning to the previous menu.")

#Helper function to process player's interest to sell a hotel (assumes property not mortgaged)
def sellHotel(player, titleDeedsNames, titleDeedsOwned, bank): 
    #Print all title deeds owned that have hotel
    for titleDeedRecord in titleDeedsOwned: 
        if (titleDeedRecord["Hotels"] != None and titleDeedRecord["Hotels"] == 1): 
            print(titleDeedRecord["Title Deed"].getName())
    print("You may need to scroll if you have many title deeds with hotels.")

    #User types in title deed to buy a hotel 
    titleDeedToSellHotel = input("Enter name of title deed you wish to sell a hotel: ")  #This needs validation

    #Search for the title deed, and get the card information
    titleDeedRecord = None 
    for titleDeed in titleDeedsOwned: 
        if (titleDeedToSellHotel == titleDeed["Title Deed"].getName()): 
            titleDeedRecord = titleDeed
    
    #If there is no title deed of such name, stop processing. 
    if (titleDeedRecord == None): 
        print("There is no title deed card with that name. Returning to previous menu.")
        return #Go to the previous caller function 
    
    #Check if that property is in the monopoly
    colorGroup = titleDeedRecord["Title Deed"].getColorGroup()
    propertiesList = Title.getColorGroup(colorGroup)
    
    propertyInGroup = False
    if (titleDeedRecord["Title Deed"].getName() in propertiesList): 
        propertyInGroup = True
    
    if (not propertyInGroup): 
        print("This property is not part of a monopoly. Returning to the previous menu.")
        return #Go to the previous caller function 

    #Check if other properties have the exactly same number as homes/hotels available for this property before selling.
    getCurrentHotels = titleDeedRecord["Hotels"]

    #Check if current property has no homes to sell
    if (getCurrentHotels == 0): 
        print("You do not have any hotels to sell.")
        return #Go to the previous caller function. 

    #Since a player would already have at most one hotel (and thus that property part of monopoly), and other functions have already handled the checking process of number of houses before selling (meaning any other properties must have at least four homes), checking the number of hotels is not necessary.
    #If other requirements are passed, sell the hotel.  
    sellBuildingAmount = titleDeedRecord["Title Deed"].getBuildingCosts(Property.HOTELS_COST) * 0.50 

    #Purchase the home by purchasing from bank and then get the home
    player.sellHotel(titleDeedToSellHotel, sellBuildingAmount, bank)

    print(player.getName() + ", has sold a hotel for " + titleDeedRecord["Title Deed"].getName() + 
        "Returning to the previous menu.")

#Helper function to process player's request to sell a property to another player
def sellProperty(playerOwner, playerReceiver, titleDeedsNames, titleDeedsOwned, bank): 
    #Print all title deeds owned by the owner 
    for titleDeed in titleDeedsNames: 
        print(titleDeed) 
    print("You may need to scroll if you own a large number of title deeds.")

    #User types in title deed to sell
    titleDeedToSellProperty = input("Enter name of property title deed you wish to sell: ")  #This needs validation

    #Search for the title deed, and get the card information
    titleDeedRecord = None 
    for titleDeed in titleDeedsOwned: 
        if (titleDeedToSellProperty == titleDeed["Title Deed"].getName()): 
            titleDeedRecord = titleDeed
    
    #If there is no title deed of such name, stop processing. 
    if (titleDeedRecord == None): 
        print("There is no title deed card with that name. Aborting sell. Returning to previous menu.")
        return #Go to the previous caller function 

    #Check if this title deed is a property
    if (titleDeedRecord["Title Deed"].getTitleType() != "Property"): 
        print("This title deed is not a property. Aborting sell. Returning to previous menu.")
        return #Go to the previous caller function  

    #Check if there is any buildings on that title deed and other title deeds of that color group. 
    #If there are any buildings, player must sell all properties first. 
    if (titleDeedRecord["Title Deed"].getTitleType() == "Property" and titleDeedRecord["Mortgaged"] == False):

        #Get the color group information from card and player's current monopolies
        colorGroup = titleDeedRecord["Title Deed"].getColorGroup()
        playerColorMonopoly = playerOwner.getColorMonopoly()
        colorGroupStats = None 

        #Get the stats information on that monopoly
        for colorMonopoly in playerColorMonopoly: 
            if (colorMonopoly["Color Group"] == colorGroup):
                colorGroupStats = colorMonopoly
        
        #Check if there is any buildings, and if so inform player the property cannot be sold until all buildings ar esold
        if (colorGroupStats["Number Buildings Built"] > 0):
            print("You cannot sell this property because there are buildings in at least one of properties in the color group " + colorGroup) 

            #List the title deeds in the color group with buildings
            propertiesList = Title.getColorGroup(colorGroup)
            for propertyItem in propertiesList:
                for titleDeed in titleDeedsOwned: 
                    if (titleDeed["Title Deed"].getName() == propertyItem): 
                        print("Property Name: " + propertyItem + 
                        "\nNumber of Houses: " + titleDeed["Houses"] + 
                        "\nNumber of Hotels: " + titleDeed["Hotels"] + "\n")
            
            print("If you wish to sell this property, " + titleDeedRecord["Title Deed"].getName() + "please sell all buildings in this color group first.")

            return  #Go to the previous caller function 
    
    #Check if the property is mortgaged
    mortgaged = titleDeedRecord["Mortgaged"]

    #Make the selling price 
    agreementReached = False
    amountWishToSell = 0

    titleDeedName = titleDeedRecord["Title Deed"].getName()
    while (not agreementReached):
        amountWishToSell = makeSellTitleDeedDeal(playerOwner, playerReceiver, titleDeedName)
        if (amountWishToSell > 0): 
            agreementReached = True

    #If agreement reached, make the sell - owner begins the selling
    titleDeedInTransit = playerOwner.sellTitle(titleDeedName, amountWishToSell)
    playerReceiver.inheritTitle(titleDeedInTransit, amountWishToSell, mortgaged, bank)

    #Clear any debt to the receiver
    reduceDebtAfterSell(playerOwner, playerReceiver)

    print(playerOwner.getName() + ", has sold the property " + titleDeedRecord["Title Deed"].getName() + " to " + playerReceiver.getName() + "\n" + "Returning to the previous menu.")

#Helper function to process player's request to sell a utility to another player
def sellUtility(playerOwner, playerReceiver, titleDeedsNames, titleDeedsOwned, bank): 
    #Print all title deeds owned by the owner 
    for titleDeed in titleDeedsNames: 
        print(titleDeed) 
    print("You may need to scroll if you own a large number of title deeds.")

    #User types in title deed to sell
    titleDeedToSellUtility = input("Enter name of utility title deed you wish to sell: ")  #This needs validation

    #Search for the title deed, and get the card information
    titleDeedRecord = None 
    for titleDeed in titleDeedsOwned: 
        if (titleDeedToSellUtility == titleDeed["Title Deed"].getName()): 
            titleDeedRecord = titleDeed
    
    #If there is no title deed of such name, stop processing. 
    if (titleDeedRecord == None): 
        print("There is no title deed card with that name. Aborting sell. Returning to previous menu.")
        return #Go to the previous caller function 

    #Check if this title deed is a utility
    if (titleDeedRecord["Title Deed"].getTitleType() != "Utility"): 
        print("This title deed is not a utility. Aborting sell. Returning to previous menu.")
        return #Go to the previous caller function  
    
    #Check if the property is mortgaged
    mortgaged = titleDeedRecord["Mortgaged"]

    #Make the selling price 
    agreementReached = False
    amountWishToSell = 0 

    while (not agreementReached): 
        amountWishToSell = makeSellTitleDeedDeal(playerOwner, playerReceiver, titleDeedRecord["Title Deed"].getName())
        if (amountWishToSell > 0): 
            agreementReached = True
        
    #If agreement reached, make the sell - owner begins the selling
    titleDeedInTransit = playerOwner.sellTitle(titleDeedRecord["Title Deed"].getName(), amountWishToSell)
    playerReceiver.inheritTitle(titleDeedInTransit, amountWishToSell, mortgaged, bank)

    #Clear any debt to the receiver
    reduceDebtAfterSell(playerOwner, playerReceiver)
    
    print(playerOwner.getName() + ", has sold the utility " + titleDeedRecord["Title Deed"].getName() + " to " + playerReceiver.getName() + "\n" + "Returning to the previous menu.")

#Helper function to process player's request to sell a utility to another player
def sellTransport(playerOwner, playerReceiver, titleDeedsNames, titleDeedsOwned, bank): 
    #Print all title deeds owned by the owner 
    for titleDeed in titleDeedsNames: 
        print(titleDeed) 
    print("You may need to scroll if you own a large number of title deeds.")

    #User types in title deed to sell
    titleDeedToSellTransport = input("Enter name of transport title deed you wish to sell: ")  #This needs validation

    #Search for the title deed, and get the card information
    titleDeedRecord = None 
    for titleDeed in titleDeedsOwned: 
        if (titleDeedToSellTransport == titleDeed["Title Deed"].getName()): 
            titleDeedRecord = titleDeed
    
    #If there is no title deed of such name, stop processing. 
    if (titleDeedRecord == None): 
        print("There is no title deed card with that name. Aborting sell. Returning to previous menu.")
        return #Go to the previous caller function 

    #Check if this title deed is a utility
    if (titleDeedRecord["Title Deed"].getTitleType() != "Transports"): 
        print("This title deed is not a transports. Aborting sell. Returning to previous menu.")
        return #Go to the previous caller function  
    
    #Check if the property is mortgaged
    mortgaged = titleDeedRecord["Mortgaged"]

    #Make the selling price 
    agreementReached = False
    amountWishToSell = 0 

    while (not agreementReached): 
        amountWishToSell = makeSellTitleDeedDeal(playerOwner, playerReceiver, titleDeedRecord["Title Deed"].getName())
        if (amountWishToSell > 0): 
            agreementReached = True
        
    #If agreement reached, make the sell - owner begins the selling
    titleDeedInTransit = playerOwner.sellTitle(titleDeedRecord["Title Deed"].getName(), amountWishToSell)
    playerReceiver.inheritTitle(titleDeedInTransit, amountWishToSell, mortgaged, bank)

    #Clear any debt to the receiver
    reduceDebtAfterSell(playerOwner, playerReceiver)

    print(playerOwner.getName() + ", has sold the transport " + titleDeedRecord["Title Deed"].getName() + " to " + playerReceiver.getName() + "\n" + "Returning to the previous menu.")

#Helper function to determine if player owns any debt to another player after sell transaction 
def reduceDebtAfterSell(playerOwner, playerReceiver): 
    #Check if there is any existing debt to the bank, and if so reduce debt. 
    debtOwned = playerOwner.getDebtRecord() 

    for record in debtOwned: 
        if (record["Player"] == playerReceiver): 
            amountOwned = record["Debt Owned"]
            currentMonetaryAmount = playerOwner.getMonetaryValue()

            #To reduce debt, the sell must result in positive monetary cash amount
            if (currentMonetaryAmount > 0):
                if (currentMonetaryAmount >= amountOwned): 
                    #Player has enough cash to clear the debt, and has at least some money
                    playerOwner.changeMonetaryValue(-1 * amountOwned) 
                    playerOwner.reduceDebt(playerReceiver, amountOwned) 
                else: 
                    #Player does not have enough cash to clear debt fully 
                    playerOwner.changeMonetaryValue(-1 * amountOwned) 
                    playerOwner.reduceDebt(playerReceiver, amountOwned - currentMonetaryAmount)

""" Helper functions to assist in selling title deeds """ 
#Helper function to select player to receive a title deed from a possible sale
def selectPlayerToSell(self, player, titleDeedType = "none"):
    playerReceiver = None 

    #Get the names of the players
    playerNames = []
    for playerItem in self.players:
        #If current player, skip
        if (playerItem.getName() == player.getName()):
            continue
        print(playerItem.getName())
        playerNames.append(playerItem.getName())

    #Request for player name, and validate the input.
    validSender = False

    playerRequest = None
    while (not validSender): 
        playerRequest = input("Select a player which you wish to sell a " + titleDeedType + " title deed: ") 

        if (playerRequest in playerNames):
            validSender = True
        else: 
            print("Please enter a valid player name.")
    
    #Get the player name from the request variable (used as a safety mechanism) and return the name
    playerReceiver = playerRequest
    return playerReceiver

#Helper function to make the selling arrangement between two players 
def makeSellTitleDeedDeal(self, playerOwner, playerReceiver, titleDeedName = ""):
    amountWishToSell = playerReceiver.provideAmount("Selling", titleDeedName)
    ownerResponse = playerOwner.decideAmount(playerReceiver.getName(), titleDeedName, amountWishToSell)

    if (ownerResponse): 
        return amountWishToSell
    else: 
        print("The owner did not accept the amount offered.")
        return 0