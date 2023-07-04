import globals
import chessEngine
import random
'''import os

from tensorflow.keras import models
model = models.load_model('model.h5')

# used for the minimax algorithm
def minimax_eval(board):
    board3d = split_dims(board)
    board3d = numpy.expand_dims(board3d, 0)
    return model(board3d)[0][0]


def minimax(board, depth, alpha, beta, maximizing_player):
    if depth == 0 or board.is_game_over():
        return minimax_eval(board)

    if maximizing_player:
        max_eval = -numpy.inf
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, False)
            board.pop()
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = numpy.inf
        for move in board.legal_moves:
            board.push(move)
            eval = minimax(board, depth - 1, alpha, beta, True)
            board.pop()
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval


# this is the actual function that gets the move from the neural network
def get_ai_move(board, depth):
    max_move = None
    max_eval = -numpy.inf

    for move in board.legal_moves:
        board.push(move)
        eval = minimax(board, depth - 1, -numpy.inf, numpy.inf, False)
        board.pop()
        if eval > max_eval:
            max_eval = eval
            max_move = move

    return max_move

# Testing code AI(white) vs Stockfish(black)
board = chess.Board()
from IPython.display import clear_output

with chess.engine.SimpleEngine.popen_uci('stockfish/7/bin/stockfish') as engine:
    while True:
        clear_output(wait=True)
        move = get_ai_move(board, 1)
        board.push(move)
        print(f'\n{board}')
        if board.is_game_over():
            print('game_over')
            break
        move = engine.analyse(board, chess.engine.Limit(time=0.1), info=chess.engine.INFO_PV)['pv'][0]
        board.push(move)
        print(f'\n{board}')
        if board.is_game_over():
            print('game_over')
            break'''

def move():
    figs = []
    choice = 'PNBRQK'
    if globals.TURN % 2 == 1:
        choice = choice.lower()
    for i, row in enumerate(globals.BOARD):
        for y, figure in enumerate(row):
            if figure in choice:
                figs.append((i, y))
    moves = []
    m = [random.choice(figs), (random.randrange(0, 7), random.randrange(0, 7))]
    while True:
        while m in moves:
            m = [random.choice(figs), (random.randrange(0, 7), random.randrange(0, 7))]
        move = Move(m[0], m[1], globals.BOARD)
        if move.isLegal() and not move.check():
            return m[0], m[1]
        else:
            moves.append(m)

