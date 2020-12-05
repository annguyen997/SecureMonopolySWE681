import socket 

import Driver

class Controller: 
    #GET
    with socket.socket()

    def __init__(): 
        driver = Driver() 


    #POST 
    #Game information would need to be displayed to web client.... 

    #Validate the input of the player
    def parseInput(self):
        pass

    #Asynchronous 
    #session Ids will be returned as base-64
    def checkSessionID(self):
        #Call Driver's check session ID 
        driver.checkSession(user,) 

        #It should return a new line with the returned byte/float value automatically 
        #Stripping new line may be needed 
        random.urandom(32)....


#???
def main(): 
    ServerSideSocket = socket.socket()
    host = ''
    port = 2004
    ThreadCount = 0 
    
    try: 
         ServerSideSocket.bind((host, port))
    except socket.error as e:
        print(str(e))

    print('Socket is listening..')
    ServerSideSocket.listen(5)

    def multi_threaded_client(connection):
        connection.send(str.encode('Server is working:'))
        while True:
            data = connection.recv(2048)
            response = 'Server message: ' + data.decode('utf-8')
            if not data:
                break
            connection.sendall(str.encode(response))
        connection.close()

    while True:
        Client, address = ServerSideSocket.accept()
        print('Connected to: ' + address[0] + ':' + str(address[1]))
        start_new_thread(multi_threaded_client, (Client, ))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount))
    ServerSideSocket.close()