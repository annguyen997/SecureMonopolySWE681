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
    TILES_REAL_ESTATE = [
		1,3,6,8,9,12,14,15,17,19,20,22,24,25,27,28,30,32,33,35,38,40]
	TILES_CHANCE      = [7,23,37]
	TILES_COMMUNITY   = [2,18,34]
	TILES_UTILITIES   = [13,29]
	TILES_TRANSPORT   = [5,16,26,36]
	TILES_TAX         = [4,39]
	TILES_NONE        = [10,21]
	TILES_JAIL        = [11]
	TILES_GO_TO_JAIL  = [31]
	TILES_GO          = [0]

    