import globals
import chessEngine
import random
import utilities
import copy
import time

depth = globals.ALGORITHMDEPTH ###use product of 2
N = 0

def move():
    start = time.time()
    global N
    N = 0
    result = listPossible(0, globals.BOARD)
    end = time.time()
    print(end - start)
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
        m = Move(move[0], move[1], board)
        if m.isLegal(board) and not m.check(board):
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
    if f.lower() == 'n':
        return 3
    if f.lower() == 'b':
        return 3
    if f.lower() == 'r':
        return 5
    if f.lower() == 'q':
        return 10
    if f.lower() == 'k':
        return 1000
    return 0

class Move():
    ranksToRows = {"1": 7, "2" : 6, "3": 5, "4" : 4, "5" : 3, "6" : 2, "7": 1, "8":0 }
    rowstoRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b" : 1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = { v: k for k, v in filesToCols.items()}
    def __init__(self, startSq, endSq, board):
        self.startRow = int(startSq[0])
        self.startCol = int(startSq[1])
        self.endRow = int(endSq[0])
        self.endCol = int(endSq[1])
        self.board = board
        self.pieceMoved = self.board[self.startRow][self.startCol]
        self.pieceCaptured = self.board[self.endRow][self.endCol]
    
    def isLegal(self, board):
        pieceMoved = board[self.startRow][self.startCol]
        pieceCaptured = board[self.endRow][self.endCol]
        ###CANT BEAT YOUR OWN###
        if pieceCaptured != '' and ((pieceMoved in 'pnbrqk' and pieceCaptured in 'pnbrqk') or(pieceMoved in 'PNBRQK' and pieceCaptured in 'PNBRQK')):
            return False
        ###PAWN###
        ###NON BEATING###
        if pieceMoved.lower() == 'p' and self.startCol == self.endCol and pieceCaptured =='':
            if pieceMoved == 'P' and ((self.startRow == 6 and self.startRow - self.endRow == 2) or self.startRow - self.endRow == 1):
                return True
            elif pieceMoved == 'p' and ((self.startRow == 1 and self.startRow - self.endRow == -2) or self.startRow - self.endRow == -1):
                return True
        ###BEATING###
        if pieceMoved.lower() == 'p' and abs(self.startCol - self.endCol) == 1 and pieceCaptured !='':
            if pieceMoved == 'P' and self.startRow - self.endRow == 1:
                return True
            elif pieceMoved == 'p' and self.startRow - self.endRow == -1:
                return True
        ###KNIGHT###
        if pieceMoved.lower() == 'n' and ((abs(self.startCol - self.endCol)==1 and abs(self.startRow - self.endRow)==2) or (abs(self.startCol - self.endCol)==2 and abs(self.startRow - self.endRow)==1)):
            return True
        ###BISHOP###
        if pieceMoved.lower() == 'b' and abs(self.startCol - self.endCol) == abs(self.startRow - self.endRow):
            for i in range(1, abs(self.startCol - self.endCol)):
                if board[self.startRow - int(i*((self.startRow - self.endRow)/abs(self.startRow - self.endRow)))][self.startCol - int(i*((self.startCol - self.endCol)/abs(self.startCol - self.endCol)))] !='':
                    return False
            return True
        ###ROOK###
        if pieceMoved.lower() == 'r':
            if self.startCol == self.endCol:
                for i in range(1, abs(self.startRow - self.endRow)):
                    if board[self.startRow - int(i*((self.startRow - self.endRow)/abs(self.startRow - self.endRow)))][self.startCol] !='':
                        return False
                return True
            if self.startRow == self.endRow:
                for i in range(1, abs(self.startCol - self.endCol)):
                    if board[self.startRow][self.startCol - int(i*((self.startCol - self.endCol)/abs(self.startCol - self.endCol)))] !='':
                        return False
                return True
        ###QUEEN###
        if pieceMoved.lower() == 'q':
            if self.startCol == self.endCol:
                for i in range(1, abs(self.startRow - self.endRow)):
                    if board[self.startRow - int(i*((self.startRow - self.endRow)/abs(self.startRow - self.endRow)))][self.startCol] !='':
                        return False
                return True
            if self.startRow == self.endRow:
                for i in range(1, abs(self.startCol - self.endCol)):
                    if board[self.startRow][self.startCol - int(i*((self.startCol - self.endCol)/abs(self.startCol - self.endCol)))] !='':
                        return False
                return True
            if abs(self.startCol - self.endCol) == abs(self.startRow - self.endRow):
                for i in range(1, abs(self.startCol - self.endCol)):
                    if board[self.startRow - int(i*((self.startRow - self.endRow)/abs(self.startRow - self.endRow)))][self.startCol - int(i*((self.startCol - self.endCol)/abs(self.startCol - self.endCol)))] !='':
                        return False
                return True
        ###KING###
        if pieceMoved.lower() == 'k' and (abs(self.startCol - self.endCol) == 1 or abs(self.startRow - self.endRow) ==1) and abs(self.startCol - self.endCol) + abs(self.startRow - self.endRow) <=2:
            return True
        ###ELSE###
        return False
    
    def check(self, b):
        board = copy.deepcopy(b)
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
            if m.isLegal(board):
                return True

if __name__ == '__main__':
    utilities.loadBoard()
    move()