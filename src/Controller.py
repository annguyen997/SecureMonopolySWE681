import socket 
import os 
from _thread import *
import uuid 
import base64

import Driver

class Controller: 
    #GET
    game_sessions = [] 
   
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
            
    """ CONTROLLER INSTANCES """ 
    #Controller instance (for each user)
    def __init__(self): 
        self.driver = Driver() 
        self.user = None
        self.sessionID = None
        self.game = None
        #Should there be a group of session IDs stored per Controller? 

    #POST 
    #Game information would need to be displayed to web client.... 

    def __incomingUser(self, username, password, mode):
        if (mode == "Authenticate"): 
            #session Ids will be returned as base-64
            generatedSessionID = self.driver.authUser(username, password)

            #It should return a new line with the returned byte/float value automatically 
            #Stripping new line may be needed 
            if (generatedSessionID == 0): 
                return 
            self.sessionID = generatedSessionID
            self.user = username 

        if (mode == "Create"): 
            userCreated = self.createUser(username, password)

            if userCreated: 
                #Once created user, authenticate to generate session ID
                #session Ids will be returned as base-64
                generatedSessionID = self.driver.authUser(username, password)
                
                #It should return a new line with the returned byte/float value automatically 
                #Stripping new line may be needed 
                if (generatedSessionID == 0): 
                    return 
                self.sessionID = generatedSessionID
                #self.id = str(generatedSessionID).strip("\n")
                self.user = username
            
    #Asynchronous call
    def checkSessionID(self, sessionID):
        #Call Driver's check session ID 
        #
        sessionExist = self.driver.checkSession(user, sessionID) 

        #If session does not exist, end player's connection
        if (not sessionExist): 
            print("Ending the session.")

            for game in game_sessions: 
                if self.sessionID in game["Player"]: 
                    game["Player"].remove(self.sessionID)

        #random.urandom(32)....

    #Create a game session - requires at least two players to play
    def createGame(self):
        #Generate game session ID
        gameID = uuid.uuid4()

        #Add session ID with player 
        players = [self.sessionID]
        Controller.game_sessions.append({"Session": gameID, "Player": players, "Active": False}) 

    #Join an existing game 
    def joinExistingGame(self, playerID, gameSessionID): 
        for game in game_sessions: 
            if str(gameSessionID) == str(game["Session"]): 
                game["Player"].append(self.sessionID)

    #Set the game variable to controller (of each client)
    def setGameInstance(self, game): 
        self.game = game
    
    #Validate the input of the player 
    #ResponseType corresponds to the context of the input in relation to the game
    def parseInput(self, inp):
        assert isinstance (inp, dict)
        #Regex parts here 

        # this will see what to call and interpret the api calls
        # i think it is best to devide up to 3 catergories
        # user stuff
        # management
        # and game

        # so I will interpret the data as so
        # dict {'user_': [data]} - user stuff
        # dict {'mana_': [data], 'sessionID_': data} - management stuff such as sessionID
        # dict {'game_': [data], 'sessionID_': data} - game data
        # 

        #user stuff
        # within [data] -> FIRST FIELD ALWAYS BE WHAT TO DO aka Authenticate/Create
        # [data] [1] = user, [data] [2] = password 
        if 'user_' in inp:
            # __incomingUser(self, username, password, mode):
            return self.__incomingUser(str(inp['user_'][1]),    # username offset in 'user_' value
                                        str(inp['user_'][2]),   # passwd offset in 'user_' value
                                        str(inp['user_'][0]))   # mode

        # management stuff
        if 'mana_' in inp:


        # game data stuff
        if 'game_' in inp: 


#???
def main(): 
    ServerSideSocket = socket.socket()
    host = ''
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
        connection.send(str.encode('Server is working:'))

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
                controllerClient.parseInput(data)


                response = 'Server message: ' + data.decode('utf-8')

                if not data:
                    break
                else: 
                    print("Received: ", response)
                    print("Sending: ", response) 
            
                controllerClient = Controller() 
                connection.sendall(str.encode(response))
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