import socket 
import os 
from _thread import *
import uuid 
import base64
import json

from Game import * 
from Driver import Driver

class Controller:
    game_sessions = [] 

    #Controller instance (for each user)
    def __init__(self): 
        self.driver = Driver() 
        self.user = None
        self.gameSession = None 
        self.game = None
        #Should there be a group of session IDs stored per Controller? 

    #Check if the number of players in that game session enough to play
    @classmethod
    def sufficientNumberPlayers(cls, gameID): 
        print("Get to sufficient number player")
        gamePlayers = None 
        print("Get to sufficient number player2")
        for gameSession in cls.game_sessions: 
            if (str(gameID) == str(gameSession["Session"]) and len(gameSession["Player"]) >= 2):
                print(len(gameSession["Player"]))
                return True
        
        return False
    
    #Print the current game session IDs and number of players
    @classmethod
    def printCurrentGameSessionIDs(cls): 
        #Print each game session avaiable in the system
        gameInfo=""
        print("entering printCurrentGameSessionIDs FOR loop")
        print(cls.game_sessions)
        for gameSession in cls.game_sessions: 
            gameInfo += "Session ID: " + gameSession["Session"] + "\t# of Players: " + str(len(gameSession["Player"]))+"\n"
            print(gameSession["Active"])
            if (gameSession["Active"]):
                print("Active Yes!")
                gameInfo += " Game Active: Yes\n"
            else:
                print("Active No!") 
                gameInfo += " Game Active: No\n"
            
            print(gameInfo)
        
        return(gameInfo+"\nGame Active indicates if there is a game available for this session. A game session with sufficient number of players may not have a game active.\n")
    
    #Get the set of usernames from the game session IDs list
    @classmethod
    def getUsernamesOfGameSessionID(cls, gameID): 
        for gameSession in cls.game_sessions: 
            if (str(gameID) == str(gameSession["Session"])):
                return gameSession["Usernames"]

    #Return the number of players of that game session 
    @classmethod
    def numberOfPlayers(cls, gameID): 
        for gameSession in cls.game_sessions: 
            if (str(gameID) == str(gameSession["Session"])):
                return len(gameSession["Player"])

    #Add session ID to an existing game session
    @classmethod
    def joinExistingSession(cls, playerID, gameID, username):
        for game in cls.game_sessions: 
            if str(gameID) == str(game["Session"]): 
                print("please help")

                #Check if the player's ID is not in the list for this session.
                #If player's ID is already in list, user just needs to join the game
                if (playerID in game["Player"]):
                    return #Player already in list, exit to previous caller
                elif (len(game["Player"]) <= 8): #If player in game is less than 8 players available 
                    game["Player"].append(playerID)
                    game["Usernames"].append(username)
                
    #Check if the game is active 
    @classmethod
    def checkGameActive(cls, gameID): 
        for gameSession in cls.game_sessions: 
            if (str(gameID) == str(gameSession["Session"]) and gameSession["Active"]):
                return True
        
        return False

    #Create a new game once there is sufficient number of players - asynchronous 
    @classmethod
    def createNewGame(cls, gameID): 
        for gameSession in cls.game_sessions: 
            if (str(gameID) == str(gameSession["Session"]) and Controller.numberOfPlayers(gameID) >= 2):
                gameSession["Active"] = True #This means enough players are available to start playing new game
                gameSession["Game Instance"] = Game()

    #Get the game instance to controller
    @classmethod
    def getGameInstance(cls, gameID): 
        for gameSession in cls.game_sessions: 
            if (str(gameID) == str(gameSession["Session"])):
                if (gameSession["Game Instance"] != None): 
                    return gameSession["Game Instance"]
                else: 
                    print("Game instance not available.")
                    return None
        
    #Game information would need to be displayed to web client.... 
    def __incomingUser(self, username, password, mode):
        print("Incoming...")
        
        if (mode == "Authenticate"): 
            #session Ids will be returned as base-64
            generatedSessionID = self.driver.authUser(username, password)

            #It should return a new line with the returned byte/float value automatically 
            #Stripping new line may be needed 
            if (generatedSessionID == 0): 
                return 
            self.user = username 
            return generatedSessionID

        if (mode == "Create"): 
            userCreated = self.driver.createUser(username, password)

            if userCreated: 
                #Once created user, authenticate to generate session ID
                #session Ids will be returned as base-64
                generatedSessionID = self.driver.authUser(username, password)
                #It should return a new line with the returned byte/float value automatically 
                #Stripping new line may be needed 
                if (generatedSessionID == 0): 
                    return 
                #self.id = str(generatedSessionID).strip("\n")
                self.user = username
                return generatedSessionID
            
    #Asynchronous call
    def __checkSessionID(self, user, sessionID):
        #Call Driver's check session ID 
        sessionExist = self.driver.checkSession(user, sessionID) 

        #If session does not exist, end player's connection
        if (not sessionExist): 
            print("Ending the session.")

            for game in game_sessions: 
                if self.sessionID in game["Player"]: 
                    game["Player"].remove(self.sessionID)
        return sessionExist
        #random.urandom(32)....

    #Create a game session - requires at least two players to play
    def __createGameSession(self, sessionID):
        #Generate game session ID
        gameID = str(uuid.uuid4())

        #Add session ID with player 
        players = [sessionID]
        Controller.game_sessions.append({"Session": gameID, "Player": players, "Usernames": [self.user],  "Active": False, "Game Instance": None})
        
        self.gameSession = gameID  #Is this needed? 
        print(gameID)

        return gameID

    #Join an existing game 
    def __joinExistingGame(self, playerID, gameID): 
        print("You got here congrats.1@#!@#!@")
        Controller.joinExistingSession(playerID, gameID, self.user)
        self.gameSession = gameID
        print("Joining Existing Game")

        if (Controller.checkGameActive()): 
            self.setGameInstance(Controller.getGameInstance(self.gameSession))

    #Check if game can be created
    def __startGame(self, gameID): 
        print("entering __startGame")
        #print(Controller.sufficientNumberPlayers(gameID))

        #Check if there is a game instance already, and if not create one. 
        if (Controller.getGameInstance(self.gameSession) == None): 
            run = Controller.sufficientNumberPlayers(gameID)
            print("asdasdqw")
            if (run):
                Controller.createNewGame(gameID) 
                print("after __startGame")
        #else: 
            #If there is a game instance already, simply join the game

        self.__setGameInstance(Controller.getGameInstance(self.gameSession))
        self.game.addPlayer(self.user, "Player #" + str(self.game.getNumberOfPlayers() + 1))

        #Run the game automatically once the sufficient number of players join 
        if (self.game.getNumberOfPlayers() == Controller.numberOfPlayers(self.gameSession)): 
            self.game.run() 

        #self.game.addPlayers(Controller.getUsernamesOfGameSessionID(self.gameSession))
    
    #Get all game instances available for viewing
    def __getGameInstancesAvailable(self): 
        Controller.printCurrentGameSessionIDs() 

    #Set the game variable to controller (of each client)
    def __setGameInstance(self, game): 
        self.game = game
    
    #Display the current game information to the web browser (i.e. client) of players and any messages of game's current state.  
    def __getCurrentGameState(self): 
        currentGameInfo = None 

        #Get the game messages 
        currentGameInfo += self.game.getGameMessages() + "\n"

        #Display order of players
        currentGameInfo += "Current Players: "
        currentPlayerList = self.game.getPlayersList()
        for player in currentPlayerList: 
            currentGameInfo += player.getName() + "\t"

        #Display the current stats of all players
        currentGameInfo += self.game.displayPlayersStats() 

        return currentGameInfo

    #Get the current function call state of the game for validating user input (for correct syntax in context of the game's current state) 
    def __getCurrentFunctionCall(self): 
        return self.game.getFunctionCallName() 

    #Store the user input to the game (after validating) and process the input accordingly
    def __storeInputToGame(self, input): 
        self.game.storeUserInput(input) 
        
        #Process the user's input in relation to the game's current state to produce results 
        self.game.routeInput() 
        
    #Player wishes to forfeit the game
    def __forfeitGame(self):
        #validate if the game and session is valid
        # 

        self.forfeitGame(self.user) 
        

    #Validate the input of the player 
    #ResponseType corresponds to the context of the input in relation to the game
    def parseInput(self, inp):
        #assert isinstance (inp, dict)
        #Regex parts here 

        # this will see what to call and interpret the api calls
        # i think it is best to devide up to 3 catergories
        # user stuff
        # management
        # and game

        # so I will interpret the data as so
        # dict {'user_': [data]} - user stuff
        # dict {'mana_': [data], 'username_': username, 'sessionID_': data} - management stuff such as sessionID
        # dict {'game_': [data], 'username_': username, 'sessionID_': data} - game data
        # 
    
        #user stuff
        # within [data] -> FIRST FIELD ALWAYS BE WHAT TO DO aka Authenticate/Create
        # [data] [1] = user, [data] [2] = password 
        if 'user_' in inp:
            inp=json.loads(inp)
            # __incomingUser(self, username, password, mode):
            return self.__incomingUser(str(inp['user_'][1]),    # username offset in 'user_' valueprint("We in parse Input")
                                        str(inp['user_'][2]),   # passwd offset in 'user_' value
                                        str(inp['user_'][0]))   # mode

        # management stuff
        if 'mana_' in inp:
            inp=json.loads(inp)
        # check session id if before anything
        # __checkSessionID(self, user, sessionID)
            if not (self.__checkSessionID(  str(inp['username_']),
                                            str(inp['sessionID_'])
                                            )):
                print("[!] LOG: Session for user %s has expired"
                        % (str(inp['username_'])) )
                return False

            ###############
            #   joinExistingGame
            ###############
            if (str(inp['mana_'][0]) == 'joinExistingGame'):
                # __joinExistingGame(self, playerID, gameID): 
                return self.__joinExistingGame(str(inp['username_']),   # playerID or username
                                        inp['mana_'][1])        # game session id

            ###############
            #   View Win Loss
            ###############

            if (str(inp['mana_'][0]) == 'viewWinLoss'):
                f = open("win_loss.txt", "r")
                stats=f.read()
                f.close()
                return str(stats)

            if (str(inp['mana_'][0]) == 'audit'):
                f = open("audit.txt", "r")
                audit=f.read()
                f.close()
                return str(audit)


            ###############
            #   createGame
            ###############
            if (str(inp['mana_'][0]) == 'createGame'):
                # __createGame(self, sessionID): 
                print("creating game")
                return self.__createGameSession(inp['sessionID_'])        # player session id
            if (str(inp['mana_'][0]) == 'startGame'):
                # __createGame(self, sessionID): 
                print("starting game")
                return self.__startGame(inp['mana_'][1])   
                
        # game data stuff
        if 'game_' in inp:
            inp=json.loads(inp)
            print("Got to game_")
            if not (self.__checkSessionID( str(inp['username_']),
                                           str(inp['sessionID_'])
                                           )):
                print("[!] LOG: Session for user %s has expired"
                        % (str(inp['username_'])) )
                return False
            if (str(inp['game_'][0]) == 'listExistingGame'):
                print("Got to list")
                return Controller.printCurrentGameSessionIDs()        # game session id

            #If player is in the session and in the game itself, then call the game 
            #if 
                
        

        
        #Use the current instance of game to send user input to the game instance
        #A remote-controller function would be added to route the input to the appropriate location in the game. 

