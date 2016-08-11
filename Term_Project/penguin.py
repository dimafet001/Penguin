#!/usr/bin/python

import pygame
from pygame import *
import sys
import time
from random import *

#########################################################################################
#########################################################################################
##############                          #################################################
##############  15 - 112 Term Project   #################################################
##############  Summer Session 1, 2014  #################################################
##############        Snow Land         #################################################
##############     By: Vincent Liu      #################################################
##############   andrew id: vincentl    #################################################
##############                          #################################################
#########################################################################################
#########################################################################################



#Color reference
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





#Screen Dimension Reference
WIN_WIDTH = 1100
WIN_HEIGHT = 600
HALF_WIDTH = int(WIN_WIDTH / 2)
HALF_HEIGHT = int(WIN_HEIGHT / 2)



#creating a sprite class for the player in the game
class Player(pygame.sprite.Sprite):
    #creating a sprite group that the player will be put in   
	penguin = pygame.sprite.Group()
	def __init__(self,x, y):
		#flags and initial values stored here to describe player
		pygame.sprite.Sprite.__init__(self)
		self.x = x         
		self.y = y
		self.image = pygame.image.load('penguin.png')   #load image for the player sprite
		self.rect = pygame.rect.Rect((self.x,self.y), self.image.get_size())  #obtain a rectangle around it
		self.resting = False  
		self.dy = 0
		self.lives = 10        #initializing lives
 		self.alive = True
		self.Reached_Goal = False    

	#update the movement and motions of the sprite
	def update(self, dt, game, screen):
		#calling multiple functions here to check the state of the player
		self.checkGoal()

		#if the player reaches the goal, he can't die anymore
		if not self.Reached_Goal:
			self.isAlive()
			self.enemeyCollision()
			self.icicleCollision()

		self.gameOver()
		last = self.rect.copy()
		key = pygame.key.get_pressed()
		#key motions for player movement

		#up direction for testing only
		#if key[pygame.K_UP]:
		#	self.rect.y -= 500 * dt
		if key[pygame.K_LEFT]:
			self.rect.x -= 300 * dt
		if key[pygame.K_RIGHT]:
			self.rect.x += 300 * dt
		if key[pygame.K_DOWN]:
		 	self.rect.y += 300 * dt
		if self.resting and key[pygame.K_SPACE]:
			self.dy = -350
			self.resting = False

		#gravity initialized here
		self.dy = min(400, self.dy + 40)
		self.rect.y += self.dy * dt

		#check for terrain collision
		#don't go through terrain, undo move if collided
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

 	#drawing the life counter
 	def drawLivesCounter(self):
 		font = pygame.font.Font(None, 36)
 		text = font.render(str(self.lives), 1, (10,10,10))
 		textpos = text.get_rect()
 		textpos.centerx = 100
 		textpos.centery = 100
 		screen.blit(text,textpos)


 	#check for if the player reached the goal, creates a sound
 	def checkGoal(self):
 		if pygame.sprite.spritecollide(self, terrain.Goal, False):
 			self.goalSound()
 			self.Reached_Goal = True


 	#sound used for collisions
 	def snowSound(self):
		sound = pygame.mixer.Sound('snow_effect.wav')
		pygame.mixer.Sound.play(sound)

	#soound used for reaching the goal
	def goalSound(self):
		sound = pygame.mixer.Sound('goal.wav')
		pygame.mixer.Sound.play(sound)

	#decrement life count by one and create sound when collide with enemey
 	def enemeyCollision(self):
 		if pygame.sprite.spritecollide(self, enemey.Enemies, False):
 			self.snowSound()
 			self.lives -= 1
 			self.rect = pygame.rect.Rect((self.x,self.y), self.image.get_size())


 	#same thing as enemeyCollision except do it for falling icicles
 	def icicleCollision(self):
 		if pygame.sprite.spritecollide(self, Icicles.Ice,False):
 			self.snowSound()
 			self.lives -= 1
 			self.rect = pygame.rect.Rect((self.x,self.y), self.image.get_size())


 	#function used to check for if the player is alive by checking if position is out of the bounds of the screen
 	def isAlive(self):
		if self.rect.left < 0 or self.rect.right > WIN_WIDTH or self.rect.top < 0 or self.rect.bottom >WIN_HEIGHT:
			self.snowSound()
			self.lives -= 1
			self.rect = pygame.rect.Rect((self.x,self.y), self.image.get_size())

	#checks for if the game is over when lives reach 0
	def gameOver(self):
		if self.lives <= 0:
			self.alive = False


