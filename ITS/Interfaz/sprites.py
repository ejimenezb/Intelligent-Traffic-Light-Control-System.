import pygame as pg 
import random
from os import path 
from settings import *

class Sprite(pg.sprite.Sprite):
	def __init__(self,game):
		self.game = game
		self.layer = 0
		self.groups = self.game.all_sprites

		pg.sprite.Sprite.__init__(self,self.groups)

	def update(self):
		pass

class Button(pg.sprite.Sprite):
	def __init__(self,game,x,y,description, accion, manual,activo,semaforo):
		self.game = game
		self.layer = 0
		self.groups = self.game.all_sprites , self.game.all_Buttons
		self.x = x
		self.y = y
		self.accion = accion
		self.estado = "OFF"
		self.manualMode = 0
		self.manual = manual
		self.activo = activo
		self.semaforo = semaforo
		pg.sprite.Sprite.__init__(self,self.groups)

		#self.image = pg.Surface((30,30))#None
		#self.image.fill(GREEN)

		#self.rect = self.image.get_rect() #None
		#self.rect.center=(x,y)


		self.image = pg.image.load("Red_Button1.png")
		self.image.set_colorkey(BLACK)

		self.imgBig = pg.transform.scale(self.image, (50, 50))#, DestSurface=None)
		self.imgSmall = pg.transform.scale(self.image, (30, 30))
		#self.ventana.blit(imagen,(551,548))
		self.image = self.imgBig

		if self.activo == 0:
			self.image = pg.Surface((30,30))#None
			self.image.fill(BLACK)

		self.rect = self.image.get_rect() #None
		self.rect.center=(x,y)
		self.description = description


		#pantalla = pg.display.set_mode((340, 280))
		#ventana.blit(imagen),(551,548))# (100, 100))
		#pg.display.update()



	def update(self):
		pass
	def setActivo(self):
		self.activo=1
	def setDesactivo(self):
		self.activo=0
	def setEstadoApagado(self):
		self.estado="OFF"

	def Onclick(self):
		#color = random.choice([BLUE, GREEN, RED, WHITE])
		#self.image.fill(color)
		#pass
		if self.activo == 1 or self.manual == 1:
			if self.estado == "OFF":
				self.estado = "ON"

				if self.manual == 1:
					self.manualMode = 1

			else:
				self.estado = "OFF"

				if self.manual == 1:
					self.manualMode = 0


			self.image = self.imgSmall#pg.transform.scale(self.image, (20, 20))  # , DestSurface=None)
			self.rect = self.image.get_rect()  # None
			self.rect.center = (self.x, self.y)
			self.accion()
	def checkClick(self, mouse_pos):
		if self.rect.collidepoint(mouse_pos):
			self.Onclick()

	def Onpull(self):
		if self.activo == 1 or self.manual == 1:
			self.image = self.imgBig #pg.transform.scale(self.image, (35, 35))  # , DestSurface=None)
			self.rect = self.image.get_rect()  # None
			self.rect.center = (self.x, self.y)
		else:
			self.image = pg.Surface((30, 30))  # None
			self.image.fill(BLACK)

