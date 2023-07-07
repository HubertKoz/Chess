import numpy as np

###GAMESTATE###
RUNNING = True
PAUSE = False
MOVING = False
CHECKMATE = False
STARTFEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
BOARD = []
CONTROLS = ['Manual', 'GPT', 'Algorithm', 'Network']
TURN = 0 ###even - white's move, odd - black's
WHITE = 'Manual'
BLACK = 'Manual'
ALGORITHMDEPTH = 2
###DISPLAY###
WIDTH, HEIGHT = 800, 400
SHOWFIELDNAMES = False
PROPERTIES = {
    'boardSize': np.array([300, 300]),
    'frameSize': 5
}
COLORS = {
    'background': np.array([126, 126, 126]),
    'lightSquare': np.array([200, 200, 200]),
    'darkSquare': np.array([50, 50, 50]),
    'frame': np.array([150, 50, 50]),
    'highlight': 1.2
}
FIELDSIZE = PROPERTIES['boardSize']/8
FIGURESPATH = 'figures/'
###UTILITIES###
FIGURESIDS = {'P': 1, 'N': 2, 'B': 3, 'R': 4, 'Q': 5, 'K': 6, 'p': 7, 'n': 8, 'b': 9, 'r': 10, 'q': 11, 'k': 12}
