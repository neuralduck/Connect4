import pygame as pg 
from connect4 import ConnectFour
class Ball:
	def __init__(self, x_pos, y_pos, color):
		#Ball(50, 0, 50, 'blue', 0.5, 0, 0, -1)
		self.x_pos = x_pos
		self.y_pos = y_pos
		self.color = color
		self.radius = 50
		self.retention =  0.08
		self.y_speed = 0
		self.circle = ''
		self.gravity = 3
		self.bounce_stop = 0.4
	def draw(self, screen):
		self.circle = pg.draw.circle(screen, self.color, (self.x_pos, self.y_pos), self.radius)
	def update_pos(self, stack_height = 0):
		height = 600
		if self.y_pos < height - self.radius - (stack_height*self.radius*2):
			self.y_speed += self.gravity
		elif self.y_speed > self.bounce_stop:
				self.y_speed = self.y_speed * -1 * self.retention
		elif abs(self.y_speed) <= self.bounce_stop:
				self.y_speed = 0
		self.y_pos += self.y_speed

class Game:
	def __init__(self):

		self.board = ConnectFour()

		self.grid2board = lambda x: int((x-50)/100)
		self.board2grid = lambda x: int((x*100)+50)
		self.p1_color = ()
		self.p2_color = ()
		self.on_screen = {50: [], 150: [], 250: [], 350: [], 450: [], 550: [], 650: []}
		self.last_played = None
		self.turn = 0
		self.game_over = False
		
		pg.init()
		self.running = True
		self.width = 700
		self.height = 600
		self.screen = pg.display.set_mode((self.width, self.height))
		pg.display.set_caption('Connect 4')
		self.fps = 60
		self.timer = pg.time.Clock()

	def draw_walls(self):
		self.p1_color = (7, 183, 38, 0.76)
		self.p2_color = (119, 3, 179, 0.76)
		self.screen.fill((165, 221, 227, 0.45))
		even = False
		for row in range(0, self.width, 100):
			for col in range(0, self.height, 100):
				if even:
					pg.draw.rect(self.screen, (140, 200, 220, 0.45), ((row, col), (100, 100)))
				even = not(even)
			even = not(even)
		for x in range(0, self.width+100, 100):
			wall = pg.draw.line(self.screen, 'white', (x, 0), (x, self.height), 3)
		for y in range(0, self.height+100, 100):
			pg.draw.line(self.screen, 'white', (0, y), (self.width, y), 3)

	def classic_board(self):
		self.p1_color = 'red'
		self.p2_color = 'yellow'
		self.screen.fill((0, 0, 255))
		for x in range(0, self.width, 100):
			for y in range(0, self.height, 100):
				x = 100*(x//100)+50
				y = 100*(y//100)+50
				pg.draw.circle(self.screen, 'black', (x, y), 48)

	def play(self):
		while self.running:
			self.timer.tick(self.fps)
			self.draw_walls()
			#self.classic_board()
			for col in self.on_screen:
				for n, ball in enumerate(self.on_screen[col]):
					ball.draw(self.screen)
					ball.update_pos(n)
			result, start, end = self.board.check()
			#print(result, start, end)
			
			#pg.draw.rect(self.screen, 'black', mouse_circle)
			if not self.game_over:
				pg.mouse.set_visible(False)
				if not self.turn:
					mouse_circle = pg.draw.circle(self.screen, self.p1_color, pg.mouse.get_pos(), 40)
				else:
					mouse_circle = pg.draw.circle(self.screen, self.p2_color, pg.mouse.get_pos(), 40)
				if result == 1:
					print('Player 1 wins')
					self.game_over = True
				elif result == -1:
					print('Player 2 wins')
					self.game_over = True
				elif result == 0:
					print('Draw')
					self.game_over = True
			else:
				#print('game over')
				pg.mouse.set_visible(True)
				if (start != None) and (end != None):
					start = list(map(self.board2grid, start))[::-1]
					end = list(map(self.board2grid, end))[::-1]
					if self.p1_color == 'red':
						pg.draw.line(self.screen, 'green', start, end, 8)
					else:
						pg.draw.line(self.screen, 'black', start, end, 5)

			for event in pg.event.get():
				if event.type == pg.QUIT:
					self.running = False
				
				if (event.type == pg.MOUSEBUTTONUP) and not(self.game_over):
					x, y = pg.mouse.get_pos()
					x = 100*(x//100)+(50)
					y = (100*(y//100)+50)-(len(self.on_screen[x])%6)*100
					#y = 0
					#print(x)
					self.last_played = x
					if len(self.on_screen[x]) < 6:
						if self.turn:
							self.on_screen[x].append(Ball(x, y, self.p2_color))
							self.board.move(int((x-50)/100), -1)
						else:
							self.on_screen[x].append(Ball(x, y, self.p1_color))
							self.board.move(self.grid2board(x), 1)
						self.turn = int(not(self.turn))
			pg.display.update()
			#print(self.board)
		pg.quit()

if __name__ == '__main__':
	game = Game()
	game.play()