import pygame
import os
import random as rnd
from Explosions import Particle, PAExplosion

pygame.mixer.init()


def cannon(self, gs, dmglist):
    for i in dmglist:
        # try:
        #     bonus = gs.targets[self.faction][i].sop // 5
        # except:
        #     bonus = 0

        gs.targets[self.faction][i].health -= self.damage  # + bonus
        gs.targets[self.faction][i].sop += 2 * self.damage
    gs.bullets[self.faction].remove(self)


def plasma(self, gs, dmglist):
    for i in dmglist:
        gs.targets[self.faction][i].health -= self.damage
        gs.targets[self.faction][i].sop += 2 * self.damage
    explosion = PAExplosion(self.centerx, self.centery, gs)
    gs.explosion_group.add(explosion)
    gs.bullets[self.faction].remove(self)


def rail(self, gs, dmglist):
    for i in dmglist:
        gs.targets[self.faction][i].health -= self.damage
        gs.targets[self.faction][i].sop += 2 * self.damage
    for num in range(8):
        gs.particle_list2.append(
            Particle(self.centerx, self.centery, 3, rnd.randint(0, 360), 10, (0, 223, 255), shrink=0.5))


AutoCannon = {'velocity': 17,
              'damage': 4,
              'energy': 14,
              'range': 3000,
              'delay': 12,
              'height': 10,
              'width': 10,
              'cost': {"Iron": 10, "Nickel": 10, "Platinum": 1, "Gold": 0},
              'name': "AutoCannon",
              'image': pygame.image.load(os.path.join('Assets', 'bullet.png')),
              'l_image': pygame.image.load(os.path.join('Assets', 'AutoCannon_Launcher.png')),
              'sound': None,
              'function': cannon}

AutoCannon2 = {'velocity': 14,
               'damage': 5,
               'energy': 15,
               'range': 2500,
               'delay': 12,
               'height': 10,
               'width': 10,
               'cost': {"Iron": 10, "Nickel": 10, "Platinum": 1, "Gold": 0},
               'name': "AP AutoCannon",
               'image': pygame.image.load(os.path.join('Assets', 'bulletAP.png')),
               'l_image': pygame.image.load(os.path.join('Assets', 'AutoCannonAP_Launcher.png')),
               'sound': None,
               'function': cannon}

Plasma = {'velocity': 9.5,
          'damage': 50,
          'energy': 150,
          'range': 1500,
          'delay': 120,
          'height': 15,
          'width': 15,
          'cost': {"Iron": 10, "Nickel": 5, "Platinum": 5, "Gold": 10},
          'name': "Plasma",
          'image': pygame.image.load(os.path.join('Assets', 'Plasma.png')),
          'l_image': pygame.image.load(os.path.join('Assets', 'Plasma_Launcher.png')),
          'sound': None,
          'function': plasma}

Railgun = {'velocity': 30,
           'damage': 10,
           'energy': 200,
           'range': 10000,
           'delay': 240,
           'height': 30,
           'width': 30,
           'cost': {"Iron": 10, "Nickel": 25, "Platinum": 10, "Gold": 1},
           'name': "Railgun",
           'image': pygame.image.load(os.path.join('Assets', 'railgun.png')),
           'l_image': pygame.image.load(os.path.join('Assets', 'Railgun_Launcher.png')),
           'sound': pygame.mixer.Sound(os.path.join('Assets', 'railgun_launch.mp3')),
           'function': rail}

BulletNames = [AutoCannon, AutoCannon2, Plasma, Railgun]
