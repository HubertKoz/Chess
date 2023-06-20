import globals
import chessEngine
import random
import utilities
import copy

depth = globals.ALGORITHMDEPTH ###use product of 2
N = 0


def move():
    result = listPossible(0, globals.BOARD)
    N = 0
    return result[1]

def listPossible(d, board):
    global N
    ###COLOR CHOICE###
    codes = 'pnbrqk'
    figures = []
    fields = []
    moves = []
    ###LISTING MOVES###
    if (globals.TURN + d)% 2 == 0:
        codes = 'PNBRQK'
    for i, row in enumerate(board):
        for y, figure in enumerate(row):
            if figure in codes and figure != '':
                figures.append((i, y))
            else:
                fields.append((i, y))
    for figure in figures:
        for field in fields:
            moves.append([figure, field])
    ###SIMULATING POSSIBLE MOVES###
    score = 0
    n = 0
    best = [0]
    for move in moves:
        m = chessEngine.Move(move[0], move[1], board)
        if m.isLegal() and not m.check():
            N += 1
            print(N)
            n += 1
            b = copy.deepcopy(board)
            b[move[1][0]][move[1][1]] = b[move[0][0]][move[0][1]]
            b[move[0][0]][move[0][1]] = ''
            if d % 2 == 0:
                score += figureValue(board[move[1][0]][move[1][1]])
                if d != depth:
                    score += listPossible(d + 1, b)[0]
            else:
                score += figureValue(board[move[1][0]][move[1][1]])
                if d != depth:
                    score -= listPossible(d + 1, b)[0]
            if d == 0:
                if score >= best[0] or len(best) < 3:
                    best = [score, move, n]
                score = 0
    if d != 0:
        if n == 0:
            score = 0
        else:
            score = score/n
        best = [score, move, n]
    return best 


def figureValue(f):
    if f.lower() == 'p':
        return 1
    if f.lower() == 'k':
        return 5
    if f.lower() == 'b':
        return 5
    if f.lower() == 'r':
        return 10
    if f.lower() == 'q':
        return 20
    if f.lower() == 'k':
        return 1000
    return 0

if __name__ == '__main__':
    utilities.loadBoard()
    move()