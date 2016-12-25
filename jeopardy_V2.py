import os, sys
import pandas as pd
import pygame
import time
from pygame.locals import *
# Constants:
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

class Question(object):
	def __init__(self):
		self.questionFont = pygame.font.SysFont('Open Sans', 32)
	def show(self,question):
		# q = prepare_size(questions,Width)
		# sizeX, sizeY = self.font.size(q)
		# self.screen.blit(self.font.render(q, True, (255,0,0)), 
		# 						(Width/2-(sizeX/2), Height/2))
		# pygame.display.update()
		print(question)
	def answer(self,answer):
		print(answer)

class Cell(object):
	def __init__(self,xPos,yPos):
		self.type = ''
		self.xPos = xPos
		self.yPos = yPos
		self.content = ''
		self.score = 0
	def set_content(self,cell_text):
		self.content = cell_text

def read_question_file(question_file):
	q={}
	cats=[]
	df = pd.read_csv(question_file+'.csv',header=0)
	for i,row in enumerate(df['Row']):
		question = str(df["Question"][i])
		answer = str(df["Answer"][i])
		score = int(df["Score"][i])
		q[(row,df['Col'][i])]={"question":question,"answer":answer,"score":score}
	Rows,Cols = int(df['Rows'][0]),int(df['Cols'][0])
	for i,cat in enumerate(range(6)):
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
		for j in range(Cols):
			cell = Cell(j,i)
			temp.append(cell)
			cell.set_content(questions[i,j])
		board_matrix.append(temp)
	return board_matrix

questions, Rows, Cols, Cats = read_question_file(question_file)
board_matrix = make_board_matrix()

for row in board_matrix:
	for cell in row:
		print(cell.xPos,cell.yPos,cell.content)

class Panel(object):
	def __init__(self):
		pygame.init()
		self.font = pygame.font.SysFont('Arial', 18)
		pygame.display.set_caption('Jeopardy board game')
		self.screen = pygame.display.set_mode((Width,Height), 0, 32)	
		self.screen.fill((white))
		pygame.display.update()
	def draw_grid(self):
		print(len(board_matrix),len(board_matrix[0]))
		for i,col in enumerate(board_matrix):
			for j,cell in enumerate(board_matrix[i]):
				self.rect = pygame.draw.rect(self.screen, (black), (i*Width/6, j*Height/8, Width/6, Height/8),2)
				try:	
					print(cell.content['score'],cell.content['question'])
					self.screen.blit(self.font.render(str(cell.content['score']), True, black), (j*Width/6, i*Height/8))
				except:
					print("exception")
		pygame.display.update()
	def clicked(self,pos):
		x,y =pos[0], pos[1]
		for i,col in enumerate(board_matrix):
			for j,cell in enumerate(board_matrix[i]):
				if i*(Width/6)<event.pos[0]<(i+1)*(Width/6):
					if(j*(Height/8)<event.pos[1]<(j+1)*(Height/8)):
						print(board_matrix[j][i].content)


		print(x,y)
gamePanel = Panel()
gamePanel.draw_grid()
while True:
	for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
            	gamePanel.clicked(event.pos)


	pygame.display.update()
	clock.tick(60)