import pygame
import numpy as np
import math
import globals
import itertools

###GRAPHICS VARIABLES###
figures = []
white = None
black = None

###CREATING A DISPLAY###
display = pygame.display.set_mode((globals.WIDTH, globals.HEIGHT), pygame.SRCALPHA)

###GRAPHICS INIT FUNCTION###
def start():
    global white
    global black
    ###FIGURES GRAPHICS LOADING###
    for i in range(12):
        figures.append(pygame.transform.scale(pygame.image.load(globals.FIGURESPATH+str(i+1)+'.png'), ((globals.PROPERTIES['boardSize'] - globals.PROPERTIES['frameSize'])/8)))

    white = DropdownList(
        np.array(((globals.WIDTH - globals.PROPERTIES['boardSize'][0])/4, globals.HEIGHT / 6)),
        np.array([(globals.WIDTH - globals.HEIGHT) / 2, globals.HEIGHT / 8]),
        globals.CONTROLS
    )

    black = DropdownList(
        np.array((globals.WIDTH -(globals.WIDTH - globals.PROPERTIES['boardSize'][0])/4, globals.HEIGHT / 6)),
        np.array([(globals.WIDTH - globals.HEIGHT) / 2, globals.HEIGHT / 8]),
        globals.CONTROLS
    )                     

###GRAPHICS MAIN UPDATE FUNCTION###
def update():
    ###SURFACE CREATION###
    display.fill(globals.COLORS['background'])
    ###DRAWING CHESSBOARD AND FIGURES###
    drawChessboard(display, np.array([globals.WIDTH, globals.HEIGHT])/2)
    drawFigures(display, np.array([globals.WIDTH, globals.HEIGHT])/2)
    ###DRAWING BUTTONS###
    font = pygame.font.SysFont("Arial", int(globals.HEIGHT/12))
    text = font.render('White', True, (255, 255, 255))
    display.blit(text, white.pos - np.array([0, globals.HEIGHT/9]) - np.array((text.get_width(), text.get_height()))/2)
    white.draw(display)
    font = pygame.font.SysFont("Arial", int(globals.HEIGHT/12))
    text = font.render('Black', True, (0, 0, 0))
    display.blit(text, black.pos - np.array([0, globals.HEIGHT/9]) - np.array((text.get_width(), text.get_height()))/2)
    black.draw(display)
    ###DRAWING INFO###
    if globals.PAUSE:
        font = pygame.font.SysFont("Arial", int(globals.PROPERTIES['boardSize'][1]/5))
        text = font.render('PAUSED', True, (255, 255, 255))
        display.blit(text, (np.array([globals.WIDTH, globals.HEIGHT])/2 - np.array((text.get_width(), text.get_height()))/2))
    ###FRAME UPDATE###
    pygame.display.flip()
    pygame.display.update()

###CLICK CHECKING FUNCTION###
def check():
    ###SURFACE CREATION###
    display.fill(globals.COLORS['background'])
    ###ELEMENTS UPDATE###
    if white.clickCheck():
        globals.WHITE = white.button.text
    if black.clickCheck():
        globals.BLACK = black.button.text


###FIELD CENTER POSITION CALCULATION FUNCTION###
def calcFields(pos):
    fieldCentres = []
    ###FIELD SIZE CALCULATION###
    fieldSize = globals.PROPERTIES['boardSize']/8
    for i, number in enumerate('87654321'):
        for y, letter in enumerate('ABCDEFGH'):
            ###OFIELD CENTER POSITION CALCULATION###
            field = {
                'pos': np.array(pos - globals.PROPERTIES['boardSize']/2 + fieldSize/2 + fieldSize*np.array([y,i])),
                'symbol': letter+number
            } 
            fieldCentres.append(field)
    return fieldCentres

###CHESSBOARD DRAWING FUNCTION###
def drawChessboard(screen, pos):
    ###CREATING SURFACE###
    surface = pygame.Surface((globals.WIDTH, globals.HEIGHT), pygame.SRCALPHA)
    ###FRAME DRAWING###
    frame = pygame.Rect(pos-(globals.PROPERTIES['boardSize'] + globals.PROPERTIES['frameSize']*2)/2 ,globals.PROPERTIES['boardSize'] + globals.PROPERTIES['frameSize']*2)
    pygame.draw.rect(surface, globals.COLORS['frame'], frame)
    ###FIELD SIZE CALCULATION###
    fieldSize = globals.PROPERTIES['boardSize']/8
    ###BACKGROUND DRAWING###
    background = pygame.Rect(pos-globals.PROPERTIES['boardSize']/2,
                                fieldSize*8)
    pygame.draw.rect(surface, globals.COLORS['darkSquare'], background)
    for i, field in enumerate(calcFields(pos)):
        ###FIELD COLOUR CHOICE###
        color = globals.COLORS['lightSquare'] if (i+math.floor(i/8)) % 2 != 0 else globals.COLORS['darkSquare']
        ###FIELD DRAWING###
        rect = pygame.Rect(field['pos']-fieldSize/2,
                                    fieldSize)
        pygame.draw.rect(surface, color, rect)
        ###OPTIONAL FIELD SYMBOL DRAWING###
        if globals.SHOWFIELDNAMES:
            color = globals.COLORS['lightSquare'] if (i + math.floor(i / 8)) % 2 == 0 else globals.COLORS[
                'darkSquare']
            font = pygame.font.SysFont("Arial", int(fieldSize[1] / 3 * 2))
            text = font.render(field['symbol'], True, color)
            surface.blit(text, (field['pos']-fieldSize/2+np.array([text.get_width(), text.get_height()])/4))
    screen.blit(surface, [0, 0])

