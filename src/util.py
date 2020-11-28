import TwoDice, Bank
from Title import Title, Property, Utility, Transports

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
        if (current['order'] == previous['order']):

            #Set the value to check for matches further in list, assuming value was not matched previously. 
            if (value == 0):
                value = current['order']
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
def getMortgage(self, player, titleDeedsNames, titleDeedsOwned, bank): 
    #Print all title deeds owned
    for titleDeed in titleDeedsNames: 
        print(titleDeed) 
    print("You may need to scroll if you own a large number of title deeds.")

    #User types in title deed to mortgage
    titleDeedToMortgage = input("Enter name of title deed you wish to mortgage: ")  #This needs validation

    #Search for the title deed, and get the card information
    titleDeedRecord  = None 
    for titleDeed in titleDeedsOwned: 
        if (titleDeedToMortgage == titleDeed["Title Deed"].getName()): 
            titleDeedRecord  = titleDeed
    
    #If there is no title deed of such name, stop processing. 
    if (titleDeedRecord  == None): 
        print("There is no title deed card with that name. Returning to previous menu.")
        return #Go to the previous caller function 
    
    #Check if there is any buildings on that title deed and other title deeds of that color group. 
    #If there are any buildings, player must sell all properties first. 
    if (titleDeedRecord["Title Deed"].getTileType() == "Property"):

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
    for titleDeed in titleDeedsOwned: 
        if (titleDeed["Title Deed"].getName() == titleDeedRecord["Title Deed"].getName()): 
            titleDeed["Mortgaged"] = True
    
    bank.subtract(mortgageValue)
    player.changeMonetaryValue(mortgageValue)

    print(player.getName() + ", your mortgage request for " + titleDeedRecord["Title Deed"].getName() + " was successful.\n" + 
        "Returning to the previous menu.")
    
#Helper function to process player's request to repay a mortgaged property back to bank
def repayMortgage(self, player, titleDeedsOwned, bank): 
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
            repayAmount = mortgageValue + (mortgageValue * Bank.MORTGAGE_INTEREST)
        else: 
            print("This property is not mortgaged. Please enter a property that is mortgaged.")
            return #Stop processing, return to the caller function. 
    else: 
        print("This property is not in your list of owned title deeds. Please try again.")
        return #Stop processing, return to the caller function.

    #Make the repayment mortgage to the bank 
    for titleDeed in titleDeedsOwned: 
        if (titleDeed["Title Deed"].getName() == titleDeedStats["Title Deed"].getName()): 
            titleDeed["Mortgaged"] = False
    
    player.changeMonetaryValue(-1 * repayAmount)
    bank.add(repayAmount)

    print(player.getName() + ", your repayment for " + titleDeedStats["Title Deed"].getName() + " was successful.\n" + 
        "Returning to the previous menu.")

#Helper function to process player's interest to get a home

#If user wishes to purchase a house - check if (1) player owns a monopoly on a color group, and then (2) homes are evenly purchased on other properties
#The property also must not be mortgaged as well as others in color group
def purchaseHome(player, titleDeedsNames, titleDeedsOwned, bank): 
    #Print all title deeds owned
    for titleDeed in titleDeedsNames: 
        print(titleDeed) 
    print("You may need to scroll if you own a large number of title deeds.")

    #User types in title deed to mortgage
    titleDeedToPurchaseHouse = input("Enter name of title deed you wish to mortgage: ")  #This needs validation

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
        
    #Check if the property is mortgaged 
    if (titleDeedRecord["Mortgaged"]): 
        print("This property is currently mortgaged. You cannot purchase any buildings.")
        return #Go to the previous caller function

    #Check if there is any buildings on that title deed and other title deeds of that color group. 
    #If there are any buildings, player must sell all properties first. 
    if (titleDeedCard.getTileType() == "Property"):






