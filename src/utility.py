import TwoDice 

#Utility methods regarding the order of the player list
def rollOrder(self, element): 
    return element['order']

def checkTies(playerListOrder): 
    playerTies = []

    #Check for ties in the rolling order of each player in game 
    previous = None 
    for current in playerListOrder:
        #If there is a tie with the current player with previous player in main list, add to PlayerTies list 
        if (current['order'] == previous['order']):

            #Check if this element's ID already exists in ties list
            elementExists = False
            for player in playerTies: 
                if player['userID'] == previous['userID']:
                    elementExists = True
                    break
    
            #If previous element does not exist in list, add to list
            if (not elementExists): 
                playerTies.append(previous) 
            playerTies.append(current)
        
        previous = current
    
    #Check if ties exist
    if (len(playerTies) > 0):
        
        tiesAgain = False 
        for player in playerTies: 
            player['order'] = TwoDice.rollDice()
            
        #Check for any ties again

        #Re-sort the list 

    else:
        #This means no ties exist in the current list, return list as is
        return playerListOrder 

