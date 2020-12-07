#! /usr/bin/python3

import io

from hashlib import pbkdf2_hmac
from os import urandom
from re import compile, search
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

	def checkPasswordStrength(self, user, password):
        ## check password req
        # length
		if (len(password) < 8 or len(password) > 32):
			#print("[!] LOG: user %s with password - '%s' - doesn't meet password length req: actual - %i" 
            #        % (str(user), str(password), str(len(password)  )))
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
		if not self.checkPasswordStrength(str(user), str(password)):
			return("[!] LOG: user %s with password - '%s' - password strength check (checkPasswordStrength): FAILED" 
		            % (str(user), str(password) ))
			return False

		hash = self.__getHash(str(password))
		a= self.__getSaltValue() + hash
		b = base64.b64encode(a)

		#store
		#try:
		with open("./user.txt", 'a') as file:
				print("aaa")
				file.writelines('{"username":'+str(
		                user) + ':' 
		                + str(b)+":0:0\n")
		        # username:hash+password
		    # just casually save that shit to a file.
		'''
		except Exception as e:
			print("[!] LOG: failed to saved new user hash to file: user - '%s' - hash '%s' - create user FAILED"
			    % (str(user), str(hash) ))
			print(e)
			return False
		'''
		return True

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
						stored_hash = user_data.split(':')
						print(stored_hash)

						# calculate hash and compare
						# i need to convert to normal int from str, 
						salt_from_storage = stored_hash[:32] # 32 is the length of the salt

						# need to check compability
						if (calcHash(password, salt_from_storage) == stored_hash[32:-1]):
							print("[!] LOG: User '%s' successful logged in"
							    % (str(user)))
							return True
						else:
							print("[!] LOG: User - '%s' authentication failed - user auth FAILED"
							    % (str(user)))
							return False

		    # just casually save that shit to a file.
		except Exception as e:
			print("[!] LOG: failed to saved new user hash to file: user - '%s' - hash '%s' - create user FAILED"
			    % (str(user), str(hash) ))
			return False

		return

#def main():
#
#	a = Driver()
#
#	a.createUser('test_user','sajAdnbash1jdas!')
#
#
#	returnx

#if __name__ == '__main__':
#	main()