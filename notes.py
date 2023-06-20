import globals
import chessEngine

sqSelected=()
playerClicks = () 
while RUNNING:
    for event in p.event.get():
        if event.type ==p.QUIT:
            RUNNING = False
        elif event.type == p.MOUSEBUTTONDOWN:
            location = p.mouse.get_pos
            col = location[0]//FIELDSIZE
            row = location[1]//FIELDSIZE
            if sqSelected == (row, col): #clicking same sq twice
                sqSelected = () #deselect
                playerClicks = [] #clear player click
            else:
                sqSelected = (row,col)
                playerClicks.append(sqSelected)
            if len(playerClicks) == 2:
                move = chessEngine.Move(playerClicks(0),playerClicks(1), gs.board )
            



