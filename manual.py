import pygame
from pygame.locals import *
import globals

sqSelected=()
playerClicks = [] 

def move(event):
    global playerClicks
    global sqSelected
    codes = 'pnbrqk'
    if globals.TURN % 2 == 0:
        codes = 'PNBRQK'
    if len(playerClicks) == 2:
        sqSelected = ()
        playerClicks = []
    if event.type == pygame.MOUSEBUTTONDOWN and abs(globals.WIDTH/2 - pygame.mouse.get_pos()[0]) < globals.PROPERTIES['boardSize'][0]/2 and abs(globals.HEIGHT/2 - pygame.mouse.get_pos()[1]) < globals.PROPERTIES['boardSize'][1]/2:
        location = pygame.mouse.get_pos()
        col = (location[0]-(globals.WIDTH-globals.PROPERTIES['boardSize'][0])/2)//globals.FIELDSIZE[0]
        row = (location[1]-(globals.HEIGHT-globals.PROPERTIES['boardSize'][1])/2)//globals.FIELDSIZE[1]
        if sqSelected == (row, col): #clicking same sq twice
            sqSelected = () #deselect
            playerClicks = [] #clear player click
        else:
            sqSelected = (row,col)
            playerClicks.append(sqSelected)
        if len(playerClicks) == 2:
            if globals.BOARD[int(playerClicks[0][0])][int(playerClicks[0][1])] not in codes:
                sqSelected = () #deselect
                playerClicks = [] #clear player click
            else:
                print(playerClicks)
                return playerClicks
    return [None, None]