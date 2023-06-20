import globals

###GAMESTATE TO FEN FUNCTION###
def getBoard():
    result = []
    for i, row in enumerate(globals.BOARD):
        space = 0
        for y, field in enumerate(row):
            if field != '':
                if space > 0:
                    result.append(str(space))
                    space = 0
                result.append(field)
            else:
                space = 1 + space
            if y == 7:
                if space > 0:
                    result.append(str(space))
                    space = 0
                if i != 7:
                    result.append('/')
    result.append(' ')
    result.append('w' if globals.TURN % 2 == 0 else 'b')
    result.append(' ')
    result.append('KQkq')
    result.append(' - 0 ')
    result.append(str((globals.TURN+1)//2))
    result = ''.join(result)
    return result

###FEN TO NUMERALTOGAMESTATE LOADING FUNCTION###
def numeralLoadBoard(data = globals.STARTFEN):
    result = []
    for i in data.split('/'):
        for j in i:
            if j.isnumeric():
                for i in range(int(j)):
                    result.append(0)
            else:
                result.append(globals.FIGURESIDS[j])
    globals.BOARD = result

###GAMESTATE LOADING FUNCTION###
def loadBoard(data = globals.STARTFEN):
    result = []
    for i in data.split('/'):
        row = []
        for j in i:
            if j.isnumeric():
                for i in range(int(j)):
                    row.append('')
            else:
                row.append(j)
        result.append(row)
    globals.BOARD = result
