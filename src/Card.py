import random

class Card(object): 
    def __init__(self, cardType, kind, value):
        self.cardType = cardType
        self.kind = kind
        self.value = value 
    
    def __str__(self):
        return "%s(Kind: %s\tValue: %s)" % (self.cardType, self.kind, str(self.value))

#Chance Cards
class ChanceCards: 
    #Listing of all CHANCE cards in Monopoly. There are 16 chance cards. 
    CHANCE_CARDS = [
		Card("Chance", "Advance", 0),
		Card("Chance", "Cash", 200),
		Card("Chance", "Cash", -50),
		Card("Chance", "Cash", 50),
		Card("Chance", "Escape Jail", None),
		Card("Chance", "Advance", 11),
		Card("Chance", "Receive", 50), # from every player
		Card("Chance", "Cash", 100),
		Card("Chance", "Cash", 20),
		Card("Chance", "Receive", 10), # from every player
		Card("Chance", "Cash", 100),
		Card("Chance", "Cash", -100),
		Card("Chance", "Cash", -150),
		Card("Chance", "Cash", 25),
		Card("Chance", "Tax", [-40, -115]), # for each [house, hotel]
		Card("Chance", "Cash", 10),
		Card("Chance", "Cash", 100)
	]

    def __init__(self): 
        #Generate the random order of the CHANCE cards
        self.pile = random.sample(range(0, len(self.CHANCE_CARDS)), len(self.CHANCE_CARDS))
        self.jailFreeUsed = False 

    def pullCard(self): 
        #Get the card that is currently at top of pile
        card = self.pile[0]

        #TODO: Add logic regarding if the Jail-Free card was selected 

        #Generate new pile with picked card placed at the bottom
        newPile = [None] * len(self.pile)
        for i in range(0, len(self.pile) - 1):
            newPile[i] = self.pile[i+1] #Shift all cards to one card higher
        newPile[len(newPile) - 1] = card #Place recently picked card to the bottom

        #Set the new pile as the game pile
        self.pile = newPile

        #Return the card that was on top of pile to user
        return self.CHANCE_CARDS[card]
    
    def __str__(self):
		# Start with calling that is a pile of cards
		string = "PILE OF CHANCE CARDS:\n"

		# Print all the chance cards in deck 
		for cardIndex in self.pile:
			string += " - "
			string += str(self.CARDS[cardIndex])
			string += "\n"

		# Return the generated string
		return string

#Community Cards 
class CommunityCards:
    #Listing of all COMMUNITY cards in Monopoly. There are 16 community cards. 
    
    COMMUNITY_CARDS = [
        Card("Advance", 0),
		Card("Cash", 200),
		Card("Cash", -50),
		Card("Cash", 50),
		Card("Escape Jail", None),
		Card("Advance", 11),
		Card("Receive", 50), # from every player
		Card("Cash", 100),
		Card("Cash", 20),
		Card("Receive", 10), # from every player
		Card("Cash", 100),
		Card("Cash", -100),
		Card("Cash", -150),
		Card("Cash", 25),
		Card("Tax", [-40, -115]), # for each [house, hotel]
		Card("Cash", 10),
		Card("Cash", 100)
	]
    
    def __init__(self): 
        #Generate the random order of the CHANCE cards
        self.pile = random.sample(range(0, len(self.COMMUNITY_CARDS)), len(self.COMMUNITY_CARDS))
        self.jailFreeUsed = False 

    def pullCard(self): 
        #Get the card that is currently at top of pile
        card = self.pile[0]

         #TODO: Add logic regarding if the Jail-Free card was selected 
        #Generate new pile with picked card placed at the bottom
        newPile = [None] * len(self.pile)
        for i in range(0, len(self.pile) - 1):
            newPile[i] = self.pile[i+1] #Shift all cards to one card higher
        newPile[len(newPile) - 1] = card #Place recently picked card to the bottom

        #Set the new pile as the game pile
        self.pile = newPile

        #Return the card that was on top of pile to user
        return self.COMMUNITY_CARDS[card]
    
    def __str__(self):
		# Start with calling that is a pile of cards
		string = "PILE OF COMMUNITY CARDS:\n"

		# Print all the community cards in deck
		for cardIndex in self.pile:
			string += " - "
			string += str(self.CARDS[cardIndex])
			string += "\n"

		# Return the generated string
		return string