import subprocess
import time
import os

class Helper: #class responsible for minor helper functions
	def __init__(self, parent):
		self.parent = parent

	def findTestResult(self, text): #given a result indicator in langParams file, extracts only that line from result text
		lines = text.splitlines()
		for line in lines:
			if len(line) > 0:
				words = line.split()
				if words[0] == self.parent.testResultIndicator:
					return line

	def isBiggestApplicableSynonym(self, synonym, word): #given a word containing a synonym and a synonym, looks at all synonyms and returns if given is the biggest one applicable in this word
		itIs = True
		for term2 in self.parent.keywords:
			for synonym2 in term2[0]:
				if (synonym in synonym2) and (synonym2 in word) and (synonym != synonym2):
					itIs = False
		return itIs

	def surroundingsInWord(self, term, word): #given a term and a word, returns what comes before and after the term in the word, in a list with two elements
		heads = ""
		for i in range(len(word)):
			if word[i] != term[0]:
				heads += word[i]
			else:
				if word[i:(i + len(term))] == term:
					return [heads, word[(i + len(term)):] ]	
				else:
					heads += word[i]

	def endOfScope(self, startLine, starWord, lines, character): #returns line and word where scope ends ("character" is a list of two elements with scope oppener in [0] and scope closer in [1])
		currentLine = 0

		scopeCount = [0, False]

		for line in lines:
			words = line.split()
			currentWord = 0	
			for word in words:
				howManyTimesEndOfScopeAppeared = 0
				currentLetter = 0
				if (currentLine >= startLine) and (currentWord >= starWord):
					if (character[0] in word) or (character[1] in word):
						for letter in word:
							if letter == character[0]:
								if not scopeCount[1]:
									scopeCount = [1, True]
								else:
									scopeCount[0] += 1
							if letter == character[1]:

								howManyTimesEndOfScopeAppeared += 1
								scopeCount[0] -= 1

								if (scopeCount[1]):
									if scopeCount[0] == 0:
										return [currentLine, currentWord, self.cutWordBeforeCharacter(word, character[1], howManyTimesEndOfScopeAppeared)]
				currentWord += 1
			currentLine += 1

	def cutWordBeforeCharacter(self, word, character, howManyTimesToCountCharacter): #returns what comes after a character in a string
		output = ""
		howManyTimesCharacterAppeared = 0
		for letter in word:
			if(howManyTimesCharacterAppeared < howManyTimesToCountCharacter):
				if (letter == character):
					howManyTimesCharacterAppeared += 1
			else:
				output += letter
		return output

	def replaceInSourceProgram(self, startLineNumber, endLineNumber, startWordNumber, endWordNumber, lines, word): #given a program separated in a list of lines (strings), a string and where the string whould br incerted (number of starting and ending lines and words), inserts the string in the text
		output = []
		inserted = False
		for i in range(len(lines)):
			if (i < startLineNumber or i > endLineNumber):
				output.append(lines[i])
			elif not inserted:
				words = lines[i].split()
				newLine = ""
				for j in range(len(words)):
					if j != 0:
						newLine += " "
					if ((j < startWordNumber) and (i == startLineNumber)) or ((j > endWordNumber) and (i == endLineNumber)):
						newLine += words[j]
					elif not inserted:
						newLine += word
						inserted = True
				output.append(newLine)
		return output

	def loadKeyword(self, words): #given a keyword structure, loads it into the parent objet's keywords list
		synonyms = []
		category = 0
		substitutionType = 0;

		error = 2

		for word in words:
			if (word[0] == ':'):
				precategory = word[1:]
				category = ['0' in precategory, '1' in precategory]

				error -=1

			elif(word[0] == '?'):
				substitutionType = word[1:]

				error -=1
			else:
				synonyms.append(word)

				error -=1

		if error > 0:
			raise Exception("Please make sure all keywords are set correctly")

		self.parent.keywords.append([synonyms, category, substitutionType])

	def checkMandatoryConfigurations(self): #checks if parent object has all necessary variables
		if not hasattr(self.parent, 'conditionalScope'):
			raise Exception("Please set conditionalScope on langParams file to prevent errors")
		if not hasattr(self.parent, 'stringScope'):
			raise Exception("Please set stringScope on langParams file to prevent errors")
		if not hasattr(self.parent, 'boolWords'):
			raise Exception("Please set boolWords on langParams file to prevent errors")
		if not hasattr(self.parent, 'returnIndicator'):
			raise Exception("Please set returnIndicator on langParams file to prevent errors")
		if not hasattr(self.parent, 'conditionalIndicator'):
			raise Exception("Please set conditionalIndicator on langParams file to prevent errors")
		if not hasattr(self.parent, 'blockScope'):
			raise Exception("Please set blockScope on langParams file to prevent errors")
		if not hasattr(self.parent, 'testResultIndicator'):
			raise Exception("Please set testResultIndicator on langParams file to prevent errors")
		if not hasattr(self.parent, 'testCommand'):
			raise Exception("Please set testCommand on langParams file to prevent errors")

	def isType0(self, word): #returns if given word is a keyword of type 0 - keywords to be directly replaced by others, or to be ignored
		for keyword in self.parent.keywords:
			for synonym in keyword[0]:
				if (word[0:len(synonym)] == synonym) and (keyword[1][0]):
					return True

