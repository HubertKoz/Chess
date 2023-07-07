import pygame
from pygame.locals import *
import globals
import chessGraphics
#import chessEngine as ce
import chessEngine2 as ce
import utilities
import manual
import gpt
import network
import algorithm


pygame.init()

def main():
    utilities.loadBoard()
    chessGraphics.start()
    while globals.RUNNING:
        ###GRAPHICS###
        chessGraphics.update()
        ###EVENTS###
        for event in pygame.event.get():
            ###MOVE###
            if not globals.PAUSE:
                globals.MOVING = True
                if (globals.WHITE == 'Manual' and globals.TURN %2 == 0) or (globals.BLACK == 'Manual' and globals.TURN % 2 == 1):
                    globals.MOVING = False
                    s, e = manual.move(event)
                elif (globals.WHITE == 'GPT' and globals.TURN %2 == 0) or (globals.BLACK == 'GPT' and globals.TURN % 2 == 1):
                    s, e = gpt.move()
                elif (globals.WHITE == 'Network' and globals.TURN %2 == 0) or (globals.BLACK == 'Network' and globals.TURN % 2 == 1):
                    s, e = network.move()
                elif (globals.WHITE == 'Algorithm' and globals.TURN %2 == 0) or (globals.BLACK == 'Algorithm' and globals.TURN % 2 == 1):
                    s, e = algorithm.move()
                if s and e:
                    ce.move(s, e)
                    s, e = None, None
                globals.MOVING = False
            ###CHECK BUTTONS###
            if event.type == pygame.MOUSEBUTTONDOWN:
                chessGraphics.check()
            ###CHECK PAUSE###
            if (event.type == KEYDOWN and event.key == K_SPACE):
                if globals.PAUSE:
                    globals.PAUSE = False
                else:
                    globals.PAUSE = True
            ###EXIT###
            if (event.type == KEYDOWN and event.key == K_q) or event.type ==pygame.QUIT:
                globals.RUNNING = False
            ###UNDO MOVE###
            if event.type == KEYDOWN and event.key == K_z:
                ce.undoMove()

if __name__ == '__main__':
    main()