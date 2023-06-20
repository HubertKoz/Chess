import pygame
from pygame.locals import *
import globals
import chessGraphics
import chessEngine
import utilities
import manual
import gpt
import network
import algorithm


pygame.init()

def main():
    gs = chessEngine.GameState()
    utilities.loadBoard()
    chessGraphics.start()
    while globals.RUNNING:
        ###GRAPHICS###
        chessGraphics.update()
        ###EVENTS###
        for event in pygame.event.get():
            ###MOVE###
            if not globals.PAUSE:
                if (globals.WHITE == 'Manual' and globals.TURN %2 == 0) or (globals.BLACK == 'Manual' and globals.TURN % 2 == 1):
                    playerClicks = manual.move(event)
                    if playerClicks:
                        move = chessEngine.Move(playerClicks[0],playerClicks[1], globals.BOARD)
                        gs.makeMove(move)
                elif (globals.WHITE == 'GPT' and globals.TURN %2 == 0) or (globals.BLACK == 'GPT' and globals.TURN % 2 == 1):
                    gptClicks = gpt.move()
                    if gptClicks:
                        move = chessEngine.Move(gptClicks[0],gptClicks[1], globals.BOARD)
                        gs.makeMove(move)
                elif (globals.WHITE == 'Network' and globals.TURN %2 == 0) or (globals.BLACK == 'Network' and globals.TURN % 2 == 1):
                    networkClicks = network.move()
                    if networkClicks:
                        move = chessEngine.Move(networkClicks[0],networkClicks[1], globals.BOARD)
                        gs.makeMove(move)
                elif (globals.WHITE == 'Algorithm' and globals.TURN %2 == 0) or (globals.BLACK == 'Algorithm' and globals.TURN % 2 == 1):
                    argorithmClicks = algorithm.move()
                    if argorithmClicks:
                        move = chessEngine.Move(argorithmClicks[0],argorithmClicks[1], globals.BOARD)
                        gs.makeMove(move)
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
                gs.undoMove()

if __name__ == '__main__':
    main()