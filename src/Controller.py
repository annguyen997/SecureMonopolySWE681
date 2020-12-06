import socket 
import os 
from _thread import * 
import base64

import Driver

class Controller: 
    #GET
    game_sessions = [] 

    #Controller instance (for each user)
    def __init__(): 
        self.driver = Driver() 
        #Should there be a group of session IDs stored per Controller? 

    #POST 
    #Game information would need to be displayed to web client.... 

    def incomingUser(self, username, password, mode):
        if (mode == "Authenticate"): 
            #session Ids will be returned as base-64
            generatedSessionID = self.driver.authUser(username, password)
            #It should return a new line with the returned byte/float value automatically 
            #Stripping new line may be needed 
            self.sessionID = str(generatedSessionID).strip("\n")
        if (mode == "Create"): 
            userCreated = self.createUser(username, password)

            if userCreated: 
                #Once created user, authenticate to generate session ID
                #session Ids will be returned as base-64
                generatedSessionID = self.driver.authUser(username, password)
                #It should return a new line with the returned byte/float value automatically 
                #Stripping new line may be needed 
                self.sessionID = str(generatedSessionID).strip("\n")
            

    #Asynchronous call
    def checkSessionID(self, sessionID):
        #Call Driver's check session ID 
        #
        sessionExist = self.driver.checkSession(user, sessionID) 

        #If session does not exist, end player's connection
        if (not sessionExist): 
            print("Ending the session.")


        #random.urandom(32)....
    

    #Create a game session - requires at least two players to play
    def __createGame(self):
        #Generate session ID
        
         
    
    #Join an existing game 
    def __joinExistingGame(self, gameSessionID): 
        pass

    #Validate the input of the player 
    #ResponseType corresponds to the context of the input in relation to the game
    def parseInput(self, input, responseType):
        #Regex parts here 

        # this will see what to call and interpret the api calls


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

                # handle data 
                # can you parse input and stuff and save it as a data structure or something
                # HOA
                controllerClient.parseInput(data)

                response = 'Server message: ' + data.decode('utf-8')

                if not data:
                    break
                else: 
                    print("Received: ", response)
                    print("Sending: ", response) 
            
             
            
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


if __name__ = "__main__":
    main() 