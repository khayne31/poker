import random
import time
global StartingAmt
global StartingBet
global Players
global totalPlayers

StartingAmt = 5000
StartingBet = StartingAmt *.05
class Player():
	def __init__(self, CPU = True, number = -1):
		self.hand = []
		self.allIn = False
		self.number = str(number)
		self.money = StartingAmt
		self.current_bet = 0
		self.player_state = CPU
		self.score = []
		self.won = False
		self.dict = {
			'1' : 0,
			'2' : 0,
			'4' : 0,
			'8' : 0,
	
		}
		self.dictAmt = {
			'2' : 0,
			'4' : 0,
		}
		if not CPU:
			self.name = input("Player #"+self.number+" Name: ")
		else: 
			self.name = "NPC #"+self.number
	def print_hand(self):
		for i in range(len(self.hand)):
			print("[",dict_values[str(self.hand[i][1])],"of",dic_suits[str(self.hand[i][0])],"]")

	def greatestSuit(self, Board):
			hand_plus_board = self.hand + Board.hand
			SuitTest = [x[0] for x in hand_plus_board]
			SuitCounter = [(SuitTest.count(1), 1), (SuitTest.count(2),2), (SuitTest.count(3),3), (SuitTest.count(4),4)]
			SuitCounter = sorted(SuitCounter)
			return SuitCounter[3]

	def deleteRepeatedValues(self, list):
		for x in list:
			if list.count(x) > 1:
				list.remove(x)
		return list

	def isFlush(self,Board):	
		return self.greatestSuit(Board)[0] >= 5

	def isPairOrTriple(self, Board, Description):
		#TODO: RETURN the card aswell as the boolean
		hand_plus_board= self.hand + Board.hand
		ValueList = [x[1] for x in hand_plus_board]
		SuitCounter = []
		for x in hand_plus_board:
			SuitCounter.append((x[1],ValueList.count(x[1])))
		pairCount = 0
		SuitCounter = self.deleteRepeatedValues(SuitCounter)
		SuitCounter = sorted(SuitCounter, reverse = True)
		amtPairandTrips = [x[1] for x in SuitCounter]
		self.dictAmt['2'] = amtPairandTrips.count(2)
		self.dictAmt['4'] = amtPairandTrips.count(3)
		for x in SuitCounter:
			if Description == "triple":
				if x[1] == 3:
					self.dict['4'] = x[0]
					return True
			if Description == "pair":
				if x[1] == 2:
					self.dict['2'] = x[0]
					return True
			if Description == "two-pair":
				if x[1] == 2:
					temp = x[0]
					pairCount += 1
				if pairCount == 2:
					if x[0] > temp:
						self.dict['3'] = x[0]
					else:
						self.dict['3'] = temp
					return True
		return False

	def isRoyalFlush(self, Board):
		if self.isFlush(Board):
			hand_plus_board = hand_plus_board = self.hand + Board.hand
			greatestSuit = self.greatestSuit(Board)[1]
			ValueTest = [x[1] for x in hand_plus_board if x[0] == greatestSuit]
			ValueTest = sorted(ValueTest)
			if ValueTest[-5:] == [10, 11, 12, 13, 14]:
				return True
		return False

	def isStraight(self, Board):
		straightTest = [2,3,4,5,6,7,8,9,10,11,12,13]
		hand_plus_board = hand_plus_board = self.hand + Board.hand
		ValueTest = [x[1] for x in hand_plus_board]
		ValueTest = sorted(ValueTest)
		self.deleteRepeatedValues(ValueTest)
		if len(hand_plus_board) == 5:
			if ValueTest == straightTest[ValueTest[0] - 2: ValueTest[0] + 3]:
				return True
		if len(hand_plus_board) == 6:
			if ValueTest[0:5] == straightTest[ValueTest[0] - 2: ValueTest[0] + 3]:
				return True
			if ValueTest[1:6] == straightTest[ValueTest[1] - 2: ValueTest[1] + 3]:
				return True
		if len(hand_plus_board) == 7:
			if ValueTest[0:5] == straightTest[ValueTest[0] - 2: ValueTest[0] + 3]:
				return True
			if ValueTest[1:6] == straightTest[ValueTest[1] - 2: ValueTest[1] + 3]:
				return True
			if ValueTest[2:7] == straightTest[ValueTest[2] - 2: ValueTest[2] + 3]:
				return True
		return False

	def isStraightFlush(self, Board):
		return self.isFlush(Board) and self.isStraight(Board)


	def fourOfAKind(self, Board):
		hand_plus_board = self.hand + Board.hand
		ValueList = [x[1] for x in hand_plus_board]
		Completed = []
		Greatest = (0,0)
		for x in ValueList:
			if x not in Completed:
				if ValueList.count(x) > Greatest[1]:
					Greatest = (x, ValueList.count(x))
				Completed.append(x)
		if Greatest[1] == 4:
			self.dict['8'] = Greatest[0]
			return True
		return False

	def fullHouse(self, Board):
		return self.isPairOrTriple(Board, "triple") and self.isPairOrTriple(Board, "pair")

	def isTwoPair(self, Board):
		return self.isPairOrTriple(Board, "two-pair")

	def HighCard(self):
		ValueList = [x[1] for x in self.hand]
		return sorted(ValueList)[1]	

	def identifyHand(self, Board):
		usless = Board.isPairOrTriple("pair")
		if self.isRoyalFlush(Board) and not Board.isRoyalFlush():
			self.score.append(10)
		elif self.isStraightFlush(Board) and not Board.isStraight():
			self.score.append(9)
		elif self.fourOfAKind(Board) and not Board.fourOfAKind():
			self.score.append(8)
		elif self.fullHouse(Board) and not Board.fullHouse():
			self.score.append(7)
		elif self.isFlush(Board) and not Board.isFlush():
			self.score.append(6)
		elif self.isStraight(Board) and not Board.isStraight():
			self.score.append(5)
		elif self.dictAmt['4'] - Board.dictAmt['4'] > 0:
			self.score.append(4)
		if self.dictAmt['2'] - Board.dictAmt['2'] == 2:
			self.score.append(3)
		elif self.score[:-1] == 7 and self.isPairOrTriple(Board, "two-pair"):
			selfscore.append(2)
		elif self.dictAmt['2'] - Board.dictAmt['2'] == 1:
			self.score.append(2)
		self.score.append(float((1/14)*self.HighCard()))
		self.dict['1'] = self.HighCard()



