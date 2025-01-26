import os
import pygame
import numpy as np
from Data.Types import StationType
from Data.Station_Functions import draw_station


Partrid = {'velocity': 5,
           'energy': 200,
           'health': 10000,
           'height': 250,
           'width': 250,
           'turrets': ['PDC'],
           'turret_pos': [np.array([0, 0])],
           'image': pygame.image.load(os.path.join('Assets', f'Partrid.png')),
           'cost': {"Iron": 100, "Nickel": 25, "Platinum": 25, "Gold": 5},
           'name': "Partrid",
           'draw': draw_station}

StationNames = [Partrid]
STATIONTYPES = {station['name']: StationType(**station) for station in StationNames}



