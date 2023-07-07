import globals
import copy
import numpy as np
import utilities

gs = None

def move(s, e):
    global gs
    if gs == None:
        gs = GameState()
    move = Move(s, e)
    gs.makeMove(move)

def undoMove():
    global gs
    if gs == None:
        gs = GameState()
    gs.undoMove()

#this class is responsible for current state of the chess game and valid moves
#ChessEngine
class GameState():
    def __init__(self):
        self.whitetoMove = True
        self.moveLog = []
    # Without castling, en-passant, queening
    def makeMove (self, move):
        startRow, startCol = move.startRow, move.startCol
        endRow, endCol = move.endRow, move.endCol

        pieceMoved = globals.BOARD[startRow][startCol]
        pieceCaptured = globals.BOARD[endRow][endCol]
        ###TEST IF LEGAL###
        if move.isLegal() and not move.doesnt_end_with_check():
            # Update the board with the move
            globals.BOARD[startRow][startCol] = ''
            globals.BOARD[endRow][endCol] = pieceMoved
            globals.TURN = globals.TURN + 1

            # Update the move log
            self.moveLog.append(move)
        else:
            print('invalid')
    
    def undoMove(self):
        if len(self.moveLog) > 0:  # Ensure there is at least one move to undo
            lastMove = self.moveLog.pop()  # Remove the last move from the move log
            startRow, startCol = lastMove.startRow, lastMove.startCol
            endRow, endCol = lastMove.endRow, lastMove.endCol

            # Restore the board state before the move
            globals.BOARD[startRow][startCol] = lastMove.pieceMoved
            globals.BOARD[endRow][endCol] = lastMove.pieceCaptured
            globals.TURN -= 1



class Move():
    ranksToRows = {"1": 7, "2" : 6, "3": 5, "4" : 4, "5" : 3, "6" : 2, "7": 1, "8":0 }
    rowstoRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b" : 1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = { v: k for k, v in filesToCols.items()}
    def __init__(self, startSq, endSq, board = None):
        self.startSq = np.array([int(startSq[0]), int(startSq[1])])
        self.endSq = np.array([int(endSq[0]), int(endSq[1])])
        self.startRow = int(startSq[0])
        self.startCol = int(startSq[1])
        self.endRow = int(endSq[0])
        self.endCol = int(endSq[1])
        if board is not None:
            self.board = board
        else:
            self.board = globals.BOARD
        self.pieceMoved = self.board[self.startSq[0]][self.startSq[1]]
        self.pieceCaptured = self.board[self.endSq[0]][self.endSq[1]]
    
    def isLegal(self):
        print('jestem tutaj')
        moves = []
        ###PAWN###
        if self.pieceMoved.lower() == 'p':
            moves = pawn_moves(self.startSq, self.board)
        ###KNIGHT###
        if self.pieceMoved.lower() == 'n':
            moves = knight_moves(self.startSq, self.board)
        ###BISHOP###
        if self.pieceMoved.lower() == 'b':
            moves = bishop_moves(self.startSq, self.board)
        ###ROOK###
        if self.pieceMoved.lower() == 'r':
            moves = rook_moves(self.startSq, self.board)
        ###QUEEN###
        if self.pieceMoved.lower() == 'q':
            moves = queen_moves(self.startSq, self.board)
        ###KING###
        if self.pieceMoved.lower() == 'k':
            moves = king_moves(self.startSq, self.board)
        for move in moves:
            print(self.startSq, self.endSq, move)
            if self.startSq[0] == move[0][0] and self.startSq[1] == move[0][1] and self.endSq[0] == move[1][0] and self.endSq[0] == move[1][0]:
                return True
        ###ELSE###
        print('illegal move')
        return False
    

    

    
    def doesnt_end_with_check(self):
        board = copy.deepcopy(self.board)
        board[self.endSq[0]][self.endSq[1]] = board[self.startSq[0]][self.startSq[1]]
        board[self.startSq[0]][self.startSq[1]] = ''
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
            