class Mutator: #Class responsible for all major processes on mutation test
	def __init__(self): #Initializes Mutator object

		self.helper = Helper(self)

		f = open("langParams.txt","r")
		lines = f.readlines()

		self.keywords = []
		self.mutations = []
		self.locations = []
		self.aliveMutantLog = []
		self.deadMutants = 0
		self.aliveMutants = 0
		self.keepUselessMutants = False
		self.saveAliveToFile = False

		for line in lines:
			words = line.split()
			if(len(words) > 0):
				if (words[0] == "conditionalScope"):
					self.conditionalScope = [words[1], words[2]]
				elif (words[0] == "stringScope"):
					self.stringScope = [words[1], words[2]]
				elif (words[0] == "boolWords"):
					self.boolWords = [words[1], words[2]]
				elif (words[0] == "returnIndicator"):
					self.returnIndicator = words[1]
				elif (words[0] == "conditionalIndicator"):
					self.conditionalIndicator = words[1]
				elif (words[0] == "blockScope"):
					self.blockScope = words[1]
				elif (words[0] == "testResultIndicator"):
					self.testResultIndicator = words[1]
				elif (words[0] == "location"):
					self.locations.append(words[1]) 
				elif (words[0] == "testCommand"):
					self.testCommand = words[1:] 
				elif (words[0] == "keepUselessMutants"):
					self.keepUselessMutants = True 
				elif (words[0] == "saveAliveToFile"):
					self.saveAliveToFile = True 
				else:
					self.helper.loadKeyword(words)
		self.helper.checkMandatoryConfigurations()

		f.close()

	def doAllLocations(self): #Makes mutations for all locations in langParams file
		for location in self.locations:
			print("In location " + location + ":")
			self.apply(location)

	def apply(self, source): #Creates mutations (via mutate function) and runs tests and comparissons for a given source code
		self.mutate(source)

		f = open(source,"r")
		sourceBackup = f.readlines()
		f.close()

		MyOut = subprocess.Popen(self.testCommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
		stdout,stderr = MyOut.communicate()

		expectedResult = [self.helper.findTestResult(stdout), stderr]

		print ("Default test result: " + str(expectedResult))

		for mutation in self.mutations:
			f = open(source,"w")
			f.writelines(mutation)
			f.close()

			MyOut = subprocess.Popen(self.testCommand, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
			stdout,stderr = MyOut.communicate()

			result = [self.helper.findTestResult(stdout), stderr]

			print("\nObtained test result: " + str(result))

			if (result[0] != expectedResult[0]) or (result[1] != expectedResult[1]):
				print("Mutant " + str(self.deadMutants + self.aliveMutants) + " killed.")
				if(self.keepUselessMutants) or (result[0] != None):
					self.deadMutants += 1
				else:
					print("Mutant did not compile properly and was not counted. include keepUselessMutants in langParams to enable counting.")
			else:
				print("Mutant " + str(self.deadMutants + self.aliveMutants) + " survived. Number " + str(len(self.aliveMutantLog)) + " in log.")
				self.aliveMutants += 1
				self.aliveMutantLog.append(mutation)

				f = open("aliveMutants/" + str(len(self.aliveMutantLog)-1) + ".txt","w")
				f.writelines(mutator.aliveMutantLog[len(self.aliveMutantLog)-1])
				f.close()


			if(self.deadMutants + self.aliveMutants > 0):
				print(str(float(self.deadMutants)*100/float(self.deadMutants + self.aliveMutants)) + "% of mutants died.\n")

		f = open(source,"w")
		f.writelines(sourceBackup)
		f.close()

	def mutate(self, path): #Creates mutations and populates object's mutations list

		f = open(path,"r")
		lines = f.readlines()

		lineNumber = 0

		self.mutations = []

		for line in lines:
			words = line.split()
			if(len(words) > 0):
				if not (self.helper.isType0(words[0])):
					wordNumber = 0
					for word in words:
						if self.conditionalIndicator in word:

							endOfCondition = self.helper.endOfScope(lineNumber, wordNumber, lines, self.conditionalScope)

							self.mutations.append(self.helper.replaceInSourceProgram(lineNumber, endOfCondition[0], wordNumber, endOfCondition[1], lines, self.conditionalIndicator + self.conditionalScope[0] + self.boolWords[0] + self.conditionalScope[1] + endOfCondition[2]))

							self.mutations.append(self.helper.replaceInSourceProgram(lineNumber, endOfCondition[0], wordNumber, endOfCondition[1], lines, self.conditionalIndicator + self.conditionalScope[0] + self.boolWords[1] + self.conditionalScope[1] + endOfCondition[2]))
						else:
							for term in self.keywords:
								for synonym in term[0]:
									if synonym in word:
										if synonym == word:
											if term[1][0]:
												count = 0
												for synonym2 in term[0]:
													if(word != synonym2):
														self.mutations.append(self.helper.replaceInSourceProgram(lineNumber, lineNumber, wordNumber, wordNumber, lines, synonym2))
													count += 1
										else:	
											if self.helper.isBiggestApplicableSynonym(synonym, word):
												if term[1][0]:
													padding = self.helper.surroundingsInWord(synonym, word)
													count = 0
													for synonym2 in term[0]:
														if(word != synonym2):
															self.mutations.append(self.helper.replaceInSourceProgram(lineNumber, lineNumber, wordNumber, wordNumber, lines, padding[0] + synonym2 + padding[1]))
														count += 1										
						wordNumber += 1
			lineNumber += 1
		print(str(len(self.mutations)) + " mutants created.")
		f.close()

#Main program

mutator = Mutator()

if(mutator.saveAliveToFile):
	os.mkdir("aliveMutants")
mutator.doAllLocations()

#os.mkdir("mutations")
#for j in range(len(mutator.locations)):
#	mutator.mutate(mutator.locations[j])

#	for i in range(len(mutator.mutations)):
#		f = open("mutations/" + str(j) + "_" + str(i) + ".txt","w")
#		f.writelines(mutator.mutations[i])
#		f.close()