class Title(object):
    def __init__(self, tileType, name, rent, homes, hotel, mortgage, ):
        self.cardType = cardType
        self.kind = kind
        self.value = value 

class Property:
    #Listing of all COMMUNITY cards in Monopoly. There are 16 community cards.
    PROPERTY_CARDS = [
        Tile("Property", "Mediterranean Avenue", 0),
		Tile("Property", "Cash", 200),
		Tile("Property", "Cash", -50),
		Tile("Property", "Cash", 50),
		Tile("Property", "Escape Jail", None),
		Tile("Property", "Advance", 11),
		Tile("Property", "Receive", 50), # from every player
		Tile("Property", "Cash", 100),
		Tile("Property", "Cash", 20),
		Tile("Property", "Receive", 10), # from every player
		Tile("Property", "Cash", 100),
		Tile("Property", "Cash", -100),
		Tile("Property", "Cash", -150),
		Tile("Property", "Cash", 25),
		Tile("Property", "Tax", [-40, -115]), # for each [house, hotel]
		Tile("Property", "Cash", 10),
		Tile("Property", "Cash", 100)
	]

    #Property Colors
    BROWN = ["Mediterranean Avenue", "Baltic Avenue"]
    LIGHT_BLUE = ["Oriental Avenue", "Vermont Avenue", "Connecticut Avenue"]
    PINK = ["St. Charles Place", "States Avenue", "Virginia Avenue"]
    ORANGE = ["St. James Place", "Tennessee Avenue", "New York Avenue"]
    RED = ["Kentucky Avenue", "Indiana Avenue", "Illinois Avenue"]
    YELLOW = ["Atlantic Avenue", "Ventnor Avenue", "Marvin Gardens"]
    GREEN = ["Pacific Avenue", "North Carolina Avenue", "Pennsylvania Avenue"]
    DARK_BLUE = ["Park Place", "Boardwalk"]


class Utility: 
    UTILITY = ["Electric Company", "Water Works"]

class Station:
    STATIONS = ["Reading Railroad", "Pennsylvania Railroad", "B. & O. Railroad", "Short Line"]