class Board():
	def __init__(self, numberPlayers = 2):
		self.pot = 0
		self.hand = []
		self.numPlayers = numberPlayers
		self.dictAmt={
			'2' : 0,
			'3' : 0,
		}
		self.current_bet = StartingBet

	def print_board_state(self):
		for i in range(len(self.hand)):
			print("[",dict_values[str(self.hand[i][1])],"of",dic_suits[str(self.hand[i][0])],"]")

	def greatestSuit(self):
			hand_plus_board = self.hand
			SuitTest = [x[0] for x in hand_plus_board]
			SuitCounter = [(SuitTest.count(1), 1), (SuitTest.count(2),2), (SuitTest.count(3),3), (SuitTest.count(4),4)]
			SuitCounter = sorted(SuitCounter)
			return SuitCounter[3]

	def deleteRepeatedValues(self, list):
		for x in list:
			if list.count(x) > 1:
				list.remove(x)
		return list

	def isFlush(self):	
		return self.greatestSuit()[0] >= 5

	def isPairOrTriple(self, Description):
		#TODO: RETURN the card aswell as the boolean
		hand_plus_board= self.hand 
		ValueList = [x[1] for x in hand_plus_board]
		SuitCounter = []
		for x in hand_plus_board:
			SuitCounter.append((x[1],ValueList.count(x[1])))
		pairCount = 0
		SuitCounter = self.deleteRepeatedValues(SuitCounter)
		SuitCounter = sorted(SuitCounter, reverse = True)
		amtPairandTrips = [x[1] for x in SuitCounter]
		self.dictAmt['2'] = amtPairandTrips.count(2)
		self.dictAmt['4'] = amtPairandTrips.count(3)
		for x in SuitCounter:
			if Description == "triple":
				if x[1] == 3:
					return True
			if Description == "pair":
				if x[1] == 2:
					return True
			if Description == "two-pair":
				if x[1] == 2:
					temp = x[0]
					pairCount += 1
				if pairCount == 2:
					return True
		return False

	def isRoyalFlush(self):
		if self.isFlush():
			hand_plus_board = hand_plus_board = self.hand
			greatestSuit = self.greatestSuit()[1]
			ValueTest = [x[1] for x in hand_plus_board if x[0] == greatestSuit]
			ValueTest = sorted(ValueTest)
			if ValueTest[-5:] == [10, 11, 12, 13, 14]:
				return True
		return False

	def isStraight(self):
		straightTest = [2,3,4,5,6,7,8,9,10,11,12,13]
		hand_plus_board = hand_plus_board = self.hand
		ValueTest = [x[1] for x in hand_plus_board]
		ValueTest = sorted(ValueTest)
		self.deleteRepeatedValues(ValueTest)
		if len(hand_plus_board) == 5:
			if ValueTest == straightTest[ValueTest[0] - 2: ValueTest[0] + 3]:
				return True
		if len(hand_plus_board) == 6:
			if ValueTest[0:5] == straightTest[ValueTest[0] - 2: ValueTest[0] + 3]:
				return True
			if ValueTest[1:6] == straightTest[ValueTest[1] - 2: ValueTest[1] + 3]:
				return True
		if len(hand_plus_board) == 7:
			if ValueTest[0:5] == straightTest[ValueTest[0] - 2: ValueTest[0] + 3]:
				return True
			if ValueTest[1:6] == straightTest[ValueTest[1] - 2: ValueTest[1] + 3]:
				return True
			if ValueTest[2:7] == straightTest[ValueTest[2] - 2: ValueTest[2] + 3]:
				return True
		return False

	def isStraightFlush(self):
		return self.isFlush() and self.isStraight()


	def fourOfAKind(self):
		hand_plus_board = self.hand
		ValueList = [x[1] for x in hand_plus_board]
		Completed = []
		Greatest = (0,0)
		for x in ValueList:
			if x not in Completed:
				if ValueList.count(x) > Greatest[1]:
					Greatest = (x, ValueList.count(x))
				Completed.append(x)
		return Greatest[1] == 4


	def fullHouse(self):
		return self.isPairOrTriple("triple") and self.isPairOrTriple("pair")

	def isTwoPair(self):
		return self.isPairOrTriple("two-pair")


