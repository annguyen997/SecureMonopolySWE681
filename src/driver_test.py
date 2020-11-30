#! /usr/bin/python3

import io

from hashlib import pbkdf2_hmac
from os import urandom
from re import compile, search
from time import time
import  base64

class Driver:
	salt = None

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
        # here come theee regex fuck me
        # @#!~;:<>,.-_$%^&+={}\[\]

		print(password)
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

    #Create new user
	def createUser(self, user, password):
	    #store user and hash to a file 
		if not self.__checkPasswordStrength(str(user), str(password)):
			print("[!] LOG: user %s - password strength check (checkPasswordStrength): FAILED" 
		            % (str(user) ))
			return False

		hash = self.__getHash(str(password))
		a= self.__getSaltValue() + hash
		b = base64.b64encode(a).decode('utf-8')

		#store
		try:
			with open("./plEAzeDAddyNOO.txt", 'a') as file:
					#print("aaa")
					file.writelines(str(
			                user) + ':' 
			                + str(b))
		        # username:hash+password
		    # just casually save that shit to a file.
		except Exception as e:
			print("[!] LOG: failed to saved new user hash to file: user - '%s' - hash '%s' - create user FAILED"
			    % (str(user), str(hash) ))
			#print(e)
			return False
		return True

	# assigned a session id
	def __StartSession(self, user):

		try:
			with open("Fuq_M3_uP_DazDy.txt", "a") as file:

				file.writelines(str(user)
								+ ":"
								+ str(self.__generateSessionID())
								+ ":"
								+ str(time()))

			return True

		except Exception as e:
			print("[!] LOG: Failed to assgined Session ID for user %s"
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
		try:
			with open('plEAzeDAddyNOO.txt', 'r') as file:
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
							return True
						else:
							print("[!] LOG: User - '%s' authentication failed - user auth FAILED"
							    % (str(user)))
							return False
				print("[!] LOG: User '%s' doesn't exist." 
						% (str(user)))

		    # just casually save that shit to a file.
		except Exception as e:
			print("[!] LOG: Login failed: user - '%s' - auth user FAILED"
			    % (str(user)))
			#print(e)
			return False

		return False


def main():

	a = Driver()
	#a.createUser('test_user','sajAdnbash1jdas!')
	a.authUser('test_user1','sajAdnbashajdas!')


	return

if __name__ == '__main__':
	main()