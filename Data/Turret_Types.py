import os
import pygame
from Data.Types import TurretType
from Data.Bullet_Types import AutoCannon, Railgun
from Data.Turret_Functions import draw_turret


PDC = {'velocity': 5,
       'av': 0.5,  # adj
       'energy': 800,
       'health': 125,
       'height': 20,
       'width': 20,
       'range': 7000,
       'bullet_types': [AutoCannon],
       'missile_types': [],
       'targets_missiles': True,
       'cost': {"Iron": 100, "Nickel": 25, "Platinum": 25, "Gold": 5},
       'name': "PDC",
       'image': pygame.image.load(os.path.join('Assets', f'PDC.png')),
       'draw': draw_turret}

RailTurret = {'velocity': 5,
              'av': 0.25,  # adj
              'energy': 1200,
              'health': 200,
              'height': 29,
              'width': 29,
              'range': 15000,
              'bullet_types': [Railgun],
              'missile_types': [],
              'targets_missiles': False,
              'cost': {"Iron": 100, "Nickel": 25, "Platinum": 25, "Gold": 5},
              'name': "Rail",
              'image': pygame.image.load(os.path.join('Assets', f'Rail.png')),
              'draw': draw_turret}

TurretNames = [PDC, RailTurret]

TURRETTYPES = {turret['name']: TurretType(**turret) for turret in TurretNames}


