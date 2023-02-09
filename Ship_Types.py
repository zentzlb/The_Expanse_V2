import numpy as np

Fighter = {'velocity': 6.5,
           'acc': 0.4,
           'av': 2,
           'energy': 600,
           'health': 150,
           'heat_capacity': 120,
           'heat_venting': 0.003,
           'height': 50,
           'width': 50,
           'range': 20000,
           'turrets': [],
           'turret_pos': [],
           'description': 'This ship is fast',
           'bullet_pos': [np.array([-15, 5]), np.array([15, 5])],
           'missile_pos': [np.array([-8, 15])],
           'primary': 2,
           'secondary': 1,
           'mine': 0,
           'utility': 1,
           'cargo_cap': 50,
           'cost': {},
           'name': "Fighter"}

HeavyFighter = {'velocity': 6,
                'acc': 0.35,
                'av': 1.5,
                'energy': 1000,
                'health': 300,
                'heat_capacity': 150,
                'heat_venting': 0.002,
                'height': 60,
                'width': 60,
                'range': 25000,
                'turrets': [],
                'turret_pos': [],
                'description': 'This ship is fast',
                'bullet_pos': [np.array([-21, 8]), np.array([21, 8])],
                'missile_pos': [np.array([0, 21])],
                'primary': 2,
                'secondary': 1,
                'mine': 0,
                'utility': 2,
                'cargo_cap': 50,
                'cost': {},
                'name': "Heavy Fighter"}

Ghost = {'velocity': 6,
         'acc': 0.3,
         'av': 1.25,
         'energy': 3000,
         'health': 250,
         'heat_capacity': 200,
         'heat_venting': 0.003,
         'height': 70,
         'width': 70,
         'range': 40000,
         'turrets': [],
         'turret_pos': [],
         'bullet_pos': [np.array([-25, 13])],
         'missile_pos': [np.array([-15, -27]), np.array([15, -27]), np.array([25, 10])],
         'primary': 1,
         'secondary': 3,
         'mine': 0,
         'utility': 2,
         'cargo_cap': 20,
         'cost': {},
         'name': "Ghost"}

Sprinter = {'velocity': 7,
            'acc': 0.5,
            'av': 1.75,
            'energy': 500,
            'health': 100,
            'heat_capacity': 100,
            'heat_venting': 0.004,
            'height': 30,
            'width': 30,
            'range': 15000,
            'turrets': [],
            'turret_pos': [],
            'bullet_pos': [np.array([8, 2])],
            'missile_pos': [np.array([-8, 2])],
            'primary': 1,
            'secondary': 1,
            'mine': 0,
            'utility': 1,
            'cargo_cap': 10,
            'cost': {},
            'name': "Sprinter"}

Frigate = {'velocity': 4,
           'acc': 0.25,
           'av': 0.5,
           'energy': 500,
           'health': 400,
           'heat_capacity': 400,
           'heat_venting': 0.001,
           'height': 80,
           'width': 80,
           'range': 20000,
           'turrets': ['PDC'],
           'turret_pos': [np.array([0, 0])],
           'bullet_pos': [np.array([-25, 5])],
           'missile_pos': [np.array([25, 5])],
           'primary': 1,
           'secondary': 1,
           'mine': 1,
           'utility': 2,
           'cargo_cap': 1000,
           'cost': {},
           'name': "Frigate"}

Destroyer = {'velocity': 3.5,
             'acc': 0.1,
             'av': 0.25,
             'energy': 5000,
             'health': 1000,
             'heat_capacity': 800,
             'heat_venting': 0.0005,
             'height': 150,
             'width': 150,
             'range': 50000,
             'turrets': ['Rail', 'PDC', 'PDC'],
             'turret_pos': [np.array([0, 0]), np.array([0, 41]), np.array([0, -41])],
             'bullet_pos': [np.array([-8, 70]), np.array([83, 70])],
             'missile_pos': [np.array([-24, 35]), np.array([24, 35])],
             'primary': 2,
             'secondary': 2,
             'mine': 1,
             'utility': 3,
             'cargo_cap': 300,
             'cost': {},
             'name': "Destroyer"}

ShipNames = [Fighter, HeavyFighter, Ghost, Sprinter, Frigate, Destroyer]
