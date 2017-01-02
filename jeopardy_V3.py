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
Cells = []
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
		self.background = ''
		
	def set_content(self,cell_text):
		self.content = cell_text

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
	'col': 0, 'row': 5, 
	})
for i,data in enumerate(df):
	Cells.append(Cell(data))

class GameBoard(object):
	def __init__(self):
		pygame.init()
		self.font = pygame.font.SysFont('Arial', 18)
		pygame.display.set_caption('Jeopardy board game')
		self.screen = pygame.display.set_mode((Width,Height), 0, 32)	
		self.screen.fill((white))
		pygame.display.update()

	def clear_screen(self,color):
		self.rect = pygame.draw.rect(self.screen, (color), (0, 0, Width, Height))

	def show_cell(self,cell):
		text = str(cell.score)
		if cell.type == 'team':
			text = cell.name
		sizeX, sizeY = self.font.size(text)
		self.rect = pygame.draw.rect(self.screen, black, 
									   (cell.xPos, 
										cell.yPos, 
										cell.width, 
										cell.height))
		self.screen.blit(self.font.render(text, True, red), (cell.xPos, cell.yPos ))
		pygame.display.update()

	def show_question(self,cell):
		text = cell.question
		sizeX, sizeY = self.font.size(text)
		self.clear_screen(black)
		self.screen.blit(self.font.render(text, True, red), (Width/2-(sizeX/2), Height/2))
		pygame.display.update()

	def clicked(self,pos):
		for cell in Cells:
			width = cell.xPos + cell.width
			height = cell.yPos + cell.height
			if cell.xPos<pos[0]<width:
				if(cell.yPos<pos[1]<height):
					return cell
		return False			

gameBoard = GameBoard()
	
for cell in Cells:
	gameBoard.show_cell(cell)

Mode = 'board_time'
while True:
	for event in pygame.event.get():
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and Mode == 'board_time':
			clicked_cell = gameBoard.clicked(event.pos)
			if clicked_cell:
				Mode = 'question_time'
				print(clicked_cell.question)
				gameBoard.show_question(clicked_cell)


