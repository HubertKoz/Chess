import globals
import copy

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

            # Switch the turn to the other player
            self.whitetoMove = not self.whitetoMove
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
    
    def pawn_move(self):
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
        return False
    
    def doesnt_end_with_check(self):
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