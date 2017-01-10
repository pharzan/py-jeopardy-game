import os, sys
import pandas as pd
import pygame
import time
from pygame.locals import *
clock = pygame.time.Clock()

# Constants:
Time_Limit= 60
Mode="main_menu"
Time_Limit = 60
Width, Height = 1200,700
width = Width/6
height = Height/8
question_file = 'qset1_backup'
Rows, Cols = 0,0

Cats = []
# Colors:
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
		if 'question' in data:
			self.question = data['question']
		if 'answer' in data:
			self.answer = data['answer']
		if 'name' in data:
			self.name = data['name']
		self.score = data['score']
		self.selected = False

		if 'background' in data:
			self.background = data['background']
		else:
			self.background = black	
		
	def set_content(self,cell_text):
		self.content = cell_text

class Team(object):
	def __init__(self,name):
		self.score = 0
		self.team_name = name
	def set_score(self,score):
		self.score = score

class GameBoard(object):
	def __init__(self):
		self.Selected_question = -1
		self.Cells=[]
		self.Teams=[]
		self.Already_selected = []
		self.Selected_Team_idx = -1
		pygame.init()
		self.font = pygame.font.SysFont('Arial', 18)
		pygame.display.set_caption('Jeopardy board game')
		self.screen = pygame.display.set_mode((Width,Height), 0, 32)	
		self.screen.fill((white))
		pygame.display.update()

	def clear_screen(self,color):
		self.rect = pygame.draw.rect(self.screen, (color), (0, 0, Width, Height))

	def update_cells(self):

		df = []
		print('Update Cells',Mode)
		self.Cells = []
		if Mode == 'board_time':
			self.Selected_Team_idx = -1
			def read_question_file(question_file):
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
			df = read_question_file(question_file)

		if Mode == 'question_time':
			s={
				'type':'button',
				'row':1,
				'col':5,
				'width':width,
				'height':height,
				'background':green,
				'score':0,'question':'CORRECT'
				}
			f={
				'type':'button',
				'row':4,
				'col':5,
				'width':width,
				'height':height,
				'background':red,
				'score':0,'question':'INCORRECT'
		}
			success = Cell(s)
			fail = Cell(f)
			self.Cells.append(success)
			self.Cells.append(fail)
		df.append({
					'answer': 'FSDGFDGFDSGFDSGSFDGSD', 
					'category': 'Trivia',
					'score': 0, 'path': 
					'nan', 
					'row': 0, 
					'type': 'team', 
					'col': 6, 
					'question': 'Team A'})
		df.append({
					'answer': 'FSDGFDGFDSGFDSGSFDGSD', 
					'category': 'Trivia',
					'score': 100, 'path': 
					'nan', 
					'row': 1, 
					'type': 'team', 
					'col': 6, 
					'question': 'Team B'})
		for data in df:
			self.Cells.append(Cell(data))
		for cell in self.Cells:
			gameBoard.show_cell(cell)

	def show_cell(self,cell):
		if cell.selected == True:
			return
		background = cell.background
		if Mode == 'board_time' and cell.type != 'team':
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
		# text = cell.name
		print(Mode)
		background = black
		if Mode == 'question_time':
				background = white
		score = str(cell.score)
		team_name = str(cell.question)
		team_score = str(cell.score)
		# sizeX, sizeY = self.font.size(text)
		self.rect = pygame.draw.rect(self.screen, background, 
									   (cell.xPos, 
										cell.yPos, 
										cell.width, 
										cell.height),2)
		self.screen.blit(self.font.render(team_name, True, red), 
										 (cell.xPos+5, cell.yPos ))
		self.screen.blit(self.font.render(team_score, True, red), 
										 (cell.xPos+5, cell.yPos+20 ))
		# self.rect = pygame.draw.rect(self.screen, black,
		# 							   (cell.xPos, 
		# 								cell.yPos, 
		# 								cell.width, 
		# 								cell.height),2)
		# self.screen.blit(self.font.render(text, True, red), 
		# 								 (cell.xPos, cell.yPos ))
		# self.screen.blit(self.font.render(score, True, red), 
		# 								 (cell.xPos, cell.yPos+25 ))

	def show_question(self,cell):
		text = cell.question
		sizeX, sizeY = self.font.size(text)
		self.clear_screen(black)
		self.screen.blit(self.font.render(text, True, red), (Width/2-(sizeX/2), Height/2))
		self.show_buttons()
		self.update_cells()
		pygame.display.update()

	def team_select(self,cell):
		self.update_cells()
		team_num = cell.xPos/width
		self.Selected_Team_idx = team_num
		# if self.Selected_Team_idx == team_num:
		# 	print('AAAA')
		# self.clear_screen(white)
		
		self.rect = pygame.draw.rect(self.screen, red, 
									   (cell.xPos, 
										cell.yPos, 
										cell.width,
										cell.height),2)
	def show_buttons(self):
		s={
			'type':'button',
			'row':1,
			'col':5,
			'width':width,
			'height':height,
			'background':green,
			'score':0,'question':'CORRECT'
		}
		f={
			'type':'button',
			'row':4,
			'col':5,
			'width':width,
			'height':height,
			'background':red,
			'score':0,'question':'INCORRECT'
		}
		success = Cell(s)
		fail = Cell(f)
		self.show_cell(success)
		self.show_cell(fail)

	def clicked(self,pos):
		for i,cell in enumerate(self.Cells):
			
			width = cell.xPos + cell.width
			height = cell.yPos + cell.height
			if cell.xPos<pos[0]<width:
				if(cell.yPos<pos[1]<height):
					if(cell.type != 'button' or cell.type != 'team'):
						self.Already_selected.append(cell)
					return cell
		return False			

	def update_score(self,cell):
		if cell.question == 'CORRECT':
			print('+++',self.Selected_Team_idx,self.Selected_question.score,self.Selected_question.selected)
		if cell.question == 'INCORRECT':
			print('---',self.Selected_Team_idx)

Mode = 'main_menu'
gameBoard = GameBoard()
gameBoard.update_cells()


while True:
	
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			clicked_cell = gameBoard.clicked(event.pos)
			if clicked_cell:
				if clicked_cell.type == 'team':
					# print('TEAM CLICKED',clicked_cell.xPos/width)
					gameBoard.team_select(clicked_cell)
				if gameBoard.Selected_Team_idx == -1:
					print('No Team Selected!!!')
					break
				if  Mode == 'question_time' and clicked_cell.type != 'team':
					clicked_cell = gameBoard.clicked(event.pos)
					gameBoard.update_score(clicked_cell)
					print('>>>>',clicked_cell.question)
					Mode = 'board_time'
					gameBoard.clear_screen(white)
					gameBoard.update_cells()
				elif Mode == 'board_time':
					clicked_cell = gameBoard.clicked(event.pos)
					if clicked_cell.type=='nan':
						clicked_cell.selected = True
						gameBoard.Selected_question=clicked_cell
						Mode = 'question_time'
						gameBoard.update_cells()
						# print('<<<<',clicked_cell.type)
						gameBoard.show_cell(clicked_cell)
					if Mode == 'question_time':
						gameBoard.show_question(clicked_cell)
				elif Mode == 'main_menu':
					# count = int(input("Number of teams: "))
					count = 3
					for i in enumerate(range(count)):
						# name = input('Team '+ str(i+1)+' name? ')
						name = 'Team'+str(i)
						team = Team(name)
						gameBoard.Teams.append(team)
					Mode = 'board_time'
					gameBoard.update_cells()
					print(gameBoard.Teams)


	pygame.display.update()
	clock.tick(60)
		# if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and Mode == 'board_time':