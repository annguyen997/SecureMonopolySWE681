import random, sys
from Board import *	

class Card(object): 
	def __init__(self, cardType, kind, value):
		self.cardType = cardType
		self.kind = kind
		self.value = value 

	def __str__(self):
		return "%s(Kind: %s, Value: %s)" % (self.cardType, self.kind, str(self.value))

	def getCardType(self):
		return self.cardType 

	def getKind(self): 
		return self.kind
	
	def getValue(self): 
		return self.value

#Chance Cards
class ChanceCards:
	#Listing of all CHANCE cards in Monopoly. There are 16 chance cards.
	CHANCE_CARDS = [
		Card("Chance", "Advance", "Go"),  										#Advance to Go, collect 200
		Card("Chance", "Advance", Board.TILES_LIST.index("Illinois Avenue")),   #If pass Go, collect 200
		Card("Chance", "Advance", Board.TILES_LIST.index("St. Charles Place")),	#If pass Go, collect 200
		Card("Chance", "Advance", "Utility"),									#Advance to nearest utility
		Card("Chance", "Advance", "Transports"), 								#Advance to nearest transport
		Card("Chance", "Credit", 50), 											#Bank dividends
		Card("Chance", "Escape Jail", None),									#Keep card until needed or traded 
		Card("Chance", "Advance", -3), 											#Go back 3 spaces
		Card("Chance", "Advance", "Go to Jail"),  								#Go directly to jail; do not collect cash (200)
		Card("Chance", "Debit Complex", [-25, -100]), 							#Make repairs on all property, pay each: [house, hotel]
		Card("Chance", "Debit", -15),											#Pay tax to poor of 15
		Card("Chance", "Advance", Board.TILES_LIST.index("Reading Railroad")),	#If pass Go, collect 200
		Card("Chance", "Advance", Board.TILES_LIST.index("Boardwalk")), 		#Advance to Boardwalk, no collecting 200
		Card("Chance", "Debit", -50), 											#Pay each player 50
		Card("Chance", "Credit", 150),											#Building and loan matures
		Card("Chance", "Credit", 100)											#Crossword win 
	]

	def __init__(self):
		#Generate the random order of the CHANCE cards
		seedValue = random.randrange(sys.maxsize)
		random.seed(seedValue)

		self.pile = ChanceCards.CHANCE_CARDS.copy()
		random.shuffle(self.pile)
		#self.pile = random.sample(range(0, len(ChanceCards.CHANCE_CARDS)), len(ChanceCards.CHANCE_CARDS))
		self.jailFreeUsed = False
	
	def __str__(self):
		# Start with calling that is a pile of cards
		string = "PILE OF CHANCE CARDS:\n"

		# Print all the chance cards in deck 
		for cardIndex in self.pile:
			string += " - "
			string += str(self.CHANCE_CARDS[cardIndex])
			string += "\n"

		# Return the generated string
		return string

	def pullCard(self):
		print(self.pile[0])

		#Get the card that is currently at top of pile
		card = self.pile[0]

		#Create a new pile for the cards
		newPile = [] * len(self.pile)
		for i in range(0, len(self.pile) - 1):
			newPile[i] = self.pile[i+1] #Shift all cards to one card higher
			
		if (card.getKind() != "Escape Jail"):
			newPile[len(newPile) - 1] = card #Place recently picked card to the bottom

		#Set the new pile as the game piles
		self.pile = newPile

		#Return the card that was on top of pile to user
		return card
	
	#Return the Jail Free Card back to the pile
	def returnJailFreeCard(self, jailFreeCard): #Verify if the card returned is a Jail Free Card
		if (jailFreeCard.getKind() != "Escape Jail"):
			return None
		
		#Create a new pile for the cards
		newPile = [None] * len(self.pile)
		for i in range(0, len(self.pile) - 1):
			newPile[i] = self.pile[i+1] #Shift all cards to one card higher

		newPile[len(newPile) - 1] = jailFreeCard #Place jail free card back to the pile

		self.pile = newPile

#Community Cards 
class CommunityCards:
	#Listing of all COMMUNITY cards in Monopoly. There are 16 community cards.
	COMMUNITY_CARDS = [
		Card("Community", "Advance", "Go"),  					#Advance to Go, collect 200
		Card("Community", "Credit", 200),						#Bank error - collect 200
		Card("Community", "Debit", -50),						#Doctor's fee 
		Card("Community", "Credit", 50),						#Capital gain from stock
		Card("Community", "Escape Jail", None),					#Keep card until needed or traded 
		Card("Community", "Advance", "Go to Jail"),  			#Go directly to jail; do not collect cash (200)
		Card("Community", "Credit", 50), 						#Collect 50 per player for opening night seats
		Card("Community", "Credit", 100),						#Holiday Fund matures - collect 100
		Card("Community", "Credit", 20),						#Refund from income tax
		Card("Community", "Credit", 10), 						#Birthday - collect 10
		Card("Community", "Credit", 100),						#Life insurance matures - collect $100
		Card("Community", "Debit", -100),						#Pay hospital fees of 100
		Card("Community", "Debit", -150),						#Pay school feeds of 150
		Card("Community", "Credit", 25),						#Receive consultancy fee
		Card("Community", "Debit Complex", [-40, -115]), 		#Make street repairs on all property, pay each: [house, hotel]
		Card("Community", "Credit", 10),						#Won second prize in beauty contest - collect 10
		Card("Community", "Credit", 100)						#Inherited 100
	]
    
	def __init__(self):
		# Generate the random order of the CHANCE cards
		seedValue = random.randrange(sys.maxsize)
		random.seed(seedValue)

		cardList = CommunityCards.COMMUNITY_CARDS.copy()
		self.pile = random.shuffle(cardList)
		#self.pile = random.sample(range(0, len(self.COMMUNITY_CARDS)), len(self.COMMUNITY_CARDS))
		self.jailFreeUsed = False 
	
	def __str__(self):
		# Start with calling that is a pile of cards
		string = "PILE OF COMMUNITY CARDS:\n"

		# Print all the community cards in deck
		for cardIndex in self.pile:
			string += " - "
			string += str(self.COMMUNITY_CARDS[cardIndex])
			string += "\n"

		# Return the generated string
		return string
	
	def pullCard(self): 
		#Get the card that is currently at top of pile
		card = self.pile[0]

		#Create a new pile for the cards
		newPile = [] * len(self.pile)
		for i in range(0, len(self.pile) - 1):
			newPile[i] = self.pile[i+1] #Shift all cards to one card higher
			
		if (card.getKind() != "Escape Jail"):
			newPile[len(newPile) - 1] = card #Place recently picked card to the bottom

		#Set the new pile as the game piles
		self.pile = newPile

		#Return the card that was on top of pile to user
		return card

	#Return the Jail Free Card back to the pile
	def returnJailFreeCard(self, jailFreeCard): #Verify if the card returned is a Jail Free Card
		if (jailFreeCard.getKind() != "Escape Jail"):
			return None
		
		#Create a new pile for the cards
		newPile = [None] * len(self.pile)
		for i in range(0, len(self.pile) - 1):
			newPile[i] = self.pile[i+1] #Shift all cards to one card higher

		newPile[len(newPile) - 1] = jailFreeCard #Place jail free card back to the pile

		self.pile = newPile 
	