class Move():
    ranksToRows = {"1": 7, "2" : 6, "3": 5, "4" : 4, "5" : 3, "6" : 2, "7": 1, "8":0 }
    rowstoRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b" : 1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = { v: k for k, v in filesToCols.items()}
    def __init__(self, startSq, endSq, board = None):
        self.startRow = int(startSq[0])
        self.startCol = int(startSq[1])
        self.endRow = int(endSq[0])
        self.endCol = int(endSq[1])
        if board is not None:
            self.board = board
        else:
            self.board = globals.BOARD
        self.pieceMoved = self.board[self.startRow][self.startCol]
        self.pieceCaptured = self.board[self.endRow][self.endCol]
    
    def isLegal(self):
        ###CANT BEAT YOUR OWN###
        if self.pieceCaptured != '' and ((self.pieceMoved in 'pnbrqk' and self.pieceCaptured in 'pnbrqk') or(self.pieceMoved in 'PNBRQK' and self.pieceCaptured in 'PNBRQK')):
            return False
        ###PAWN###
        ###NON BEATING###
        if self.pieceMoved.lower() == 'p' and self.startCol == self.endCol and self.pieceCaptured =='':
            if self.pieceMoved == 'P' and ((self.startRow == 6 and self.startRow - self.endRow == 2) or self.startRow - self.endRow == 1):
                return True
            elif self.pieceMoved == 'p' and ((self.startRow == 1 and self.startRow - self.endRow == -2) or self.startRow - self.endRow == -1):
                return True
        ###BEATING###
        if self.pieceMoved.lower() == 'p' and abs(self.startCol - self.endCol) == 1 and self.pieceCaptured !='':
            if self.pieceMoved == 'P' and self.startRow - self.endRow == 1:
                return True
            elif self.pieceMoved == 'p' and self.startRow - self.endRow == -1:
                return True
        ###KNIGHT###
        if self.pieceMoved.lower() == 'n' and ((abs(self.startCol - self.endCol)==1 and abs(self.startRow - self.endRow)==2) or (abs(self.startCol - self.endCol)==2 and abs(self.startRow - self.endRow)==1)):
            return True
        ###BISHOP###
        if self.pieceMoved.lower() == 'b' and abs(self.startCol - self.endCol) == abs(self.startRow - self.endRow):
            for i in range(1, abs(self.startCol - self.endCol)):
                if self.board[self.startRow - int(i*((self.startRow - self.endRow)/abs(self.startRow - self.endRow)))][self.startCol - int(i*((self.startCol - self.endCol)/abs(self.startCol - self.endCol)))] !='':
                    return False
            return True
        ###ROOK###
        if self.pieceMoved.lower() == 'r':
            if self.startCol == self.endCol:
                for i in range(1, abs(self.startRow - self.endRow)):
                    if self.board[self.startRow - int(i*((self.startRow - self.endRow)/abs(self.startRow - self.endRow)))][self.startCol] !='':
                        return False
                return True
            if self.startRow == self.endRow:
                for i in range(1, abs(self.startCol - self.endCol)):
                    if self.board[self.startRow][self.startCol - int(i*((self.startCol - self.endCol)/abs(self.startCol - self.endCol)))] !='':
                        return False
                return True
        ###QUEEN###
        if self.pieceMoved.lower() == 'q':
            if self.startCol == self.endCol:
                for i in range(1, abs(self.startRow - self.endRow)):
                    if self.board[self.startRow - int(i*((self.startRow - self.endRow)/abs(self.startRow - self.endRow)))][self.startCol] !='':
                        return False
                return True
            if self.startRow == self.endRow:
                for i in range(1, abs(self.startCol - self.endCol)):
                    if self.board[self.startRow][self.startCol - int(i*((self.startCol - self.endCol)/abs(self.startCol - self.endCol)))] !='':
                        return False
                return True
            if abs(self.startCol - self.endCol) == abs(self.startRow - self.endRow):
                for i in range(1, abs(self.startCol - self.endCol)):
                    if self.board[self.startRow - int(i*((self.startRow - self.endRow)/abs(self.startRow - self.endRow)))][self.startCol - int(i*((self.startCol - self.endCol)/abs(self.startCol - self.endCol)))] !='':
                        return False
                return True
        ###KING###
        if self.pieceMoved.lower() == 'k' and (abs(self.startCol - self.endCol) == 1 or abs(self.startRow - self.endRow) ==1) and abs(self.startCol - self.endCol) + abs(self.startRow - self.endRow) <=2:
            return True
        ###ELSE###
        return False
    
    def check(self):
        board = copy.deepcopy(self.board)
        board[self.endRow][self.endCol] = board[self.startRow][self.startCol]
        board[self.startRow][self.startCol] = ''
        ###COLOR CHOICE###
        codes = 'pnbrqk'
        king = 'K'
        figures = []
        moves = []
        ###LISTING MOVES###
        if (globals.TURN + 1) % 2 == 0:
            codes = 'PNBRQK'
            king = 'k'
        for i, row in enumerate(board):
            for y, figure in enumerate(row):
                if figure in codes and figure != '':
                    figures.append((i, y))
                elif figure == king:
                    king = (i, y)
        for figure in figures:
                moves.append([figure, king])
        ###SIMULATING POSSIBLE MOVES###
        for move in moves:
            m = Move(move[0], move[1], board)
            if m.isLegal():
                return True
