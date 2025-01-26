import os
from typing import Callable
from .Missile_Functions import *
from Data.Types import MissileType
from Data.Missile_Functions import dumb_guidance, drunk_guidance, smart_guidance, init_missile

pygame.mixer.init()

Seeker = {'velocity': 6,  # adj
          'acc': 0.5,
          'av': 0.7,  # adj
          'damage': 10,
          'exp_damage': 20,
          'exp_radius': 100,
          'energy': 200,
          'range': 8000,
          'health': 2,
          'delay': 400,  # adj
          'height': 12,
          'width': 12,
          'guidance': smart_guidance,
          'par_num': 1,
          'par_rnd': 0,
          'cost': {},
          'name': "Seeker",
          'image': pygame.image.load(os.path.join('Assets', 'smallmissile1.png')),
          'sound': pygame.mixer.Sound('Assets/missile_launch.mp3'),
          'init': init_missile,
          'explosion': explosion,
          'draw': draw_missile}

Sneaker = {'velocity': 5.6,  # adj
           'acc': 0.5,
           'av': 0.8,  # adj
           'damage': 10,
           'exp_damage': 20,
           'exp_radius': 100,
           'energy': 200,
           'range': 8000,
           'health': 2,
           'delay': 400,  # adj
           'height': 12,
           'width': 12,
           'guidance': sneaker_guidance,
           'par_num': 1,
           'par_rnd': 0,
           'cost': {},
           'name': "Sneaker",
           'image': pygame.image.load(os.path.join('Assets', 'sneaker_missile.png')),
           'sound': pygame.mixer.Sound('Assets/missile_launch.mp3'),
           'init': init_swarm,
           'explosion': explosion,
           'draw': draw_missile}

EMPMissile = {'velocity': 4.25,  # adj
              'acc': 0.5,
              'av': 0.25,  # adj
              'damage': 10,
              'exp_damage': 85,
              'exp_radius': 200,
              'energy': 250,
              'range': 3000,
              'health': 10,
              'delay': 500,  # adj
              'height': 15,
              'width': 15,
              'guidance': dumb_guidance,
              'par_num': 2,
              'par_rnd': 70,
              'cost': {},
              'name': "EMP Missile",
              'image': pygame.image.load(os.path.join('Assets', 'torpedo.png')),
              'sound': pygame.mixer.Sound('Assets/missile_launch.mp3'),
              'init': init_missile,
              'explosion': emp_explosion,
              'draw': draw_missile}

SwarmMissile = {'velocity': 4.5,  # adj
                'acc': 0.5,
                'av': 1.25,  # adj
                'damage': 15,
                'exp_damage': 10,
                'exp_radius': 50,
                'energy': 180,
                'range': 4500,
                'health': 3,
                'delay': 180,  # adj
                'height': 10,
                'width': 10,
                'guidance': drunk_guidance,
                'par_num': 1,
                'par_rnd': 40,
                'cost': {},
                'name': "Swarm Missile",
                'image': pygame.image.load(os.path.join('Assets', 'swarm_missile.png')),
                'sound': pygame.mixer.Sound('Assets/missile_launch.mp3'),
                'init': init_missile,
                'explosion': explosion,
                'draw': draw_missile}

SmartMissile = {'velocity': 9,
                'acc': 0.5,
                'av': 0.7,  # adj
                'damage': 10,
                'exp_damage': 15,
                'exp_radius': 80,
                'energy': 220,
                'range': 15000,
                'health': 2,
                'delay': 480,  # adj
                'height': 12,
                'width': 12,
                'guidance': smart_guidance,
                'par_num': 1,
                'par_rnd': 0,
                'cost': {},
                'name': "Smart Missile",
                'image': pygame.image.load(os.path.join('Assets', 'smartmissile.png')),
                'sound': pygame.mixer.Sound('Assets/missile_launch.mp3'),
                'init': init_missile,
                'explosion': explosion,
                'draw': draw_missile}

IonOrb = {'velocity': 4.5,  # adj
          'acc': 0.5,
          'av': 1,  # adj
          'damage': 20,
          'exp_damage': 0,
          'exp_radius': 0,
          'energy': 180,
          'range': 4000,
          'health': 2,
          'delay': 360,  # adj
          'height': 10,
          'width': 10,
          'guidance': dumb_guidance,
          'par_num': 0,
          'par_rnd': 0,
          'cost': {},
          'name': "Ion Orb",
          'image': pygame.image.load(os.path.join('Assets', 'Ion_Orb.png')),
          'sound': pygame.mixer.Sound('Assets/missile_launch.mp3'),
          'init': init_missile,
          'explosion': HeatOrb,
          'draw': draw_orb}

PhotonTorpedo = {'velocity': 4,  # adj
                 'acc': 0.5,
                 'av': 1.2,  # adj
                 'damage': 20,
                 'exp_damage': 5,
                 'exp_radius': 50,
                 'energy': 180,
                 'range': 3250,
                 'health': 2,
                 'delay': 360,  # adj
                 'height': 10,
                 'width': 10,
                 'guidance': dumb_guidance,
                 'par_num': 0,
                 'par_rnd': 0,
                 'cost': {},
                 'name': "Photon Torpedo",
                 'image': pygame.image.load(os.path.join('Assets', 'photon_torpedo.png')),
                 'sound': pygame.mixer.Sound('Assets/missile_launch.mp3'),
                 'init': init_missile,
                 'explosion': photon_explosion,
                 'draw': draw_circ}

MissileNames = [Seeker, Sneaker, EMPMissile, SwarmMissile, SmartMissile, IonOrb, PhotonTorpedo]
MISSILETYPES = {missile['name']: MissileType(**missile) for missile in MissileNames}
