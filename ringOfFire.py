import sys
import os
import random
from msvcrt import getch
# # # To-do:
# # # - Write fetchRule(key)
# # # - Write writeRule(key, newRule)
__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
faces = ["Ace","2","3","4","5","6","7","8","9","10","Jack","Queen","King"]
suits = ["Spades", "Hearts", "Clubs", "Diamonds"]
cards = {}

def generateDeck():
	count = 1
	for face in faces:
		for suit in suits:
			cards[count] = face + " of " + suit
			count += 1
	return cards

def playGame():
	kingCount = 0
	cards = generateDeck()
	print "Deck shuffled\n"
	deckRemaining = cards
	while len(deckRemaining) != 0:
		print "Press ENTER to draw next card, or ESC to exit game"
		key = ord(getch())
		if key == 13: #Enter
			nextCard = drawCard(deckRemaining)
			rule = getRule(nextCard)
			print "\n---------------------------------------------"
			print nextCard + " : " + rule
			# Check if final king
			if (nextCard.startswith("King")&(kingCount <3)):
				kingCount += 1
				print "Top up the pint!"
			elif (nextCard.startswith("King")&(kingCount == 3)):
				print "Final king - finish the cup!"
			print "---------------------------------------------\n"
		elif key == 27: #ESC
			print "Are you sure? Press ENTER to exit, or ESC to cancel"
			while True:
				key = ord(getch())
				if key == 13: #Enter
					sys.exit()
				elif key == 27: #ESC
					break
	print "======================================================"
	print "Congratulations - you completed the game"
	print "Play a new game? Press ENTER to restart, or ESC to return to main menu"
	key = ord(getch())
	if key == 13: #Enter
		playGame()
	elif key == 27: #ESC
		print "======================================================"
		menuSelection()

def readDictionary():
	with open(os.path.join(__location__, 'RofRules.txt'), 'rb') as f:
		rules = {}
		for line in f.read().splitlines():
			face = line.partition(" : ")[0]
			rule = line.partition(" : ")[2]
			rules[face] = rule
	return rules

def writeDictionary(rules):
	with open(os.path.join(__location__, 'RofRules.txt'), 'wb') as f:
		try:
			for key in rules:
				f.write(key + " : " + rules[key] + "\n")
			print "Successfully wrote rules\n--------------------"
		except:
			print "Writing rules failed\n--------------------"

def drawCard(deckRemaining):
	deckRemainingKeys = deckRemaining.keys()
	randomDeckKey = deckRemainingKeys[random.randrange(0,len(deckRemainingKeys),1)]
	pickedCard = deckRemaining.pop(randomDeckKey)
	return pickedCard

def getRule(cardToCheck):
	rules = readDictionary()
	face = cardToCheck.split(" of ",1)[0]
	ruleForCard = rules[face] #Cuts down to just face
	return ruleForCard

def setRule(cardToWrite, ruleToWrite):
	try:
		rules = readDictionary()
		face = cardToWrite.split(" of ",1)
		rules.__setitem__(face[0],ruleToWrite)
		writeDictionary(rules)
		print "--------------\nSuccessfully wrote rule\n--------------"
	except:
		print "--------------\nFailed to write rule\n--------------"

def editRule():
	while True:
		with open(os.path.join(__location__, 'RofRules.txt')) as openRules:
			print "\n--------------\nCurrent rules:\n--------------\n" + openRules.read() + "\n--------------\n"
		cardToWrite = raw_input("--------------\nPlease choose a card to edit, or press X to exit:\n").lower().capitalize()
		while True:
			if cardToWrite == "King":
				print "I'm afraid you can't change that rule"
				break
			elif cardToWrite in faces:
				newRule = raw_input("--------------\nPlease enter the rule:\n")
				setRule(cardToWrite, newRule)
				break
			else:
				print "I'm sorry, that wasn't a valid entry\n"
				break
		continue
def menuSelection():
	# # Need to change to key(getch) instead
	while True:
		print "Please select an option:\nPlay (p)\nHow to Play (h)\nView Rules (v)\nEdit rules (e)\nExit (x)\n"

		response = raw_input("Please select an option:\nPlay (p)\nHow to Play (h)\nView Rules (v)\nEdit rules (e)\nExit (x)\n").lower()
		if ((response == "p") | (response == "play")):
			print "Play!\n"
			playGame()
		elif ((response == "h") | (response == "how")):
			print "\n-------------------------\nThis is a drinking game where each player in turn draws a card, associated with a particular drinking challenge. The player (or a different player, if the rule necessitates) must then complete the challenge. This should continue around the players until all cards have been drawn, or until sufficiently mashed.\n-------------------------\n"
			continue
		elif ((response == "v") | (response == "view")):
			__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
			openRules = open(os.path.join(__location__, 'RofRules.txt'));
			print "\n--------------\nCurrent rules:\n--------------\n" + openRules.read() + "\n--------------"
			openRules.close()
			continue
		elif ((response == "e") | (response == "edit")):
			print "\n------------------\nEdit screen\n------------------\n"
			editRule()
		elif ((response == "x") | (response == "exit")):
			print "Thank you for playing!"
			sys.exit()
		else:
			print "I'm sorry, that wasn't a valid entry"
			continue
print "\n=======================\nWelcome to Ring of Fire!\n=======================\n"

# Check for valid rule file, and create one if not present
if not "RofRules.txt" in os.listdir(__location__):
	defaultRules = {"Ace":"Waterfall","2":"You","3":"Me","4":"Girls","5":"Jive","6":"Guys","7":"Heaven","8":"Mate","9":"Rhyme","10":"Thumbmaster","Jack":"Make a rule","Queen":"Question Master","King":"Kings cup"}
	print "Folder doesn't contain rule file\nWriting new file..."
	# Replace with OrderedDict in future
	writeDictionary(defaultRules)
menuSelection()