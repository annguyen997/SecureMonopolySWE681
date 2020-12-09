#! /usr/bin/python3
from Controller import *
import time

import random
import threading
import io
import base64

# fuzz case. 1 fuzz case
def fuzz(case,  inp):

	# write out the input to temp files?
	# this let you see what is being produce
	# as the fuzzer going
	with open(f"/Users/tnorria/Desktop/SecureMonopolySWE681/src/corpus/tmp_inputs/tmp{case}", "w") as file:
		file.write(str(base64.b64encode(inp).decode('utf-8')))

	#username = f"fuzz-test{inp}"
	a = Controller()
	try : 
		a.parseInput(inp = inp)
	# watch for False return aka any thing fail within 
	
	except Exception as e:
		with open(f"./corpus/crashes/tmp{case}", "w") as crash_file:
			crash_file.write(str(base64.b64encode(inp).decode('utf-8')))
			crash_file.write("\n\n\n\n"+str(e)+"\n")
			print("EXCEPTION, oh fuckkkkk!!!!")


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

with open('./corpus/controller_input.txt', 'r') as data:
	corpus_all = data.readlines()

	for data in corpus_all:
		#print(data)
		corpus.add(data.encode('utf-8'))

# go back to list,
# since we are done with set cuz for dupping not unique input

corpus = list(map(bytearray, corpus))
#print(len(corpus))

start = time.time()

cases = 0

def worker(thred_id):
	global start, corpus, cases
	while True:
		inp = bytearray(random.choice(corpus))

		# godly mutating fuzzer
		for _ in range(random.randint(1,8)):
			inp[random.randint(0, len(inp) - 1)] = random.randint(0,255)

		fuzz(cases, inp)

		cases += 1

		current = time.time() - start



		fuzz_per_sec = float(cases) / current
		print(f"[{current:10.4f}] Fuzz case {cases} done | case per sec: {fuzz_per_sec:10.4f}")

# 4 threads fuzzing
for thr_id in range(2):
	threading.Thread(target=worker, args=[thr_id]).start()

while threading.active_count() > 0:
	time.sleep(0.1)




