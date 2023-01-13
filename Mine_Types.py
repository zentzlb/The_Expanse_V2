import os
import pygame

pygame.mixer.init()

BlackHole = {'damage': 1,
             'exp_damage': 0,
             'exp_radius': 60,
             'energy': 500,
             'time': 4000,
             'delay': 300,
             'height': 19,
             'width': 19,
             'par_num': 30,
             'par_rnd': 0,
             'cost': {"Iron": 100, "Nickel": 125, "Platinum": 10, "Gold": 10},
             'name': "Black Hole",
             'image': pygame.image.load(os.path.join('Assets', 'black_hole.png')),
             'sound': pygame.mixer.Sound('Assets//missile_launch.mp3'),
             'function': None}

MineNames = [BlackHole]