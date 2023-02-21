import os
import pygame
import numpy as np

Partrid = {'velocity': 5,
           'energy': 200,
           'health': 10000,
           'height': 250,
           'width': 250,
           'turrets': ['PDC'],
           'turret_pos': [np.array([0, 0])],
           'image': pygame.image.load(os.path.join('Assets', f'Partrid.png')),
           'cost': {"Iron": 100, "Nickel": 25, "Platinum": 25, "Gold": 5},
           'name': "Partrid"}

StationNames = [Partrid]
