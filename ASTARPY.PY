import pygame
import math
from queue import PriorityQueue

def a_Star():
	#Pygame window initialization
	pygame.init()
	pygame.font.init()
	#sets the window's dimensions
	WIDTH = 800
	WIN = pygame.display.set_mode((WIDTH, WIDTH))
	pygame.display.set_caption("A* Path Finding Algorithm")
	FONT = pygame.font.SysFont(None, 30)
	#Colors to be used in the application
	WHITE = (255, 255, 255)
	TEXT_RED = (255, 0, 0)
	text_surface = FONT.render("Created by Tauqeer Ali Khan - ID: D3576809", True,TEXT_RED)
	RED = (255, 0, 0)
	GREEN = (0, 255, 0)
	BLUE = (0, 255, 0)
	YELLOW = (255, 255, 0)
	WHITE = (255, 255, 255)
	BLACK = (0, 0, 0)
	ORANGE = (255, 165 ,0)
	GREY = (128, 128, 128)
	TURQUOISE = (64, 224, 208)
	PURPLE=(64, 0, 208)
	GRAY=(50, 50, 50)

#The Spot class models individual grid points, managing their position, state colors, and interactions with neighboring points 
	class Spot:
		def __init__(self, row, col, width, total_rows):
			self.row = row
			self.col = col
			self.x = row * width
			self.y = col * width
			self.color = WHITE
			self.neighbors = []
			self.width = width
			self.total_rows = total_rows

		def get_pos(self):
			return self.row, self.col

		def is_closed(self):
			return self.color == TURQUOISE

		def is_open(self):
			return self.color == GREEN

		def is_barrier(self):
			return self.color == ORANGE

		def is_start(self):
			return self.color == BLACK

		def is_end(self):
			return self.color == RED

		def reset(self):
			self.color = WHITE

		def make_start(self):
			self.color = BLACK

		def make_closed(self):
			self.color = TURQUOISE

		def make_open(self):
			self.color = GREEN

		def make_barrier(self):
			self.color = ORANGE

		def make_end(self):
			self.color = RED

		def make_path(self):
			self.color = PURPLE

		def draw(self, win):
			pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
		
		#This method updates the neighbors
		def update_neighbors(self, grid):
			self.neighbors = []
			if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
				self.neighbors.append(grid[self.row + 1][self.col])

			if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
				self.neighbors.append(grid[self.row - 1][self.col])

			if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
				self.neighbors.append(grid[self.row][self.col + 1])

			if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
				self.neighbors.append(grid[self.row][self.col - 1])

		#Method used for Comparison
		def __lt__(self, other):
			return False

	#Heuristic Function which calculates manhattan distance
	def h(p1, p2):
		x1, y1 = p1
		x2, y2 = p2
		return abs(x1 - x2) + abs(y1 - y2)

	#This function, reconstruct_path, is used to reconstruct the path from a starting point to an ending point
	def reconstruct_path(came_from, current, draw):
		while current in came_from:
			current = came_from[current]
			current.make_path()
			draw()


	def algorithm(draw, grid, start, end):
		count = 0
		#Sets up various data structures such as a priority queue (open_set) to manage spots, 
		#initializes dictionaries (g_score, f_score), and creates a set (open_set_hash) to keep track of spots in the open set.
		open_set = PriorityQueue()
		open_set.put((0, count, start))
		came_from = {}
		g_score = {spot: float("inf") for row in grid for spot in row}
		g_score[start] = 0
		f_score = {spot: float("inf") for row in grid for spot in row}
		f_score[start] = h(start.get_pos(), end.get_pos())

		open_set_hash = {start}
		#Retrieves the current spot from the open_set based on its priority (determined by the f_score).
		while not open_set.empty():
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()

			current = open_set.get()[2]
			open_set_hash.remove(current)
			#If the current spot is the end spot, 
			#reconstructs the path using the reconstruct_path function, marks the end spot, and returns True.
			if current == end:
				reconstruct_path(came_from, end, draw)
				end.make_end()
				return True
			#Examines neighboring spots of the current spot.
			for neighbor in current.neighbors:
				temp_g_score = g_score[current] + 1

				if temp_g_score < g_score[neighbor]:
					came_from[neighbor] = current
					g_score[neighbor] = temp_g_score
					f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
					if neighbor not in open_set_hash:
						count += 1
						open_set.put((f_score[neighbor], count, neighbor))
						open_set_hash.add(neighbor)
						neighbor.make_open()
			#Updates the visualization (draw()) to reflect changes in the spots.
			draw()

			if current != start:
				current.make_closed()

		return False


	def make_grid(rows, width):
		grid = []
		gap = width // rows
		for i in range(rows):
			grid.append([])
			for j in range(rows):
				spot = Spot(i, j, gap, rows)
				grid[i].append(spot)

		return grid

	#Takes a Pygame window (win), the number of rows, and the total width as parameters.
	def draw_grid(win, rows, width):
		gap = width // rows
		for i in range(rows):
			pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
			for j in range(rows):
				pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


	def draw(win, grid, rows, width):
		win.fill(WHITE)

		for row in grid:
			for spot in row:
				spot.draw(win)

		draw_grid(win, rows, width)
		pygame.display.update()


	def get_clicked_pos(pos, rows, width):
		gap = width // rows
		y, x = pos

		row = y // gap
		col = x // gap

		return row, col


	def main(win, width):
		ROWS = 50
		grid = make_grid(ROWS, width)

		start = None
		end = None

		run = True
		#the loop, calls functions to draw the grid on the window (win) and updates the display to show any changes made.
		while run:
			draw(win, grid, ROWS, width)
			win.blit(text_surface, (10, 10))
			pygame.display.update()
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					run = False
				#Detect the left mouse click 
				if pygame.mouse.get_pressed()[0]: # LEFT
					pos = pygame.mouse.get_pos()
					row, col = get_clicked_pos(pos, ROWS, width)
					spot = grid[row][col]
					if not start and spot != end:
						start = spot
						start.make_start()

					elif not end and spot != start:
						end = spot
						end.make_end()

					elif spot != end and spot != start:
						spot.make_barrier()
				#Identify and handle a right mouse click to remove the drawn point on the grid.
				elif pygame.mouse.get_pressed()[2]: 
					pos = pygame.mouse.get_pos()
					row, col = get_clicked_pos(pos, ROWS, width)
					spot = grid[row][col]
					spot.reset()
					if spot == start:
						start = None
					elif spot == end:
						end = None

				if event.type == pygame.KEYDOWN:
					#Spacebar (pygame.K_SPACE): Initiates the pathfinding algorithm (algorithm) if both start and end points are defined.
					if event.key == pygame.K_SPACE and start and end:
						for row in grid:
							for spot in row:
								spot.update_neighbors(grid)

						algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
					#'C' key (pygame.K_c): Clears the grid and resets start and end points.
					if event.key == pygame.K_c:
						start = None
						end = None
						grid = make_grid(ROWS, width)

		#pygame.quit()


	main(WIN, WIDTH)
# import pygame
# import sys

# # Initialize Pygame
# pygame.init()

# # Define colors
# black = (0, 0, 0)
# white = (255, 255, 255)

# # Set up the display
# width, height = 400, 300
# screen = pygame.display.set_mode((width, height))
# pygame.display.set_caption('Pop-up Window')

# # Main loop
# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Fill the screen with white color
#     screen.fill(white)

#     pygame.display.flip()

# # Quit Pygame properly
# pygame.quit()
# sys.exit()

