import os
import math
import random as rnd
import pygame
from Explosions import Particle, ExplosionDamage

pygame.mixer.init()
pygame.display.init()


def explosion(self, gs):
    for i in range(100):
        c = rnd.randint(100, 200)
        gs.particle_list2.append(Particle(self.centerx, self.centery, -rnd.randint(1, self.er // 20),
                                          rnd.randint(0, 360), 10,
                                          (c + 50, c, 100), shrink=0.5))

    ExplosionDamage(self.exp_damage, self.centerx, self.centery, self.er, gs.targets[self.faction], gs)


def proximity(self, gs):

    if self.timer > self.arm:
        dr2 = self.mine_type.det_radius * self.mine_type.det_radius
        for target in gs.targets[self.faction]:
            dx = target.centerx - self.centerx
            dy = target.centery - self.centery
            if dx * dx + dy * dy < dr2:
                explosion(self, gs)
                gs.missiles[self.faction].remove(self)
                break


def black_hole(self, gs):
    if self.timer > self.arm:
        for i in range(self.mine_type.par_num):
            angle = rnd.randint(-180, 180)
            r = rnd.randint(95, 105)
            x = self.centerx + r * math.sin(math.pi * angle / 180)
            y = self.centery + r * math.cos(math.pi * angle / 180)
            gs.particle_list2.append(Particle(x, y, 10, angle + 180, 10, (rnd.randint(0, 30), 0, rnd.randint(0, 100))))
    else:
        for i in range(self.timer // 10):
            angle = rnd.randint(-180, 180)
            r = rnd.randint(1, 100)
            x = self.centerx + r * math.sin(math.pi * angle / 180)
            y = self.centery + r * math.cos(math.pi * angle / 180)
            gs.particle_list2.append(
                Particle(x, y, 0, 0, 10, (rnd.randint(0, 30), 0, rnd.randint(0, 100))))
    if self.grav and self.timer > self.arm:
        for ship in gs.targets[self.faction]:
            dx = ship.centerx - self.centerx
            dy = ship.centery - self.centery
            r2 = dx * dx + dy * dy
            if r2 < 1000000:
                ship.vx -= (dx * 50) / (r2 + 1)
                ship.vy -= (dy * 50) / (r2 + 1)
                if ship.vx * ship.vx + ship.vy * ship.vy > ship.velocity * ship.velocity:
                    ship.vx = ship.vx * ship.velocity / math.sqrt(ship.vx ** 2 + ship.vy ** 2)
                    ship.vy = ship.vy * ship.velocity / math.sqrt(ship.vx ** 2 + ship.vy ** 2)

    if self.collidelist(gs.targets[self.faction]) != -1:  # mine detonates
        # if self.exptype is not None:
        #     explosion = self.exptype(self.centerx, self.centery, gs)
        #     gs.explosion_group.add(explosion)
        dmgList = self.collidelistall(gs.targets[self.faction])
        for i in dmgList:
            gs.targets[self.faction][i].health -= self.damage
            gs.targets[self.faction][i].heat += 2 * self.damage
        if not self.pen:
            gs.missiles[self.faction].remove(self)


ProximityMine = {'damage': 0,
                 'exp_damage': 100,
                 'exp_radius': 500,
                 'det_radius': 300,
                 'energy': 0,
                 'time': 1600,
                 'delay': 80,
                 'arm': 80,
                 'height': 20,
                 'width': 20,
                 'par_num': 0,
                 'par_rnd': 0,
                 'cost': {},
                 'name': "Proximity Mine",
                 'pen': False,
                 'emp': False,
                 'grav': False,
                 'image': pygame.image.load(os.path.join('Assets', 'space_mine.png')),
                 'sound': pygame.mixer.Sound('Assets//missile_launch.mp3'),
                 'function': proximity,
                 'explosion': explosion}

BlackHole = {'damage': 1,
             'exp_damage': 0,
             'exp_radius': 0,
             'det_radius': 0,
             'energy': 400,
             'time': 3200,
             'delay': 400,
             'arm': 160,
             'height': 19,
             'width': 19,
             'par_num': 30,
             'par_rnd': 0,
             'cost': {},
             'name': "Black Hole",
             'pen': True,
             'emp': False,
             'grav': True,
             'image': pygame.image.load(os.path.join('Assets', 'black_hole.png')),
             'sound': pygame.mixer.Sound('Assets//missile_launch.mp3'),
             'function': black_hole,
             'explosion': None}

MineNames = [ProximityMine, BlackHole]
