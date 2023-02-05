import numpy as np
import random as rnd
import pygame
import math
import os
from Explosions import Particle


def auto_loader(ship, gs, faction):
    if ship.missileC > 1 and ship.energy > 1:
        ship.missileC -= 1
        ship.energy -= 1


def jump_drive(ship, gs, faction):
    if ship.energy > ship.height * 4:
        ship.energy -= ship.height * 4
        for i in range(0, 60, 2):
            gs.particle_list.append(
                Particle(ship.centerx + ship.vx * i, ship.centery + ship.vy * i, 1, rnd.randint(0, 360), 1,
                         (220, 220, 255), shrink=0.99, glow=(100, 100, 150)))
        ship.fx = ship.fx + ship.vx * 60
        ship.fy = ship.fy + ship.vy * 60


def chaff(ship, gs, faction):
    if ship.energy > 100:
        ship.energy -= 100
        for f in range(len(gs.missiles)):
            if f != faction:
                for missile in gs.missiles[f]:
                    if missile.target is ship:
                        missile.target = None
        for i in range(0, 10):
            gs.ships[faction].append(Spark(ship.centerx + rnd.randint(-ship.width, ship.width), ship.centery + rnd.randint(-ship.height, ship.height), rnd.randint(0, 359)))


class Spark(pygame.Rect):
    def __init__(self, x, y, angle):
        super().__init__(x, y, 10, 10)
        self.velocity = 6 * rnd.random() + 1
        self.angle = 0
        self.fx = x
        self.fy = y
        self.cx = x
        self.cy = y
        self.health = 5
        self.sop = 0
        self.vx = self.velocity * math.cos(angle)
        self.vy = self.velocity * math.sin(angle)
        self.counter = 0
        self.turrets = []
        self.is_visible = True
        self.is_player = False
        self.image = pygame.image.load(os.path.join('Assets', 'chaff.png')).convert_alpha()

    def scoot(self, gs, faction):
        self.angle = rnd.randint(0, 89)

        self.fx += self.vx
        self.fy += self.vy

        self.x = round(self.fx)
        self.y = round(self.fy)

        self.cx = round(self.x + (
                self.width - self.height * abs(math.sin(self.angle * math.pi / 180)) - self.width * abs(
            math.cos(self.angle * math.pi / 180))) / 2)
        self.cy = round(self.y + (
                self.height - self.width * abs(math.sin(self.angle * math.pi / 180)) - self.height * abs(
            math.cos(self.angle * math.pi / 180))) / 2)
        self.health -= 0.01


AutoLoader = {'function': auto_loader,
              'energy': '1',
              'delay': 0,
              'description': 'This ship is fast',
              'cost': {},
              'name': "Auto Loader"}

JumpDrive = {'function': jump_drive,
             'energy': 'ship.height * 5',
             'delay': 60,
             'description': 'This ship is fast',
             'cost': {},
             'name': "Jump Drive"}

Chaff = {'function': chaff,
         'energy': '100',
         'delay': 240,
         'description': 'This ship is fast',
         'cost': {},
         'name': "Chaff"}

UtilityNames = [AutoLoader, JumpDrive]
