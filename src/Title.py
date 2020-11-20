class Title(object):
    def __init__(self, tileType, name, printed, rent, mortgage, rentCosts = [0], buildingCosts = [0], colorGroup = None):
        self.titleType = titleType              #The type of the title deed
        self.name = name                        #The name of the property or utility
        self.printed = printed                  #The printed value when player lands on title deed if no one has claimed
        self.rent = rent                        #The rental price for non-owners
        self.mortgage = mortgage                #The rental price in mortgaged value for non-owners 

        #These instance variables may vary by title type 
        self.rentCosts = rentCosts              #The rent costs associated with title deed based on number of homes/hotels
        self.buildingCosts = buildingCosts      #The building costs associated with title deed, pending on home/hotel 
        self.colorGroup = colorGroup            #Color group of the title deed (Property cards only)

        def getTitleType(self):
            return self.titleType
        
        def getName(self):
            return self.name 
        
        def getPrintedValue(self):
            return self.printed
        
        def getRentValue(self):
            return self.rent
        
        def getMortgageValue(self):
            return self.mortgage
        
        def getRentCosts(self, index):
            return self.rentCosts[index]
        
        def getBuildingCosts(self, index):
            return self.buildingCosts[index]
        
        def getColorGroup(self):
            return self.colorGroup

        """
        Notes: 
        - Rent Costs are in this order: [1 House, 2 Houses, 3 Houses, 4 Houses, Hotel]
        - Building Costs are in this order [Home, Hotel]

        - For each property, up to 4 homes are permitted. To purchase a hotel, 4 homes must be returned to bank. 
        - For each property, up to 1 hotel is permitted with no homes. 

        - A player can buy any house or hotel on their turn or between other players' turns.
        - A player must buy all title deeds of a color group in order to purchase homes and hotels. Owning all sites of a color group is known as "owning a monopoly". 
        - Players' must build houses evenly (e.g. a player cannot build a second house on a title deed/site until every site of that color group has at least one house).

        """

class Property:
    #Property Colors
    BROWN = ["Mediterranean Avenue", "Baltic Avenue"]
    LIGHT_BLUE = ["Oriental Avenue", "Vermont Avenue", "Connecticut Avenue"]
    PINK = ["St. Charles Place", "States Avenue", "Virginia Avenue"]
    ORANGE = ["St. James Place", "Tennessee Avenue", "New York Avenue"]
    RED = ["Kentucky Avenue", "Indiana Avenue", "Illinois Avenue"]
    YELLOW = ["Atlantic Avenue", "Ventnor Avenue", "Marvin Gardens"]
    GREEN = ["Pacific Avenue", "North Carolina Avenue", "Pennsylvania Avenue"]
    DARK_BLUE = ["Park Place", "Boardwalk"]
    
    #The constant value for players to pay rent on undeveloped sites if an owner gets all title deeds of a color group
    DOUBLE_RENT = 2 

    #Number of properties permitted
    HOMES_RENT = [1, 2, 3, 4]
    HOTEL_RENT = [1]            #This would be the value '5' in the rent costs list 

    #Listing of all COMMUNITY cards in Monopoly. There are 16 community cards.
    PROPERTY_CARDS = [
        Title("Property", "Mediterranean Avenue", 60, 2, 30, [10, 30, 90, 160, 250], [50, 50], 'BROWN'),
		Title("Property", "Baltic Avenue", 60, 4, 30, [20, 60, 180, 320, 450], [50, 50], 'BROWN'),

		Title("Property", "Oriental Avenue", 100, 6, 50, [30, 90, 270, 400, 550], [50, 50], 'LIGHT_BLUE'),
		Title("Property", "Vermont Avenue", 100, 6, 50, [30, 90, 270, 400, 550], [50, 50], 'LIGHT_BLUE'),
		Title("Property", "Connecticut Avenue", 120, 8, 60, [40, 100, 300, 450, 600], [50, 50], 'LIGHT_BLUE'),

		Title("Property", "St. Charles Place", 140, 10, 70, [50, 150, 450, 625, 750], [100, 100], 'PINK'),
		Title("Property", "States Avenue", 140, 10, 70, [50, 150, 450, 625, 750], [100, 100], 'PINK'),
		Title("Property", "Virginia Avenue", 160, 12, 80, [60, 180, 500, 700, 900], [100, 100], 'PINK'),

		Title("Property", "St. James Place", 180, 14, 90, [70, 200, 550, 750, 950], [100, 100], 'ORANGE'),
		Title("Property", "Tennessee Avenue", 180, 14, 90, [70, 200, 550, 750, 950], [100, 100], 'ORANGE'),
		Title("Property", "New York Avenue", 200, 16, 100, [80, 220, 600, 800, 1000], [100, 100], 'ORANGE'),

		Title("Property", "Kentucky Avenue", 220, 18, 110, [90, 250, 700, 875, 1050], [150, 150], 'RED'),
		Title("Property", "Indiana Avenue", 220, 18, 110, [90, 250, 700, 875, 1050], [150, 150], 'RED'),
		Title("Property", "Illinois Avenue", 240, 20, 120, [100, 300, 750, 925, 1100], [150, 150], 'RED'),

		Title("Property", "Atlantic Avenue", 260, 22, 130, [110, 330, 800, 975, 1150], [150, 150], 'YELLOW'),
		Title("Property", "Ventnor Avenue", 260, 22, 130, [110, 330, 800, 975, 1150], [150, 150], 'YELLOW'),
		Title("Property", "Marvin Gardens", 280, 24, 140, [120, 360, 850, 1025, 1200], [150, 150], 'YELLOW'),

        Title("Property", "Pacific Avenue", 300, 26, 150, [130, 390, 900, 1100, 1275], [200, 200], 'GREEN'),
		Title("Property", "North Carolina Avenue", 300, 26, 150, [130, 390, 900, 1100, 1275], [200, 200], 'GREEN'),
		Title("Property", "Pennsylvania Avenue", 320, 28, 160, [150, 450, 1000, 1200, 1400], [200, 200], 'GREEN'),

        Title("Property", "Park Place", 350, 35, 175, [175, 500, 1100, 1300, 1500], [200, 200], 'DARK_BLUE'),
		Title("Property", "Boardwalk", 400, 50, 200, [200, 600, 1400, 1700, 2000], [200, 200], 'DARK_BLUE')
	]

    def __init__(self): 
        self.properties = PROPERTY_CARDS

class Utility: 
    UTILITY = ["Electric Company", "Water Works"]

    UTILITY_CARDS = [
        #Utilies do not have buildings and the associated rental costs and do not have a color group
        Title("Utility", "Electric Company", 150, [4, 10], 75),
		Title("Property", "Water Works", 150, [4, 10], 75)
    ]

    def __init__(self): 
        self.utilities = UTILITY_CARDS

class Transports:
    TRANSPORTS = ["Reading Railroad", "Pennsylvania Railroad", "B. & O. Railroad", "Short Line"]

    TRANSPORTS_CARDS = [
        #Transports do not have buildings and a color group, but do have tiered rental amounts
        Title("Transports", "Reading Railroad", 200, [25, 50, 100, 200], 100),
        Title("Transports", "Pennsylvania Railroad", 200, [25, 50, 100, 200], 100), 
        Title("Transports", "B. & O. Railroad", 200, [25, 50, 100, 200], 100), 
        Title("Transports", "Short Line", 200, [25, 50, 100, 200], 100)
    ]

    def __init__(self): 
        self.transports = TRANSPORTS_CARDS
