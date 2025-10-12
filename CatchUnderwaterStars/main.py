import pygame
from hero import Hero

pygame.init()

pygame.display.set_caption('CATCH UNDERWATER STARTS')
window = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()
background = pygame.transform.scale(pygame.image.load('background.jpg'), (1200, 800))
hero = Hero(window)


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

    window.blit(background, (0, 0))
    hero.update()
    pygame.display.update()
    clock.tick(60)


