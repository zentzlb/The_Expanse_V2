import os
import pygame

PDC = {'velocity': 5,
       'av': 1.5,
       'energy': 200,
       'health': 125,
       'height': 20,
       'width': 20,
       'range': 7000,
       'bullet_types': ['AutoCannon'],
       'missile_type': None,
       'cost': {"Iron": 100, "Nickel": 25, "Platinum": 25, "Gold": 5},
       'name': "PDC",
       'image': pygame.image.load(os.path.join('Assets', f'PDC.png'))}

RailTurret = {'velocity': 5,
              'av': 0.5,
              'energy': 1000,
              'health': 200,
              'height': 29,
              'width': 29,
              'range': 10000,
              'bullet_types': ['Railgun'],
              'missile_type': None,
              'cost': {"Iron": 100, "Nickel": 25, "Platinum": 25, "Gold": 5},
              'name': "Rail",
              'image': pygame.image.load(os.path.join('Assets', f'Rail.png'))}

TurretNames = [PDC, RailTurret]