###FIGURES DRAWING FUNCTION###
def drawFigures(screen, pos):
    ###CREATING SURFACE###
    surface = pygame.Surface((globals.WIDTH, globals.HEIGHT), pygame.SRCALPHA)
    ###FIELD SIZE CALCULATION###
    fieldSize = globals.PROPERTIES['boardSize']/8
    for figure, field in zip(list(itertools.chain(*globals.BOARD)), calcFields(pos)):
        ###FIGURE DRAWING###
        if figure != '':
            surface.blit(figures[globals.FIGURESIDS[figure]-1], field['pos']-fieldSize/2)
    screen.blit(surface, [0, 0])

###BUTTON CLASS###
class Button:
    def __init__(self, pos, size, text = ''):
        self.size = size
        self.pos = pos
        self.text = text
        self.color = np.array((70, 70, 70))
        self.border = 2
        self.borderColor = np.array((0, 0, 0))
        self.isOver = False

    def draw(self, screen):
        ###CHECK IF MOUSE IS OVER###
        self.checkIfOver()
        ###CREATING A SURFACE###
        surface = pygame.Surface((globals.WIDTH, globals.HEIGHT), pygame.SRCALPHA)
        # rysowanie ramy
        fill = pygame.Rect(self.pos - (self.size + self.border*2)/2, self.size + self.border*2)
        pygame.draw.rect(surface, self.borderColor if not self.isOver else self.borderColor*globals.COLORS['highlight'], fill)
        # rysowanie przycisku
        fill = pygame.Rect(self.pos-self.size/2, self.size)
        pygame.draw.rect(surface, self.color if not self.isOver else self.color*globals.COLORS['highlight'], fill)
        # rysowanie tekstu
        font = pygame.font.SysFont("Arial", int(self.size[1] / 3 * 2))
        text = font.render(self.text, True, (255, 255, 255))
        surface.blit(text, (self.pos - np.array((text.get_width(), text.get_height()))/2))
        # nakładanie powierzchni
        screen.blit(surface, [0, 0])

    def checkIfOver(self):
        mouseX, mouseY = pygame.mouse.get_pos()
        if abs(self.pos[0] - mouseX) < self.size[0]/2 and abs(self.pos[1] - mouseY) < self.size[1]/2:
            self.isOver = True
        else:
            self.isOver = False

    def clickCheck(self):
        if self.isOver:
            return True

class DropdownList:
    def __init__(self, pos, size, options):
        self.size = size
        self.pos = pos
        self.color = np.array((70, 70, 70))
        self.border = 2
        self.borderColor = np.array((0, 0, 0))
        self.isOver = False
        self.rolledDown = False
        self.values = ['1', '2', '3']
        self.currentValue = self.values[0]
        self.button = Button(self.pos, self.size, text=options[0])
        self.list = []
        for i, option in enumerate(options):
            if i > 0:
                self.list.append(Button(self.pos + self.size * (0, i), self.size, text=option))

    def clickCheck(self):
        if self.button.isOver:
            if self.rolledDown:
                self.rolledDown = False
            else:
                self.rolledDown = True
        if self.rolledDown:
            for i, button in enumerate(self.list):
                if button.clickCheck():
                    self.list.append(self.button)
                    self.button = self.list.pop(i)
                    self.list[-1].pos, self.button.pos = self.button.pos, self.list[-1].pos
                    self.rolledDown = False
                    return True
                    

    def draw(self, screen):
        if self.rolledDown:
            surface = pygame.Surface((globals.WIDTH, globals.HEIGHT), pygame.SRCALPHA)
            self.button.draw(surface)
            if self.rolledDown:
                for button in self.list:
                    button.draw(surface)
            screen.blit(surface, [0,0])
        else:
            surface = pygame.Surface((globals.WIDTH, globals.HEIGHT), pygame.SRCALPHA)
            self.button.draw(surface)
            screen.blit(surface, [0,0])
