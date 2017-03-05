# coding: utf-8

import pygame
from Button import Button

class Chessboard:
	def __init__(self, game):

		self.font = game.font
		self.game = game
		self.grid_size = 26  # the width of grid
		self.start_x, self.start_y = 30, 50 # the coordinate of the left-up-most check grid 
		self.edge_size = self.grid_size / 2 # the width of blank around the checkboard
		self.grid_count = 19  # the number of grid each column or row
		# init a return button
		self.return_to_welcome = Button([600, 500], [150, 30], "Return", self.font)
		self.win_num = 5


	def draw(self):

		game = self.game
		screen = game.screen

		# draw retrun button
		self.return_to_welcome.draw(screen)

		# draw a rectangle, using RGB(185, 122, 87)
		pygame.draw.rect(screen, (185, 122, 87),
						 [self.start_x - self.edge_size, 
						  self.start_y - self.edge_size,
						  (self.grid_count - 1) * self.grid_size + self.edge_size * 2,
						  (self.grid_count - 1) * self.grid_size + self.edge_size * 2],
						 0)  # boundary line width

		# draw horizontal grid line, using black
		for r in range(self.grid_count):
			y = self.start_y + r * self.grid_size
			pygame.draw.line(screen, 
							 (0,0,0), 
							 [self.start_x, y],
							 [self.start_x + self.grid_size * (self.grid_count - 1), y],
							 2) # line width

		# draw vertical grid line, using black
		for c in range(self.grid_count):
			x = self.start_x + c * self.grid_size
			pygame.draw.line(screen, 
							 (0,0,0),
							 [x, self.start_y],
							 [x, self.start_y + self.grid_size * (self.grid_count - 1)],
							 2)  

		# draw pieces
		for r in range(self.grid_count):
			for c in range(self.grid_count):
				piece = game.current_game[r,c]
				if piece != 0:
					if piece == 1:
						color = (0, 0, 0)
					else:
						color = (255, 255, 255)

					x = self.start_x + r * self.grid_size
					y = self.start_y + c * self.grid_size
					pygame.draw.circle(screen, color, [x, y], self.grid_size // 2)


	def handle_key_event(self, e):
		game = self.game
		pos = e.pos
		if (self.return_to_welcome.check(pos)):
			game.window = 0
		else:
			game.window = 1
		absolute_r = pos[0] - (self.start_x - self.grid_size / 2)
		absolute_c = pos[1] - (self.start_y - self.grid_size / 2)
		absolute_r = absolute_r / self.grid_size
		absolute_c = absolute_c / self.grid_size
		#relative_x, relative_y = absolute_to_relative(absolute_nx, absolute_ny)
		if (absolute_r < 0 or absolute_r > 18 or absolute_c < 0 or absolute_c > 18):
			return
		
		# check if this position have been positioned a piece

		check = game.current_game[absolute_r, absolute_c]
		if(check == 0):
			if game.with_AI:
				if game.AI_first != game.current_color - 1:
					game.current_game[absolute_r, absolute_c] = game.current_color
					self.check_win(absolute_r, absolute_c)
					game.current_color %= 2
					game.current_color += 1
			else:
				game.current_game[absolute_r, absolute_c] = game.current_color
				self.check_win(absolute_r, absolute_c)
				game.current_color %= 2
				game.current_color += 1

	def get_continuous_count(self, r, c, dr, dc):
		game = self.game
		piece = game.current_game[r, c]
		if piece == 0:
			return 0

		result = 0
		i = 1
		while True:
			new_r = r + dr * i
			new_c = c + dc * i
			if 0 <= new_r < self.grid_count and 0 <= new_c < self.grid_count:
				if game.current_game[new_r, new_c] == piece:
					result += 1
				else:
					break
			else:
				break
			i += 1
		return result

	def check_win(self, r, c):
		game = self.game
		n_count = self.get_continuous_count(r, c, -1, 0)
		s_count = self.get_continuous_count(r, c, 1, 0)

		e_count = self.get_continuous_count(r, c, 0, 1)
		w_count = self.get_continuous_count(r, c, 0, -1)

		se_count = self.get_continuous_count(r, c, 1, 1)
		nw_count = self.get_continuous_count(r, c, -1, -1)

		ne_count = self.get_continuous_count(r, c, -1, 1)
		sw_count = self.get_continuous_count(r, c, 1, -1)


		if (n_count + s_count + 1 >= self.win_num ) or (e_count + w_count + 1 >= self.win_num ) or \
			(se_count + nw_count + 1 >= self.win_num ) or (ne_count + sw_count + 1 >= self.win_num ):
			game.win = game.current_game[r, c]
			game.game_over = True





