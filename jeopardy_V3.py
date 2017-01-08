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



class GameBoard(object):
	def __init__(self):
		self.Cells=[]
		pygame.init()
		self.font = pygame.font.SysFont('Arial', 18)
		pygame.display.set_caption('Jeopardy board game')
		self.screen = pygame.display.set_mode((Width,Height), 0, 32)	
		self.screen.fill((white))
		pygame.display.update()

	def clear_screen(self,color):
		self.rect = pygame.draw.rect(self.screen, (color), (0, 0, Width, Height))

	def update_cells(self):
		self.Cells = []
		if Mode == 'board_time':
			print('Here')		
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
			df.append({
				'name': 'Team A',
				'type': 'team', 
				'category': '10G',
				'path': 'blah.txt', 
				'score': 200, 
				'col': 5, 'row': 0, 
				'selected':False
				})
			for data in df:
				self.Cells.append(Cell(data))
			for cell in self.Cells:
				gameBoard.show_cell(cell)
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

	def show_cell(self,cell):
		# print(cell.type != 'team')
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
		pygame.display.update()


	def show_team(self,cell):
		text = cell.name
		score = str(cell.score)
		sizeX, sizeY = self.font.size(text)
		self.screen.blit(self.font.render(text, True, red), 
										 (cell.xPos, cell.yPos ))
		self.screen.blit(self.font.render(score, True, red), 
										 (cell.xPos, cell.yPos+25 ))

	def show_question(self,cell):
		text = cell.question
		sizeX, sizeY = self.font.size(text)
		self.clear_screen(black)
		self.screen.blit(self.font.render(text, True, red), (Width/2-(sizeX/2), Height/2))
		self.show_buttons()
		pygame.display.update()

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
		for cell in self.Cells:
			width = cell.xPos + cell.width
			height = cell.yPos + cell.height
			if cell.xPos<pos[0]<width:
				if(cell.yPos<pos[1]<height):
					return cell
		return False			
Mode = 'board_time'
gameBoard = GameBoard()
gameBoard.update_cells()


while True:
	
	for event in pygame.event.get():
		gameBoard.update_cells()
		print(Mode)
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
			if  Mode == 'question_time':
				clicked_cell = gameBoard.clicked(event.pos)
				if clicked_cell.question == 'CORRECT':
					Mode = 'board_time'
					print('Correct clicked')
				if clicked_cell.question == 'INCORRECT':
					print('inCorrect clicked')
			if Mode == 'board_time':
				clicked_cell = gameBoard.clicked(event.pos)
				if clicked_cell.type=='nan':
					Mode = 'question_time'
					print(clicked_cell.type)
					gameBoard.show_cell(clicked_cell)
				if Mode == 'question_time':
					gameBoard.show_question(clicked_cell)
						
		# if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and Mode == 'board_time':
			



