import os
import pygame
from Data.Types import DebrisType


Pipe = {'av': 2,
        'time': 6000,
        'image': pygame.image.load(os.path.join('Assets', 'debris.png')),
        'name': "Pipe"}

Plate = {'av': 2,
         'time': 6000,
         'image': pygame.image.load(os.path.join('Assets', 'debris2.png')),
         'name': "Plate"}

Pilot = {'av': 2,
         'time': 6000,
         'image': pygame.image.load(os.path.join('Assets', 'debris3.png')),
         'name': "Pilot"}

Debris = [Pipe, Plate, Pilot]
DEBRISTYPES = {debris['name']: DebrisType(**debris) for debris in Debris}


