# -*- coding: utf-8 -*-
"""
RokuVoiceControl.py: Simple interface to control 
	a Roku streaming player over telnet using
	either voice or text entry

@author: rwalker (r_walker at zoho.com)
"""
import speech_recognition as sr
from telnetlib import Telnet
from argparse import ArgumentParser
import sys

# NOTE: TimeoutError type is used by speech_recognition but appears to be
# only a predefined Exception in Python3.  So we add it to the module here.
class TimeoutError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
sr.TimeoutError = TimeoutError

class Concept:
	''' A concept class to associate keywords to actions'''
	def __init__(self, words, action):
			self.keywords  = words
			self.action = action

	def conceptMatch(self, tokens):
		''' Simple concept matching'''
		for word in tokens:
			if word.lower() in self.keywords:
				return(self.action)

# Concept data for RokuRemote
PlayConcept = Concept(['play'], 'press p')
SelectConcept = Concept(['select','ok'], 'press s')
LeftConcept = Concept(['minus','left', 'decrement'], 'press l')
RightConcept = Concept(['right','plus','increment'], 'press r')
UpConcept = Concept(['up'], 'press u')
DownConcept = Concept(['down'], 'press d')
FastForwardConcept = Concept(['advance','fast','forward'], 'press f')
RewindConcept = Concept(['rewind','reverse'], 'press b')
HomeConcept = Concept(['home','done'], 'press h')
BackConcept = Concept(['back'], 'press b')
PauseConcept = Concept(['pause','paws','hold','wait','stop'],'press p')
ConceptList = [PlayConcept, SelectConcept, LeftConcept, RightConcept, 
	UpConcept, DownConcept, FastForwardConcept, RewindConcept,
	HomeConcept, BackConcept, PauseConcept]

class RokuRemote:
	''' RokuRemote class telnets into Roku on host at port.'''
	def __init__(self, host, port, conceptList):
		self.connection = Telnet(host, port)
		self.concepts  = ConceptList
	
	def processRequest(self, req):
		'''send a text string to the Roku instance'''
		tokens = req.split(" ")
		for concept in self.concepts:
			action = concept.conceptMatch(tokens)
			if action is not None:
				print("Here's what I heard: '" + action + "'")
				self.connection.write(action +'\n')
				return
			
		# if we didn't find a match...
		print("I didn't get that.  Please try again.")

if __name__=="__main__":
	argparser = ArgumentParser(usage="RokuVoiceControl.py host port")
	argparser.add_argument("host")
	argparser.add_argument("port")
	args = argparser.parse_args()
	welcomeString = '''
##############################################################
Welcome to the voice driven Roku remote!
To use this remote, you need to enable dev mode on your Roku.  
To do this, press the following buttons on your roku remote: 
Home (3 times), Up (twice), Right, Left, Right, Left, Right.

##############################################################
Type a command or enter 'v' to engage voice control.  Type or
say 'quit' to exit remote.
'''
	# initialize
	print(welcomeString)
	rokuRemote = RokuRemote(args.host, args.port, ConceptList)
	recognizer = sr.Recognizer()
	recognizer.energy_threshold = 2000
	recognizer.pause_threshold = .5
	command = ''

	# run the remote interface
	while(command!='quit'):
		command = raw_input("Roku>> ")
		rec_success = True
		if command == 'v':
			with sr.Microphone() as source:
				try:          
					audio = recognizer.listen(source, timeout=2)
					try:
						print("Recognizing...")
						command = recognizer.recognize(audio)
						rec_sucess = False
						print("Recieved voice command: " + command)
					except LookupError:                       
						print("Could not process voice command.")
				except sr.TimeoutError:
					print("Didn't detect any speech.")
		if command == 'quit':
			break
		if rec_success == True:
			rokuRemote.processRequest(command)
