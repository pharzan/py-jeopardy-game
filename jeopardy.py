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
        self.font = pygame.font.SysFont('Arial', 25)
        pygame.display.set_caption('Box Test')
        self.screen = pygame.display.set_mode((width,height), 0, 32)
        self.screen.fill((white))
        pygame.display.update()


    def addRect(self,headers):
        self.rect = pygame.draw.rect(self.screen, (blue), (0, 0, width, 100))
        curser=width/6
        for x,header in enumerate(headers):
            self.rect = pygame.draw.rect(self.screen, (black), (0, 0, curser, 100),5)
            curser+=width/6
            pygame.display.update()

        
        pygame.display.update()

    def addText(self,headers):
        curser=0
        for x,header in enumerate(headers):
            print(curser)
            self.screen.blit(self.font.render(header, True, (255,0,0)), (curser, 100))
            curser+=width/6
            pygame.display.update()

crashed = False
pane1= Pane()
headers=['The Dianasours','Notable Women','Oxford Dictionary', 'Belguim', 'Composer By Countary', 'Name That Instrument']
question=['What is your name?']
pane1.addRect(headers)
# pane1.addText(headers)

while not crashed:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for col in range(len(headers)):
                if(col*(width/6)<event.pos[0]<(col+1)*(width/6)):
                    print('col',col)
                    for row in range(5):
                        if(row*(height/6)<event.pos[1]<(row+1)*(height/6)):
                            print('row',row)
            
            

        if event.type == pygame.QUIT:
            crashed = True

        # print(event)

    pygame.display.update()
    clock.tick(60)
