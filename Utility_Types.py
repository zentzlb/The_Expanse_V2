import numpy as np
import random as rnd
from Explosions import Particle


def auto_loader(ship, gs):
    if ship.missileC > 1 and ship.energy > 1:
        ship.missileC -= 1
        ship.energy -= 1


def jump_drive(ship, gs):
    if ship.energy > ship.height * 4:
        ship.energy -= ship.height * 4
        for i in range(0, 60, 2):
            gs.particle_list.append(Particle(ship.centerx + ship.vx * i, ship.centery + ship.vy * i, 1, rnd.randint(0, 360), 1, (220, 220, 255), shrink=0.99, glow=(100, 100, 150)))
        ship.fx = ship.fx + ship.vx * 60
        ship.fy = ship.fy + ship.vy * 60


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

UtilityNames = [AutoLoader, JumpDrive]

