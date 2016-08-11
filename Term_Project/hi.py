import pygame
from pygame import *
from pygame import display
from pygame import movie
import sys
import time
from random import *


#Colors
Aqua = (0, 255, 255)
Black = (0, 0, 0)
Blue = (0, 0, 255)
CornflowerBlue = (100, 149, 237)
Fuchsia = (255, 0, 255)
Gray = (128, 128, 128)
Green = (0, 128, 0)
Lime = (0, 255, 0)
Maroon = (128, 0, 0)
NavyBlue = (0, 0, 128)
Olive = (128, 128, 0)
Purple = (128, 0, 128)
Red = (255, 0, 0)
Silver = (192, 192, 192)
Teal = (0, 128, 128)
White = (255, 255, 255)
Yellow = (255, 255, 0)

screen_width = 800
screen_height = 600

#global lives
#lives = 10


speed = [1,1]
gravity = 0.1

WIN_WIDTH = 1100
WIN_HEIGHT = 600
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)
global HORIZ_MOV_INCR
HORIZ_MOV_INCR = 10

CAMERA_SLACK = 30



class Player(pygame.sprite.Sprite):   #class player which is a sprite
	penguin = pygame.sprite.Group()
	def __init__(self,x, y):
		#super(Player,self).__init__(*groups)
		pygame.sprite.Sprite.__init__(self)
		self.x = x
		self.y = y
		self.image = pygame.image.load('penguin.png')   #load image into the player
		self.rect = pygame.rect.Rect((self.x,self.y), self.image.get_size())  #obtain a rectangle around it
		self.resting = False  #flag stored to know when the character is resting
		self.dy = 0
		self.lives = 10
		self.alive = True
		self.Reached_Goal = False    

	def update(self, dt, game, screen):
		self.isAlive()
		self.checkGoal()
		self.enemeyCollision()
		self.icicleCollision()
		self.gameOver()
		last = self.rect.copy()
		key = pygame.key.get_pressed()
		if key[pygame.K_UP]:
			self.rect.y -= 500 * dt
		if key[pygame.K_LEFT]:
			self.rect.x -= 300 * dt
		if key[pygame.K_RIGHT]:
			self.rect.x += 300 * dt
		if key[pygame.K_DOWN]:
		 	self.rect.y += 300 * dt
		if self.resting and key[pygame.K_SPACE]:
			self.dy = -300
			self.resting = False
		self.dy = min(400, self.dy + 40)

		self.rect.y += self.dy * dt

		new = self.rect
		for cell in pygame.sprite.spritecollide(self, terrain.All_Terrain ,False):
			cell = cell.rect
			if last.right <= cell.left and new.right > cell.left:
 				new.right = cell.left
 			if last.left >= cell.right and new.left < cell.right:
 				new.left = cell.right
 			if last.bottom <= cell.top and new.bottom > cell.top:
 				self.resting = True
 				new.bottom = cell.top
 				self.dy = 0
 			if last.top >= cell.bottom and new.top < cell.bottom:
 				new.top = cell.bottom
 				self.dy = 0

 
 	def drawLivesCounter(self):
 		font = pygame.font.Font(None, 36)
 		text = font.render(str(self.lives), 1, (10,10,10))
 		textpos = text.get_rect()
 		textpos.centerx = 100
 		textpos.centery = 100
 		screen.blit(text,textpos)


 	def checkGoal(self):
 		if pygame.sprite.spritecollide(self, terrain.Goal, False):
 			self.goalSound()
 			self.Reached_Goal = True

 	#def playMusic(self):
 	#	file = 'snow.mp3'
 	#	pygame.mixer.init()
 	#	pygame.mixer.music.load(file)
 	#	pygame.mixer.music.play(-1)

 	def snowSound(self):
 		#file = snow_effect.wav
		sound = pygame.mixer.Sound('snow_effect.wav')
		#pygame.mixer.music.load(file)
		#pygame.mixer.music.play()
		pygame.mixer.Sound.play(sound)

	def goalSound(self):
		sound = pygame.mixer.Sound('goal.wav')
		pygame.mixer.Sound.play(sound)

 	def enemeyCollision(self):
 		if pygame.sprite.spritecollide(self, enemey.Enemies, False):
 			self.snowSound()
 			self.lives -= 1
 			#self.rect = pygame.rect.Rect((self.x,self.y), self.image.get_size())
 			#self.playMusic()

 	def icicleCollision(self):
 		if pygame.sprite.spritecollide(self, Icicles.Ice,False):
 			self.snowSound()
 			self.lives -= 1
 			#self.rect = pygame.rect.Rect((self.x,self.y), self.image.get_size())
 			#self.playMusic()



 	def isAlive(self):
		if self.rect.left < 0 or self.rect.right > WIN_WIDTH or self.rect.top < 0 or self.rect.bottom >WIN_HEIGHT:
			self.snowSound()
			self.lives -= 1
			#self.rect = pygame.rect.Rect((self.x,self.y), self.image.get_size())
			#self.playMusic()

	def gameOver(self):
		if self.lives <= 0:
			self.alive = False


