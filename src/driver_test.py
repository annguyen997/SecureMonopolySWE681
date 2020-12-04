#! /usr/bin/python	
from Driver import *

import afl
import sys

'''
	fuzzing stuff
'''

def main():

	afl.init()

	a = Driver()

	try:
		a.createUser('test_user',sys.stdin.read())
		a.authUser('test_user','sajAdnbash1jdas!')

	except Exception as e:
		print("[!!!] FUZZING: EXCEPTION CAUGHT: %s" % (str()))
	return

if __name__ == '__main__':
	main()