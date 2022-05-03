import pygame
pygame.init()
screen = pygame.display.set_mode([640, 480])

active = True
while active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
            break
    screen.fill((255, 255, 255))
    pygame.draw.rect(screen, (0, 0, 0), (100, 100, 25, 25))
    pygame.display.update()

pygame.quit()
quit()
