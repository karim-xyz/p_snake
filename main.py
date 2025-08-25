import pygame, sys, random
pygame.init()

screen_w, screen_h = 128, 128
screen = pygame.display.set_mode((screen_w, screen_h), pygame.SCALED | pygame.RESIZABLE)
pygame.display.set_caption('snake')

clock = pygame.time.Clock()
fps = 20

black = pygame.Color(0, 0, 0, 255)
white = pygame.Color(255, 241, 232, 255)
gray = pygame.Color(95, 87, 79, 255)
green = pygame.Color(0, 228, 54, 255)
red = pygame.Color(255, 0, 77, 255)

pygame.mixer.init()
eat_sound = pygame.mixer.Sound('./food.mp3')

my_font = pygame.font.Font('./pico-8.otf', 6)

paused = False
game_over = False
collision = False
just_hit = False

class Snake:
	def __init__(self, direction, blocks, color):
		self.direction = direction
		self.last_direction = direction
		self.blocks = blocks
		self.block_size = 2
		self.color = color
		self.new_head = self.blocks[0]
		self.score = 0
	
	def update(self):
		for block in self.blocks:
			pygame.draw.rect(screen, self.color, (block[0], block[1], self.block_size, self.block_size))
	
	def move(self):
		if self.direction == 'right':
			self.new_head = [self.blocks[0][0]+self.block_size, self.blocks[0][1]]
			self.blocks.insert(0, self.new_head)
			self.blocks.pop()
			self.last_direction = self.direction
		if self.direction == 'left':
			self.new_head = [self.blocks[0][0]-self.block_size, self.blocks[0][1]]
			self.blocks.insert(0, self.new_head)
			self.blocks.pop()
			self.last_direction = self.direction
		if self.direction == 'up':
			self.new_head = [self.blocks[0][0], self.blocks[0][1]-self.block_size]
			self.blocks.insert(0, self.new_head)
			self.blocks.pop()
			self.last_direction = self.direction
		if self.direction == 'down':
			self.new_head = [self.blocks[0][0], self.blocks[0][1]+self.block_size]
			self.blocks.insert(0, self.new_head)
			self.blocks.pop()
			self.last_direction = self.direction
	
	def check_end(self):
		if self.new_head[0] >= screen_w-2:
			return True
		if self.new_head[0] <= 2:
			return True
		if self.new_head[1] <= 8:
			return True
		if self.new_head[1] >= screen_h-2:
			return True
		for block in self.blocks[1:]:
			if self.new_head == block:
				return True

snake = Snake(
	direction = 'null',
	blocks = [[30, 50], [28, 50], [26, 50], [24, 50]],
	color = green
)

class Fruit:
	def __init__(self, color):
		self.pos_x = random.randrange(2, screen_w-4, 2)
		self.pos_y = random.randrange(10, screen_h-4, 2)
		self.size = 2
		self.color = color
		self.rect = pygame.Rect(self.pos_x, self.pos_y, self.size, self.size)
	
	def update(self, collision):
		pygame.draw.rect(screen, fruit.color, fruit.rect)
		if snake.new_head == [fruit.pos_x, fruit.pos_y]:
			collision = True
		if collision:
			pygame.mixer.Sound.play(eat_sound)
			self.pos_x = random.randrange(2, screen_w-4, 2)
			self.pos_y = random.randrange(10, screen_h-4, 2)
			self.rect = pygame.Rect(self.pos_x, self.pos_y, self.size, self.size)
			if snake.direction == 'right':
				snake.new_head = [snake.blocks[0][0]+snake.block_size, snake.blocks[0][1]]
				snake.blocks.insert(0, snake.new_head)
			if snake.direction == 'left':
				snake.new_head = [snake.blocks[0][0]-snake.block_size, snake.blocks[0][1]]
				snake.blocks.insert(0, snake.new_head)
			if snake.direction == 'up':
				snake.new_head = [snake.blocks[0][0], snake.blocks[0][1]-snake.block_size]
				snake.blocks.insert(0, snake.new_head)
			if snake.direction == 'down':
				snake.new_head = [snake.blocks[0][0], snake.blocks[0][1]+snake.block_size]
				snake.blocks.insert(0, snake.new_head)
			snake.score += 1
			collision = False

fruit = Fruit(red)

def show_score():
	score_surface = my_font.render(f"score: {snake.score}", True, white)
	screen.blit(score_surface, (1, 1))

def draw_borders():
	pygame.draw.rect(screen, gray, (0, 8, screen_w, screen_h-8), 2)

def pause_game():
	if paused:
		snake.direction = 'stopped'
		snake.last_direction = snake.last_direction
		pause_surface = my_font.render("pause", True, white)
		pause_rect = pause_surface.get_rect(center = [screen_w/2, (screen_h-8)/2])
		screen.blit(pause_surface, pause_rect)

def end_game():
	if game_over:
		snake.direction = 'stopped'
		end_surface = my_font.render("game over", True, white)
		end_rect = end_surface.get_rect(center = [screen_w/2, (screen_h-8)/2])
		screen.blit(end_surface, end_rect)

running = True
while running:
	
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False
			if event.key == pygame.K_f:
				pygame.display.toggle_fullscreen()
			
			if event.key == pygame.K_RIGHT and snake.direction != 'left' and snake.direction != 'stopped':
				snake.direction = 'right'
			if event.key == pygame.K_LEFT and snake.direction != 'right' and snake.direction != 'stopped' and snake.direction != 'null':
				snake.direction = 'left'
			if event.key == pygame.K_UP and snake.direction != 'down' and snake.direction != 'stopped':
				snake.direction = 'up'
			if event.key == pygame.K_DOWN and snake.direction != 'up' and snake.direction != 'stopped':
				snake.direction = 'down'
			if game_over and event.key == pygame.K_RETURN:
				running = False
			if not paused and event.key == pygame.K_SPACE and not game_over:
				paused = True
			elif paused and event.key == pygame.K_SPACE:
				paused = False
				snake.direction = snake.last_direction
	
	screen.fill(black)
	fruit.update(collision)
	snake.move()
	snake.update()
	draw_borders()
	show_score()
	pause_game()
	game_over = snake.check_end()
	end_game()
	pygame.display.update()
	clock.tick(fps)
	
pygame.quit()
sys.exit()
