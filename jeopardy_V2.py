import os, sys
import pandas as pd
import pygame
import time
from pygame.locals import *
# Constants:
Time_Limit= 60
Mode="main_menu"
Time_Limit = 60
Width, Height = 1200,800
question_file = 'qset1_backup'
Rows, Cols = 0,0
Cats = []
clock = pygame.time.Clock()
# Colors:
white = (255,255,255)
grey = (160,160,160)
black = (0,0,0)
blue = (0,0,255)
red = (255,0,0)
green = (0,255,0)
yellow = (255,255,0)

class Player(object):
	def __init__(self):
		self.score = 0
		self.team_name = ""
	def set_score(self,score):
		self.score = score

class Cell(object):
	def __init__(self,xPos,yPos):
		self.type = ''
		self.xPos = xPos
		self.yPos = yPos
		self.content = ''
		self.score = 0
		self.selected = False
		self.type = ''
	def set_content(self,cell_text):
		self.content = cell_text

class Timer(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((Width,Height), 0, 32)
        self.font = pygame.font.SysFont('Arial', 32)
        self.timer_y_pos=0 # top
        self.box_width = Width/6 #set to middle of screen
        self.box_height = 100
        self.timer_x_pos = Width/2 - self.box_width/2
        self.counter=0
        self.startTime=0
        self.elapsed=0
    def start(self):
        self.startTime = time.clock()
    def show(self):
        self.elapsed = round(time.clock() - self.startTime,1)
        elapsed = str(self.elapsed)
        sizeX, sizeY = self.font.size(elapsed)
        middle_X = self.timer_x_pos+self.box_width/2-sizeX/2
        middle_Y = self.box_height/2-sizeY/2
        self.rect = pygame.draw.rect(self.screen, (blue), (self.timer_x_pos, self.timer_y_pos, self.box_width, self.box_height))
        self.screen.blit(self.font.render(elapsed, True, yellow), (middle_X, middle_Y))
        if self.elapsed >= Time_Limit:
            pygame.mixer.music.load('buzzer2.wav')
            pygame.mixer.music.play()
            timer.start()
    def check_click(self,pos):
    	#check click on timer
    	return False

class Panel(object):
	def __init__(self):
		pygame.init()
		self.font = pygame.font.SysFont('Arial', 18)
		pygame.display.set_caption('Jeopardy board game')
		self.screen = pygame.display.set_mode((Width,Height), 0, 32)	
		self.screen.fill((white))
		pygame.display.update()

	def center(self,txt,box_width,box_height):
		sizeX, sizeY = self.font.size(txt)
		middle_X = Width/6+Width/12
		middle_Y = box_height/2-sizeY/2
		return middle_X, middle_Y
	def draw_grid(self):
		text=''
		for i,col in enumerate(board_matrix):
			for j,cell in enumerate(board_matrix[i]):
				if cell.selected:
					self.rect = pygame.draw.rect(self.screen, (black), (i*Width/6, j*Height/8, Width/6, Height/8))
				self.rect = pygame.draw.rect(self.screen, (black), (i*Width/6, j*Height/8, Width/6, Height/8),2)
				try:
					text = str(cell.content['score'])
					sizeX, sizeY = self.font.size(text)
					self.screen.blit(self.font.render(text, True, black), (j*Width/6+((Width/12)-sizeX), i*Height/8+((Height/16)-sizeY)))
				except:
					text = str(cell.content)
					sizeX, sizeY = self.font.size(text)
					self.screen.blit(self.font.render(text, True, black), (j*Width/6, i*Height/8))

				
		pygame.display.update()
	def clicked(self,pos):
		# Returns false if already selected
		question_type = 'normal'
		path = ''
		x,y =pos[0], pos[1]
		for i,col in enumerate(board_matrix):
			for j,cell in enumerate(board_matrix[i]):
				if not cell.selected:
					if i*(Width/6)<event.pos[0]<(i+1)*(Width/6):
						if(j*(Height/8)<event.pos[1]<(j+1)*(Height/8)):
							selected = board_matrix[j][i].content
							question_type = board_matrix[j][i].content['type']
							path = board_matrix[j][i].content['path']
							cell.selected = True
							return selected, question_type, path
		return False
					

	def show_question(self,q):
		done_flag = False
		question_txt = q['question']
		sizeX, sizeY = self.font.size(question_txt)
		self.clear_screen(black)
		self.screen.blit(self.font.render(question_txt, True, red), (Width/2-(sizeX/2), Height/2))
		pygame.display.update()
		while not done_flag:
			for event in pygame.event.get():
				if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
					# in question click detection
					return "board_time"
			
			
	def show_picture_question(self,q,path):
		self.clear_screen(black)
		img = pygame.image.load(path)
		X,Y = img.get_rect().size
		self.screen.blit(img,(Width/2-X/2,Height/2-Y/2))
		# pygame.display.flip()
	def show_audio_question(self,q,path):
		done_flag = False
		self.clear_screen(black)
		pygame.display.update()
		sound = pygame.mixer.Sound(path)
		# X,Y = img.get_rect().size
		channel = sound.play()
		while channel.get_busy():
			pygame.time.wait(1)
			print('playing')
		return "board_time"
		# pygame.display.flip()

	def clear_screen(self,color):
		self.rect = pygame.draw.rect(self.screen, (color), (0, 0, Width, Height))

class Team(object):
	def __init__(self,teams):
		self.players=Team.Players()
		self.team_names = []
		self.number_of_teams = teams
	class Players(object):
		def __init__(self):
			self.teams = 0
			self.scores = 0
	def set_name(self,name):
		name = str(name)
		self.team_names.append(name)

def read_question_file(question_file):
	q={}
	cats=[]
	df = pd.read_csv(question_file+'.csv',header=0)
	for i,row in enumerate(df['Row']):
		question = str(df["Question"][i])
		answer = str(df["Answer"][i])
		score = int(df["Score"][i])
		category = str(df["Categories"][i])
		t = str(df["Type"][i])
		path = str(df["Path"][i])

		q[(row,df['Col'][i])]={"question":question,
								"answer":answer,
								"score":score, 
								"category":category, 
								"type":t,
								"path":path}

	Rows,Cols = int(df['Rows'][0]),int(df['Cols'][0])
	for i in range(0,30,5):
		Cats.append(df['Categories'][i])
	return q, Rows, Cols, Cats

def make_board_matrix():
	board_matrix = []
	temp=[]
	for i,cat in enumerate(Cats):
		cell = Cell(0,i)
		cell.content = cat
		temp.append(cell)
	board_matrix.append(temp)
	for i in range(Rows):
		temp = []
		for j in range(Cols+1):
			cell = Cell(j,i)
			temp.append(cell)
			cell.set_content(questions[i,j])
		board_matrix.append(temp)
	return board_matrix

questions, Rows, Cols, Cats = read_question_file(question_file)
board_matrix = make_board_matrix()
gamePanel = Panel()
timer = Timer()

# players = Players()

while True:
	# Mouse events and mode change
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and Mode=='board_time':
			selected_question, question_type, path = gamePanel.clicked(event.pos)
			timer.start()
			if selected_question!= False:
				Mode = 'question_time'
		# elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and Mode=='question_time':
		# 	if not timer.check_click(event.pos):
		# 		Mode = 'board_time'
		# game process:
	if Mode == 'board_time':
		gamePanel.clear_screen(white)
		gamePanel.draw_grid()
	if Mode == 'question_time':
		if question_type == 'picture':
			print('picture question')
			gamePanel.show_picture_question(selected_question,path)
		elif question_type == 'audio':
			print('audio question')
			Mode = gamePanel.show_audio_question(selected_question,path)
		else:
			print('Normal')
			Mode = gamePanel.show_question(selected_question)
		timer.show()
	if Mode == 'main_menu':
		number_of_teams = int(input("Number of teams: "))
		teams = Team(number_of_teams)
		for i,team in enumerate(range(number_of_teams)):
			print(teams)
			# name = input('Team '+ str(i+1)+' name? ')
			# players.team_names.append(name)
		Mode = 'board_time'
	if event.type == QUIT:
		pygame.display.quit()
		sys.exit()
	pygame.display.update()
	clock.tick(60)