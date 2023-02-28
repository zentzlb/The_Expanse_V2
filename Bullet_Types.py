import pygame
import os
import numpy as np
import random as rnd
import math
from Explosions import Particle, PAExplosion, glow_circle, trans_circle
from Weapon_Class import Bullet, Beam
from pygame.locals import *

pygame.mixer.init()


def init_bullet(ship, gs, faction):
    if ship.is_ship:
        pos = ship.center + ship.Q.transpose().dot(ship.ship_type.bullet_pos[ship.bullet_sel]) - np.array(
            [ship.bullet_types[ship.bullet_sel].width // 2, ship.bullet_types[ship.bullet_sel].height // 2])
    else:
        pos = ship.center - np.array([ship.bullet_types[ship.bullet_sel].width // 2, ship.bullet_types[ship.bullet_sel].height // 2])
    bullet = Bullet(pos[0], pos[1], ship.angle,
                    ship.bullet_types[ship.bullet_sel], faction, gs)
    gs.bullets[faction].append(bullet)


def init_spray(ship, gs, faction):
    if ship.is_ship:
        pos = ship.center + ship.Q.transpose().dot(ship.ship_type.bullet_pos[ship.bullet_sel]) - np.array(
            [ship.bullet_types[ship.bullet_sel].width // 2, ship.bullet_types[ship.bullet_sel].height // 2])
    else:
        pos = ship.center - np.array([ship.bullet_types[ship.bullet_sel].width // 2, ship.bullet_types[ship.bullet_sel].height // 2])
    bullet = Bullet(pos[0], pos[1], ship.angle + rnd.randint(-10, 10),
                    ship.bullet_types[ship.bullet_sel], faction, gs)
    gs.bullets[faction].append(bullet)


def init_beam(ship, gs, faction):
    if ship.is_ship:
        pos = ship.center + ship.Qt.dot(ship.ship_type.bullet_pos[ship.bullet_sel])
    else:
        pos = ship.center
    beam = Beam(pos[0], pos[1], ship.angle, ship.bullet_types[ship.bullet_sel], faction, gs)
    gs.lines.append(beam)


def draw_bullet(bullet, gs):
    gs.WIN.blit(bullet.image, (bullet.x - gs.x, bullet.y - gs.y))


def draw_flame(bullet, gs):
    scale = (bullet.range / bullet.velocity - bullet.timer) / 10
    radius1 = 2 + round(scale/2)
    # radius2 = 1 + bullet.timer // 40
    x = bullet.centerx - gs.x
    y = bullet.centery - gs.y
    r = 255 / (1 + scale)
    g = rnd.randint(0, 200) / (1 + scale)
    color1 = (r, g, 0)
    surf = pygame.Surface((radius1 * 2, radius1 * 2))
    surf.set_colorkey((0, 0, 0))
    pygame.draw.circle(surf, color1, (radius1, radius1), radius1)
    gs.WIN.blit(surf, (x - radius1, y - radius1), special_flags=BLEND_RGB_ADD)


def draw_beam(beam, gs):
    shift = np.array([gs.x, gs.y])
    p1 = beam.p1 - shift
    p2 = beam.p2 - shift
    pygame.draw.line(gs.WIN, beam.color, p1, p2, width=1)
    glow_circle(gs.WIN, p2[0], p2[1], rnd.randint(5, 10), (150, 50, 0, 50))
    glow_circle(gs.WIN, p1[0], p1[1], rnd.randint(3, 5), (150, 50, 0, 50))


def cannon(self, gs, dmglist):
    for i in dmglist:
        self.targets[i].health -= self.damage  # + bonus
        self.targets[i].heat += self.damage
    self.timer = 0


def heat_cannon(self, gs, dmglist):
    for i in dmglist:
        self.targets[i].health -= self.damage  # + bonus
        self.targets[i].heat += 2 * self.damage
    self.timer = 0


def flame(self, gs, dmglist):
    for i in dmglist:
        self.targets[i].health -= self.damage  # + bonus
        self.targets[i].heat += 2 * self.damage
    self.timer = 0
    # gs.bullets[self.faction].remove(self)


def plasma(self, gs, dmglist):
    for i in dmglist:
        self.targets[i].health -= self.damage
        self.targets[i].heat += self.damage
    explosion = PAExplosion(self.centerx, self.centery, gs)
    gs.explosion_group.add(explosion)
    self.timer = 0
    # gs.bullets[self.faction].remove(self)


def heat_laser(self, gs, ship):
    ship.heat += 1
    gs.particle_list2.append(Particle(self.p2[0], self.p2[1], 5, rnd.randint(0, 360), 3, self.color, shrink=0.5))


def rail(self, gs, dmglist):
    for i in dmglist:
        self.targets[i].health -= self.damage
        self.targets[i].heat += self.damage
    for num in range(8):
        gs.particle_list2.append(
            Particle(self.centerx, self.centery, 3, rnd.randint(0, 360), 10, (0, 223, 255), shrink=0.5))


"""FLAME THROWER IMAGE"""
flame_image = pygame.Surface((6, 6), pygame.SRCALPHA)
# flame_image.set_colorkey((0, 0, 0))
pygame.draw.circle(flame_image, (255, 200, 0, 100), (3, 3), 3)
pygame.draw.circle(flame_image, (255, 0, 0, 150), (3, 3), 1)

AutoCannon = {'velocity': 17,
              'damage': 4,
              'energy': 13,
              'range': 3000,
              'delay': 12,
              'targets_missiles': True,
              'height': 10,
              'width': 10,
              'cost': {},
              'name': "AutoCannon",
              'image': pygame.image.load(os.path.join('Assets', 'bullet.png')),
              'l_image': pygame.image.load(os.path.join('Assets', 'AutoCannon_Launcher.png')),
              'sound': pygame.mixer.Sound(os.path.join('Assets', 'AutoCannon_launch.mp3')),
              'function': cannon,
              'init': init_bullet,
              'draw': draw_bullet}

AutoCannon2 = {'velocity': 15,
               'damage': 5,
               'energy': 15,
               'range': 2500,
               'delay': 12,
               'targets_missiles': True,
               'height': 10,
               'width': 10,
               'cost': {},
               'name': "AP AutoCannon",
               'image': pygame.image.load(os.path.join('Assets', 'bulletAP.png')),
               'l_image': pygame.image.load(os.path.join('Assets', 'AutoCannonAP_Launcher.png')),
               'sound': pygame.mixer.Sound(os.path.join('Assets', 'AutoCannon_launch.mp3')),
               'function': cannon,
               'init': init_bullet,
               'draw': draw_bullet}

AutoCannon3 = {'velocity': 15,
               'damage': 4,
               'energy': 15,
               'range': 2500,
               'delay': 12,
               'targets_missiles': True,
               'height': 10,
               'width': 10,
               'cost': {},
               'name': "IN AutoCannon",
               'image': pygame.image.load(os.path.join('Assets', 'bulletIN.png')),
               'l_image': pygame.image.load(os.path.join('Assets', 'AutoCannonIN_Launcher.png')),
               'sound': pygame.mixer.Sound(os.path.join('Assets', 'AutoCannon_launch.mp3')),
               'function': heat_cannon,
               'init': init_bullet,
               'draw': draw_bullet}

Plasma = {'velocity': 10.5,
          'damage': 55,
          'energy': 140,
          'range': 1000,
          'delay': 120,
          'targets_missiles': False,
          'height': 15,
          'width': 15,
          'cost': {},
          'name': "Plasma",
          'image': pygame.image.load(os.path.join('Assets', 'Plasma.png')),
          'l_image': pygame.image.load(os.path.join('Assets', 'Plasma_Launcher.png')),
          'sound': pygame.mixer.Sound(os.path.join('Assets', 'PA_launch.mp3')),
          'function': plasma,
          'init': init_bullet,
          'draw': draw_bullet}

Railgun = {'velocity': 30,
           'damage': 10,
           'energy': 190,
           'range': 10000,
           'delay': 240,
           'targets_missiles': False,
           'height': 30,
           'width': 30,
           'cost': {},
           'name': "Railgun",
           'image': pygame.image.load(os.path.join('Assets', 'railgun.png')),
           'l_image': pygame.image.load(os.path.join('Assets', 'Railgun_Launcher.png')),
           'sound': pygame.mixer.Sound(os.path.join('Assets', 'railgun_launch.mp3')),
           'function': rail,
           'init': init_bullet,
           'draw': draw_bullet}

FlameThrower = {'velocity': 10,
                'damage': 1,
                'energy': 1.5,
                'range': 600,
                'delay': 1,
                'targets_missiles': False,
                'height': 6,
                'width': 6,
                'cost': {},
                'name': "Flame Thrower",
                'image': flame_image,
                'l_image': pygame.image.load(os.path.join('Assets', 'FlameThrower_Launcher.png')),
                'sound': None,
                'function': flame,
                'init': init_spray,
                'draw': draw_flame}

BeamLaser = {'velocity': math.inf,
              'damage': 0,
              'energy': 1,
              'range': 900,
              'delay': 1,
              'targets_missiles': False,
              'height': 0,
              'width': 0,
              'cost': {},
              'name': "Beam Laser",
              'image': pygame.Surface((1, 1)),
              'l_image': pygame.image.load(os.path.join('Assets', 'BeamLaser_Launcher.png')),
              'sound': None,
              'function': heat_laser,
              'init': init_beam,
              'draw': draw_beam}

BulletNames = [AutoCannon, AutoCannon2, AutoCannon3, Plasma, Railgun, FlameThrower, BeamLaser]
