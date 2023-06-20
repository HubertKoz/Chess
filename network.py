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
        move = chessEngine.Move(m[0], m[1], globals.BOARD)
        if move.isLegal() and not move.check():
            return m[0], m[1]
        else:
            moves.append(m)

