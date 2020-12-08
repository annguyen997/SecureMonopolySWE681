#This board is based on most versions of Monopoly, and any variations are not considered. 
class Board: 
	TILES_LIST = ["Go",
	"Mediterranean Avenue",
	"Community Chest",
	"Baltic Avenue",
	"Income Tax",
	"Reading Railroad",
	"Oriental Avenue",
	"Chance",
	"Vermont Avenue",
	"Connecticut Avenue",
	"Just Visiting",
	"In Jail",
	"St. Charles Place",
	"Electric Company",
	"States Avenue",
	"Virginia Avenue",
	"Pennsylvania Railroad",
	"St. James Place",
	"Community Chest",
	"Tennessee Avenue",
	"New York Avenue",
	"Free Parking",
	"Kentucky Avenue",
	"Chance",
	"Indiana Avenue",
	"Illinois Avenue",
	"B & O Railroad",
	"Atlantic Avenue",
	"Ventinor Avenue",
	"Waterworks",
	"Marvin Gardens",
	"Go To Jail",
	"Pacific Avenue",
	"North Carolina Avenue",
	"Community Chest",
	"Pennsylvania Avenue",
	"Short Line",
	"Chance",
	"Park Place",
	"Luxury Tax",
	"Boardwalk"]

	#Numbering of all tiles 
	TILES_REAL_ESTATE = [1,3,6,8,9,12,14,15,17,19,20,22,24,25,27,28,30,32,33,35,38,40]
	TILES_CHANCE = [7,23,37]
	TILES_COMMUNITY = [2,18,34]
	TILES_UTILITY = [13,29]
	TILES_TRANSPORTS = [5,16,26,36]
	TILES_TAX = [4,39]
	TILES_NONE = [10,21]
	TILES_JAIL = [11]
	TILES_GO_TO_JAIL = [31]
	TILES_GO = [0]

	def __init__(self): 
		self.numberTiles = self.getNumberofTiles()		#Get the number of tiles in game
		self.hits = [0] * self.numberTiles           	#Keep track of the number of times a player arrives at a particular tile on board

	def getNumberofTiles(self):
		return (len(Board.TILES_REAL_ESTATE) + len(Board.TILES_CHANCE) +
				len(Board.TILES_COMMUNITY) + len(Board.TILES_UTILITY) +
				len(Board.TILES_TRANSPORTS) + len(Board.TILES_TAX) +
				len(Board.TILES_NONE) + len(Board.TILES_JAIL) +
				len(Board.TILES_GO_TO_JAIL) + len(Board.TILES_GO))
	
	def getTileType(self, playerPosition): 
		#Return the string of type of tile corresponding to position of player
		if playerPosition in Board.TILES_REAL_ESTATE: 
			return "Property"
		elif playerPosition in Board.TILES_CHANCE:
			return "Chance Card"
		elif playerPosition in Board.TILES_COMMUNITY:
			return "Community Card"
		elif playerPosition in Board.TILES_UTILITY:
			return "Utility"
		elif playerPosition in Board.TILES_TRANSPORTS:
			return "Transports"
		elif playerPosition in Board.TILES_TAX:
			return "Tax"
		elif playerPosition in Board.TILES_JAIL:
			return "Jail"
		elif playerPosition in Board.TILES_GO_TO_JAIL:
			return "Go to Jail"
		elif playerPosition in Board.TILES_GO:
			return "Go"
		else:
			return "None"
	
	#Track the number of times players arrive in that tile (using the array)
	def hit(self, tileNum): 
		self.hits[tileNum] += 1
	
	#Get the number of times a tile has been reached, for purposes like property purchasing.
	def getNumberofHits(self, tileNum): 
		return self.hits[tileNum]
