import os, sys
import pandas as pd
import pygame
import time
from pygame.locals import *
# Constants:
Time_Limit= 60
Mode="board_time"
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
	def set_content(self,cell_text):
		self.content = cell_text

class Timer(object):
    def __init__(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode((Width,Height), 0, 32)
        self.font = pygame.font.SysFont('Arial', 32)
        self.timer_x_pos=(Width/2)-(Width/12)
        self.timer_y_pos=Width/6
        self.counter=0
        self.startTime=0
        self.elapsed=0

    def start(self):
        self.startTime = time.clock()

    def show(self):
        self.elapsed = round(time.clock() - self.startTime,1)
        self.rect = pygame.draw.rect(self.screen, (blue), (self.timer_x_pos, 500, self.timer_y_pos, 100))
        self.screen.blit(self.font.render(str(self.elapsed), True, yellow), (self.timer_x_pos+25,550))
        if self.elapsed >= Time_Limit:
            pygame.mixer.music.load('buzzer2.wav')
            pygame.mixer.music.play()
            timer.start()


def read_question_file(question_file):
	q={}
	cats=[]
	df = pd.read_csv(question_file+'.csv',header=0)
	for i,row in enumerate(df['Row']):
		question = str(df["Question"][i])
		answer = str(df["Answer"][i])
		score = int(df["Score"][i])
		category = str(df["Categories"][i])
		q[(row,df['Col'][i])]={"question":question,"answer":answer,"score":score, "category":category}
	Rows,Cols = int(df['Rows'][0]),int(df['Cols'][0])
	for i in range(0,30,5):
		# print(i)
		# print(df['Categories'][i])
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
print(board_matrix[1][5].content)
# for row in board_matrix:
# 	for cell in row:
# 		print(cell.xPos,cell.yPos,cell.content)

class Panel(object):
	def __init__(self):
		pygame.init()
		self.font = pygame.font.SysFont('Arial', 18)
		pygame.display.set_caption('Jeopardy board game')
		self.screen = pygame.display.set_mode((Width,Height), 0, 32)	
		self.screen.fill((white))
		pygame.display.update()
	def draw_grid(self):
		# print(len(board_matrix),len(board_matrix[0]))
		for i,col in enumerate(board_matrix):
			for j,cell in enumerate(board_matrix[i]):
				self.rect = pygame.draw.rect(self.screen, (black), (i*Width/6, j*Height/8, Width/6, Height/8),2)
				try:	
					# print(cell.content['score'],cell.content['question'])
					self.screen.blit(self.font.render(str(cell.content['score']), True, black), (j*Width/6, i*Height/8))
				except:
					# print(">>>>>>>",str(cell.content))
					self.screen.blit(self.font.render(str(cell.content), True, red), (j*Width/6, i*Height/8))
		pygame.display.update()
	def clicked(self,pos):
		x,y =pos[0], pos[1]
		for i,col in enumerate(board_matrix):
			for j,cell in enumerate(board_matrix[i]):
				if i*(Width/6)<event.pos[0]<(i+1)*(Width/6):
					if(j*(Height/8)<event.pos[1]<(j+1)*(Height/8)):
						selected = board_matrix[j][i].content
						return selected
		# print(x,y)
	def show_question(self,q):
		question_txt = q['question']

		sizeX, sizeY = self.font.size(question_txt)
		self.rect = pygame.draw.rect(self.screen, (black), (0, 0, Width, Height))
		self.screen.blit(self.font.render(question_txt, True, red), (Width/2-(sizeX/2), Height/2))

	def clear_screen(self,color):
		self.rect = pygame.draw.rect(self.screen, (color), (0, 0, Width, Height))

gamePanel = Panel()
timer = Timer()

while True:
	# Mouse events and mode change
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and Mode=='board_time':
			selected_question = gamePanel.clicked(event.pos)
			timer.start()
			Mode = 'question_time'
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and Mode=='question_time':
			Mode = 'board_time'
		# game process:
	if Mode == 'board_time':
		gamePanel.clear_screen(white)
		gamePanel.draw_grid()
	if Mode == 'question_time':
		gamePanel.show_question(selected_question)
		timer.show()
	pygame.display.update()
	clock.tick(60)