import os
import pygame
import random as rnd
import math
from Explosions import Particle, ExplosionDamage

pygame.mixer.init()


def explosion(self, gs, dmgList):
    for i in dmgList:
        gs.targets[self.faction][i].health -= self.damage
        gs.targets[self.faction][i].sop += 2 * self.damage

    for i in range(100):
        c = rnd.randint(100, 200)
        gs.particle_list2.append(Particle(self.centerx, self.centery, -rnd.randint(1, self.er // 20),
                                          rnd.randint(0, 360), 10,
                                          (c + 50, c, 100), shrink=0.5))

    ExplosionDamage(self.exp_damage, self.centerx, self.centery, self.er, gs.targets[self.faction], gs)


def emp_explosion(self, gs, dmgList):
    for i in dmgList:
        gs.targets[self.faction][i].health -= self.damage
        gs.targets[self.faction][i].sop += 2 * self.damage
        gs.targets[self.faction][i].energy = 0
        # target_list[i].bulletC += 180
        # target_list[i].missileC += 180
        for turret in gs.targets[self.faction][i].turrets:
            turret.energy = 0
            turret.angle += 120 * rnd.uniform(-1, 1) / math.pi
            # turret.bulletC += 180
            # turret.missileC += 180
    for i in range(150):
        c = rnd.randint(100, 200)
        gs.particle_list2.append(Particle(self.centerx, self.centery, -rnd.randint(1, self.er // 20),
                                          rnd.randint(0, 360), 10,
                                          (c + 50, c, 100), shrink=0.5))

    ExplosionDamage(self.exp_damage, self.centerx, self.centery, self.er, gs.targets[self.faction], gs)


Seeker = {'velocity': 10.5,
          'av': 0.75,
          'damage': 10,
          'exp_damage': 15,
          'exp_radius': 100,
          'energy': 200,
          'range': 7000,
          'delay': 180,
          'height': 12,
          'width': 12,
          'drunk': False,
          'smart': False,
          'par_num': 1,
          'par_rnd': 0,
          'cost': {},
          'name': "Seeker",
          'image': pygame.image.load(os.path.join('Assets', 'smallmissile1.png')),
          'sound': pygame.mixer.Sound('Assets//missile_launch.mp3'),
          'explosion': explosion}

EMPMissile = {'velocity': 8.5,
              'av': 0.5,
              'damage': 15,
              'exp_damage': 80,
              'exp_radius': 200,
              'energy': 250,
              'range': 4000,
              'delay': 250,
              'height': 15,
              'width': 15,
              'drunk': False,
              'smart': False,
              'par_num': 2,
              'par_rnd': 70,
              'cost': {},
              'name': "EMP Missile",
              'image': pygame.image.load(os.path.join('Assets', 'torpedo.png')),
              'sound': pygame.mixer.Sound('Assets//missile_launch.mp3'),
              'explosion': emp_explosion}

SwarmMissile = {'velocity': 9,
                'av': 2.5,
                'damage': 15,
                'exp_damage': 5,
                'exp_radius': 50,
                'energy': 180,
                'range': 5000,
                'delay': 90,
                'height': 10,
                'width': 10,
                'drunk': True,
                'smart': False,
                'par_num': 1,
                'par_rnd': 40,
                'cost': {},
                'name': "Swarm Missile",
                'image': pygame.image.load(os.path.join('Assets', 'swarm_missile.png')),
                'sound': pygame.mixer.Sound('Assets//missile_launch.mp3'),
                'explosion': explosion}

SmartMissile = {'velocity': 11,
                'av': 0.5,
                'damage': 10,
                'exp_damage': 10,
                'exp_radius': 80,
                'energy': 220,
                'range': 15000,
                'delay': 240,
                'height': 12,
                'width': 12,
                'drunk': False,
                'smart': True,
                'par_num': 1,
                'par_rnd': 0,
                'cost': {},
                'name': "Smart Missile",
                'image': pygame.image.load(os.path.join('Assets', 'smartmissile.png')),
                'sound': pygame.mixer.Sound('Assets//missile_launch.mp3'),
                'explosion': explosion}

MissileNames = [Seeker, EMPMissile, SwarmMissile, SmartMissile]
