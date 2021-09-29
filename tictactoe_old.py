#An attempt to create a tic-tac-toe game without the pygame module
'''The game should run in terminal with single and multiplayer support.
depending on the initial success, further functionality 
(like difficulty levels) can be added later
'''
import random

'''Creating a board'''

class Board():
	"""A class to store board state"""
	def __init__(self):
		self.horizontal_separator = '---|---|---'
		self.board = []

	def create_empty_board(self,size=3):
		self.board = [['.'] * size for n in range(size)] # Put rows together to create a board
		return self.board

	def print_board(self):
		i = 0
		for row in self.board:
			j = 0
			for place in row:
				print(' ' + place + ' ', end = '')
				if j != 2:
					print('|', end='')
					j+=1
				else:
					print('')
			
			if i != 2:
				print(self.horizontal_separator)
				i+=1
	
	def select_square(self, board_state):
		square_selected = False
		while square_selected == False:	
			square = str(input("Which space would you like to play?"
				"\nEnter in row, colomn format: "))
			square = square.replace(',', ' ')
			square = square.split() #'square' is now a list
			if board_state[int(square[0])][int(square[1])] != '.':
				print("You really can't do that, try again!\n")
			else:
					square_selected = True
		return square
	
	def combinations(self, board_state):
		'''This functions stores all rows, columns and diagonals as a list
		to be analyzed so the next move can be determined'''
		combinations = []
		'''Adding rows'''
		for row in board_state:
			combinations.append(row)
	
		dimension = range(len(board_state))
		'''Adding columns'''
		for element in dimension:
			column = []
			for row in dimension:
				column.append(board_state[row][element])
			combinations.append(column)
		
		'''Adding diagonals'''
		diagonal_1 = []
		diagonal_2 = []
		for i in dimension:
			diagonal_1.append(board_state[i][i])
			diagonal_2.append(board_state[max(dimension)-i][i])
		combinations.append(diagonal_1)
		combinations.append(diagonal_2)	
		
		return combinations
	
	def check_win(self, combinations):
		for combination in combinations:
			if combination == ['X', 'X', 'X'] or combination == ['O', 'O', 'O']:
				print("------ Game Over! ------")
				return False
				
	def human_turn(self, board_state, row_coord, col_coord, user_symbol):
		board_state[row_coord][col_coord] = user_symbol
		return board_state
		
class AI(Board):
	"""A class dedicated to optimizing computer's performance during the game
	It needs to be capable of analyzing the board, preventing the human player 
	from winning and winning if possible"""
	#This may be a subclass for Board()
	def __init__(self, symbol):
		super(AI, self).__init__()
		self.symbol = symbol #passes X or O, depending on who went first
		if self.symbol == 'X':
			self.enemy = 'O'
		else:
			self.enemy = 'X'
		self.test_symbol = 'T'

	def tic_or_tac(self):
		print('AI is playng with ' + self.symbol + "'s\nGood luck!")

	def get_score(self, board_state, position, test_symbol):
		'''This function is going to take 'position' dictionary as an 
		argument and determine the score for it. Score will be stored 
		under 'score' key in the dictionary.
	
		position = {
			'row':0
			'colum':1
			'score':
		}

		Score consists of three elements:
		1. positional_score: How many combinations the value will appear in.
		
		
		2. enemy_score: SUM(n*(-1)^n) where n is the number of enemy symbols in the 
		combination
		
		3. friendly_score: SUM(m^m) where m is the number of friendly symbols in the 
		combination
		'''	
		board_state[position['row']][position['column']] = test_symbol
		
		positional_score = 0
		enemy_score = 0
		friendly_score = 0
		for combination in self.combinations(board_state):
			if test_symbol in combination:
				positional_score += 1
				
				enemies = combination.count(self.enemy)
				enemy_score += enemies*(-1)**enemies
				
				friends = combination.count(self.symbol)
				friendly_score += friends*friends*friends
				
			score = positional_score + enemy_score + friendly_score
		
		position['score'] = score
		board_state[position['row']][position['column']] = '.'
		return position
	
	def build_data(self,board_state):
		positions = []
		for row_num, row in enumerate(board_state):
			for col_num, column in enumerate(row):
				if column == '.':
					position = {'row':row_num,'column':col_num,'score':0}
					position = self.get_score(board_state, position, self.test_symbol)
					positions.append(position)
		return positions
	
	def print_scores(self, positions):
		for position in positions:
			print(position)
	
	def get_highest_score(self, positions):
		scores = []
		for position in positions:
			scores.append(position['score'])
		max_score = max(scores)
		best_positions = []
		for position in positions:
			if position['score'] == max_score:
				best_positions.append(position)

		return random.choice(best_positions)
			
	def ai_turn(self, board_state):
		positions = self.build_data(board_state)
		position = self.get_highest_score(positions)
		board_state[position['row']][position['column']] = self.symbol
		return board_state
	
class User():
	def __init__(self):
		self.symbol = ''
	
	def get_symbol(self):
		status = True
		while status:
			symbol = str(input("Please type the symbol of your choice (X or O): "))
			if symbol in ['X', 'O']:
				self.symbol = symbol
				status = False
			else:
				print('\nPlease choose one of the available symbols')
'''
game = Board()
game.create_empty_board()
game.board[1][1] = 'X'
game.print_board()
print(game.combinations(game.board))
computer = AI('O')
#computer.tic_or_tac()
positions = computer.build_data(game.board)
#computer.print_scores(positions)
print(computer.get_highest_score(positions))
game.board = computer.ai_turn(game.board)
game.print_board()
print(game.check_win(game.combinations(game.board)))

'''
print("--- --- --- Let's play TicTacToe! --- --- ---\n")
game = Board()
game.create_empty_board()
game.print_board()
print()
you = User()
you.get_symbol()
if you.symbol == 'X':
	computer = AI('O')
else:
	computer = AI('X')

computer.tic_or_tac()
game_status = None
while game_status == None:
	coordinates = game.select_square(game.board)
	#game.board[int(coordinates[0])][int(coordinates[1])] = you.symbol
	game.human_turn(game.board,int(coordinates[0]),int(coordinates[1]),you.symbol)
	game.print_board()
	print('\n')
	game_status = game.check_win(game.combinations(game.board))
	if game_status == False:
		break
	try:
		print("--- Computer's turn ---")
		computer.ai_turn(game.board)
		game.print_board()
		print('\n')
		game_status = game.check_win(game.combinations(game.board))
	except ValueError:
		print("---It's a Draw---")
		break
