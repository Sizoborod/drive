import pygame
from random import *


class Plane(pygame.sprite.Sprite):
    def __init__(self, y, speed, surf, group):
        pygame.sprite.Sprite.__init__(self)
        self.image = surf
        self.rect = self.image.get_rect(center=(0, y))
        self.speed = speed
        self.add(group)

    def update(self, *args):
        if self.rect.x < args[0] - 20:
            self.rect.x += self.speed
        else:
            self.kill()


def createPlane(group):
    indx = randint(0, len(plane_surf) - 1)
    y = randint(20, H - 20)
    speed = randint(1, 4)

    return Plane(y, speed, plane_surf[indx], group)

pygame.init()

BLACK = (0, 0, 0)
W, H = 1000, 570

sc = pygame.display.set_mode((W, H))
bg = pygame.image.load('img/back.png').convert()
pygame.time.set_timer(pygame.USEREVENT, 5000)

plane_images = ['plane.png']
plane_surf = [pygame.image.load('img/'+path).convert_alpha() for path in plane_images]

planes = pygame.sprite.Group()

clock = pygame.time.Clock()
FPS = 60

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.USEREVENT:
            createPlane(planes)

    sc.blit(bg, (0, 0))
    planes.draw(sc)
    pygame.display.update()

    clock.tick(FPS)

    planes.update(H)