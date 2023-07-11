import globals
import copy
import numpy as np
import utilities

gs = None
moveLog = []

def move(s, e):
    move = Move(s, e)
    ###TEST IF LEGAL###
    if move.isLegal(s, globals.BOARD) and not move.check(s, e, globals.BOARD):
        # Update the board with the move
        globals.BOARD[move.endSq[0]][move.endSq[1]] = globals.BOARD[move.startSq[0]][move.startSq[1]]
        globals.BOARD[move.startSq[0]][move.startSq[1]] = ''
        globals.TURN = globals.TURN + 1
        # Update the move log
        moveLog.append(move)
    else:
        print('invalid')

def undoMove():
    if len(moveLog) > 0:  # Ensure there is at least one move to undo
        move = moveLog.pop()  # Remove the last move from the move log

        # Restore the board state before the move
        globals.BOARD[move.startSq[0]][move.startSq[1]] = move.pieceMoved
        globals.BOARD[move.endSq[0]][move.endSq[1]] = move.pieceCaptured
        globals.TURN -= 1

class Move():
    ranksToRows = {"1": 7, "2" : 6, "3": 5, "4" : 4, "5" : 3, "6" : 2, "7": 1, "8":0 }
    rowstoRanks = {v: k for k, v in ranksToRows.items()}

    filesToCols = {"a": 0, "b" : 1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7}
    colsToFiles = { v: k for k, v in filesToCols.items()}
    def __init__(self, startSq, endSq, board = None):
        self.startSq = np.array([int(startSq[0]), int(startSq[1])])
        self.endSq = np.array([int(endSq[0]), int(endSq[1])])
        if board is not None:
            self.board = board
        else:
            self.board = globals.BOARD
        self.pieceMoved = self.board[self.startSq[0]][self.startSq[1]]
        self.pieceCaptured = self.board[self.endSq[0]][self.endSq[1]]
    
    #####FIGURE MOVE LISTING FUNCTIONS#####
    def isLegal(self, s, b):
        s = np.array((int(s[0]), int(s[1])))
        moves = []
        ###PAWN MOVES###
        if self.pieceMoved.lower() == 'p':
            if b[s[0]][s[1]] == 'P':
                x = -1
            else:
                x = 1
            ###NON BEATING###
            e = s +(x, 0)
            if b[e[0]][e[1]] == '':
                if field_exists(e):
                    moves.append((s, e))
                e = s +(2*x, 0)
                if ((s[0] == 1 and x == 1) or (s[0] == 6 and x == -1)) and b[e[0]][e[1]] == '':
                    if field_exists(e):
                        moves.append((s, e))
            ###BEATING###
            e = s +(x, 1)
            if field_exists(e):
                if b[e[0]][e[1]] != '' and b[s[0]][s[1]].isupper() != b[e[0]][e[1]].isupper():
                    moves.append((s, e))
            e = s +(x, -1)
            if field_exists(e):
                if b[e[0]][e[1]] != '' and b[s[0]][s[1]].isupper() != b[e[0]][e[1]].isupper():
                    moves.append((s, e))
        ###KNIGHT MOVES###
        if self.pieceMoved.lower() == 'n':
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
        ###BISHOP, ROOK and QUEEN MOVES###
        if self.pieceMoved.lower() in 'brq' and self.pieceMoved != '':
            directions = []
            ###BISHOP AND QUEEN DIRECTIONS
            if self.pieceMoved.lower() in 'bq' and self.pieceMoved != '':
                directions.append([1, -1])
                directions.append([1, 1])
                directions.append([-1, -1])
                directions.append([-1, 1])
            ###ROOK AND QUEEN DIRECTIONS###
            if self.pieceMoved.lower() in 'rq' and self.pieceMoved != '':
                directions.append([0, -1])
                directions.append([0, 1])
                directions.append([-1, 0])
                directions.append([1, 0])
            ###MOVES###
            for direction in directions:
                for i in range(1, 7):
                    e = s+np.array(direction)*i
                    if not field_exists(e):
                        break
                    if b[e[0]][e[1]] == '' or b[s[0]][s[1]].isupper() != b[e[0]][e[1]].isupper():
                        moves.append((s, e))
                    if b[e[0]][e[1]] != '':
                        break
        ###KING MOVES###
        if self.pieceMoved.lower() == 'k':
            directions = [[1,1],[1,0],[1,-1],[0,1],[0,0],[0,-1],[-1,1],[-1,0],[-1,-1]]
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
        ###EVALUATION###
        for move in moves:
            if self.startSq[0] == move[0][0] and self.startSq[1] == move[0][1] and self.endSq[0] == move[1][0] and self.endSq[1] == move[1][1]:
                print('legal move')
                return True
        ###ELSE###
        print('illegal move')
        return False
    
    def check(self, s, e, b):
        s = np.array([int(s[0]), int(s[1])])
        e = np.array([int(e[0]), int(e[1])])
        board = copy.deepcopy(b)
        board[e[0]][e[1]] = board[s[0]][s[1]]
        board[s[0]][s[1]] = ''
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
            if m.isLegal(move[0], board):
                return True
        return False

def field_exists(field):
    if field[0] < 0 or field[1] < 0 or field[0] > 7 or field[1] > 7:
        return False
    return True
            
if __name__=='__main__':
    print('chessEngine2')