#creating a terrain class which is a sprite
class terrain(pygame.sprite.Sprite):
	#creating various sprite groups which will contain the current sprites
	All_Terrain = pygame.sprite.Group()
	Goal = pygame.sprite.Group()
	Snow = pygame.sprite.Group()

	#initial parameters taking in the sprite image and x,y coordinates when creates
	def __init__(self, image, x, y):
			pygame.sprite.Sprite.__init__(self)
			self.image = image
			self.rect = pygame.rect.Rect((x,y), self.image.get_size())

#now creating an enemey classs just like terrain class
class enemey(pygame.sprite.Sprite):
	Enemies = pygame.sprite.Group()

	#enemey will have additional parameters of direction, dx "speed", and platform_width
	def __init__(self, image, x, y, direction, dx, platform_width):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.direction = direction
		self.dx = dx
		self.platform_width = platform_width
		self.rect = pygame.rect.Rect((x,y), self.image.get_size())
		self.last = self.rect.copy()

	#updates the movement of the enemey, uses platform_width to check how far to move
	def update(self, dt, game, screen):
		if self.direction == "right":
			self.rect.x += self.dx * dt
			if self.rect.x >= self.last.x + self.platform_width /2:
				self.direction = "left"
		if self.direction == "left":
			self.rect.x -= self.dx * dt
			if self.rect.x <= self.last.x - self.platform_width / 2:
				self.direction = "right" 
		


		

