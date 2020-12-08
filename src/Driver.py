import Game

import io
import base64
import time

from hashlib import pbkdf2_hmac
from os import urandom
from re import compile, search


class Driver: 
    salt = None

    #Empty constructor
    def __init__(self):
        self.salt = None
        
    #View win/loss statistics of players and others
    def viewStatistics(self):
        pass

    #See game moves of completed games
    def viewGameMoves(self): 
        pass

    #Starts a new game
    def createNewGame(self): 
        return Game()

    #Join existing game that needs players      
    def joinExistingGame(self, game): 
        pass

    # get a random salt values so it doesnt have to be same salt all the times
    def __generateSalt(self):
        self.salt = urandom(32)
        return 0

    # get the salt value, if none, generate
    def __getSaltValue(self):
        if self.salt is None:
            self.__generateSalt()
            return self.salt
        else:
            return self.salt

    def __generateSessionID(self):
        return urandom(32)

    # https://nitratine.net/blog/post/how-to-hash-passwords-in-python/
    def __getHash(self, password):
        # does this vuln to timing attack?
        return pbkdf2_hmac(
                        'sha256',   # use sha256 for this bullshit
                        password.encode('utf-8'),   # encode the password
                        self.__getSaltValue(), # this will get the salt value.
                        100000, # recommended 100,000 iter of sha256
                        dklen=128 # length of the hash
                            )
    def __calcHash(self, password, salt):
        # does this vuln to timing attack?
        return pbkdf2_hmac(
                        'sha256',   # use sha256 for this bullshit
                        password.encode('utf-8'),   # encode the password
                        salt, # this will get the salt value.
                        100000, # recommended 100,000 iter of sha256
                        dklen=128 # length of the hash
                            )


    def __checkPasswordStrength(self, user, password):
        ## check password req
        # length
        if (len(password) < 8 or len(password) > 32):
            print("[!] LOG: user %s with password - '%s' - doesn't meet password length req: actual - %i" 
                    % (str(user), str(password), str(len(password)  )))
            return False

        #complexity
        # a-z A-Z 0-9 special chars
        # @#!~;:<>,.-_$%^&+={}\[\]

        #print(password)
        lowercase = compile(r'[a-z]')
        uppercase = compile(r'[A-Z]')
        number = compile(r'[0-9]')
        special = compile(r'[^A-Za-z0-9]')

        if (lowercase.search(str(password)) is None):
            print("[!] LOG: user %s with password - '%s' - doesn't meet the password complexity: LOWERCASE" 
                    % (str(user), str(password) ))
            return False
        if (uppercase.search(str(password)) is None):
            print("[!] LOG: user %s with password - '%s' - doesn't meet the password complexity: UPPERCASE" 
                    % (str(user), str(password) ))
            return False
        if (number.search(str(password)) is None):
            print("[!] LOG: user %s with password - '%s' - doesn't meet the password complexity: NUMBER" 
                    % (str(user), str(password) ))
            return False
        if (special.search(str(password)) is None):
            print("[!] LOG: user %s with password - '%s' - doesn't meet the password complexity: SPECIAL" 
                    % (str(user), str(password) ))
            return False
        return True

    def __checkUser(self, user):
        with open('./plEAzeDAddyNOO.txt', 'r') as file:
            data = file.readlines()
            for user_data in data:
                # find user in list
                if (str(user) == str(user_data.split(':')[0])):
                    return True
        return False

    #Create new user
    def createUser(self, user, password):
        print("creating user")
        user = str(user).strip("\n")
        password = str(password).strip("\n")
        print(user)
        print(password)

        # check if user is already there
        #if not self.__checkUser(str(user)):
        #    print("[!] LOG: create user %s failed - user already registered: FAILED" 
        #            % (str(user) ))
        #    return False

        #store user and hash to a file 
        if not self.__checkPasswordStrength(str(user), str(password)):
            print("[!] LOG: user %s - password strength check (checkPasswordStrength): FAILED" 
                    % (str(user) ))
            return False

        hash = self.__getHash(str(password))
        a= self.__getSaltValue() + hash
        b = base64.b64encode(a).decode('utf-8')
        print(b)
        #store
        try:
            with open("./plEAzeDAddyNOO.txt", 'a') as file:
                    #print("aaa")
                    file.writelines(str(
                            user) + ':' 
                            + str(b)+"\n")
                # username:hash+password
            # just casually save that shit to a file.
        except Exception as e:
            print("[!] LOG: failed to saved new user hash to file: user - '%s' - hash '%s' - create user FAILED"
                % (str(user), str(hash) ))
            print(e)
            return False
        return True

    # assigned a session id
    def __StartSession(self, user):

        user = str(user).strip("\n")
        sessionID = self.__generateSessionID()
        try:
            with open("./Fuq_M3_uP_DazDy.txt", "a+") as file:

                file.writelines(str(user)
                                + ":"
                                + str(base64.b64encode(sessionID).decode('utf-8'))
                                + ":"
                                + str(time()))

            return ssessionID

        except Exception as e:
            print("[!] LOG: Failed to assigned Session ID for user %s"
                % (str(user)))
            #print(e)
        return 0

    def removeSessionID(self, user):
        user = str(user).strip("\n")
        
        try:
            with open("./Fuq_M3_uP_DazDy.txt", "wr") as file:
                lines = file.readlines()

                for line in lines:
                    if not str(user) in line:
                        file.write(line)

                return True
        except Exception as e:
            print("[!] LOG: failed to remove user %s current SESSION ID"
                    % (str(user)) )
            return False

    def checkSession(self, user, encodedSessionID):
        user = str(user).strip("\n") #Checks the session ID - ensure it is a float or byte
        encodedSessionID = str(encodedSessionID).strip("\n")

        try:
            with open("./Fuq_M3_uP_DazDy.txt", "r") as file:
                data = file.readlines()
            
                for user_data in data:
                    # find user in list
                    if (str(user) == str(user_data.split(':')[0])):
                        stored_ID = base64.b64decode(user_data.split(':')[1])
                        stored_time = user_data.split(':')[-1]

                        current_time = time.time()

                        # longer than a day? nah nah nahhhhhh
                        if (current_time - float(stored_time) > 86400.00):
                            # remove the current entry
                            self.removeSessionID(str(user))
                            return False

                        # check for the session id
                        if not (base64.b64decode(encodedSessionID) == stored_ID):
                            # remove the current entry
                            self.removeSessionID(str(user))
                            return False
            return True

        except Exception as e:
            print("[!] LOG: Failed to check SessionID for user %s - Session ID failed"
                    % (str(user)))
            print(e)

            return False


    #Authenticate existing user 
    def authUser(self, user, password):
        #get hash and find user
        '''
        get salt values
        salt_from_storage = storage[:32] # 32 is the length of the salt
        key_from_storage = storage[32:]
        '''

        user = str(user).strip("\n")
        password = str(password).strip("\n")

        try:
            with open('./plEAzeDAddyNOO.txt', 'r') as file:
                data = file.readlines()
            
                for user_data in data:
                    # find user in list
                    if (str(user) == str(user_data.split(':')[0])):
                        stored_hash = base64.b64decode(user_data.split(':')[-1])

                        # calculate hash and compare
                        # i need to convert to normal int from str, 
                        salt_from_storage = stored_hash[:32] # 32 is the length of the salt

                        # need to check compability
                        if (self.__calcHash(password, salt_from_storage) == stored_hash[32:]):
                            print("[!] LOG: User '%s' successful logged in"
                                % (str(user)))

                            # NEED SESSION ID
                            
                            return self.__StartSession(str(user))
                        else:
                            print("[!] LOG: User - '%s' authentication failed - user auth FAILED"
                                % (str(user)))
                            return False  #Should this be None? 
                print("[!] LOG: User '%s' doesn't exist." % (str(user)))

        # just casually save it to a file.
        except Exception as e:
            print("[!] LOG: Login failed: user - '%s' - auth user FAILED"
                % (str(user)))
            #print(e)
            return False

        return False
