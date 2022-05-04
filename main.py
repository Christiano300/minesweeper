import pygame
from random import choice
pygame.init()
size = width, height = 225, 275
screen = pygame.display.set_mode(size)
BOARDWIDTH = 9
BOARDHEIGHT = 9
NUMBER_OF_MINES = 10
tiles = pygame.sprite.Group()
clock = pygame.time.Clock()

imagenames = ["empty", "1", "2", "3", "4", "5", "6", "7", "8", "flag", "mine", "tile"]
images = [pygame.image.load(f"files/{i}.png").convert_alpha() for i in imagenames]

class Tile:
    def __init__(self, x, y):
        # Set Tile State: 0 means empty, 10 means mine,
        # 1-8 means number of mines,9 means flag
        self.state = 0
        self.hidden = True
        self.x = x
        self.y = y
    
    def set_mine(self):
        if self.state == 10:
            choice(choice(board)).set_mine()
        else:
            self.state = 10
            
    def determine_mines(self):
        if self.state == 0:
            total = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    xpos = self.x + i
                    ypos = self.y + j
                    if xpos > 0 and ypos > 0 and i * j:
                        try:
                            if board[xpos][ypos].state == 10:
                                total += 1
                        except IndexError:
                            pass
            self.state = total
    
    def reveal(self):
        if self.state == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    xpos = self.x + i
                    ypos = self.y + j
                    if xpos > 0 and ypos > 0 and i * j:
                        try:
                            if board[xpos][ypos].state in range(9):
                                board[xpos][ypos].reveal()
                        except IndexError:
                            pass
        self.hidden = False
    
    def draw(self):
        if self.hidden:
            screen.blit(images[-1], (self.x * 25, self.y * 25 + 50))
        else:
            screen.blit(images[self.state], (self.x * 25, self.y * 25 + 50))

board = [[Tile(i, j) for i in range(BOARDHEIGHT)] for j in range(BOARDWIDTH)]
for i in range(NUMBER_OF_MINES):
    choice(choice(board)).set_mine()
for row in board:
    for tile in row:
        tile.determine_mines()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    for row in board:
        for tile in row:
            tile.draw()
    pygame.display.update()
    clock.tick(60)