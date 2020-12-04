#! /usr/bin/python3
from Driver import *


import random
import io

'''
	fuzzing stuff
'''

# We gonna fuzz stuff
# first we need a corpus
# this will just be valid input into our functions
# AKA just strings of password and user name.
# I will grab it just from the web
# https://github.com/danielmiessler/SecLists/blob/master/Passwords/Common-Credentials/10-million-password-list-top-100000.txt

corpus = set()

with open('./corpus/top_100000_pass.txt', 'r') as data:
	corpus_all = data.readlines()

	for data in corpus_all:
		#print(data)
		corpus.add(data)

# go back to list,
# since we are done with set cuz for dupping not unique input

corpus = list(corpus)

print(len(corpus))