#####FIGURE MOVE LISTING FUNCTIONS#####
###PAWN###            
def pawn_moves(s, b):
    moves = []
    s = np.array((int(s[0]), int(s[1])))
    if b[s[0]][s[1]] == 'P':
        x = -1
    else:
        x = 1
    ###NON BEATING###
    if b[s[0]+x][s[1]] == '':
        e = s +(x, 0)
        if field_exists(e):
            moves.append((s, e))
        if ((s[0] == 1 and x == 1) or (s[0] == 6 and x == -1)) and b[s[0]+2*x][s[1]] == '':
            e = s +(2*x, 0)
            if field_exists(e):
                moves.append((s, e))
    ###BEATING###
    e = s +(x, 1)
    if field_exists(e):
        if b[e[0]][e[1]] != '' and b[s[0]][s[1]].isupper() != b[e[0]][e[1]].isupper():
            moves.append(s, e)
    e = s +(x, -1)
    if field_exists(e):
        if b[e[0]][e[1]] != '' and b[s[0]][s[1]].isupper() != b[e[0]][e[1]].isupper():
            moves.append(s, e)
    return moves

###KNIGTH###
def knight_moves(s, b):
    s = np.array((int(s[0]), int(s[1])))
    moves = []
    for i in [-1, 1]:
        for y in [-2, 2]:
            e = s + (i, y)
            if field_exists(s+(i, y)):
                if b[e[0]][e[1]] == '' or b[s[0]][s[1]].isupper() != b[e[0]][e[1]].isupper():
                    moves.append((s, s+(i, y)))
            e = s + (y, i)
            if field_exists(s+(y, i)):
                if b[e[0]][e[1]] == '' or b[s[0]][s[1]].isupper() != b[e[0]][e[1]].isupper():
                    moves.append((s, s+(y, i)))
    return moves

###BISHOP###
def bishop_moves(s, b):
    s = np.array((int(s[0]), int(s[1])))
    moves = []
    directions = []
    for i in [1, -1]:
        for y in [1, -1]:
            directions.append(np.array((i,y)))
    for direction in directions:
        for i in range(1, 7):
            e = s+direction*i
            if not field_exists(e):
                break
            if b[e[0]][e[1]] == '' or b[s[0]][s[1]].isupper() != b[e[0]][e[1]].isupper():
                moves.append((s, e))
            if b[e[0]][e[1]] != '':
                break
    return moves

###ROOK###
def rook_moves(s, b):
    s = np.array((int(s[0]), int(s[1])))
    moves = []
    directions = []
    for i in [1, -1]:
        directions.append(np.array((i,0)))
        directions.append(np.array((0,i)))
    for direction in directions:
        for i in range(1, 7):
            e = s+direction*i
            if not field_exists(e):
                break
            if b[e[0]][e[1]] == '' or b[s[0]][s[1]].isupper() != b[e[0]][e[1]].isupper():
                moves.append((s, e))
            if b[e[0]][e[1]] != '':
                break
    return moves

###QUEEN###
def queen_moves(s, b):
    s = np.array((int(s[0]), int(s[1])))
    moves = []
    for move in bishop_moves(s, b):
        moves.append(move)
    for move in rook_moves(s, b):
        moves.append(move)
    return moves

###KING###
def king_moves(s, b):
    moves = []
    s = np.array((int(s[0]), int(s[1])))
    directions = []
    for i in [1, -1]:
        directions.append(np.array((i,0)))
        directions.append(np.array((0,i)))
        for y in [1, -1]:
            directions.append(np.array((i,y)))
    for direction in directions:
        e = s + direction
        if field_exists(e):
            if b[e[0]][e[1]] == '' or b[s[0]][s[1]].isupper() != b[e[0]][e[1]].isupper():
                moves.append((s, e))
    return moves

def field_exists(field):
    if field[0] < 0 or field[1] < 0 or field[0] > 7 or field[1] > 7:
        return False
    return True
            
if __name__=='__main__':
    utilities.loadBoard()