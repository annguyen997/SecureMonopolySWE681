import Game

import io

from hashlib import pbkdf2_hmac
from os import urandom
from re import compile, search
from io import open, readlines, writelines

class Driver: 
    salt = None

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
    def generateSalt(self):
        self.salt = urandom(32)
        pass

    # get the salt value, if none, generate
    def getSaltValue(self):
        if self.salt is None:
            self.generateSalt()
            return self.salt
        else:
            return self.salt


    # https://nitratine.net/blog/post/how-to-hash-passwords-in-python/
    def getHash(self, password):
        # does this vuln to timing attack?
        return pbkdf2_hmac(
                        'sha256',   # use sha256 for this bullshit
                        password.encode('utf-8'),   # encode the password
                        getSaltValue(), # this will get the salt value.
                        100000, # recommended 100,000 iter of sha256
                        dklen=128 # length of the hash
                            )

    def checkPasswordStrength(self, password):
        ## check password req
        # length
        if (len(password) < 8 or len(password) > 32):
            print("[!] LOG: user %s with password - '%s' - doesn't meet length req with length %i" 
                    % (str(user), str(password), str(len(password)  )))
            return False
        #complexity
        # a-z A-Z 0-9 special chars
        # here come theee regex fuck me
        # @#!~;:<>,.-_$%^&+={}\[\]

        lowercase = compile(r'[a-z]')
        uppercase = compile(r'[A-Z]')
        number = compile(r'[0-9]')
        special = compile(r'[@#!~;:<>,.-_$%|^&+={}\[\]\']')

        if (lowercase.search(password.encode(utf-8) is None)):
            print("[!] LOG: user %s with password - '%s' - doesn't meet the password complexity: LOWERCASE" 
                    % (str(user), str(password) ))
            return False
        if (uppercase.search(password.encode(utf-8) is None)):
            print("[!] LOG: user %s with password - '%s' - doesn't meet the password complexity: UPPERCASE" 
                    % (str(user), str(password) ))
            return False
        if (number.search(password.encode(utf-8) is None)):
            print("[!] LOG: user %s with password - '%s' - doesn't meet the password complexity: NUMBER" 
                    % (str(user), str(password) ))
            return False
        if (special.search(password.encode(utf-8) is None)):
            print("[!] LOG: user %s with password - '%s' - doesn't meet the password complexity: SPECIAL" 
                    % (str(user), str(password) ))
            return False
        return True

    #Create new user
    def createUser(self, user, password):
        #store user and hash to a file 
        if not checkPasswordStrength(str(password)):
            print("[!] LOG: user %s with password - '%s' - password strength check (checkPasswordStrength): FAILED" 
                    % (str(user), str(password) ))
            return -1

        hash = getHash(str(password))

        # store hash
        storage = user + ':' + salt + hash 

        #store
        try:


        except Exception as e:
            print("[!] LOG: failed to saved new user hash to file: user - '%s' - hash '%s' - create user FAILED"
                % (str(user), str(hash) ))
            return -1

        return

    #Authenticate existing user 
    def authUser(self, user, password):
        #get hash and find user
        '''
        get salt values
        salt_from_storage = storage[:32] # 32 is the length of the salt
        key_from_storage = storage[32:]
        '''
        return

    #Determine timer