dic_hand_types = {
	'1' : "High Card",
	'2' : "A Pair",
	'3' : "Two pairs",
	'4' : "A Triple",
	'5' : "A Straight",
	'6' : "A Flush",
	'7' : "A Full House",
	'8' : "Four of a Kind",
	'9' : "A Straight Flush",
	'10' : "A Royal Flush"
}

dic_suits = {
	'1' : "Spades",
	'2' : "Hearts",
	'3' : "Clubs",
	'4' : "Diamonds"
}

dict_values = {
	'2' : "2",
	'3' : "3",
	'4' : "4",
	'5' : "5",
	'6' : "6",
	'7' : "7",
	'8' : "8",
	'9' : "9",
	'10' : "10",
	'11' : "Jack",
	'12' : "Queen",
	'13' : "King",
	'14' : "Ace"
}

Deck = [
	(1,2),
	(1,3),
	(1,4),
	(1,5),
	(1,6),
	(1,7),
	(1,8),
	(1,9),
	(1,10),
	(1,11),
	(1,12),
	(1,13),
	(1,14),
	(2,2),
	(2,3),
	(2,4),
	(2,5),
	(2,6),
	(2,7),
	(2,8),
	(2,9),
	(2,10),
	(2,11),
	(2,12),
	(2,13),
	(2,14),
	(3,2),
	(3,3),
	(3,4),
	(3,5),
	(3,6),
	(3,7),
	(3,8),
	(3,9),
	(3,10),
	(3,11),
	(3,12),
	(3,13),
	(3,14),
	(4,2),
	(4,3),
	(4,4),
	(4,5),
	(4,6),
	(4,7),
	(4,8),
	(4,9),
	(4,10),
	(4,11),
	(4,12),
	(4,13),
	(4,14),
]

Current_Deck = Deck
Drawn = []
totalPlayers = []
Players = totalPlayers
Board = Board()


def draw_a_card():
	card = Current_Deck[random.randint(0,len(Current_Deck)-1)]
	Drawn.append(card)
	Current_Deck.remove(card)
	return card

def Deal_hands():
	for i in range(2):
		for x in Players:
			x.hand.append(draw_a_card())
def stage1(Board):
	for i in range(3):
		Board.hand.append(draw_a_card())

