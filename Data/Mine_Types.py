import os
import pygame
from typing import Callable
from .Mine_Functions import *
from Data.Types import MineType

pygame.display.init()

ProximityMine = {'damage': 0,
                 'exp_damage': 100,
                 'exp_radius': 500,
                 'det_radius': 300,
                 'energy': 0,
                 'time': 1600,
                 'delay': 80,
                 'arm': 80,
                 'health': 50,
                 'height': 20,
                 'width': 20,
                 'par_num': 0,
                 'par_rnd': 0,
                 'cost': {},
                 'name': "Proximity Mine",
                 'pen': False,
                 'emp': False,
                 'grav': False,
                 'image': pygame.image.load(os.path.join('Assets', 'space_mine.png')),
                 'sound': pygame.mixer.Sound('Assets/missile_launch.mp3'),
                 'init': init_mine,
                 'function': proximity,
                 'draw': draw_mine,
                 'explosion': explosion}

BlackHole = {'damage': 1,
             'exp_damage': 0,
             'exp_radius': 0,
             'det_radius': 0,
             'energy': 400,
             'time': 3200,
             'delay': 400,
             'arm': 160,
             'health': 1000,
             'height': 19,
             'width': 19,
             'par_num': 30,
             'par_rnd': 0,
             'cost': {},
             'name': "Black Hole",
             'pen': True,
             'emp': False,
             'grav': True,
             'image': pygame.image.load(os.path.join(r'Assets', 'black_hole.png')),
             'sound': pygame.mixer.Sound('Assets/missile_launch.mp3'),
             'init': init_mine,
             'function': black_hole,
             'draw': draw_mine,
             'explosion': lambda *args, **kwargs: []}

MineNames = [ProximityMine, BlackHole]
MINETYPES = {mine['name']: MineType(**mine) for mine in MineNames}
