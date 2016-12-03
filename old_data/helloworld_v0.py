import pygame, sys
from pygame.locals import *

import os
import subprocess
board=[[0 for x in range(50)] for y in range(50)]
board[0][0]=1
board[1][1]=1
board[1][2]=1
board[2][1]=1
board[0][2]=1
screen=[[0 for x in range(50)] for y in range(50)]
def printBoardAndScreen():
    os.system("clear")
    print "\n"*50
    for x in range(len(board)):
        for y in range(len(board[0])):
            print board[x][y],
            if y ==len(board[0])-1:
                print
    print
    for x in range(len(screen)):
        for y in range(len(screen[0])):
            print screen[x][y],
            if y ==len(screen[0])-1:
                print
    print
def printScreen():
    for x in range(len(screen)):
        for y in range(len(screen[0])):
            print screen[x][y],
            if y ==len(screen[0])-1:
                print
    print
def printBoard():
    os.system("clear")
    print "\n"*50
    for x in range(len(board)):
        for y in range(len(board[0])):
            print board[x][y],
            if y ==len(board[0])-1:
                print
def printAscii():
    os.system("clear")
    #print "\n"*50
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y]==1:
                print "*",
            else:
                print ".",
            if y ==len(board[0])-1:
                print
    print
def printPyGame():
    for x in range(len(board)):
        for y in range(len(board[0])):
            if board[x][y]==1:
                drawCell(x*12,y*12)
            else:
                drawBoard(x*12,y*12)
def check(x,y):
    viz=0
    if y>0:
        if x>0:
            if board[x-1][y-1]==1:
                viz+=1
        if board[x][y-1]==1:
            viz+=1
        if x<len(board)-1:
            if board[x+1][y-1]==1:
                viz+=1
    if x>0:
        if board[x-1][y]==1:
            viz+=1
    if x<len(board)-1:
        if board[x+1][y]==1:
            viz+=1
    if y<len(board[0])-1:
        if x>0:
            if board[x-1][y+1]==1:
                viz+=1
        if board[x][y+1]==1:
            viz+=1
        if x<len(board)-1:
            if board[x+1][y+1]==1:
                viz+=1
    if viz == 2 and board[x][y]!=1:
        viz-=1
    screen[x][y]=viz
def gerate(x,y):
    if screen[x][y]==3:
        board[x][y]=1
    if screen[x][y]>3:
        board[x][y]=0
    if screen[x][y]==2:
        board[x][y]=1
    if screen[x][y]<2:
        board[x][y]=0

pygame.init()

windowSurface = pygame.display.set_mode((600,700),0,32)

pygame.display.set_caption("Runnig!")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (67, 18, 174)
YELLOW= (255,211,0)

windowSurface.fill(WHITE)

def drawCell(x,y):
    x+=5
    y+=5
    pygame.draw.polygon(windowSurface, YELLOW, ((x-5, y-5), (x+5, y-5), (x+5, y+5), (x-5, y+5)))
def drawBoard(x,y):
    x+=5
    y+=5
    pygame.draw.polygon(windowSurface, BLUE, ((x-5, y-5), (x+5, y-5), (x+5, y+5), (x-5, y+5)))
running=True
paused=False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX,mouseY) = pygame.mouse.get_pos()
            if board[mouseX/12][mouseY/12]==1:
                board[mouseX/12][mouseY/12]=0
            else:
                board[mouseX/12][mouseY/12]=1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                paused=(True,False)[paused]
                if paused == True:
                    pygame.display.set_caption("Paused...")
                else:
                    pygame.display.set_caption("Runnig!")
            elif event.key == pygame.K_c:
                for x in range(len(board)):
                    for y in range(len(board[0])):
                        board[x][y]=0
    if paused==False:
        '''
        for x in range(0,1300,12):
            for y in range(0,700,12):
                drawBoard(x,y)
                '''
        os.system("sleep 0.5")
        for x in range(len(screen)):
            for y in range(len(screen[0])):
                check(x,y)
        for x in range(len(board)):
            for y in range(len(board[0])):
                gerate(x,y)
    printPyGame()
    pygame.display.update()