#???
def main(): 
    ServerSideSocket = socket.socket()
    host = '127.0.0.1'
    port = 2004
    ThreadCount = 0 

    controllerClient = None
    
    print("Waiting for the connection response.")
    try: 
         ServerSideSocket.bind((host, port))
    except socket.error as e:
        print(str(e))

    print('Socket is listening for a connection')
    ServerSideSocket.listen(5)

    def multi_threaded_client(connection):
        #connection.send(str.encode('Server is working:'))

        controllerClient = Controller()
        while True:
            try: 
                data = connection.recv(2048)

                # REGEX PARTS HERE

                # handle data 
                # can you parse input and stuff and save it as a data structure or something
                # HOA

                '''
                if data is not valid:
                    connection.send("data contains invalid input")
                '''
                print(data.decode('utf-8'))
                response=controllerClient.parseInput(data.decode('utf-8'))



                print("response..2")
                print(response)


                if not data:
                    print("Did i break?")
                    break
                else: 
                    print("Received: ", data)
                    print("Sending: ", response) 
            
                print(connection.sendall(response))
            except: 
                break
        
        connection.close()

    while True:
        Client, address = ServerSideSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(multi_threaded_client, (Client, ))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    ServerSideSocket.close()


if __name__ == "__main__":
    main() 
