class GameInstances: 
    game_sessions = [] 

    #Check if the number of players in that game session enough to play
    @staticmethod
    def sufficientNumberPlayers(self, gameSessionID): 
        gamePlayers = None 
        
        for gameSession in game_sessions: 
            if (str(gameSessionID) == str(gameSession["Session"]) and len(gameSession["Player"]) >= 2):
                return True
        
        return False
    
    #Return the number of players of that game session 
    @staticmethod
    def numberOfPlayers(self, gameSessionID): 
        for gameSession in game_sessions: 
            if (str(gameSessionID) == str(gameSession["Session"])):
                return len(gameSession["Player"])

    #Add session ID to an existing game session
    @staticmethod
    def joinExistingSession(self, playerID, gameSessionID):
        for game in game_sessions: 
            if str(gameSessionID) == str(game["Session"]): 
                game["Player"].append(self.playerID)
        
    #Create a new game - asynchronous 
    @staticmethod
    def createNewGame(self, gameSessionID): 
        gamePlayers = None 
        
        for gameSession in game_sessions: 
            if (str(gameSessionID) == str(gameSession["Session"]) and len(gameSession["Player"]) >= 2):
                gamePlayers = gameSession["Player"]
                gameSession["Active"] = True #This means enough players are available to start playing new game

        if (gamePlayers): 
            return driver.createNewGame() 

    