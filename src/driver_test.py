#! /usr/bin/python3
from Driver import createUser, authUser

from time import time


'''
	fuzzing stuff
'''

#def randomshit():

#	for x in range(0,32):
def main():

	a = Driver()
	a.createUser('test_user','sajAdnbash1jdas!')
	a.authUser('test_user','sajAdnbash1jdas!')


	return

if __name__ == '__main__':
	main()