import os
import sys
from random import randint, randrange
import pygame

pygame.init()
size = width, height = 500, 500
screen = pygame.display.set_mode(size)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


class Bomb(pygame.sprite.Sprite):
    image_boom = load_image('boom.png')
    image = load_image('bomb.png')

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Bomb.image
        self.rect = self.image.get_rect()
        self.rect.x = randint(50, 450)
        self.rect.y = randint(50, 450)

    def update(self, *args):
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image = Bomb.image_boom
            self.rect.x -= 20
            self.rect.y -= 20


running = True
pygame.display.set_caption('Машинка')
all_sprite = pygame.sprite.Group()
for i in range(20):
    all_sprite.add(Bomb())
flag = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        all_sprite.update(event)
    all_sprite.draw(screen)
    pygame.display.flip()

pygame.quit()
