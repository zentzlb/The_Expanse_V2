import os
import pygame
import random as rnd
from Explosions import Particle

pygame.mixer.init()

def explosion(self, gs, mylist):
    for i in range(50):
        c = rnd.randint(100, 200)
        gs.particle_list2.append(Particle(self.centerx, self.centery, -rnd.randint(1, self.er // 20),
                                          rnd.randint(0, 360), 10,
                                          (c + 50, c, 100), shrink=0.5))

Seeker = {'velocity': 9.5,
          'av': 0.75,
          'damage': 13,
          'exp_damage': 7,
          'exp_radius': 100,
          'energy': 150,
          'range': 7000,
          'delay': 120,
          'height': 12,
          'width': 12,
          'drunk': False,
          'smart': False,
          'par_num': 1,
          'par_rnd': 0,
          'cost': {"Iron": 100, "Nickel": 125, "Platinum": 10, "Gold": 10},
          'name': "Seeker",
          'image': pygame.image.load(os.path.join('Assets', 'smallmissile1.png')),
          'sound': pygame.mixer.Sound('Assets//missile_launch.mp3'),
          'function': explosion}

EMPMissile = {'velocity': 8,
              'av': 0.5,
              'damage': 15,
              'exp_damage': 60,
              'exp_radius': 200,
              'energy': 230,
              'range': 3000,
              'delay': 250,
              'height': 15,
              'width': 15,
              'drunk': False,
              'smart': False,
              'par_num': 4,
              'par_rnd': 70,
              'cost': {"Iron": 100, "Nickel": 50, "Platinum": 15, "Gold": 50},
              'name': "EMP Missile",
              'image': pygame.image.load(os.path.join('Assets', 'torpedo.png')),
              'sound': pygame.mixer.Sound('Assets//missile_launch.mp3'),
              'function': explosion}

SwarmMissile = {'velocity': 8.5,
                'av': 2.5,
                'damage': 10,
                'exp_damage': 5,
                'exp_radius': 50,
                'energy': 100,
                'range': 4000,
                'delay': 40,
                'height': 10,
                'width': 10,
                'drunk': True,
                'smart': False,
                'par_num': 2,
                'par_rnd': 30,
                'cost': {"Iron": 100, "Nickel": 50, "Platinum": 15, "Gold": 50},
                'name': "Swarm Missile",
                'image': pygame.image.load(os.path.join('Assets', 'swarm_missile.png')),
                'sound': pygame.mixer.Sound('Assets//missile_launch.mp3'),
                'function': explosion}

SmartMissile = {'velocity': 10,
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
                'cost': {"Iron": 100, "Nickel": 125, "Platinum": 10, "Gold": 10},
                'name': "Smart Missile",
                'image': pygame.image.load(os.path.join('Assets', 'smartmissile.png')),
                'sound': pygame.mixer.Sound('Assets//missile_launch.mp3'),
                'function': explosion}

MissileNames = [Seeker, EMPMissile, SwarmMissile, SmartMissile]
