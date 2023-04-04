import numpy as np

Fighter = {'velocity': 3.3,  # adj
           'acc': 0.1,  # adj
           'av': 1,  # adj
           'energy': 800,
           'health': 150,
           'heat_capacity': 110,
           'heat_venting': 0.002,  # adj
           'height': 40,
           'width': 40,
           'range': 20000,
           'turrets': [],
           'turret_pos': [],
           'description': 'This ship is fast',
           'bullet_pos': [np.array([-11, 9]), np.array([11, 9])],
           'missile_pos': [np.array([0, 9])],
           'emblem_pos': [(15, 14)],
           'primary': 2,
           'secondary': 1,
           'mine': 0,
           'utility': 1,
           'cargo_cap': 50,
           'cost': {},
           'name': "Corpus 9"}

Uboat = {'velocity': 3.2,  # adj
         'acc': 0.15,  # adj
         'av': 1.25,  # adj
         'energy': 1200,
         'health': 200,
         'heat_capacity': 150,
         'heat_venting': 0.0025,  # adj
         'height': 40,
         'width': 40,
         'range': 30000,
         'turrets': [],
         'turret_pos': [],
         'description': 'This ship is fast',
         'bullet_pos': [np.array([0, 4])],
         'missile_pos': [],
         'emblem_pos': [],
         'primary': 1,
         'secondary': 0,
         'mine': 0,
         'utility': 3,
         'cargo_cap': 50,
         'cost': {},
         'name': "Sarhakum"}

HeavyFighter = {'velocity': 3,  # adj
                'acc': 0.09,  # adj
                'av': 0.8,  # adj
                'energy': 1200,
                'health': 300,
                'heat_capacity': 175,
                'heat_venting': 0.001,  # adj
                'height': 60,
                'width': 60,
                'range': 25000,
                'turrets': [],
                'turret_pos': [],
                'description': 'This ship is fast',
                'bullet_pos': [np.array([-21, 14]), np.array([21, 14])],
                'missile_pos': [np.array([0, 21])],
                'emblem_pos': [],
                'primary': 2,
                'secondary': 1,
                'mine': 0,
                'utility': 2,
                'cargo_cap': 50,
                'cost': {},
                'name': "Rakreem"}

Ghost = {'velocity': 3,  # adj
         'acc': 0.08,  # adj
         'av': 0.75,  # adj
         'energy': 3000,
         'health': 250,
         'heat_capacity': 200,
         'heat_venting': 0.001,  # adj
         'height': 70,
         'width': 70,
         'range': 40000,
         'turrets': [],
         'turret_pos': [],
         'bullet_pos': [np.array([-25, 13]), np.array([25, 13])],
         'missile_pos': [np.array([-15, -27]), np.array([15, -27])],  # , np.array([25, 10])],
         'emblem_pos': [(30, 31)],
         'primary': 2,
         'secondary': 2,
         'mine': 0,
         'utility': 3,
         'cargo_cap': 20,
         'cost': {},
         'name': "Velinture"}

Sprinter = {'velocity': 3.5,  # adj
            'acc': 0.2,  # adj
            'av': 1,  # adj
            'energy': 500,
            'health': 100,
            'heat_capacity': 90,
            'heat_venting': 0.003,  # adj
            'height': 30,
            'width': 30,
            'range': 15000,
            'turrets': [],
            'turret_pos': [],
            'bullet_pos': [np.array([8, 2])],
            'missile_pos': [np.array([-8, 2])],
            'emblem_pos': [(10, 6)],
            'primary': 1,
            'secondary': 1,
            'mine': 0,
            'utility': 1,
            'cargo_cap': 10,
            'cost': {},
            'name': "Pelomir"}

Frigate = {'velocity': 2,  # adj
           'acc': 0.02,  # adj
           'av': 0.25,
           'energy': 500,
           'health': 400,
           'heat_capacity': 300,
           'heat_venting': 0.0005,  # adj
           'height': 80,
           'width': 80,
           'range': 20000,
           'turrets': ['PDC'],
           'turret_pos': [np.array([0, -5])],
           'bullet_pos': [np.array([0, 16])],
           'missile_pos': [],
           'emblem_pos': [(35, 8)],
           'primary': 1,
           'secondary': 0,
           'mine': 1,
           'utility': 2,
           'cargo_cap': 1000,
           'cost': {},
           'name': "Harfute"}

Destroyer = {'velocity': 1.75,  # adj
             'acc': 0.01,  # adj
             'av': 0.2,  # adj
             'energy': 5000,
             'health': 1000,
             'heat_capacity': 500,
             'heat_venting': 0.0002,  # adj
             'height': 150,
             'width': 150,
             'range': 50000,
             'turrets': ['Rail', 'PDC', 'PDC'],
             'turret_pos': [np.array([0, 0]), np.array([0, 41]), np.array([0, -41])],
             'bullet_pos': [np.array([0, 65])],
             'missile_pos': [np.array([-24, 35]), np.array([24, 35])],
             'emblem_pos': [(70, 94)],
             'primary': 1,
             'secondary': 2,
             'mine': 1,
             'utility': 3,
             'cargo_cap': 300,
             'cost': {},
             'name': "Audigote"}

Pafonteer = {'velocity': 3.3,  # adj
             'acc': 0.10,  # adj
             'av': 0.5,  # adj
             'energy': 700,
             'health': 120,
             'heat_capacity': 90,
             'heat_venting': 0.002,  # adj
             'height': 40,
             'width': 40,
             'range': 40000,
             'turrets': [],
             'turret_pos': [],
             'bullet_pos': [np.array([-12, 19])],
             'missile_pos': [],
             'emblem_pos': [(3, 11)],
             'primary': 1,
             'secondary': 0,
             'mine': 0,
             'utility': 1,
             'cargo_cap': 450,
             'cost': {},
             'name': "Pafonteer"}

Ontulus = {'velocity': 3.25,  # adj
           'acc': 0.1,  # adj
           'av': 0.5,  # adj
           'energy': 1500,
           'health': 300,
           'heat_capacity': 200,
           'heat_venting': 0.001,  # adj
           'height': 70,
           'width': 70,
           'range': 30000,
           'turrets': [],
           'turret_pos': [],
           'description': 'This ship is fast',
           'bullet_pos': [np.array([-22, 18])],
           'missile_pos': [np.array([22, 18])],
           'emblem_pos': [(30, 42)],
           'primary': 1,
           'secondary': 1,
           'mine': 1,
           'utility': 2,
           'cargo_cap': 50,
           'cost': {},
           'name': "Ontulus"}

Garvantex = {'velocity': 2.5,  # adj
           'acc': 0.025,  # adj
           'av': 0.25,  # adj
           'energy': 6000,
           'health': 700,
           'heat_capacity': 400,
           'heat_venting': 0.0006,  # adj
           'height': 90,
           'width': 90,
           'range': 35000,
           'turrets': [],
           'turret_pos': [],
           'description': 'This ship is fast',
           'bullet_pos': [np.array([0, 0]), np.array([-10, 10]), np.array([10, 10])],
           'missile_pos': [],
           'emblem_pos': [(31, 31), (49, 31)],
           'primary': 3,
           'secondary': 0,
           'mine': 0,
           'utility': 1,
           'cargo_cap': 50,
           'cost': {},
           'name': "Garvantex"}

ShipNames = [Fighter, Uboat, HeavyFighter, Ghost, Sprinter, Frigate, Destroyer, Pafonteer, Ontulus, Garvantex]
