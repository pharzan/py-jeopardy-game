import os, sys
import pandas as pd
import pygame
import time
from pygame.locals import *
clock = pygame.time.Clock()

# Constants ::
Time_Limit= 60
Width, Height = 1200,700
width = Width/6
height = Height/8
question_file = 'qset1_backup'
# Rows, Cols = 0,0
Mode = 'board_time'
# COLORS ::
white = (255,255,255)
grey = (160,160,160)
black = (0,0,0)
blue = (0,0,255)
red = (255,0,0)
green = (0,255,0)
yellow = (255,255,0)

class Cell(object):
	def __init__(self,data):
		self.type = data['type']
		self.xPos = data['row']*width
		self.yPos = data['col']*height
		self.width = width
		self.height= height
		if 'Mode' in data:
			self.Mode = data['Mode']
		if 'question' in data:
			self.question = data['question']
		if 'answer' in data:
			self.answer = data['answer']
		if 'name' in data:
			self.name = data['name']
		if 'path' in data:
			self.path = data['path']
		self.score = data['score']
		self.selected = False

		if 'background' in data:
			self.background = data['background']
		else:
			self.background = black	
		
	def set_content(self,cell_text):
		self.content = cell_text

class GameBoard(object):
	def __init__(self):
		self.Selected_question = -1
		self.BoardCells=[]
		self.Teams=[]
		self.Buttons =[]
		self.Selected_Team_idx = -1
		self.current_question = {}
		self.selected_team = 0
		self.previous_team = 0
		pygame.init()
		self.font = pygame.font.SysFont('Arial', 18)
		pygame.display.set_caption('Jeopardy board game')
		self.screen = pygame.display.set_mode((Width,Height), 0, 32)	
		self.screen.fill((white))
		pygame.display.update()
		questions = self.read_question_file(question_file)
		for q in questions:
			self.BoardCells.append(Cell(q))
		self.Teams.append(Cell({
					'answer': 'FSDGFDGFDSGFDSGSFDGSD', 
					'category': 'Trivia',
					'score': 0, 'path': 
					'nan', 
					'row': 0, 
					'type': 'team', 
					'col': 6, 
					'question': 'Team A',
					'selected':False}))
		self.Teams.append(Cell({
					'answer': 'FSDGFDGFDSGFDSGSFDGSD', 
					'category': 'Trivia',
					'score': 100, 'path': 
					'nan', 
					'row': 1, 
					'type': 'team', 
					'col': 6, 
					'question': 'Team B',
					'selected':False}))

		s={ 'Mode':'question_time',
			'type':'button',
			'row':1,
			'col':5,
			'width':width,
			'height':height,
			'background':green,
			'score':0,'question':'CORRECT'
		}
		f={'Mode':'question_time',
			'type':'button',
			'row':4,
			'col':5,
			'width':width,
			'height':height,
			'background':red,
			'score':0,'question':'INCORRECT'
		}
		self.Buttons.append(Cell(s))
		self.Buttons.append(Cell(f))

	def read_question_file(self,question_file):
				q=[]
				cats=[]
				df = pd.read_csv(question_file+'.csv',header=0)
				
				for i,row in enumerate(df['Row']):
					question = str(df["Question"][i])
					answer = str(df["Answer"][i])
					score = int(df["Score"][i])
					category = str(df["Categories"][i])
					t = str(df["Type"][i])
					path = str(df["Path"][i])
					col = int(df["Col"][i])
					row = int(df["Row"][i])
					q.append({'question':question,
							  "answer":answer,
							  "score":score, 
							  "category":category, 
					 		  "type":t,
							  "path":path,
							  "row" : row,
							  "col" : col
							  })
				return q 
	def clear_screen(self,color):
		self.rect = pygame.draw.rect(self.screen, (color), (0, 0, Width, Height))

	def show_cell(self,cell):
		background = cell.background		
		if(cell.selected):
			self.rect = pygame.draw.rect(self.screen, cell.background, 
									   (cell.xPos, 
										cell.yPos, 
										cell.width, 
										cell.height))

		elif Mode == 'board_time' and cell.type != 'team':
			text = str(cell.score)
			self.rect = pygame.draw.rect(self.screen, background, 
									   (cell.xPos, 
										cell.yPos, 
										cell.width, 
										cell.height),2)
			self.screen.blit(self.font.render(text, True, red), 
										 (cell.xPos, cell.yPos ))
		if cell.type == 'button':
				self.rect = pygame.draw.rect(self.screen, background, 
									   (cell.xPos, 
										cell.yPos, 
										cell.width, 
										cell.height))
		if cell.type == 'team':
			self.show_team(cell)
		pygame.display.update()

	def show_team(self,cell):
		foreground = red
		background = black
		if Mode == 'question_time':
				background = white
		## the next line clear the background for the teams
		self.rect = pygame.draw.rect(self.screen, background, 
									   (cell.xPos, 
										cell.yPos, 
										cell.width, 
										cell.height))
		if cell.selected:
			self.rect = pygame.draw.rect(self.screen, background, 
									   (cell.xPos, 
										cell.yPos, 
										cell.width, 
										cell.height))
			self.rect = pygame.draw.rect(self.screen, yellow, 
									   (cell.xPos, 
										cell.yPos, 
										cell.width-10, 
										cell.height-10))

		score = str(cell.score)
		team_name = str(cell.question)
		team_score = str(cell.score)
		self.rect = pygame.draw.rect(self.screen, background, 
									   (cell.xPos, 
										cell.yPos, 
										cell.width, 
										cell.height),2)
		self.screen.blit(self.font.render(team_name, True, foreground), 
										 (cell.xPos+5, cell.yPos ))
		self.screen.blit(self.font.render(team_score, True, foreground), 
										 (cell.xPos+5, cell.yPos+20 ))

	def show_question(self,cell):
		
		text = cell.question
		sizeX, sizeY = self.font.size(text)
		self.clear_screen(black)
		self.screen.blit(self.font.render(text, True, red), (Width/2-(sizeX/2), Height/2))
		# self.show_buttons()
		self.update_cells()
		pygame.display.update()
		if cell.type == 'picture':
			print('picture',cell.path)
			img = pygame.image.load(cell.path)
			self.screen.blit(img,(width,height))
			pygame.display.flip()

	def update_cells(self):
		if Mode == 'board_time':
			gameBoard.clear_screen(white)
			for cell in self.BoardCells:
				gameBoard.show_cell(cell)

		for button in self.Buttons:
			if Mode == button.Mode:
				self.show_cell(button)
		for team in self.Teams:
			gameBoard.show_cell(team)
		pygame.display.update()

	def clicked(self,pos):
		if gameBoard.selected_team  != 0:
			gameBoard.previous_team = gameBoard.selected_team

		all_cells = [self.BoardCells,self.Teams,self.Buttons]
		for i,cells in enumerate(all_cells):
			for cell in cells:
				width = cell.xPos + cell.width
				height = cell.yPos + cell.height
				if cell.xPos<pos[0]<width:
					if(cell.yPos<pos[1]<height):
						if cell.type == 'team':
							gameBoard.selected_team=cell;
							self.reset_team_select()
							cell.selected = not cell.selected
						return cell
		return False		

	def reset_team_select(self):
		for team in self.Teams:
			team.selected = False

	def check_team_select(self):
		for team in self.Teams:
			if team.selected:
				return team
		return False

	def check_button(self,btn):
		current_score = self.current_question.score
		if btn.question=='CORRECT':
			selected_team = self.check_team_select()
			self.update_score(current_score,False)
		elif btn.question=='INCORRECT':
			selected_team = self.check_team_select()
			self.update_score(-current_score,False)
		gameBoard.update_cells()

	def update_score(self,score,team_select):
		if team_select:
			for team in gameBoard.Teams:
				if team.selected:
					print ('here we have a prevoius team and we in board mode so we deduct from prevoius team');
					gameBoard.previous_team.score = gameBoard.previous_team.score + score
		else:
			selected_team = self.check_team_select()
			selected_team.score = selected_team.score + score
		
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
        pygame.display.update()
        # self.screen.update()
    def check_click(self,pos):
    	#check click on timer
    	return False

timer = Timer()
gameBoard = GameBoard()
gameBoard.update_cells()
while True:
	if Mode=='question_time':
		timer.show()
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:	
			clicked_cell = gameBoard.clicked(event.pos)
			gameBoard.update_cells()
			if clicked_cell:
				print('>>>',clicked_cell.type,clicked_cell.question,clicked_cell.selected)
				if gameBoard.check_team_select():
					if Mode == 'question_time':
						if clicked_cell.type == 'button':
							Mode = 'board_time'
							gameBoard.check_button(clicked_cell)
						elif clicked_cell.type == 'team':
							print('team select')
							
							gameBoard.update_score(-gameBoard.current_question.score,True)
						gameBoard.update_cells()
					elif Mode == 'board_time':
						if not clicked_cell.selected:
							Mode = 'question_time'
							clicked_cell.selected = True
							gameBoard.current_question = clicked_cell
							gameBoard.show_question(clicked_cell)
							timer.start()

	pygame.display.update()
	clock.tick(60)