import pygame
import os

TerminusCorp = {'color': (0, 50, 150),  # adj
                'name': "Terminus Corporation",
                'image': pygame.image.load(os.path.join('Assets', 'Factions', 'Terminus Corporation.png')),
                'ship_images': {},
                'channel': {}}

SpacePirates = {'color': (0, 0, 0),  # adj
                'name': "Space Pirates",
                'image': pygame.image.load(os.path.join('Assets', 'Factions', 'Space Pirates.png')),
                'ship_images': {},
                'channel': {}}

RebelAlliance = {'color': (255, 0, 0),  # adj
                 'name': "Rebel Alliance",
                 'image': pygame.image.load(os.path.join('Assets', 'Factions', 'Rebel Alliance.png')),
                 'ship_images': {},
                 'channel': {}}

FactionList = [TerminusCorp, SpacePirates, RebelAlliance]


