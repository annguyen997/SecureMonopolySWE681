import TwoDice 

#Utility methods regarding the order of the player list
def rollOrder(self, element): 
    return element['order']

def checkTies(playerListOrder): 
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
        
        #If there is no tie with current player with previous player of main list, start roll new dice values, and the set the new player positions in main list 
        elif (value != 0): 
            value = 0  #Reset the value to zero
            
            #Check if there are at least two players tied - safety measure
            if (len(playerTies) > 1):
                tieBroken = False 

                #Keep rolling new dice values until tie is broken
                while (not tieBroken):
                    #Roll the dice again for each player with a tie
                    for player in playerTies: 
                        player['order'] = TwoDice.rollDiceBreakTie()
                    
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

        #Replace previous element with current element. That element would then be checked with the next element
        previous = current
        index += 1 
    
    #Return the list order to the caller
    return playerListOrder

