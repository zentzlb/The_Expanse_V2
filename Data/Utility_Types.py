from typing import Callable
from .Utility_Functions import *
from Data.Types import UtilityType


AutoLoader = {'function': auto_loader,
              'logic': use_auto_loader,
              'energy': '1',
              'delay': 0,
              'description': 'This ship is fast',
              'cost': {},
              'name': "Auto Loader",
              'draw': lambda: None}

JumpDrive = {'function': jump_drive,
             'logic': use_jump_drive,
             'energy': 'ship.height * 2',
             'delay': 180,  # adj
             'description': 'This ship is fast',
             'cost': {},
             'name': "Jump Drive",
             'draw': lambda: None}

Cloak = {'function': cloak,
         'logic': null,
         'energy': '0.5',
         'delay': 120,  # adj
         'description': 'This ship is fast',
         'cost': {},
         'name': "Cloak",
         'draw': lambda: None}

Reactor = {'function': overload_reactor,
           'logic': use_overload_reactor,
           'energy': '0',
           'delay': 1,
           'description': 'This ship is fast',
           'cost': {},
           'name': "Reactor",
           'draw': lambda: None}

HeatSink = {'function': heat_sink,
            'logic': use_heat_sink,
            'energy': '1',
            'delay': 1,
            'description': 'This ship is fast',
            'cost': {},
            'name': "Heat Sink",
            'draw': lambda: None}

GravityRepulsor = {'function': repulsor,
                   'logic': use_repulsor,
                   'energy': '1',
                   'delay': 200,
                   'description': 'This ship is fast',
                   'cost': {},
                   'name': "Gravity Repulsor",
                   'draw': lambda: None}


UtilityNames = [AutoLoader, JumpDrive, Cloak, Reactor, HeatSink, GravityRepulsor]
UTILITYTYPES = {util['name']: UtilityType(**util) for util in UtilityNames}
