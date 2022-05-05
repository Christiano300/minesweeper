import pygame
from random import choice
pygame.init()

BOARDWIDTH = 5
BOARDHEIGHT = 5
shift_pressed = False
size = width, height = BOARDWIDTH * 25, BOARDHEIGHT * 25 + 50
screen = pygame.display.set_mode(size)

NUMBER_OF_MINES = 1
tiles = pygame.sprite.Group()
clock = pygame.time.Clock()

imagenames = ["empty", "1", "2", "3", "4",
              "5", "6", "7", "8", "flag", "mine", "tile"]
images = [pygame.image.load(
    f"files/{i}.png").convert_alpha() for i in imagenames]


class Tile:
    def __init__(self, x, y):
        self.state = 0
        self.hidden = True
        self.flagged = False
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
                    x = self.x + i
                    y = self.y + j
                    if x >= 0 and y >= 0:
                        try:
                            if board[y][x].state == 10:
                                total += 1
                        except IndexError:
                            pass
            self.state = total

    def reveal(self):
        self.hidden = False
        if self.state == 0:
            for i in range(-1, 2):
                for j in range(-1, 2):
                    x = self.x + i
                    y = self.y + j
                    if x >= 0 and y >= 0:
                        try:
                            tile = board[y][x]
                            if tile.state in range(9) and tile.hidden == True:
                                tile.reveal()
                        except IndexError:
                            pass

    def draw(self):
        if self.hidden:
            screen.blit(images[-1], (self.x * 25, self.y * 25 + 50))
            if self.flagged:
                screen.blit(images[9], (self.x * 25, self.y * 25 + 50))
        else:
            screen.blit(images[0], (self.x * 25, self.y * 25 + 50))
            screen.blit(images[self.state], (self.x * 25, self.y * 25 + 50))

def process_input(pos, reveal):
    x = pos[0] // 25
    y = (pos[1] - 50) // 25
    if x >= 0 and y >= 0:
        tile = board[y][x]
        if reveal:
            if not tile.flagged:
                tile.reveal()
        else:
            if tile.hidden:
                if tile.flagged:
                    tile.flagged = False
                else:
                    tile.flagged = True
    count = sum([sum([int(j.flagged) for j in i]) for i in board])
    if count == NUMBER_OF_MINES:
        quit()

board = [[Tile(i, j) for i in range(BOARDWIDTH)] for j in range(BOARDHEIGHT)]
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
            
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                process_input(event.pos, True)
            elif event.button == 3:
                process_input(event.pos, False) 

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                process_input(pygame.mouse.get_pos(), True)
            elif event.key == pygame.K_f:
                process_input(pygame.mouse.get_pos(), False)
            elif event.key == pygame.K_c:
                for i in board:
                    for j in i:
                        j.hidden = False
            elif event.key == pygame.K_LSHIFT:
                shift_pressed = True
            elif event.key == pygame.K_r:
                if shift_pressed:
                    for i in board:
                        for j in i:
                            if j.state == 10 and j.hidden == False:
                                j.hidden = True
                else:
                    for i in board:
                        for j in i:
                            j.state = 0
                            j.hidden = True
                    for i in range(NUMBER_OF_MINES):
                        choice(choice(board)).set_mine()
                    for row in board:
                        for tile in row:
                            tile.determine_mines()
                    	
        elif event.type == pygame.KEYUP and event.key == pygame.K_LSHIFT:
            shift_pressed = False

    for row in board:
        for tile in row:
            tile.draw()
    pygame.display.update()
    clock.tick(60)