def betting(Board, raising = False):
	#TODO: make it so that if evryone folds the remaining player is the winner
	manualPlayers = [player for player in Players if player.player_state == False]
	toRaise = False
	if raising:
		print("\n\nSomeone decided to raise. We are now raising... \n\n")
	for player in manualPlayers:
		print("=================================")
		print("You have this much money:", player.money)
		print("The current bet is:", Board.current_bet)
		print("The pot is:", Board.pot)
		if player.money > 0 or not player.allIn:
			print("\n",player.name+"'s Hand: ")
			player.print_hand()
			print("\nThe Board: ")
			Board.print_board_state()	
			print("=================================")
			print("\n")
			bet = int(input(player.name + " do you want to 1) check, 2) raise, or 3) fold?:"))
			if bet == 2 and player.money - Board.current_bet < 0:
				bet = input("You dont have enough funds to raise, please either 1) check or 3) fold")
			if bet == 1 and player.money - Board.current_bet < 0:
				bet = input("You dont have enough funds to check, please 3) Fold 4) All i've got")
			elif bet == 1:
				player.money = player.money - Board.current_bet
				Board.pot += Board.current_bet
				print("The current bet is:", Board.current_bet)
				#TODO: make it so that if they dont have enough money everything they have goes into the pot
			elif bet == 2 and player.money - Board.current_bet >= 0:
				raiseAmt = int(input("By how much do you want to raise by?: "))
				while(player.money - (Board.current_bet + raiseAmt)< 0):
					print("Not enough money raise again!")
					raiseAmt = int(input("By how much do you want to raise by?: "))
				Board.current_bet = raiseAmt + Board.current_bet

				toRaise = True
				player.money = player.money - Board.current_bet
				Board.pot += Board.current_bet
			elif bet == 3:
				print("You have been eliminated")
				Players.remove(player)
				manualPlayers.remove(player)
			elif bet == 4:
				player.allIn = True
				Board.pot += player.money
				player.money = 0

		elif not player.allIn:
			if not player.allIn:
				print("You have been eliminated")
				Players.remove(player)
				manualPlayers.remove(player)
			else:
				print("You are all in. Passing...")
		clearScreen()


	cpuPlayers = [player for player in Players if player.player_state == True]

	for player in cpuPlayers:
		decision = random.randint(1,100)
		if player.money > 0:
			if decision <= 16:
				#Fold
				Players.remove(player)
				cpuPlayers.remove(player)
			elif decision <= 46 and player.money - Board.current_bet > 0:
				#Raise
				if decision % 8 == 0:#12.5%
					#all in 
					raiseAmt = player.money
				else:
					raiseAmt = random.randint(1,int((player.money - Board.current_bet)*.2))
				Board.current_bet = raiseAmt + Board.current_bet
				toRaise = True
				player.money = player.money - Board.current_bet
				Board.pot += Board.current_bet
			elif decision <= 100:
				#TODO: make it so that if they dont have enough money everything they have goes into the pot
				if player.money < Board.current_bet:
					Board.pot += player.money
					player.money = 0
				player.money = player.money - Board.current_bet
				Board.pot += Board.current_bet
		else:
			Players.remove(player)
			cpuPlayers.remove(player)

	if toRaise:
		betting(Board, raising = True)


def Game(Board):
	print("\n1st stage betting")
	betting(Board)
	print("\n\ndealing cards...\n\n")
	for i in range(3):
		Board.hand.append(draw_a_card())
	print("2nd stage betting")
	betting(Board)
	print("\n\ndealing cards...\n\n")
	Board.hand.append(draw_a_card())
	print("Final betting")
	betting(Board)
	print("\n\ndealing cards...\n\n")
	Board.hand.append(draw_a_card())
	winning(Board)

def win_condition(Board):
	for player in Players:
		player.identifyHand(Board)
	playerList = [player.score for player in Players if len(player.score) > 0]
	playerList = sorted(playerList, reverse = True)
	winning_score = playerList[0]
	winners = []
	for player in Players:
		if player.score == winning_score:
			winners.append(player)

	if len(winners) > 1:
		score = winners[0].score
		greatestValue = (0, Player())
		newWinners = []
		lastGreatestValue = 0
		if score not in [2,3,4,8]:
			for winner in winners:
				if winner.dict['1'] == greatestValue:
					newWinners.append[winner]
				if winner.dict['1'] > greatestValue[0]:
					newWinners = []
					newWinners.append(winner)
					lastGreatestValue = greatestValue
					greatestValue = (winner.dict['1'], winner)

		else:
			for winner in winners:
				if winner.dict[str(score)] == greatestValue:
						newWinners.append[winner]
				if winner.dict[str(score)] > greatestValue[0]:
					newWinners = []
					newWinners.append(winner)
					lastGreatestValue = greatestValue
					greatestValue = (winner.dict[str(score)], winner)
		return newWinners
	else:
		return winners

def winning(Board):
	winners = win_condition(Board)
	if len(winners) > 1:
		for item in winners:
			item.won = True
			sys.flush()
			print(item.name, "has tied with a")
			item.money = Board.pot/len(winners)
	else: 
		print(winners[0].name, "has won with:")
		for item in winners[0].score[:-1]:
			print(dic_hand_types[str(item)])
		if len(winners[0].score[:-1]) == 0:
			print(" a high Card:", winners[0].HighCard())

		winners[0].money = Board.pot
	Board.pot = 0

def clearScreen():
	for i in  range(40):
		print("\n")

def intro():
	numManPlayers = int(input("How many manual players do you want?: "))
	numNPC = int(input("How many NPC's?: "))
	for i in range(numManPlayers):
		totalPlayers.append(Player(CPU=False, number = i+1))
	for i in range(numNPC):
		totalPlayers.append(Player(number = i+1))
	Deal_hands()



def matches(Board):
	quit = False
	intro()
	while(not quit):
		Players = totalPlayers
		Game(Board)
		toQuit = int(input("Do you want to quit 1) yes 2) no: "))
		if toQuit == 1:
			print("Quitting...")
			quit = True
matches(Board)