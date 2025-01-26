from Data.Types import BulletType, Vessel, Projectile, Guided
from Data.Bullet_Functions import *
import os
import math
import pygame

pygame.mixer.init()

# if __name__ == '__main__':
# PATH = r'..\Assets'
# else:
PATH = r'Assets'

"""FLAME THROWER IMAGE"""
flame_image = pygame.Surface((6, 6), pygame.SRCALPHA)
# flame_image.set_colorkey((0, 0, 0))
pygame.draw.circle(flame_image, (255, 200, 0, 100), (3, 3), 3)
pygame.draw.circle(flame_image, (255, 0, 0, 150), (3, 3), 1)

AutoCannon = {'velocity': 10,  # adj
              'damage': 2,
              'exp_damage': 0,
              'exp_radius': 0,
              'energy': 7,
              'range': 5000,
              'delay': 11,  # adj
              'target_types': (Vessel, Guided),
              'height': 10,
              'width': 10,
              'cost': {},
              'name': "AutoCannon",
              'image': pygame.image.load(os.path.join(PATH, 'bullet.png')),
              'l_image': pygame.image.load(os.path.join(PATH, 'AutoCannonHV_Launcher.png')),
              'sound': pygame.mixer.Sound(os.path.join(PATH, 'AutoCannon_launch.mp3')),
              'function': cannon,
              'init': init_bullet,
              'draw': draw_bullet}

AutoCannon2 = {'velocity': 9.5,  # adj
               'damage': 3,
               'exp_damage': 0,
               'exp_radius': 0,
               'energy': 12,
               'range': 4000,
               'delay': 15,  # adj
               'target_types': (Vessel, Guided),
               'height': 10,
               'width': 10,
               'cost': {},
               'name': "AP AutoCannon",
               'image': pygame.image.load(os.path.join(PATH, 'bulletAP.png')),
               'l_image': pygame.image.load(os.path.join(PATH, 'AutoCannonAP_Launcher.png')),
               'sound': pygame.mixer.Sound(os.path.join(PATH, 'AutoCannon_launch.mp3')),
               'function': cannon,
               'init': init_bullet,
               'draw': draw_bullet}

AutoCannon3 = {'velocity': 9.5,  # adj
               'damage': 2,
               'exp_damage': 0,
               'exp_radius': 0,
               'energy': 12,
               'range': 4000,
               'delay': 17,  # adj
               'target_types': (Vessel, Guided),
               'height': 10,
               'width': 10,
               'cost': {},
               'name': "IN AutoCannon",
               'image': pygame.image.load(os.path.join(PATH, 'bulletIN.png')),
               'l_image': pygame.image.load(os.path.join(PATH, 'AutoCannonIN_Launcher.png')),
               'sound': pygame.mixer.Sound(os.path.join(PATH, 'AutoCannon_launch.mp3')),
               'function': heat_cannon,
               'init': init_bullet,
               'draw': draw_bullet}

Plasma = {'velocity': 5.5,  # adj
          'damage': 50,
          'exp_damage': 0,
          'exp_radius': 0,
          'energy': 110,
          'range': 1000,
          'delay': 250,  # adj
          'target_types': (Vessel,),
          'height': 15,
          'width': 15,
          'cost': {},
          'name': "Plasma",
          'image': pygame.image.load(os.path.join(PATH, 'Plasma.png')),
          'l_image': pygame.image.load(os.path.join(PATH, 'Plasma_Launcher.png')),
          'sound': pygame.mixer.Sound(os.path.join(PATH, 'PA_launch.mp3')),
          'function': plasma,
          'init': init_bullet,
          'draw': draw_bullet}


Cannon = {'velocity': 8,  # adj
          'damage': 1,
          'exp_damage': 45,
          'exp_radius': 150,
          'energy': 120,
          'range': 3000,
          'delay': 400,  # adj
          'target_types': (Vessel,),
          'height': 12,
          'width': 12,
          'cost': {},
          'name': "Cannon",
          'image': pygame.image.load(os.path.join(PATH, 'Cannon.png')),
          'l_image': pygame.image.load(os.path.join(PATH, 'Cannon_Launcher.png')),
          'sound': pygame.mixer.Sound(os.path.join(PATH, 'AutoCannon_launch.mp3')),
          'function': he_cannon,
          'init': init_cannon,
          'draw': draw_bullet}


Railgun = {'velocity': 25,  # adj
           'damage': 11,
           'exp_damage': 0,
           'exp_radius': 0,
           'energy': 120,
           'range': 10000,
           'delay': 480,  # adj
           'target_types': (Vessel,),
           'height': 30,
           'width': 30,
           'cost': {},
           'name': "Railgun",
           'image': pygame.image.load(os.path.join(PATH, 'railgun.png')),
           'l_image': pygame.image.load(os.path.join(PATH, 'Railgun_Launcher.png')),
           'sound': pygame.mixer.Sound(os.path.join(PATH, 'railgun_launch.mp3')),
           'function': rail,
           'init': init_bullet,
           'draw': draw_bullet}

FlameThrower = {'velocity': 5.5,  # adj
                'damage': 0,
                'exp_damage': 0,
                'exp_radius': 0,
                'energy': 0.75,  # adj
                'range': 600,
                'delay': 1,
                'target_types': (Vessel,),
                'height': 6,
                'width': 6,
                'cost': {},
                'name': "Flame Thrower",
                'image': flame_image,
                'l_image': pygame.image.load(os.path.join(PATH, 'FlameThrower_Launcher.png')),
                'sound': None,
                'function': flame,
                'init': init_spray,
                'draw': draw_flame}

BeamLaser = {'velocity': math.inf,
             'damage': 0,
             'exp_damage': 0,
             'exp_radius': 0,
             'energy': 0.5,  # adj
             'range': 900,
             'delay': 1,
             'target_types': (Vessel,),
             'height': 0,
             'width': 0,
             'cost': {},
             'name': "Beam Laser",
             'image': pygame.Surface((1, 1)),
             'l_image': pygame.image.load(os.path.join(PATH, 'BeamLaser_Launcher.png')),
             'sound': None,
             'function': heat_laser,
             'init': init_beam,
             'draw': lambda *args: None}

BulletNames = [AutoCannon, AutoCannon2, AutoCannon3, Plasma, Cannon, Railgun, FlameThrower, BeamLaser]
BULLETTYPES = {bullet['name']: BulletType(**bullet) for bullet in BulletNames}

if __name__ == '__main__':
    print(locals())
