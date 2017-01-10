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

class GameBoard(object):
	def __init__(self):
		self.Selected_question = -1
		self.BoardCells=[]
		self.Teams=[]
		self.Selected_Team_idx = -1
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
			print('HERE')
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

	def show_question(self,cell):
		text = cell.question
		sizeX, sizeY = self.font.size(text)
		self.clear_screen(black)
		self.screen.blit(self.font.render(text, True, red), (Width/2-(sizeX/2), Height/2))
		# self.show_buttons()
		self.update_cells()
		pygame.display.update()


	def update_cells(self):
		if Mode == 'board_time':
			gameBoard.clear_screen(white)
			for cell in self.BoardCells:
				gameBoard.show_cell(cell)
		for team in self.Teams:
			gameBoard.show_cell(team)
		pygame.display.update()

	def clicked(self,pos):
		all_cells = [self.BoardCells,self.Teams]
		for i,cells in enumerate(all_cells):
			for cell in cells:
				width = cell.xPos + cell.width
				height = cell.yPos + cell.height
				if cell.xPos<pos[0]<width:
					if(cell.yPos<pos[1]<height):
						if(cell.type != 'button' and cell.type != 'team'):
							# print(cell.selected)
							print('AAAA')
							# cell.selected = True
						if cell.type == 'team':
							self.reset_team_select()
							cell.selected = not cell.selected
						return cell
		return False		

	def reset_team_select(self):
		for team in self.Teams:
			team.selected = False
gameBoard = GameBoard()
gameBoard.update_cells()
while True:
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:	
			clicked_cell = gameBoard.clicked(event.pos)
			gameBoard.update_cells()
			if clicked_cell:
				print(clicked_cell.question,clicked_cell.selected)
				print('clicked')
				if Mode == 'question_time':	
					Mode = 'board_time'
					gameBoard.update_cells()
				elif Mode == 'board_time':
					if not clicked_cell.selected:
						Mode = 'question_time'
						clicked_cell.selected = True
						gameBoard.show_question(clicked_cell)

	pygame.display.update()
	clock.tick(60)