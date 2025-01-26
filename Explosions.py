from abc import ABC

import pygame
import math
import random as rnd
import os
from Data.Types import COLOR3, COLOR4, DebrisType, Particle, glow_circle, Vessel, Debris, Entity
from Data.Debris_Types import DEBRISTYPES
from pygame.locals import *


def ShipExplosion(ship: Vessel):

    x_min, x_max = round(ship.x), round(ship.x + ship.width)
    y_min, y_max = round(ship.y), round(ship.y + ship.height)
    size = round(math.log(ship.height))
    events = []
    for num in range(50):
        c = rnd.randint(100, 200)
        events.append(Particle(ship.centerx, ship.centery, -rnd.randint(1, round(math.sqrt(ship.height))),
                               rnd.randint(0, 360), 10,
                               (c + 50, c, 100), shrink=0.75))
        events.append(
            Particle(rnd.randint(x_min, x_max),
                     rnd.randint(y_min, y_max),
                     3 * rnd.random(),
                     rnd.randint(0, 360),
                     size,
                     (rnd.randint(200, 255), rnd.randint(200, 255), 200),
                     shrink=0.98))

    for j in range(size):
        debris = rnd.choice(list(DEBRISTYPES.values()))
        events.append(Debris(ship.centerx, ship.centery, rnd.random(), rnd.randint(0, 360), debris, 6000,
                             rnd.random() - 0.5))

    return events



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


class PhotonExplosion:
    def __init__(self, x, y, gs):
        self.x = x
        self.y = y
        self.gs = gs
        self.timer = 60
        self.radius = 60

    def scoot(self):
        self.timer -= 1
        if self.timer < 1:
            self.radius = 0

    def draw(self, gs):
        image = gs.images['PhotonExplosion'][self.timer]
        x = self.x - gs.x - image.get_width() // 2
        y = self.y - gs.y - image.get_height() // 2
        gs.WIN.blit(image, (x, y), special_flags=BLEND_RGB_ADD)
        # for r in range(self.timer):
        #     glow_circle(gs.WIN, self.x - self.gs.x, self.y - self.gs.y, r, (4, 4, 5))


class OrbExplosion:
    def __init__(self, x, y, gs, ship=None):
        self.ship = ship
        self.x = x
        self.y = y
        self.gs = gs
        self.timer = 10
        self.radius = 60
        self.expanding = True

    def scoot(self):
        if self.ship is not None:
            self.x = self.ship.centerx
            self.y = self.ship.centery
        if self.expanding:
            if self.timer < self.radius:
                self.timer += 1
            else:
                self.expanding = False
        else:
            self.timer -= 1
        if self.timer < 1:
            self.radius = 0

    def draw(self, gs):
        image = gs.images['OrbExplosion'][self.timer]
        x = self.x - gs.x - image.get_width() // 2
        y = self.y - gs.y - image.get_height() // 2
        gs.WIN.blit(image, (x, y), special_flags=BLEND_RGB_ADD)
        # for r in range(self.timer // 2):
        #     glow_circle(gs.WIN, self.x - self.gs.x, self.y - self.gs.y, r, (5, 4, 1))


"""EXPLOSION DAMAGE CALCULATION"""


def ExplosionDamage(max_damage, xo, yo, exp, entity_list):
    events = []
    for target in entity_list:
        d = (math.sqrt((target.centerx - xo) ** 2 + (target.centery - yo) ** 2))
        r = math.sqrt(target.height * target.width)
        if d < exp + r:
            damage = round(2 * max_damage / (1 + math.exp((d + 1) / (r + exp + 1))))
            events += target - damage
            target.heat += damage
    return events


"""PARTICLE CLASS"""

