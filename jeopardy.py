import os, sys
import pandas as pd
import pygame
import time
from pygame.locals import *
MAX_TIME_LIMIT = 20
if not pygame.font: print ('Warning, fonts disabled')
if not pygame.mixer: print ('Warning, sound disabled')
df = pd.read_csv('qset1.csv',header=0)
q={}
board_matrix=[
              ["First","Second","Third","Fourth","Fifth","Sixth"],
              [200,200,200,200,200,200],
              [400,400,400,400,400,400],
              [600,600,600,600,600,600],
              [800,800,800,800,800,800],
              [1000,1000,1000,1000,1000,1000]
              ]

for i,row in enumerate(df['Row']):
        question = str(df["Question"][i])
        answer = str(df["Answer"][i])
        q[(row,df['Col'][i])]={"question":question,"answer":answer}
for i,cat in enumerate(range(6)):
    board_matrix[0][i]=df['Categories'][i]

class Player(object):
    def __init__(self):
        self.score = 0
        # self.team_name=team_name
        # self.players = players

    def set_score(self,score):
        self.score = score


p1 = Player()
p1.set_score(99)
show_question_flag=False
start_flag = False
team_number = int(input("Number of teams: "))
team_names = []
team_scores = []
already_selected = []

for i in range(team_number):
    name=input("Team Name: ")
    team_names.append(name)
    team_scores.append(0)

# print(team_names)
pygame.init()
gameDisplay = pygame.display.set_mode((800,600))
pygame.display.set_caption('Jeoprady by Pharzan')
clock = pygame.time.Clock()

white = (255,255,255)
grey = (160,160,160)
black = (0,0,0)
blue = (0,0,255)
red = (255,0,0)
green = (0,255,0)
yellow = (255,255,0)

width, height = 1200,600
class Pane(object):
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont('Arial', 18)
        pygame.display.set_caption('Box Test')
        self.screen = pygame.display.set_mode((width,800), 0, 32)
        self.screen.fill((white))
        self.draw_grid_flag=True
        pygame.display.update()


    def draw_grid(self):
        if self.draw_grid_flag: 
            self.screen.fill((white))    
            self.rect = pygame.draw.rect(self.screen, (blue), (0, 0, width, 100))
        
            self.draw_grid_flag=False
            self.show_score()
        # pygame.display.update()

        curser=width/6


        for row in range(6):
            curser=width/6
            for x,header in enumerate(range(6)):
                self.rect = pygame.draw.rect(self.screen, (black), (0, row*100, curser, 100),2)
                curser+=width/6
                # pygame.display.update()
        pygame.display.update()

    def clear_already_selected(self,col,row):
        pygame.draw.rect(self.screen, (black), (row*(width/6), col*100, width/6, 100))
        
    def show_score(self):
        curser=0
        self.rect = pygame.draw.rect(self.screen, (grey), (0,600 , width, 100))
        for team in team_names:
            self.screen.blit(self.font.render(team, True, (255,0,0)), (curser, 600))
            curser+=width/6
        curser=0
        for score in team_scores:
            self.screen.blit(self.font.render(str(score), True, (255,0,0)), (curser, 620))
            curser+=width/6

    def addText(self,pos,text):

        print(pos,text)
        x = pos[0]*width/6+10
        y= 100*pos[1]+35
        color = red
        print('Y',y)
        if y<100:
            color=yellow

        self.screen.blit(self.font.render(str(text), True, color), (x, y))
        
        # for x,header in enumerate(headers):
        #     print(curser)
        #     self.screen.blit(self.font.render(header, True, (255,0,0)), (curser, 100))
        #     curser+=width/6
        #     pygame.display.update()

class Question(object):
    def __init__(self):
        pygame.init()
        self.font = pygame.font.SysFont('Arial', 24)
        pygame.display.set_caption('Box Test')
        self.screen = pygame.display.set_mode((width,height+200), 0, 32)
        self.screen.fill((white))
        pygame.display.update()

    def show(self,q):
        # curser=0
        self.rect = pygame.draw.rect(self.screen, (black), (0, 0, width, height))
        sizeX, sizeY = self.font.size(q)
        if (sizeX>width):
            print("TEXT TOOO LONG!!!")
        print('SHOW QUESTION:',r,c)
        self.screen.blit(self.font.render(q, True, (255,0,0)), (width/2-(sizeX/2), height/2))
        # timer_box:
        # self.rect = pygame.draw.rect(self.screen, (blue), ((width/2)-(width/12), 500, width/6, 100))

        # curser+=width/6
        pygame.display.update()

    def show_answer(self,text):
        self.screen.fill((black))
        sizeX, sizeY = self.font.size(text)
        self.screen.blit(self.font.render(str(text), True, (255,0,0)), (width/2-(sizeX/2), height/2))
        self.rect = pygame.draw.rect(self.screen, (green), ((width/6), 500, width/6, 100))
        self.rect = pygame.draw.rect(self.screen, (red), (4*(width/6), 500, width/6, 100))
        self.rect = pygame.draw.rect(self.screen, (grey), ((width/2)-(width/(18*2)), 500, width/18, 100))
        pygame.display.update()