#class created for falling snow
class FallingSnow(pygame.sprite.Sprite):
	Snowy = pygame.sprite.Group()

	#same parameters as floor
	def __init__(self, image, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = pygame.rect.Rect((x,y), self.image.get_size())
		self.rect.y = y

	#method used to update position of falling snow
	def update(self, dt, game, screen):
		#snow just always fall down
		self.rect.y += 100 * dt



#sprite class for cloud that is similar to enemey
class cloud(pygame.sprite.Sprite):
	Clouds = pygame.sprite.Group()

	#moves just like enemey but takes in screen_width not platform_width
	def __init__(self, image, x, y, direction, dx, screen_width):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.direction = direction
		self.dx = dx
		self.screen_width = screen_width
		self.rect = pygame.rect.Rect((x,y), self.image.get_size())
		self.last = self.rect.copy()

	#update method for cloud movement, player cannot collide with cloud
	def update(self, dt, game, screen):
		if self.direction == "right":
			self.rect.x += self.dx * dt
			if self.rect.x >= self.last.x + self.screen_width / 2.5:
				self.direction = "left"
		if self.direction == "left":
			self.rect.x -= self.dx * dt
			if self.rect.x <= self.last.x - self.screen_width / 2.5:
				self.direction = "right" 



#icicles class that can collide with player
class Icicles(pygame.sprite.Sprite):
	Ice = pygame.sprite.Group()
	def __init__(self, image, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.image = image
		self.rect = pygame.rect.Rect((x,y), self.image.get_size())

	#icicles fall down like the falling snow
	def update(self, dt, game, screen):
		self.rect.y += 90 * dt



##################  LOADING ALL THE IMAGES #############################
################## USED THROUGHOUT CODE    #############################


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

background_2 = pygame.image.load('Background_2.jpg')
background_3 = pygame.image.load('Background_3.png')
background_4 = pygame.image.load('Background_4.jpg')
main_title = pygame.image.load('main_title.png')
levels = pygame.image.load('levels.png')
levels_text = pygame.image.load('Levels_Text.png')

text_bubble1 = pygame.image.load('text_bubble1.png')
text_bubble2 = pygame.image.load('text_bubble2.png')
text_bubble3 = pygame.image.load('text_bubble3.png')
text_instructions = pygame.image.load('Instruction_Text.png')
text_bubble4 = pygame.image.load('text_bubble4.png')
care_text = pygame.image.load('care_text.png')

left_arrow = pygame.image.load('left_arrow.png')
right_arrow = pygame.image.load('right_arrow.png')
escape_button = pygame.image.load('escape_button.png')
end = pygame.image.load('end.png')


########################################################################
########################################################################





############################# CREATING ALL THE LEVELS HERE IN FORMS OF LISTS ###############################

#####LIST EXAMPLE: LEVEL  = [[small_floors], [large_floors], [goal], [enemies], [cloud], [player]]

Level_1 = [[terrain(small_floor, 550,350), terrain(small_floor, 350, 300), terrain(small_floor, 600, 200)], [terrain(large_floor, 30, 300), terrain(large_floor, 900, 300)], [terrain(goal, 950, 215)], [enemey(snowman, 1700, 300, "right", 50, 125)], [cloud(cloud_image, 2000, 20, "right", 10, 10)], [Player(30,200)]]
Level_2 = [[terrain(small_floor, 1000, 237), terrain(small_floor, 900,300), terrain(small_floor, 500, 500)],[terrain(large_floor,30,250), terrain(large_floor,300,300), terrain(large_floor, 700, 400)],[terrain(goal,1000,150)],[  enemey(snowman, 800, 340, "right", 50, 125),enemey(snowman, 400,240, "right", 50, 125) ], [cloud(cloud_image, HALF_WIDTH , 50, "right", 100, WIN_WIDTH)], [Player(100,150)]  ]
Level_3 = [[terrain(small_floor, 500, 500)], [terrain(large_floor, 30, 150), terrain(large_floor, 800, 300)], [terrain(goal, 900, 215)], [enemey(snowman, 1500,240, "right", 50, 125)] , [cloud(cloud_image, HALF_WIDTH , 50, "right", 100, WIN_WIDTH)], [Player(30,30)]]

Level_4 = [[terrain(small_floor, 525 , 500)],[terrain(large_floor,475,200)],[terrain(goal,525,420)],[  enemey(snowman, 1700, 340, "right", 50, 125)], [cloud(cloud_image, HALF_WIDTH , 50, "right", 100, WIN_WIDTH), cloud(cloud_image, HALF_WIDTH + 200, 150, "right", 100, WIN_WIDTH)], [Player(550,100)] ]


Level_5 = [[terrain(small_floor, 200, 500), terrain(small_floor, 775,425), terrain(small_floor, 950, 500)],[terrain(large_floor,0,250), terrain(large_floor,240,225), terrain(large_floor, 480 , 200), terrain(large_floor,720,180)],[terrain(goal,200,415)],[  enemey(snowman, 2000, 340, "right", 50, 125)], [cloud(cloud_image, HALF_WIDTH , 50, "right", 100, WIN_WIDTH), cloud(cloud_image, HALF_WIDTH + 50 , 50, "left", 100, WIN_WIDTH)], [Player(30,30)] ]

Level_6 = [[terrain(small_floor, 50, 450), terrain(small_floor, 150,450), terrain(small_floor, 300, 450), terrain(small_floor,500, 450)],[terrain(large_floor,800,450)],[terrain(goal,900,365)],[  enemey(snowman, 1700, 340, "right", 50, 125)], [cloud(cloud_image, HALF_WIDTH , 50, "right", 100, WIN_WIDTH)], [Player(50,350)] ]
Level_7 = [[terrain(small_floor, 500, 300)], [terrain(large_floor, 30, 500), terrain(large_floor, 100, 200), terrain(large_floor,600, 400 ), terrain(large_floor, 800, 125)], [terrain(goal, 850, 40)], [enemey(snowman, 200, 145, "right", 50, 125), enemey(snowman,650, 345, "left", 50, 125)], [cloud(cloud_image,  HALF_WIDTH, 50, "left", 100, WIN_WIDTH)], [Player(50,400)]]

Level_8 = [[terrain(small_floor, 500, 500)],[terrain(large_floor,400,150)],[terrain(goal,500,70)],[  enemey(snowman, 1700, 340, "right", 50, 125)], [cloud(cloud_image, HALF_WIDTH , 50, "right", 100, WIN_WIDTH)], [Player(500, 425)] ] 



Level_9 = [[terrain(small_floor, 125,500)], [terrain(large_floor, 30, 245), terrain(large_floor, 350, 100), terrain(large_floor, 350, 350), terrain(large_floor, 700,245), terrain(large_floor,350, 530)], [terrain(goal, 400, 445)], [enemey(snowman, 470, 293, "right", 50, 125),enemey(snowman, 130, 190 , "left", 50,125), enemey(snowman,430,477, "right", 50,125), enemey(snowman,755, 190, "left", 50,125)], [cloud(cloud_image, HALF_WIDTH, 20, "right", 100, WIN_WIDTH)], [Player(400,5)]]





Level_10 = [[terrain(small_floor, 20,550), terrain(small_floor, 100, 100), terrain(small_floor, 250, 450), terrain(small_floor, 600, 200), terrain(small_floor, 800, 400), terrain(small_floor, 850, 150)], [terrain(large_floor, 30, 250), terrain(large_floor, 900, 525), terrain(large_floor, 450, 400)], [terrain(goal, 850, 70)], [enemey(snowman, 115 , 197, "right", 50, 175), enemey(snowman, 530, 345, "left", 50, 125), enemey(snowman, 960, 475, "left", 50, 125)], [cloud(cloud_image, HALF_WIDTH, 20, "right", 100, WIN_WIDTH), cloud(cloud_image, HALF_WIDTH - 80, 10, "left", 100, WIN_WIDTH), cloud(cloud_image, HALF_WIDTH + 50, 40, "left", 100, WIN_WIDTH)], [Player(20,475)]]


###############################################################################################################





#class created for game
class Game(object):

###############################################################
############### METHODS USE TO DRAW STATES OF GAME ############	
###############################################################


	def drawEndGame(self,screen):
		screen.blit(background_3, (0,0))
		screen.blit(end, (HALF_WIDTH - 550, HALF_HEIGHT - 200))
		pygame.display.flip()

	def drawLevelsMap(self,screen):
		screen.blit(levels, (0,0))
		screen.blit(levels_text, (HALF_WIDTH - 265 , HALF_HEIGHT - 275))
		screen.blit(care_text, (HALF_WIDTH / 2, HALF_HEIGHT + 225))
		pygame.display.flip()

	def drawMainScreen(self,screen):

		screen.blit(background_2, (0,0))
		screen.blit(text_2, (HALF_WIDTH / 2.3, HALF_HEIGHT / 0.75))
		screen.blit(main_title, (HALF_WIDTH / 1.7, HALF_HEIGHT / 4))

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
		screen.blit(main_penguin, (265,245))
		screen.blit(snowman, (875, 268))
		screen.blit(icicle_image, ( 820, 235))
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

		

	#This will be used to display the move counter on the screen, always changing
	def drawClickCounter(self,screen):
		font = pygame.font.Font(None,36)
		text = font.render("Moves:" + str(self.clicks), 1, (10,10,10))
		textpos = text.get_rect()
		textpos.centerx = 220
		textpos.centery = 50
		screen.blit(text, textpos)

	#This will be used to display the lives counter on the screen, always changing
	def drawLifeBox(self,screen):
		font = pygame.font.Font(None,36)
		text = font.render("Lives:" + str(self.level[5][0].lives) , 1, (10,10,10))
		textpos = text.get_rect()
		textpos.centerx = 100
		textpos.centery = 50
		screen.blit(text, textpos)

	#This displays a message if you reach the end of the level and collide with the goal
	def drawLevelWon(self,screen):
		font = pygame.font.Font(None,36)
		text = font.render("Level Complete, Press n to continue", 1, (10,10,10))
		textpos = text.get_rect()
		textpos.centerx = screen.get_rect().centerx
		textpos.centery = screen.get_rect().centery
		screen.blit(text, textpos)

	#method called when all lives are lost
	def drawGameOver(self,screen):
		font = pygame.font.Font(None, 36)
		text = font.render("Game Over", 1, (10,10,10))
		text1 = font.render("Press Escape to quit", 1, (10,10,10))
		textpos = text.get_rect()
		textpos.centerx = screen.get_rect().centerx
		textpos.centery = screen.get_rect().centery
		screen.blit(text1, (WIN_WIDTH / 2 - 125, WIN_HEIGHT / 2 + 50 ))
		screen.blit(text, textpos)
		pygame.display.flip()

	#sound for when a click is made
	def click_sound(self):
		#loading sound file
		sound = pygame.mixer.Sound('click.wav')
		#using the mixer feature in pygame
		pygame.mixer.Sound.play(sound)


#################   ALL THESE METHODS BELOW USE TO INITIALIZE THE OBJECTS AND SPRITES IN GAME ###################

	#randomized placement of icicles and falling snow on map
	def initIcicles(self):
		Icicles.Ice.add(Icicles(icicle_image, randint(200,1100), 50))

	def initFallingSnow(self):
			FallingSnow.Snowy.add(FallingSnow(snow1,randint(0,1000),0))

	#adding the instances from the level into the sprite group
	def initClouds(self, level):
		for x in level[4]:
			cloud.Clouds.add(x)

	#same as initClouds except for index 5 of the list
	def initPlayer(self, level):
		for x in level[5]:
			Player.penguin.add(x)
	
	#same as above
	def initEnemies(self, level):
			for x in level[3]:	
				enemey.Enemies.add(x)


	#same as above
	def initGoal(self, level):
		for x in level[2]:
			terrain.Goal.add(x)

	def initSnow(self):
		self.snows = []
		#print self.snows
		for x in self.snows:
			terrain.All_Terrain.add(x)

	def initFloor(self, level):
		for x in level[1]:
			terrain.All_Terrain.add(x)
		for y in level[0]:
			terrain.All_Terrain.add(y)



	#main method defined here
	def main(self,screen):
		#setting up many flags to indicate the state of the game
		self.MenuScreen = True

		self.HelpScreen_1 = False
		self.HelpScreen_2 = False
		self.HelpScreen_3 = False
		self.HelpScreen_4 = False

		self.LevelsMap = False

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


		#other displays and flags initialized here also
		self.objects = pygame.sprite.Group()
		self.GameOver = False
		self.clock = pygame.time.Clock()
		self.background = pygame.image.load('snow.png')
		pygame.display.set_caption("Penguin")


		#call run method
		self.run()



	#run method called by main()
	def run(self):
		#initializing first level
		self.initLevel(Level_1)


		#while loop to actually run the game, always running once started
		while True:
			#initializing clock speed
			self.dt = self.clock.tick(100)
	#		print self.MenuScreen

############## IF STATEMENTS CHECKING THE STATE OF THE GAME ###############################

			if not self.MenuScreen:
				if not self.HelpScreen_1:
					if not self.HelpScreen_2:
						if not self.HelpScreen_3:
							if not self.HelpScreen_4:
								if not self.LevelsMap:
									if self.level[5][0].alive:

################## USER MOVEMENT ALLOWED HERE THROUGH KEYBOARD CLICKS #######################
##################          CHECKS WHICH LEVEL PLAYER IS ON           #######################

										for event in pygame.event.get():
											if self.level[5][0].Reached_Goal == True:
												if not self.End_game:
													if not self.Level_10:
														if not self.Level_9:
															if not self.Level_8:
																if not self.Level_7:
																	if not self.Level_6:
																		if not self.Level_5:
																			if not self.Level_4:
																				if not self.Level_3:
																					if not self.Level_2:

############################## STATEMENTS USED TO INDICATE INDIVIDUAL ACTIONS FOR EACH LEVEL #########################################
############################## ALSO SETS FLAGS TO APPROPRIATE STATE WHEN CERTAIN KEY PRESSED #########################################
############################## CLEARS OLD LEVEL AND GOES TO NEXT LEVEL WHEN REACHED GOAL     #########################################

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
															self.clearLevel(Level_10)
															self.drawEndGame(screen)
															self.Level_10 = False
															self.End_game = True
															self.level[5][0].Reached_Goal = False

########################### ONCE ON THE END SCREEN, CAN QUUIT BY HITTING ESCAPE OR Q ##########################
												else:
													if (event.type == pygame.KEYDOWN) and event.key == pygame.K_q:
														sys.exit(0)


											if event.type == pygame.QUIT:
												return

											# can quit at any point in time at any level
											if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
												return

											# KEEPS TRACK OF MOUSE MOVEMENT
											if event.type == pygame.MOUSEMOTION:
												self.x, self.y = event.pos
												#print (self.x,self.y)

											# IF MOUSE CLICKED, ADD TERRAIN AND DECREMENT MOVE COUNT
											if self.clicks > 0:
												if event.type ==pygame.MOUSEBUTTONDOWN and event.button == 1:

											#ALSO SET APPRORPIATE SOUND
													self.click_sound()
													self.clicks -= 1
													terrain.All_Terrain.add(terrain(snow,self.x,self.y))

										#ALWAYS UPDATING IN REDRAWALL FUNCTION
										self.redrawAll()

									#Actions allowed on the main screen
									else:
										for event in pygame.event.get():
											if event.type == pygame.QUIT:
												return
											if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
												return
											#if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
											#	Game().main(screen)
										self.drawGameOver(screen)


									#speed at which snow falls
									if self.dt % 5 == 0:
										self.initFallingSnow()

########### LEVEL OPTIONS, SETS APPROPRIATE AMOUNT OF CLICKS FOR EACH LEVEL ######################

								else:
									for event in pygame.event.get():
										if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
											self.clicks = 40
											self.LevelsMap = False
										if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
											self.clicks = 30
											self.LevelsMap = False
										if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
											self.clicks = 20
											self.LevelsMap = False
										if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
											self.LevelsMap = False
											self.MenuScreen = True

									#draws the screen for the level map
									self.drawLevelsMap(screen)

############ What to do on appropriate help screen options ####################
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

					for event in pygame.event.get():
						if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
							self.HelpScreen_1 = False
							self.MenuScreen = True
						if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
							self.HelpScreen_1 = False
							self.HelpScreen_2 = True

					self.drawHelpScreen_1(screen)
					
##### MENU SCREEN OPTIONS ###############
			else:
				for event in pygame.event.get():
					if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
						self.MenuScreen = False
						self.LevelsMap = True


					if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
						sys.exit(0)
					if event.type == pygame.QUIT:
						sys.exit(0)
					if event.type == pygame.KEYDOWN and event.key == pygame.K_h:
						self.HelpScreen_1 = True
						self.MenuScreen = False
				self.drawMainScreen(screen)



	#initialiizing level, this creates the instances by getting them from level parameter
	def initLevel(self, level):

		self.level = level
		self.initClouds(level)
		self.initSnow()
		self.initEnemies(level)
		self.initFloor(level)
		self.initGoal(level)
		self.initPlayer(level)

	#clear any level when called with level parameter
	def clearLevel(self,level):

		#removes sprites from the certain groups
		enemey.Enemies.remove(level[3])
		terrain.All_Terrain.empty()
		terrain.All_Terrain.remove(level[0])
		terrain.All_Terrain.remove(level[1])
		terrain.Goal.remove(level[2])
		cloud.Clouds.remove(level[4])
		Player.penguin.remove(level[5])




	#draws the level after initialized
	def drawLevel(self,level):

		

		FallingSnow.Snowy.draw(screen)
		terrain.All_Terrain.draw(screen)
		terrain.Goal.draw(screen)

		cloud.Clouds.draw(screen)
		enemey.Enemies.draw(screen)
		Icicles.Ice.draw(screen)

		Player.penguin.draw(screen)






	#redraw all function always being called and updated
	def redrawAll(self):

		#initializing icicles and speed for certain levels
		#if self.Level_4:
		#	if self.dt % 15 == 0:
		#		self.initIcicles()
		if self.Level_2:
			if self.dt % 11 == 0:
				self.initIcicles()
		if self.Level_5:
			if self.dt % 13 == 0:
				self.initIcicles()
		if self.Level_6:
			if self.dt % 11 == 0:
				self.initIcicles()
		#if self.Level_7:
		#	if self.dt % 10 == 0:
		#		self.initIcicles()
		#if self.Level_8:
		#	if self.dt % 10 == 0:
		#		self.initIcicles()
		if self.Level_10:
			if self.dt % 11 == 0:
				self.initIcicles()

		#updating the movement of the player on screen
		self.objects.update(self.dt / 1000., self, screen)

		#making the background appear
		screen.blit(self.background, (0,0))
 
		#creating the lifebox and clickcounter by calling their respective functions
		self.drawLifeBox(screen)
		self.drawClickCounter(screen)

		#updating the movement of the ice, snow, player, cloud, and enemey
		Icicles.Ice.update(self.dt / 1000., self, screen)
		FallingSnow.Snowy.update(self.dt / 1000., self, screen)
		Player.penguin.update(self.dt / 1000., self, screen)

		cloud.Clouds.update(self.dt / 1000., self, screen)

		enemey.Enemies.update(self.dt / 1000., self, screen)

###### THIS DRAWS THE APPROPRIATE LEVEL FOR THE CURRENT STATE OF THE GAME ######
######            USES THE PREVIOUSLY INITIALIZED FLAGS                   ######

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

		#draws level complete if goal is reached
		if self.level[5][0].Reached_Goal:
			self.drawLevelWon(screen)

		#NEED THIS TO MAKE FEATURES APPEAR ON SCREEN
		pygame.display.flip()




############### CODE TO START THE GAME AND INITIALIZE EVERYTHING #####################
if __name__ == '__main__':
	file = 'snow.mp3'
	pygame.init()
	pygame.mixer.init()
	pygame.mixer.music.load(file)
	pygame.mixer.music.play(-1)
	screen = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
	Game().main(screen)
