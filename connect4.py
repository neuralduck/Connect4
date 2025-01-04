import os

class ConnectFour:
	def __init__(self):
		self.rows: int = 6
		self.columns: int = 7
		self.board = [[0 for _ in range(self.columns)] for _ in range(self.rows)]
		self.symbol1 = '\N{WHITE CIRCLE}'
		self.symbol2 = '\N{BLACK CIRCLE}'
		self.move_count = {i: 0 for i in range(7)}

	def __str__(self):
		board_str = ''
		get_symbol = lambda x: f'{self.symbol1}' if x == 1 else f'{self.symbol2}' if x == -1 else ' '
		#get_symbol = lambda x: f'{1}' if x == 1 else f'{-1}' if x == -1 else ' '
		dash = '\N{Horizontal Bar}'
		board_str += '| '+' | '.join(list(map(str, range(7))))+' |'+'\n'
		board_str += '-'*29+'\n'
		for row in self.board:
			board_str += '| '+' | '.join(list(map(get_symbol, row)))+' |'+'\n'
			board_str += '-'*29+'\n'
		return board_str

	def move(self, column, mark):
		if self.move_count[column] < 6:
			for cell in list(range(6))[::-1]:
				if self.board[cell][column] == 0:
					self.board[cell][column] = mark
					self.move_count[column] += 1
					break
	def get_value(self):
		value = 0
		result, *_ = self.check()
		if result != 3:
			value += 1000*result
		
		def get_score(window):
			score = 0
			match window.count(0):
				case 1:
					if window.count(1) == 3:
						score += 100
					if window.count(-1) == 3:
						score += -100
				case 2:
					if window.count(1) == 2:
						score += 50
					if window.count(-1) == 2:
						score += -50
				case _:
					score += window.count(1) - window.count(-1)
			return score
		
		#horizontal
		for c in range(self.columns-3):
			for r in range(self.rows):
				window = self.board[r][c:c+4]
				value += get_score(window)
		#vertical
		for c in range(self.columns):
			for r in range(self.rows-3):
				window = [self.board[r][c], self.board[r+1][c], self.board[r+2][c], self.board[r+3][c]]
				value += get_score(window)
		#/diagonal/
		for c in range(self.columns-3):
			for r in range(self.rows-3):
				window = [self.board[r][c], self.board[r+1][c+1],self.board[r+2][c+2], self.board[r+3][c+3]]
				value += get_score(window)
		#\diagonal\
		for c in range(self.columns-3):
			for r in range(3, self.rows):
				window = [self.board[r][c], self.board[r-1][c+1], self.board[r-2][c+2], self.board[r-3][c+3]]
				value += get_score(window)
		
		return value
	
	def available_moves(self):
		#returns a list of column numbers with empty cells
		return list(map(lambda x: x[0], filter(lambda x: True if x[1] < 6 else False, self.move_count.items())))
	
	def num_cells(self):
		#number of empty cells in the board, for draw and game over checks
		return 42 - sum(self.move_count.values())

	def check(self):
		# +1 player 1 | -1 player 2 | 0 draw | 3 game not over
		if self.num_cells() == 0:
			return (0, None, None)
		#horizontal
		for c in range(self.columns-3):
			for r in range(self.rows):
				if self.board[r][c] == self.board[r][c+1] == self.board[r][c+2] == self.board[r][c+3] != 0:
					return (self.board[r][c], (r, c), (r, c+3))
		#vertical
		for c in range(self.columns):
			for r in range(self.rows-3):
				if self.board[r][c] == self.board[r+1][c] == self.board[r+2][c] == self.board[r+3][c] != 0:
					return (self.board[r][c], (r, c), (r+3, c))
		#/diagonal/
		for c in range(self.columns-3):
			for r in range(self.rows-3):
				if self.board[r][c] == self.board[r+1][c+1] == self.board[r+2][c+2] == self.board[r+3][c+3] != 0:
					return (self.board[r][c], (r, c), (r+3, c+3))
		#\diagonal\
		for c in range(self.columns-3):
			for r in range(3, self.rows):
				if self.board[r][c] == self.board[r-1][c+1] == self.board[r-2][c+2] == self.board[r-3][c+3] != 0:
					return (self.board[r][c], (r, c), (r-3, c+3))
		return (3, None, None)

if __name__ == '__main__':
	def info():
		os.system('clear||cls')
		print(board)
	turn = 1
	board = ConnectFour()
	player1 = 1
	player2 = -1
	while True:
		info()
		print(board.value())
		if turn:
			choice = int(input(f"Player 1 choice ({board.symbol1}): "))
		else:
			choice = int(input(f"Player 2 choice ({board.symbol2}): "))
		if board.move_count[choice] == 6:
			print('column full')
			continue
		if choice not in range(7):
			print('pick a choice within range')
			continue
		if turn:
			board.move(choice, player1)
		else:
			board.move(choice, player2)
		turn = int(not(turn))
		result = board.check()
		if result == 1:
			info()
			print(f'Player 1 ({board.symbol1}) wins')
			break
		elif result == -1:
			info()
			print(f'Player 2 ({board.symbol2}) wins')
			break
		elif result == 0:
			info()
			print('Draw')
			break