class terrain(pygame.sprite.Sprite):
	All_Terrain = pygame.sprite.Group()
	Goal = pygame.sprite.Group()
	Snow = pygame.sprite.Group()
	def __init__(self, image, x, y):
			pygame.sprite.Sprite.__init__(self)
			#self.image = pygame.image.load('floor_large.png')
			self.image = image
			self.rect = pygame.rect.Rect((x,y), self.image.get_size())

class enemey(pygame.sprite.Sprite):
	Enemies = pygame.sprite.Group()
	def __init__(self, image, x, y, direction, dx, platform_width):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		#self.x = x
		#self.rect.centery = y
		#platform_width = 
		#self.direction = "right"
		self.direction = direction
		self.dx = dx
		self.platform_width = platform_width

		self.rect = pygame.rect.Rect((x,y), self.image.get_size())
		self.last = self.rect.copy()
		#self.rect.x = x

	#def update(self, dt, game, screen, platform_width, direction, dx):
	def update(self, dt, game, screen):
		if self.direction == "right":
			self.rect.x += self.dx * dt
			if self.rect.x >= self.last.x + self.platform_width /2:
				self.direction = "left"
		if self.direction == "left":
			self.rect.x -= self.dx * dt
			if self.rect.x <= self.last.x - self.platform_width / 2:
				self.direction = "right" 
		
		#if self.rect.x == self.last.x:
			#self.direction = right
		#	self.rect.x += dx * dt
		#if self.rect.x == self.last.x - platform_width / 2:
			#self.direction = right
		#	self.rect.x -= dx * dt
		#if self.rect.x == self.last.x + platform_width / 2:
			#self.drection = left
		#	self.rect.x += dx * dt

		#self.rect.x -= randint(-50,50) * dt

		


