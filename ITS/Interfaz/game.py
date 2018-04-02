import pygame as pg
import random
from os import path
from sprites import * #import sprites
from settings import *
import time
tpause=0
taux=0
time_count1=0
time_count2=0
Semf_1 = []
Semf_2 = []
manual_Mode = 0
class Game():
	def __init__(self):
		pg.init()
		pg.mixer.init()
		self.ventana=pg.display.set_mode((ancho,largo))
		pg.display.set_caption(NAME)
		self.Clock=pg.time.Clock()
		self.running=True


	def new(self, num_s1, num_s2):
		#inicia un nuevo juego
		#global Semf_1, Semf_2
		#global manual_Mode
		self.playing=True
		self.all_sprites=pg.sprite.Group()
		self.all_Buttons=pg.sprite.Group()
		self.all_LEDS = pg.sprite.Group()
		self.all_Veh = pg.sprite.Group()

		self.inf_font = pg.font.Font(pg.font.match_font("times new roman"), 20)
		self.message_font = pg.font.Font(pg.font.match_font("times new roman"), 25)
		self.subTitle_font = pg.font.Font(pg.font.match_font("times new roman"), 30)
		self.title_font = pg.font.Font(pg.font.match_font("times new roman"), 35)

		#Button(self, 200, 300, "PAPI", self.PRUEBA)
		Button(self, 800, 200, "Modo Manual", self.PRUEBA,1,1,0)
		#print(manual_Mode)
		#if manual_Mode == 1:
		Button(self, 700, 400, "Semaforo 1", self.PRUEBA,0,0,1)
		Button(self, 900, 400, "Semaforo 2", self.PRUEBA,0,0,2)

		n=0
		Semf_1.append(LED(self, 98, 180+n, "green", " "))#168
		Semf_1.append(LED(self, 148, 180+n, "yellow","Semaforo 1"))#218
		Semf_1.append(LED(self, 198, 180+n, "red", " "))#268

		Semf_2.append(LED(self, 286, 180+n, "green", " "))#286
		Semf_2.append(LED(self, 336, 180+n, "yellow", "Semaforo 2"))#336
		Semf_2.append(LED(self, 386, 180+n, "red", " "))#386

		Vehicle(self, 65, 400+n, "car", "Carro",num_s1[0])
		Vehicle(self, 160, 400+n, "truck","Camioneta", num_s1[1])

		Vehicle(self, 270, 400+n, "car", "Carro",num_s2[0])
		Vehicle(self, 375, 400+n, "truck","Camioneta", num_s2[1])

	def run(self,start_time):
		#game loop
		#global manual_Mode
		while self.playing:
			self.Clock.tick(FPS)
			self.events()
			#print(manual_Mode)
			#if manual_Mode ==1:
				#Button(self, 500, 400, "Semaforo 2", self.PRUEBA, 0)
			self.update()
			self.drawing(start_time)

	def events(self):
		#game loop events
		global manual_Mode
		for event in pg.event.get():
			if event.type== pg.QUIT:
				if self.playing==True:
					self.playing=False
				self.running=False

			if event.type == pg.MOUSEBUTTONDOWN:
				mouse_pos = pg.mouse.get_pos()
				#print("chequeo")
				for button in self.all_Buttons:
					button.checkClick(mouse_pos)
					if button.activo==1 and button.manual==1:
						manual_Mode = button.manualMode
					print("Manual mode: " + str(manual_Mode) + " activo: " + str(button.activo)+ " Boton de control: "+str(button.manual))

			print("Manual mode: "+str(manual_Mode))
			if manual_Mode == 1:
				for button in self.all_Buttons:
					button.setActivo()
					print("Manual mode: " + str(manual_Mode) + " activo: " + str(button.activo)+" Boton de control: "+str(button.manual))
					"""
					if button.manual == 0:
						if button.semaforo == 1:
							if button.estado == "OFF":
								#for led in Semf_1:
								#if led.semaforo == 1:
								Semf_1[0].OnLED
								Semf_1[1].OffLED
								Semf_1[2].OffLED
							else:
								Semf_1[2].OnLED
								Semf_1[1].OffLED
								Semf_1[2].OffLED
						else:
							if button.estado == "OFF":
								Semf_2[0].OnLED
								Semf_2[1].OffLED
								Semf_2[2].OffLED
							else:
								Semf_2[2].OnLED
								Semf_2[1].OffLED
								Semf_2[2].OffLED
			"""
			else:
				for button in self.all_Buttons:
					if button.manual != 1:
						button.setDesactivo()

					#print(manual_Mode)
			if event.type == pg.MOUSEBUTTONUP:
				#mouse_pos = pg.mouse.get_pos()

				for button in self.all_Buttons:
					button.Onpull()


	def update(self):
		#game loop update
		self.all_sprites.update()


	def drawing(self, start_time):
		#game loop draw
		#time_count = TIME
		global tpause, time_count1, time_count2, manual_Mode#, taux

		self.ventana.fill(BLACK)
		self.all_sprites.draw(self.ventana)
		self.draw_text(self.ventana, "Sistema de Monitoreo y Control de Vialidad", 550, 50, self.title_font, BLUE)
		self.draw_text(self.ventana, "Semaforos", 240, 95, self.title_font, WHITE)
		self.draw_text(self.ventana, "Vehiculos por canal", 225, 300, self.title_font, WHITE)

		for button in self.all_Buttons:
			if button.activo == 1 or button.manual == 1:
				self.draw_text(self.ventana, button.description, button.rect.centerx, button.rect.centery-50, self.subTitle_font, WHITE)
				self.draw_text(self.ventana, button.estado, button.rect.centerx + 50, button.rect.centery, self.inf_font, WHITE)
			else:
				button.setEstadoApagado()

				#print(button.estado)
		for led in self.all_LEDS:
			self.draw_text(self.ventana, led.description, led.rect.centerx, led.rect.centery - 50, self.message_font, WHITE)

		for veh in self.all_Veh:
			self.draw_text(self.ventana, veh.description, veh.rect.centerx, veh.rect.centery - 40, self.message_font, WHITE)
			self.draw_text(self.ventana, veh.num, veh.rect.centerx, veh.rect.centery + 40, self.inf_font, WHITE)
		#self.draw_text(self.ventana, "Carro", 700, 700 - 40, self.message_font, WHITE)
		#self.draw_text(self.ventana, "Camioneta", truck.rect.centerx, truck.rect.centery - 40, self.message_font, WHITE)
		#print("Manual mode: "+str(manual_Mode))
		if manual_Mode == 1:
			self.draw_text(self.ventana, "Habilitar Semaforo por emergencia", 800, 260, self.message_font, WHITE)

		stop_time = time.time()
		Time = stop_time - start_time

		if Time > 1 and Time < 1.15:
			tpause = Time
		taux = Time - tpause

		if taux > 1 and taux < 1.15:
			tpause = Time
			time_count1 = time_count1-1
			time_count2 = time_count2-1

		if time_count1 <= 0:
			time_count1 = 0

		if time_count2 <= 0:
			time_count2 = 0

		self.draw_time(time_count1, 148, 230)
		self.draw_time(time_count2, 336, 230)


		pg.display.flip()

	def draw_new_game_screen(self):
		#draw the new game screen
		pass

	def draw_game_over_screen(self):
		#draw the game over screen
		pass

	RED = (255, 0 ,0)
	def draw_text(self, surface, value, x, y, font, color):
		#draw text in the screen
		text_image = font.render(value, True, color)
		rect = text_image.get_rect()
		rect.center=(x,y)
		surface.blit(text_image, rect)

	def draw_time(self, t, x, y):
		#for t in range(time):
		if t >= 0:
			num = str(t)
		else:
			num = "0"
			print("Error Tiempo negativo: "+str(t))
		self.draw_text(self.ventana, num, x, y, self.subTitle_font, WHITE)

		#pass

	def PRUEBA(self):
		print("Estoy probando... Quien lea esto es marico")

game = Game()
game.draw_new_game_screen()
start_time = time.time()

TIME_1 = 10
time_count1 = TIME_1

TIME_2 = 20
time_count2 = TIME_2

num_s1=[]
num_s1.append(10)
num_s1.append(6)

num_s2=[]
num_s2.append(13)
num_s2.append(8)

while game.running:
	game.new(num_s1, num_s2)
	game.run(start_time)#,tpause,taux)
	game.draw_game_over_screen()

pg.quit()