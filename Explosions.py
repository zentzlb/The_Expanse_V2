import pygame
import math
import random as rnd
from pygame.locals import *

"""SHIP EXPLOSION"""


# class ShipExplosion(pygame.sprite.Sprite):
#     def __init__(self, x, y, gs):
#         pygame.sprite.Sprite.__init__(self)
#         self.images = []
#         for num in range(1, 16):
#             img = pygame.image.load(f"Assets/Blast{num}.png")
#             img = pygame.transform.scale(img, (90, 90))
#             self.images.append(img)
#         self.index = 0
#         self.image = self.images[self.index]
#         self.x = x
#         self.y = y
#         self.gs = gs
#         self.rect = self.image.get_rect()
#         self.rect.center = [x - gs.x, y - gs.y]
#         self.counter = 0
#
#     def update(self):
#         explosion_speed = 2
#         self.counter += 1
#         self.rect.center = [self.x - self.gs.x, self.y - self.gs.y]
#
#         if self.counter >= explosion_speed and self.index < len(self.images) - 1:
#             self.counter = 0
#             self.index += 1
#             self.image = self.images[self.index]
#
#         if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
#             self.kill()

def ShipExplosion(ship, gs):
    size = round(math.log(ship.height))
    for num in range(50):
        c = rnd.randint(100, 200)
        gs.particle_list2.append(Particle(ship.centerx, ship.centery, -rnd.randint(1, round(math.sqrt(ship.height))),
                                          rnd.randint(0, 360), 10,
                                          (c + 50, c, 100), shrink=0.75))
        gs.particle_list2.append(
            Particle(rnd.randint(ship.x, ship.x+ship.width), rnd.randint(ship.y, ship.y+ship.height), 3*rnd.random(), rnd.randint(0, 360), size, (rnd.randint(200, 255), rnd.randint(200, 255), 200), shrink=0.98))



"""MISSILE EXPLOSION"""


class MissileExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y, gs, exp_radius):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 11):
            img = pygame.image.load(f"Assets/smallblast{num}.png")
            img = pygame.transform.scale(img, (exp_radius * 2, exp_radius * 2))
            self.images.append(img)
            gs.particle_list2.append(Particle(x, y, -rnd.randint(exp_radius // 10 - 1, exp_radius // 10 + 1),
                                              rnd.randint(0, 360), 10,
                                              (rnd.randint(100, 255), rnd.randint(100, 255), 100)))
        self.index = 0
        self.image = self.images[self.index]
        self.x = x
        self.y = y
        self.gs = gs
        self.rect = self.image.get_rect()
        self.rect.center = [x - gs.x, y - gs.y]
        self.counter = 0

    def update(self):
        explosion_speed = 2
        self.counter += 1

        self.rect.center = [self.x - self.gs.x, self.y - self.gs.y]

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


"""RAIL EXPLOSION"""


class RailExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y, gs):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 8):
            img = pygame.image.load(f"Assets/railgun_blast{num}.png")
            self.images.append(img)
            gs.particle_list2.append(Particle(x, y, 3, rnd.randint(0, 360), 10, (0, 223, 255), shrink=0.5))
        self.index = 0
        self.image = self.images[self.index]
        self.x = x
        self.y = y
        self.gs = gs
        self.rect = self.image.get_rect()
        self.rect.center = [x - gs.x, y - gs.y]
        self.counter = 0

    def update(self):
        explosion_speed = 1
        self.counter += 1
        self.rect.center = [self.x - self.gs.x, self.y - self.gs.y]

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()


"""PA EXPLOSION"""


class PAExplosion(pygame.sprite.Sprite):
    def __init__(self, x, y, gs):
        pygame.sprite.Sprite.__init__(self)
        self.images = []
        for num in range(1, 14):
            img = pygame.image.load(f"Assets/pa_blast{num}.png")
            self.images.append(img)
        self.index = 0
        self.image = self.images[self.index]
        self.x = x
        self.y = y
        self.gs = gs
        self.rect = self.image.get_rect()
        self.rect.center = [x - gs.x, y - gs.y]
        self.counter = 0

    def update(self):
        explosion_speed = 1
        self.counter += 1
        self.rect.center = [self.x - self.gs.x, self.y - self.gs.y]

        if self.counter >= explosion_speed and self.index < len(self.images) - 1:
            self.counter = 0
            self.index += 1
            self.image = self.images[self.index]

        if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
            self.kill()

"""EXPLOSION DAMAGE CALCULATION"""

def ExplosionDamage(max_damage, xo, yo, exp, target_list, gs):
    for target in target_list:
        d = (math.sqrt((target.centerx - xo) ** 2 + (target.centery - yo) ** 2))
        r = math.sqrt(target.height * target.width)
        if d < exp + r:
            damage = round(2 * max_damage / (1 + math.exp((d + 1) / (r + exp + 1))))
            target.health -= damage
            target.heat += damage


"""PARTICLE CLASS"""


class Particle:
    def __init__(self, x, y, v, angle, radius, color, shrink=0, vx=0, vy=0, glow=(0, 0, 0), show=True):
        self.x = x
        self.y = y
        self.fx = x
        self.fy = y
        self.vx = v * math.sin(angle * math.pi / 180) + vx
        self.vy = v * math.cos(angle * math.pi / 180) + vy
        self.color = color
        self.radius = radius
        self.shrink = shrink
        self.glow = glow
        self.show = show

    def update(self):
        self.fx += self.vx
        self.fy += self.vy
        self.x = round(self.fx)
        self.y = round(self.fy)
        if rnd.random() > self.shrink:
            self.radius -= 1
    
    def draw(self, gs):
        pygame.draw.circle(gs.WIN, self.color, (self.x - gs.x, self.y - gs.y), self.radius)
        if self.glow != (0, 0, 0):
            glow_circle(gs.WIN, self.x - gs.x, self.y - gs.y, 2 * self.radius, self.glow)


def trans_circle(display, x, y, radius, color):
    surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(surf, color, (radius, radius), radius)
    display.blit(surf, (x - radius, y - radius))


def glow_circle(display, x, y, radius, color):
    surf = pygame.Surface((radius * 2, radius * 2))
    surf.set_colorkey((0, 0, 0))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    display.blit(surf, (x - radius, y - radius), special_flags=BLEND_RGB_ADD)