class Timer(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((width,800), 0, 32)
        self.font = pygame.font.SysFont('Arial', 32)
        self.timer_x_pos=(width/2)-(width/12)
        self.timer_y_pos=width/6
        self.counter=0
        self.startTime=0
        self.elapsed=0

    def start(self):
        self.startTime = time.clock()

    def show(self):
        self.elapsed = round(time.clock()-self.startTime,1)
        self.rect = pygame.draw.rect(self.screen, (blue), (self.timer_x_pos, 500, self.timer_y_pos, 100))
        self.screen.blit(self.font.render(str(self.elapsed), True, (255,255,0)), (self.timer_x_pos+25,550))
        if self.elapsed >= MAX_TIME_LIMIT:
            pygame.mixer.music.load('buzzer2.wav')
            pygame.mixer.music.play()
            timer.start()

current_selected=[0,0]
team_selected = False
question_time = False
pane1= Pane()
question_screen = Question()
timer = Timer()
grid_drawn_flag = False
selected_team_index=-1
show_timer_flag = False

while 1:
    click_count=0
    clock.tick(60)
    while not question_time:
        r, c = 0 , 0
        if not grid_drawn_flag:
            pane1.draw_grid()
            for i in range(6):
                for j in range(6):
                    pane1.addText((i,j),board_matrix[j][i])
            grid_drawn_flag=True

        for each_already_selected in already_selected:
            # print(each_already_selected[0],each_already_selected[1])
            pane1.clear_already_selected(each_already_selected[0],each_already_selected[1])
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if team_selected:
                    print('Board Time')        
                    for col in range(7):
                        if(col*(width/6)<event.pos[0]<(col+1)*(width/6)):
                            # print('col',col)
                            c = col
                            for row in range(6):
                                if(row*(height/6)<event.pos[1]<(row+1)*(height/6)):
                                    r = row
                                    print('Clicked on:',r,c,'SCORE:',board_matrix[r][c])
                                    show_question_flag = True
                                    if (r,c) not in already_selected:
                                        already_selected.append((r,c))
                                        current_selected = [r,c]
                                        question_time = True
                                    else:
                                        print('already selected')
                else:
                    print('First select a team')
                    for col in range(6):
                        if(col*(width/6)<event.pos[0]<(col+1)*(width/6) and event.pos[1]>600):
                            # answering_team = teams[col]
                            print('Selected Team:',col, 'Selected Team Name:',team_names[col],'score',team_scores[col])
                            selected_team_index = col
                            team_selected = True

            if event.type == pygame.QUIT:
                crashed = True
            # print(event)
        pygame.display.update()
        clock.tick(60)

    while question_time:
        
        grid_drawn_flag = False
        if show_timer_flag:
            timer.show()
        
        if show_question_flag:
            print("Current Selected",current_selected)
            timer.start()
            try:
                question=q[current_selected[0],current_selected[1]]['question']
                print("Question:",q[current_selected[0],current_selected[1]]['question'])
            except:
                print('No Question Found For Position')
            question_screen.show(question)
            show_question_flag = False
            show_timer_flag = True
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                print(event.pos[0],event.pos[1])
                if event.pos[1]<600:
                    if event.pos[0]>500 and event.pos[0]<700 and show_timer_flag: 
                        print('Timer')
                        timer.start()
                        break
                    click_count+=1
                    # question_screen.show_answer()
                    print(q[r,c]['answer'])
                    question_screen.show_answer(q[r,c]['answer'])
                    show_timer_flag = False
                    print("Selected Question",c,r,"Points:",board_matrix[c][r],'Click Count:',click_count)
                    print("Question Time")
                    if click_count==2:
                        if (event.pos[0]>(width/6) and event.pos[0]<2*(width/6)):
                            print ("RIGHTTTTT")
                            team_scores[selected_team_index] = team_scores[selected_team_index]+board_matrix[r][c]
                        elif (event.pos[0]>4*(width/6) and event.pos[0]<5*(width/6)):
                            print('WRONGGGG!')
                            team_scores[selected_team_index] = team_scores[selected_team_index]-board_matrix[r][c]
                        print('Second Click:',event.pos[0],event.pos[1])
                        team_selected = False
                        question_time = False
                        pane1.draw_grid_flag = True
                        click_count = 0
                else:
                    print('NEW TEAM SELECT MODE!')
                    for col in range(6):
                        if(col*(width/6)<event.pos[0]<(col+1)*(width/6) and event.pos[1]>600):
                            # answering_team = teams[col]
                            print('New Selected Team:',col, 'Selected Team Name:',team_names[col],
                                  'score',team_scores[col],
                                  'Previous selected team score',team_scores[selected_team_index],
                                  'Score:',board_matrix[r][c])
                            team_scores[selected_team_index]=team_scores[selected_team_index]-board_matrix[r][c]
                            selected_team_index = col
                            pane1.show_score()

        pygame.display.update()
        clock.tick(60)
