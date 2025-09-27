# Essential imports
import sys
import pygame
from typing import TypeAlias
import math
import random as rnd

position: TypeAlias = tuple[float, float]

# Pygame setup
pygame.init()
FPS = 120
WIDTH = 800
HEIGHT = 450
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Window")
CLOCK = pygame.time.Clock()
MOUSE_POS = (0, 0)

# Create gravity variable and projectile force variable
GRAVITY = 0.01

class Mixer:
    def __init__(self, *paths):
        self.sounds = [pygame.mixer.Sound(path) for path in paths]

    def play(self, i: int, volume: int = 1):
        if i < len(self.sounds):
            self.sounds[i].set_volume(volume)
            self.sounds[i].play(loops=0, fade_ms=50)



class Drop:
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 2

    def update(self):
        self.vy += GRAVITY
        self.x += self.vx
        self.y += self.vy

    def draw(self, surf: pygame.Surface):
        pygame.draw.circle(surf, (100, 100, 255), (self.x, self.y), radius=3)


class Link:
    def __init__(self, size: float, xy1: position, xy2: position):
        self.size = size
        self.xy1 = xy1
        self.xy2 = xy2
        self.vx = 0
        self.vy = 0

    def update(self, pos: position):
        self.vy += GRAVITY
        self.xy1 = pos
        x1, y1 = self.xy1
        x2, y2 = self.xy2
        x2 += self.vx
        y2 += self.vy
        dx = x1 - x2
        dy = y1 - y2
        angle = math.atan2(dy, dx)
        x2 = x1 - self.size * math.cos(angle)
        y2 = y1 - self.size * math.sin(angle)
        self.xy2 = (x2, y2)

class Chain:
    def __init__(self, links: list[Link]):
        self.links: list[Link] = links

    def update(self, pos: position):
        for link in self.links:
            link.update(pos)
            pos = link.xy2

    def draw(self, surf: pygame.Surface):
        for link in self.links:
            pygame.draw.line(surf, (90, 90, 90), link.xy1, link.xy2, width=3)

SIZE = 10
MIXER = Mixer(*[r"C:\Users\logan\PycharmProjects\Space_Arcade\Assets\AutoCannon_launch.mp3",
               r"C:\Users\logan\PycharmProjects\Space_Arcade\Assets\missile_launch.mp3",
               r"C:\Users\logan\PycharmProjects\Space_Arcade\Assets\PA_launch.mp3",
               r"C:\Users\logan\PycharmProjects\Space_Arcade\Assets\railgun_launch.mp3"])
CHAIN = Chain([Link(SIZE, (200, 200+i*SIZE), (200, 200+(i+1)*SIZE)) for i in range(20)])
DROPS: list[Drop] = []

# Main display loop
while True:
    SCREEN.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            MOUSE_POS = event.pos

        if event.type == pygame.KEYDOWN:
            str_ = event.unicode
            print(str_)
            try:
                i = int(str_)
                MIXER.play(i)
            except ValueError:
                print('not working')
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()

    CHAIN.update(MOUSE_POS)
    if rnd.random() > 0.99:
        end_link = CHAIN.links[-1]
        DROPS.append(Drop(*end_link.xy2))
    CHAIN.draw(SCREEN)
    for drop in DROPS:
        drop.update()
        drop.draw(SCREEN)
    DROPS = [drop for drop in DROPS if drop.y <= HEIGHT]
    pygame.display.flip()
    CLOCK.tick(FPS)