class FallingSnow(pygame.sprite.Sprite):
	Snowy = pygame.sprite.Group()
	def __init__(self, image, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = pygame.rect.Rect((x,y), self.image.get_size())
		self.rect.y = y

	def update(self, dt, game, screen):
		self.rect.y += 100 * dt




class cloud(pygame.sprite.Sprite):
	Clouds = pygame.sprite.Group()
	def __init__(self, image, x, y, direction, dx, screen_width):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.direction = direction
		self.dx = dx
		self.screen_width = screen_width
		self.rect = pygame.rect.Rect((x,y), self.image.get_size())
		self.last = self.rect.copy()

	def update(self, dt, game, screen):
		if self.direction == "right":
			self.rect.x += self.dx * dt
			if self.rect.x >= self.last.x + self.screen_width / 2.5:
				self.direction = "left"
		if self.direction == "left":
			self.rect.x -= self.dx * dt
			if self.rect.x <= self.last.x - self.screen_width / 2.5:
				self.direction = "right" 



class Icicles(pygame.sprite.Sprite):
	Ice = pygame.sprite.Group()
	def __init__(self, image, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = pygame.rect.Rect((x,y), self.image.get_size())

	def update(self, dt, game, screen):
		self.rect.y += 100 * dt




main_penguin = pygame.image.load('penguin.png')
snowman = pygame.image.load('snowman.png')
large_floor = pygame.image.load('floor_large.png')
snow = pygame.image.load('tile.png')
goal = pygame.image.load('goal.png')
small_floor = pygame.image.load('floor_small.png')
snow1 = pygame.image.load('snow1.png')
cloud_image = pygame.image.load('cloud.png')
icicle_image = pygame.image.load('icicle.png')
text_1 = pygame.image.load('Text_1.png')
text_2 = pygame.image.load('Text_2.png')
text_3 = pygame.image.load('text_3.png')
text_4 = pygame.image.load('text_4.png')
background_1 = pygame.image.load('Background_1.png')
background_2 = pygame.image.load('Background_2.jpg')
background_3 = pygame.image.load('Background_3.png')
background_4 = pygame.image.load('Background_4.jpg')
main_title = pygame.image.load('main_title.png')

text_bubble1 = pygame.image.load('text_bubble1.png')
text_bubble2 = pygame.image.load('text_bubble2.png')
text_bubble3 = pygame.image.load('text_bubble3.png')
text_instructions = pygame.image.load('Instruction_Text.png')
text_bubble4 = pygame.image.load('text_bubble4.png')

left_arrow = pygame.image.load('left_arrow.png')
right_arrow = pygame.image.load('right_arrow.png')
escape_button = pygame.image.load('escape_button.png')
	#def drawTerrain(self)

#class enemy(pygame.sprite.Sprite):

#class ScrolledGroup(pygame.sprite.Group):
#	def draw(self,surface):
#		for sprite in self.sprites():
#			surface.blit(sprite.image, (sprite.rect.x - self.camera_x, sprite.rect.y))





#all_fonts = pygame.font.get_fonts()

#class levels(object):
#	def __init__(self, background, sprites):



#########  LEVELS #########


# = [[small_floors], [large_floors], [goal], [enemies], [clouds]]
Level_1 = [[terrain(small_floor, 550,350), terrain(small_floor, 350, 300), terrain(small_floor, 600, 200)], [terrain(large_floor, 30, 300), terrain(large_floor, 900, 300)], [terrain(goal, 950, 215)], [enemey(snowman, 1700, 300, "right", 50, 125)], [cloud(cloud_image, 2000, 20, "right", 10, 10)], [Player(30,200)]]
Level_2 = [[terrain(small_floor, 1000, 237), terrain(small_floor, 900,300), terrain(small_floor, 500, 500)],[terrain(large_floor,30,150), terrain(large_floor,300,300), terrain(large_floor, 700, 400)],[terrain(goal,1000,150)],[  enemey(snowman, 800, 340, "right", 50, 125),enemey(snowman, 400,240, "right", 50, 125) ], [cloud(cloud_image, HALF_WIDTH , 50, "right", 100, WIN_WIDTH)], [Player(30,30)]  ]
Level_3 = [[terrain(small_floor, 500, 500)], [terrain(large_floor, 30, 150), terrain(large_floor, 800, 300)], [terrain(goal, 900, 215)], [enemey(snowman, 1500,240, "right", 50, 125)] , [cloud(cloud_image, HALF_WIDTH , 50, "right", 100, WIN_WIDTH)], [Player(30,30)]]

Level_4 = [[terrain(small_floor, 525 , 500)],[terrain(large_floor,475,200)],[terrain(goal,525,420)],[  enemey(snowman, 1700, 340, "right", 50, 125)], [cloud(cloud_image, HALF_WIDTH , 50, "right", 100, WIN_WIDTH), cloud(cloud_image, HALF_WIDTH + 200, 150, "right", 100, WIN_WIDTH)], [Player(550,100)] ]


Level_5 = [[terrain(small_floor, 200, 500), terrain(small_floor, 775,425), terrain(small_floor, 950, 500)],[terrain(large_floor,0,250), terrain(large_floor,240,225), terrain(large_floor, 480 , 200), terrain(large_floor,720,180)],[terrain(goal,200,415)],[  enemey(snowman, 2000, 340, "right", 50, 125)], [cloud(cloud_image, HALF_WIDTH , 50, "right", 100, WIN_WIDTH), cloud(cloud_image, HALF_WIDTH + 50 , 50, "left", 100, WIN_WIDTH)], [Player(30,30)] ]

Level_6 = [[terrain(small_floor, 50, 200), terrain(small_floor, 150,200), terrain(small_floor, 300, 200), terrain(small_floor,500, 200)],[terrain(large_floor,800,200)],[terrain(goal,900,115)],[  enemey(snowman, 1700, 340, "right", 50, 125)], [cloud(cloud_image, HALF_WIDTH , 50, "right", 100, WIN_WIDTH)], [Player(50,100)] ]
Level_7 = [[terrain(small_floor, 500, 500)],[terrain(large_floor,400,150)],[terrain(goal,500,70)],[  enemey(snowman, 1700, 340, "right", 50, 125)], [cloud(cloud_image, HALF_WIDTH , 50, "right", 100, WIN_WIDTH)], [Player(500, 425)] ] 
Level_8 = [[terrain(small_floor, 500, 300)], [terrain(large_floor, 30, 500), terrain(large_floor, 100, 200), terrain(large_floor,600, 400 ), terrain(large_floor, 800, 125)], [terrain(goal, 850, 40)], [enemey(snowman, 200, 145, "right", 50, 125), enemey(snowman,650, 345, "left", 50, 125)], [cloud(cloud_image,  HALF_WIDTH, 50, "left", 100, WIN_WIDTH)], [Player(50,400)]]



Level_9 = [[terrain(small_floor, 125,500)], [terrain(large_floor, 30, 245), terrain(large_floor, 350, 100), terrain(large_floor, 350, 350), terrain(large_floor, 700,245), terrain(large_floor,350, 530)], [terrain(goal, 400, 445)], [enemey(snowman, 470, 293, "right", 50, 125),enemey(snowman, 130, 190 , "left", 50,125), enemey(snowman,430,477, "right", 50,125), enemey(snowman,755, 190, "left", 50,125)], [cloud(cloud_image, HALF_WIDTH, 20, "right", 100, WIN_WIDTH)], [Player(400,5)]]





Level_10 = [[terrain(small_floor, 20,550), terrain(small_floor, 100, 100), terrain(small_floor, 250, 450), terrain(small_floor, 600, 200), terrain(small_floor, 800, 400), terrain(small_floor, 850, 150)], [terrain(large_floor, 30, 250), terrain(large_floor, 900, 525), terrain(large_floor, 450, 400)], [terrain(goal, 850, 70)], [enemey(snowman, 115 , 197, "right", 50, 175), enemey(snowman, 530, 345, "left", 50, 125), enemey(snowman, 960, 475, "left", 50, 125)], [cloud(cloud_image, HALF_WIDTH, 20, "right", 100, WIN_WIDTH), cloud(cloud_image, HALF_WIDTH - 80, 10, "left", 100, WIN_WIDTH), cloud(cloud_image, HALF_WIDTH + 50, 40, "left", 100, WIN_WIDTH)], [Player(20,475)]]






class Game(object):
	#def __init__(self):
	#	self.lives = 10
		
	#def FallingSnow(self):
	#snow = []
	#	while True:
	#		terrain.Snow.add(terrain(snow,randint(0,WIN_WIDTH),50))
	#		time.sleep(1)
		
	#def drawPauseScreen(self):
	def drawEndGame(self,screen):
		screen.blit(background_3, (0,0))
		#pygame.display.flip()

	def drawMainScreen(self,screen):
		#main_background = pygame.image.load()
		screen.blit(background_2, (0,0))
		screen.blit(text_2, (HALF_WIDTH / 2.3, HALF_HEIGHT / 0.75))
		screen.blit(main_title, (HALF_WIDTH / 1.7, HALF_HEIGHT / 4))
		#font = pygame.font.Font(Comic Sans MS,50)
		#text = font.render("Press Enter To Start", 1, Blue)
		#textpos = text.get_rect()
		#textpos.centerx = HALF_WIDTH
		#textpos.centery = HALF_HEIGHT
		#screen.blit(text, textpos)
		pygame.display.flip()

	def drawHelpScreen_1(self,screen):
		screen.blit(background_3, (0,0))
		screen.blit(text_bubble1, (500, 50))
		screen.blit(text_3, (15, 110))
		screen.blit(right_arrow, (950, 500))
		screen.blit(escape_button, (850, 500))
		pygame.display.flip()

	def drawHelpScreen_2(self,screen):
		screen.blit(self.background, (0,0))
		screen.blit(text_instructions, (50, 50))
		screen.blit(main_penguin, (275,240))
		screen.blit(snowman, (875, 268))
		screen.blit(cloud_image, (50, 100))
		screen.blit(right_arrow, (950, 500))
		screen.blit(left_arrow, (850, 500))
		pygame.display.flip()


	def drawHelpScreen_3(self,screen):
		screen.blit(background_3, (0,0))
		screen.blit(text_bubble2, (-100, 20))
		screen.blit(right_arrow, (950, 500))
		screen.blit(left_arrow, (850, 500))
		pygame.display.flip()

	def drawHelpScreen_4(self,screen):
		screen.blit(background_4, (0,0))
		screen.blit(text_bubble4, (200,50))
		screen.blit(left_arrow, (850, 500))
		screen.blit(escape_button, (950, 500))
		pygame.display.flip()

		


	def drawClickCounter(self,screen):
		font = pygame.font.Font(None,36)
		text = font.render("Moves:" + str(self.clicks), 1, (10,10,10))
		textpos = text.get_rect()
		textpos.centerx = 220
		textpos.centery = 50
		screen.blit(text, textpos)

	def drawLifeBox(self,screen):
		font = pygame.font.Font(None,36)
		text = font.render("Lives:" + str(self.level[5][0].lives) , 1, (10,10,10))
		textpos = text.get_rect()
		textpos.centerx = 100
		textpos.centery = 50
		screen.blit(text, textpos)

	def drawLevelWon(self,screen):
		font = pygame.font.Font(None,36)
		text = font.render("Level Complete", 1, (10,10,10))
		textpos = text.get_rect()
		textpos.centerx = screen.get_rect().centerx
		textpos.centery = screen.get_rect().centery
		screen.blit(text, textpos)

	def drawGameOver(self,screen):
		#self.redrawAll()
		font = pygame.font.Font(None, 36)
		text = font.render("Game Over", 1, (10,10,10))
		textpos = text.get_rect()
		textpos.centerx = screen.get_rect().centerx
		textpos.centery = screen.get_rect().centery
		
		screen.blit(text, textpos)
		pygame.display.flip()

	def initIcicles(self):
		Icicles.Ice.add(Icicles(icicle_image, randint(200,1100), 50))

	def initFallingSnow(self):
			#time.sleep(10)
			FallingSnow.Snowy.add(FallingSnow(snow1,randint(0,1000),0))

	def initClouds(self, level):
		for x in level[4]:
			cloud.Clouds.add(x)

	def initPlayer(self, level):
		for x in level[5]:
			Player.penguin.add(x)



		#cloud.Clouds.add(cloud(cloud_image, HALF_WIDTH , 50, "right", 100, WIN_WIDTH))
	

	def initEnemies(self, level):
		#if level[3] != "None":
			for x in level[3]:	
				enemey.Enemies.add(x)
		#enemey.Enemies.add(enemey(snowman, 800, 340, "right", 50, 125))
		#enemey.Enemies.add(enemey(snowman, 400,240, "right", 50, 125))
		#self.rect.x+= x_speed
		#enemey.update()

	
	def initGoal(self, level):
		#for x in range(100):
		for x in level[2]:
			terrain.Goal.add(x)

	def initSnow(self):
		self.snows = []
		print self.snows
		for x in self.snows:
			terrain.All_Terrain.add(x)

	def initFloor(self, level):
		#self.image = pygame.image.load('floor_large.png')
		#small_floors = [terrain(small_floor, 1000, 237), terrain(small_floor, 900,300), terrain(small_floor, 500, 500)]
		#large_floors = [terrain(large_floor,30,150), terrain(large_floor,300,300), terrain(large_floor, 700, 400)]
		for x in level[1]:
			terrain.All_Terrain.add(x)
		for y in level[0]:
			terrain.All_Terrain.add(y)



#		floor = pygame.sprite.Sprite(self.floors)
#		ice = pygame.image.load('floor_large.png')
#		floor.image = ice
#		floor.rect = pygame.rect.Rect((200,500), floor.image.get_size())
#		self.sprites.add(self.floors)

	def main(self,screen):
		global cameraX, cameraY
		self.MenuScreen = True
		self.HelpScreen_1 = False
		self.HelpScreen_2 = False
		self.HelpScreen_3 = False
		self.HelpScreen_4 = False
		#self.HelpScreen_2 = False

		self.Level_1 = True
		self.Level_2 = False
		self.Level_3 = False
		self.Level_4 = False
		self.Level_5 = False

		self.Level_6 = False
		self.Level_7 = False
		self.Level_8 = False
		self.Level_9 = False
		self.Level_10 = False
		self.End_game = False

		self.repeat = False

		#self.lives = 10



		self.world_shift_x = 0
		self.left_viewbox = WIN_WIDTH/2 - WIN_WIDTH/8
		self.right_viewbox = WIN_WIDTH/2 + WIN_WIDTH/10
		self.objects = pygame.sprite.Group()
		self.GameOver = False
		self.clicks = 10
		self.clock = pygame.time.Clock()
		self.background = pygame.image.load('snow.png')
		pygame.display.set_caption("Penguin")
		#self.tile = pygame.image.load('tile.png')
		#self.sprites = pygame.sprite.Group()

		#self.camera = Camera(complex_camera, HALF_WIDTH, HALF_HEIGHT)
		#self.player = Player(self.objects)


		#self.cloud = cloud(self.objects)
		#self.x = self.cloud.rect.x
		#self.camera = Camera(screen, self.player.rect,WIN_WIDTH, WIN_HEIGHT)
		#sprites = ScrolledGroup()
		#sprites.camera_x = 0
		#self.floors = pygame.sprite.Group()
		#self.FallingSnow()

		#self.initIcicles()
		#self.initFallingSnow()
		#self.initEnemies()
		#self.initClouds()
		#self.initSnow()
		#self.initFloor()
		#self.initGoal()


		self.run()
		######### creating level 1
	#def get
	def click_sound(self):
		#file = snow_effect.wav
		sound = pygame.mixer.Sound('click.wav')
		#pygame.mixer.music.load(file)
		#pygame.mixer.music.play()
		pygame.mixer.Sound.play(sound)



	def run(self):
		#self.player = Player(self.objects)
		self.initLevel(Level_1)
		#if not self.Level_1:
		#	self.initLevel(Level_2)
		#else:
		#	self.initLevel(Level_1)



		while True:
			self.dt = self.clock.tick(60)
			print self.MenuScreen
			if not self.MenuScreen:
				if not self.HelpScreen_1:
					if not self.HelpScreen_2:
						if not self.HelpScreen_3:
							if not self.HelpScreen_4:
								if not self.End_game:
									if self.level[5][0].alive:
										for event in pygame.event.get():
											if self.level[5][0].Reached_Goal == True:
												if not self.Level_10:
													if not self.Level_9:
														if not self.Level_8:
															if not self.Level_7:
																if not self.Level_6:
																	if not self.Level_5:
																		if not self.Level_4:
																			if not self.Level_3:
																				if not self.Level_2:
																					if (event.type == pygame.KEYDOWN) and event.key == pygame.K_n:
																						self.clearLevel(Level_1)
																						self.initLevel(Level_2)
																						self.Level_1 = False
																						self.Level_2 = True
																						self.level[5][0].Reached_Goal = False
																				else:
																					if (event.type == pygame.KEYDOWN) and event.key == pygame.K_n:
																						self.clearLevel(Level_2)
																						self.initLevel(Level_3)
																						self.Level_2 = False
																						self.Level_3 = True
																						self.level[5][0].Reached_Goal = False
																			else:
																				if (event.type == pygame.KEYDOWN) and event.key == pygame.K_n:
																					self.clearLevel(Level_3)
																					self.initLevel(Level_4)
																					self.Level_3 = False
																					self.Level_4 = True
																					self.level[5][0].Reached_Goal = False
																		else:
																			if (event.type == pygame.KEYDOWN) and event.key == pygame.K_n:
																				self.clearLevel(Level_4)
																				self.initLevel(Level_5)
																				self.Level_4 = False
																				self.Level_5 = True
																				self.level[5][0].Reached_Goal = False
																	else:
																		if (event.type == pygame.KEYDOWN) and event.key == pygame.K_n:
																			self.clearLevel(Level_5)
																			self.initLevel(Level_6)
																			self.Level_5 = False
																			self.Level_6 = True
																			self.level[5][0].Reached_Goal = False
																else:
																	if (event.type == pygame.KEYDOWN) and event.key == pygame.K_n:
																		self.clearLevel(Level_6)
																		self.initLevel(Level_7)
																		self.Level_6 = False
																		self.Level_7 = True
																		self.level[5][0].Reached_Goal = False
															else:
																if (event.type == pygame.KEYDOWN) and event.key == pygame.K_n:
																	self.clearLevel(Level_7)
																	self.initLevel(Level_8)
																	self.Level_7 = False
																	self.Level_8 = True
																	self.level[5][0].Reached_Goal = False
														else:
															if (event.type == pygame.KEYDOWN) and event.key == pygame.K_n:
																self.clearLevel(Level_8)
																self.initLevel(Level_9)
																self.Level_8 = False
																self.Level_9 = True
																self.level[5][0].Reached_Goal = False

													else:
														if (event.type == pygame.KEYDOWN) and event.key == pygame.K_n:		
															self.clearLevel(Level_9)
															self.initLevel(Level_10)
															self.Level_9 = False
															self.Level_10 = True
															self.level[5][0].Reached_Goal = False
												else:
													if (event.type == pygame.KEYDOWN) and event.key == pygame.K_n:
														pygame.mixer.quit()
														self.clearLevel(Level_10)
														self.drawEndGame(screen)
														self.Level_10 = False
														self.End_game = True
														self.level[5][0].Reached_Goal = False
											

											if (event.type == pygame.KEYDOWN) and event.key == pygame.K_q:
												self.main(screen)
												#break

											if event.type == pygame.QUIT:
												return
											if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
												return
											if event.type == pygame.MOUSEMOTION:
												self.x, self.y = event.pos
												print (self.x,self.y)
											if self.clicks > 0:
												if event.type ==pygame.MOUSEBUTTONDOWN and event.button == 1:
												#self.snows.append(terrain(snow,self.x,self.y))
													self.click_sound()
													self.clicks -= 1
													terrain.All_Terrain.add(terrain(snow,self.x,self.y))

									#if not self.MenuScreen:
										self.redrawAll()
									else:
										for event in pygame.event.get():
											if event.type == pygame.QUIT:
												return
											if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
												return
											if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
												self.main(screen)
										self.drawGameOver(screen)

							#	if self.dt % 10 == 0:
							#		self.initIcicles()
			
									if self.dt % 5 == 0:
								
										self.initFallingSnow()
								else:
									for event in pygame.event.get():
										if (event.type == pygame.KEYDOWN) and event.key == pygame.K_n:
													#self.clearLevel(Level_10)
													#self.drawMainScreen(screen)
													#self.Level_10 = False
											#pygame.mixer.quit()
											#screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
											
											#pygame.display.init()
											#pygame.movie.Movie('penguin_dance.mpg')
											#pygame.movie.Movie.set_display(screen)
											#pygame.movie.Movie.play()







											
											pygame.display.init()
											
											movie = pygame.movie.Movie('penguin_dance.mpg')
											screen1 = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
											#screen1 = pygame.display.set_mode(movie.get_size())
											movie_screen = pygame.Surface(movie.get_size()).convert()
											movie.set_display(screen1)
											movie.play()

											#playing = True
											#while playing:
											screen1.blit(movie_screen, (0,0))
											pygame.display.update()
											#pygame.display.update()
											#self.clock.tick(60)

											
											
											#self.movie = pygame.movie.Movie('penguin_dance.mpg')
											#self.resolution = self.movie.get_size()
											#self.movie_length = self.movie.get_length()
											#self.image_surface = pygame.Surface(self.resolution)
											#self.image_surface.fill([0,0,0])
											#self.movie.set_display(screen)
											#self.movie.play()
											#m.play()

											#pygame.display.init()
											#movie = pygame.movie.Movie('penguin_dance.mpg')
											#w,h = movie.get_size()
											#display = pygame.display.set_mode((w,h))
											#movie.set_display(display)
											#movie.play()

											#pygame.movie.init()
											#mygame.movie.Movie.load('penguin_dance.mpg')
											#pygame.movie.Movie.play(1)
											#pygame.movie.Movie('penguin_dance.mpg')
											#ygame.movie.Movie.play()
											#movie_screen = pygame.Surface(movie.get_size()).convert()
											#playing = True



	
											#while playing:
											#screen.blit(movie_screen, (0,0))
											#pygame.display.update()
											#self.clock.tick(60)
											#sys.exit(0)
											#self.End_game = False
											#self.MenuScreen = True
											#self.repeat = True
											#self.level[5][0].Reached_Goal = False

							else:
								for event in pygame.event.get():
									if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
										self.HelpScreen_4 = False
										self.HelpScreen_3 = False
										self.HelpScreen_2 = False
										self.HelpScreen_1 = False
										self.MenuScreen = True
									if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
										self.HelpScreen_4 = False
										self.HelpScreen_3 = True
								self.drawHelpScreen_4(screen)

						else:
							for event in pygame.event.get():
								if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
									self.HelpScreen_3 = False
									self.HelpScreen_2 = True
								if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
									self.HelpScreen_3 = False
									self.HelpScreen_4 = True
							self.drawHelpScreen_3(screen)

					else:
						for event in pygame.event.get():
							if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
								self.HelpScreen_2 = False
								self.HelpScreen_1 = True
							if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
								self.HelpScreen_2 = False
								self.HelpScreen_3 = True
						self.drawHelpScreen_2(screen)

							
				else:
					#self.drawHelpScreen_1(screen)
					for event in pygame.event.get():
						if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
							self.HelpScreen_1 = False
							self.MenuScreen = True
						if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
							self.HelpScreen_1 = False
							self.HelpScreen_2 = True

					self.drawHelpScreen_1(screen)
					

			else:
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
						self.MenuScreen = False
						#self.Level_1 = True
						#self.clearLevel(Level_1)
						#self.initLevel(Level_1)
						#if self.repeat == True:
						#	self.main(screen)
						#self.clearLevel(Level_1)
						#self.initLevel(Level_1)

					if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
						sys.exit(0)
					if event.type == pygame.QUIT:
						sys.exit(0)
					if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
						self.HelpScreen_1 = True
						self.MenuScreen = False
				self.drawMainScreen(screen)

				#self.redrawAll()
				#self.drawGameOver()
			#self.redrawAll()


			#self.run_viewbox()


			#self.camera.update(self.player)
				#enemey.update()
						#self.initSnow()
						#screen.blit(self.tile, (self.x,self.y))
						#pygame.display.flip()
			#print self.player.alive
			#if self.player.alive == False:
				#sys.exit(0)
			
			#Player.drawLivesCounter()


			#print Player.lives
			#self.redrawAll()
			#for e in self.objects:
			#	screen.blit(e.image, self.camera.apply(e))
			#if Player.alive == True:
			#print self.GameOver
			#if not self.GameOver:
			#	self.redrawAll()


	def initLevel(self, level):
		#self.objects.remove()
		#self.initIcicles()
		#self.initFallingSnow()
		self.level = level
		self.initClouds(level)
		self.initSnow()
		self.initEnemies(level)
		self.initFloor(level)
		self.initGoal(level)
		self.initPlayer(level)
		#self.player = Player(self.objects)

	def clearLevel(self,level):
		#self.objects.remove(terrain.All_Terrain)
		#self.objects.remove(terrain.Goal)
		#self.objects.remove(terrain.Snow)
		#self.objects.remove(FallingSnow.Snowy)
		#Icicles.Ice.remove(
		#cloud.Clouds.remove(cloud(cloud_image, HALF_WIDTH , 50, "right", 100, WIN_WIDTH))
		enemey.Enemies.remove(level[3])
		terrain.All_Terrain.empty()
		terrain.All_Terrain.remove(level[0])
		terrain.All_Terrain.remove(level[1])
		terrain.Goal.remove(level[2])
		cloud.Clouds.remove(level[4])
		Player.penguin.remove(level[5])
		#self.objects.remove(self.player)




	def drawLevel(self,level):
		#self.objects.add(terrain.All_Terrain)
		#self.objects.add(terrain.Goal)
		#terrain.Goal.draw(screen)
		#self.objects.add(terrain.Snow)
		#self.objects.add(FallingSnow.Snowy)
		

		FallingSnow.Snowy.draw(screen)
		terrain.All_Terrain.draw(screen)
		terrain.Goal.draw(screen)
		#self.objects.draw(screen)
		cloud.Clouds.draw(screen)
		enemey.Enemies.draw(screen)
		Icicles.Ice.draw(screen)
		#self.objects.draw(screen)
		Player.penguin.draw(screen)




# = [[small_floors], [large_floors], [goal], [enemies]]

	#def pickLevel(self):



	def redrawAll(self):

	#	if self.player.Reached_Goal:
	#		if not self.Level_2:
	#			self.drawLevelWon(screen)

				#self.player.Reached_Goal = False
				#for event in pygame.event.get():
					#if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
						#print "hi"
						#self.player.Reached_Goal = False
	#					self.Level_1 = False
	#					self.Level_2 = True	
	#					self.clearLevel(Level_1)
	#					self.initLevel(Level_2)		
		#	else:

	#	if not  self.Level_1:
	#		self.drawLevel(Level_2)
	#	else:
	#		self.drawLevel(Level_1)

		#self.initIcicles()
		#self.initFallingSnow()
		#self.initEnemies(level)
		#self.initClouds()
		#self.initSnow()
		#self.initFloor(level)
		#self.initGoal(level)
		if self.Level_3:
			if self.dt % 10 == 0:
				self.initIcicles()



		self.objects.update(self.dt / 1000., self, screen)
		#self.objects.add(terrain.All_Terrain)
		#self.objects.add(terrain.Goal)
		#self.objects.add(terrain.Snow)
		#self.objects.add(enemey.Enemies)
		#self.objects.add(FallingSnow.Snowy)

		#enemey.Enemies.draw(screen)

		#self.camera.update(self.player)
		
		#FallingSnow.Snowy.update(self.dt / 1000., self, screen)
		#if not self.MenuScreen:
		screen.blit(self.background, (0,0))
		self.drawLifeBox(screen)
		self.drawClickCounter(screen)
		Icicles.Ice.update(self.dt / 1000., self, screen)
		FallingSnow.Snowy.update(self.dt / 1000., self, screen)
		Player.penguin.update(self.dt / 1000., self, screen)
		#Icicles.Ice.draw(screen)
		#Camera.draw_sprites(screen, self.objects)
		#Camera.update()
		#self.camera.update(self.player)
		#self.objects.draw(screen)
		cloud.Clouds.update(self.dt / 1000., self, screen)
		#cloud.Clouds.draw(screen)
		enemey.Enemies.update(self.dt / 1000., self, screen)
		if self.Level_1:
			self.drawLevel(Level_1)
		if self.Level_2:
			self.drawLevel(Level_2)
		if self.Level_3:
			self.drawLevel(Level_3)
		if self.Level_4:
			self.drawLevel(Level_4)
		if self.Level_5:
			self.drawLevel(Level_5)
		if self.Level_6:
			self.drawLevel(Level_6)
		if self.Level_7:
			self.drawLevel(Level_7)
		if self.Level_8:
			self.drawLevel(Level_8)
		if self.Level_9:
			self.drawLevel(Level_9)
		if self.Level_10:
			self.drawLevel(Level_10)
		if self.End_game:
			self.drawEndGame(screen)


		if self.level[5][0].Reached_Goal:
			self.drawLevelWon(screen)

		#enemey.Enemies.draw(screen)
		#if self.player.Reached_Goal:
		#	if not self.Level_2:
		#		self.drawLevelWon(screen)
				#self.player.Reached_Goal = False
				#for event in pygame.event.get():
					#if event.type == pygame.KEYDOWN and event.key == pygame.K_n:
						#print "hi"
						#self.player.Reached_Goal = False
		#				self.Level_1 = False
		#				self.Level_2 = True	
		#				self.clearLevel(Level_1)
		#				self.initLevel(Level_2)		
		#	else:




			#self.initLevel(Level_2)
			#self.redrawAll()

		#terrain.All_Terrain.draw(screen)
		#terrain.Goal.draw(screen)
		#self.sprites.draw(screen)
		pygame.display.flip()


#	def drawLine(self):




if __name__ == '__main__':
	file = 'snow.mp3'
	pygame.init()
	pygame.mixer.init()
	pygame.mixer.music.load(file)
	pygame.mixer.music.play(-1)
	screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
	Game().main(screen)