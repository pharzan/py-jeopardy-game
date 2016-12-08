import os, sys
import pygame
from pygame.locals import *

if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')

pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('A bit Racey')
clock = pygame.time.Clock()

white = (255,255,255)
black = (0,0,0)
blue = (0,0,255)

width, height = 1200,600
class Pane(object):
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont('Arial', 18)
        pygame.display.set_caption('Box Test')
        self.screen = pygame.display.set_mode((width,height), 0, 32)
        self.screen.fill((white))
        pygame.display.update()


    def draw_grid(self,headers):
        self.rect = pygame.draw.rect(self.screen, (blue), (0, 0, width, 100))
        pygame.display.update()

        curser=width/6

        for x,header in enumerate(headers):
            self.rect = pygame.draw.rect(self.screen, (black), (0, 0, curser, 100),2)
            curser+=width/6
            pygame.display.update()

        for row in range(6):
            curser=width/6
            for x,header in enumerate(headers):
                self.rect = pygame.draw.rect(self.screen, (black), (0, row*100, curser, 100),2)
                curser+=width/6
                pygame.display.update()
        

    def addText(self,headers):
        curser=0
        for x,header in enumerate(headers):
            print(curser)
            self.screen.blit(self.font.render(header, True, (255,0,0)), (curser, 100))
            curser+=width/6
            pygame.display.update()

class Question(object):
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont('Arial', 18)
        pygame.display.set_caption('Box Test')
        self.screen = pygame.display.set_mode((width,height), 0, 32)
        self.screen.fill((white))
        pygame.display.update()

    def show(self,r,c):
        curser=0
        print('SHOW QUESTION:',r,c)
        # self.screen.blit(self.font.render(q, True, (255,0,0)), (curser, 100))
        # curser+=width/6
        # pygame.display.update()


crashed = False
pane1= Pane()
question_screen = Question()

headers=['The Dianasours','Notable Women','Oxford Dictionary', 'Belguim', 'Composer By Countary', 'Name That Instrument']
question=['What is your name?']
pane1.draw_grid(headers)
pane1.addText(headers)

while not crashed:
    r, c = 0 , 0
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for col in range(len(headers)):
                if(col*(width/6)<event.pos[0]<(col+1)*(width/6)):
                    # print('col',col)
                    c=col
                    for row in range(6):
                        if(row*(height/6)<event.pos[1]<(row+1)*(height/6)):
                            # print('row',row)
                            r=row
            question_screen.show(r,c)
            

        if event.type == pygame.QUIT:
            crashed = True

        # print(event)

    pygame.display.update()
    clock.tick(60)