class LED(pg.sprite.Sprite):
	def __init__(self, game, x, y, color, description):
		self.game = game
		self.layer = 0
		self.groups = self.game.all_sprites, self.game.all_LEDS
		self.x = x
		self.y = y
		self.color = color
		self.description = description
		self.estado = 0

		pg.sprite.Sprite.__init__(self, self.groups)

		#Luces brillantes
		self.image = pg.image.load("Luz_verde_b.jpg")
		self.image.set_colorkey(BLACK)
		self.imgGreen = pg.transform.scale(self.image, (50, 50))  # , DestSurface=None)

		self.image = pg.image.load("Luz_roja_b.jpg")
		self.image.set_colorkey(BLACK)
		self.imgRed = pg.transform.scale(self.image, (50, 50))  # , DestSurface=None)

		self.image = pg.image.load("Luz_amarilla_b.jpg")
		self.image.set_colorkey(BLACK)
		self.imgYellow = pg.transform.scale(self.image, (50, 50))  # , DestSurface=None)

		#Luces opacas
		self.image = pg.image.load("Luz_verde_opaca.png")
		self.image.set_colorkey(BLACK)
		self.imgGreenO = pg.transform.scale(self.image, (50, 50))  # , DestSurface=None)

		self.image = pg.image.load("Luz_roja_opaca.png")
		self.image.set_colorkey(BLACK)
		self.imgRedO = pg.transform.scale(self.image, (50, 50))  # , DestSurface=None)

		self.image = pg.image.load("Luz_amarilla_opaca.png")
		self.image.set_colorkey(BLACK)
		self.imgYellowO = pg.transform.scale(self.image, (50, 50))  # , DestSurface=None)


		if self.color == "green":
			self.image = self.imgGreenO
			#self.image.fill((0, 0, 255,127))
			#self.imgGreenOff = self.image
		else:
			if self.color == "red":
				self.image = self.imgRedO
				#self.image.fill((0, 0, 255))
			else:
				if self.color == "yellow":
					self.image = self.imgYellowO
					#self.image.fill((0, 0, 255))

		self.rect = self.image.get_rect()  # None
		self.rect.center = (x, y)

	def OnLED(self):
		#if self.estado == 0:
		self.estado = 1
		if self.color == "green":
			self.image = self.imgGreen
		else:
			if self.color == "red":
				self.image = self.imgRed
			else:
				if self.color == "yellow":
					self.image = self.imgYellow

				#self.ledOn = self.imgGreen
				#self.image = self.ledOn

		self.rect = self.image.get_rect()  # None
		self.rect.center = (self.x, self.y)

	def OffLED(self):
		self.estado = 0
		if self.color == "green":
			self.image = self.imgGreenO
		else:
			if self.color == "red":
				self.image = self.imgRedO
			else:
				if self.color == "yellow":
					self.image = self.imgYellowO

		# self.ledOn = self.imgGreen
		# self.image = self.ledOn

		self.rect = self.image.get_rect()  # None
		self.rect.center = (self.x, self.y)

	def Color(self):

		if self.color == "red":
			self.image = self.imgRed
		else:
			if self.color == "green":
				self.image = self.imgGreen
			else:
				if self.color == "yellow":
					self.image = self.imgYellow

class Vehicle(pg.sprite.Sprite):
	def __init__(self, game, x, y, type, description, num):
		self.game = game
		self.layer = 0
		self.groups = self.game.all_sprites, self.game.all_Veh
		self.x = x
		self.y = y
		#self.color = color
		self.description = description
		self.type = type
		self.num = str(num)
		#self.estado = "off"

		pg.sprite.Sprite.__init__(self, self.groups)

		self.image = pg.image.load("carro_b.jpg")
		self.image.set_colorkey(BLACK)
		self.imgCar = pg.transform.scale(self.image, (70, 25))  # , DestSurface=None)

		self.image = pg.image.load("Camioneta.jpg")
		self.image.set_colorkey(BLACK)
		self.imageTruck = pg.transform.scale(self.image, (90, 50))  # , DestSurface=None)

		if self.type == "car":
			self.image = self.imgCar
		else:
			if self.type == "truck":
				self.image = self.imageTruck

		self.rect = self.image.get_rect()  # None
		self.rect.center = (x, y)
"""
class Truck(pg.sprite.Sprite):
	def __init__(self, game, x, y, description):
		self.game = game
		self.layer = 0
		self.groups = self.game.all_sprites#, self.game.all_LEDS
		self.x = x
		self.y = y
		#self.color = color
		self.description = description
		#self.estado = "off"

		pg.sprite.Sprite.__init__(self, self.groups)

		self.image = pg.image.load("Camioneta.jpg")
		self.image.set_colorkey(BLACK)
		self.image = pg.transform.scale(self.image, (90, 50))  # , DestSurface=None)

		self.rect = self.image.get_rect()  # None
		self.rect.center = (x, y)
"""