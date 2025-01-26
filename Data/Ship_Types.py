import numpy as np
from Data.Types import ShipType
from Data.Ship_Functions import draw_ship

Fighter = {'velocity': 3.2,  # adj
           'acc': 0.1,  # adj
           'lat': 0.15,
           'rev': 0.05,
           'av': 1,  # adj
           'energy': 800,
           'health': 150,
           'heat_capacity': 120,
           'heat_venting': 0.2,  # adj
           'height': 40,
           'width': 40,
           'range': 20000,
           'turrets': [],
           'thrust_pos': [np.array([0, -15])],
           'turret_pos': [],
           'description': 'This ship is fast',
           'bullet_pos': [np.array([-11, 9]), np.array([11, 9])],
           'missile_pos': [np.array([0, 9])],
           'emblem_pos': [(15, 14)],
           'primary': 2,
           'secondary': 1,
           'mine': 0,
           'utility': 1,
           'cargo_cap': 20,
           'cost': {},
           'draw': draw_ship,
           'name': "Corpus 9"}

Dragonfly = {'velocity': 2.7,  # adj
             'acc': 0.1,  # adj
             'lat': 0.9,
             'rev': 0.8,
             'av': 1,  # adj
             'energy': 1100,
             'health': 200,
             'heat_capacity': 150,
             'heat_venting': 0.2,  # adj
             'height': 50,
             'width': 50,
             'range': 20000,
             'turrets': [],
             'thrust_pos': [],
             'turret_pos': [],
             'description': 'This ship is fast',
             'bullet_pos': [np.array([0, 20])],
             'missile_pos': [np.array([-13, 4]), np.array([13, 4])],
             'emblem_pos': [],
             'primary': 1,
             'secondary': 2,
             'mine': 0,
             'utility': 2,
             'cargo_cap': 20,
             'cost': {},
             'draw': draw_ship,
             'name': "Dragonfly"}

Nasool = {'velocity': 4.4,  # adj
          'acc': 0.15,  # adj
          'lat': 0.15,
          'rev': 0.05,
          'av': 1,  # adj
          'energy': 800,
          'health': 125,
          'heat_capacity': 100,
          'heat_venting': 0.2,  # adj
          'height': 42,
          'width': 42,
          'range': 25000,
          'turrets': [],
          'thrust_pos': [np.array([-55, 42]), np.array([55, 42]), np.array([0, -52])],
          'turret_pos': [],
          'description': 'This ship is fast',
          'bullet_pos': [np.array([0, -7])],
          'missile_pos': [],
          'emblem_pos': [],
          'primary': 1,
          'secondary': 0,
          'mine': 1,
          'utility': 0,
          'cargo_cap': 40,
          'cost': {},
          'draw': draw_ship,
          'name': "Nasool"}

Uboat = {'velocity': 3.2,  # adj
         'acc': 0.15,  # adj
         'lat': 0.15,
         'rev': 0.05,
         'av': 1.5,  # adj
         'energy': 1200,
         'health': 220,
         'heat_capacity': 170,
         'heat_venting': 0.25,  # adj
         'height': 40,
         'width': 40,
         'range': 30000,
         'turrets': [],
         'thrust_pos': [np.array([0, -15])],
         'turret_pos': [],
         'description': 'This ship is fast',
         'bullet_pos': [np.array([0, 4])],
         'missile_pos': [],
         'emblem_pos': [],
         'primary': 1,
         'secondary': 0,
         'mine': 0,
         'utility': 3,
         'cargo_cap': 30,
         'cost': {},
         'draw': draw_ship,
         'name': "Sarhakum"}

HeavyFighter = {'velocity': 3.1,  # adj
                'acc': 0.09,  # adj
                'lat': 0.15,
                'rev': 0.05,
                'av': 0.8,  # adj
                'energy': 1200,
                'health': 300,
                'heat_capacity': 175,
                'heat_venting': 0.05,  # adj
                'height': 60,
                'width': 60,
                'range': 25000,
                'turrets': [],
                'thrust_pos': [np.array([10, -20]), np.array([-10, -20])],
                'turret_pos': [],
                'description': 'This ship is fast',
                'bullet_pos': [np.array([-21, 14]), np.array([21, 14])],
                'missile_pos': [np.array([0, 21])],
                'emblem_pos': [],
                'primary': 2,
                'secondary': 1,
                'mine': 0,
                'utility': 2,
                'cargo_cap': 30,
                'cost': {},
                'draw': draw_ship,
                'name': "Rakreem"}

Ghost = {'velocity': 3,  # adj
         'acc': 0.08,  # adj
         'lat': 0.15,
         'rev': 0.05,
         'av': 0.75,  # adj
         'energy': 3000,
         'health': 280,
         'heat_capacity': 200,
         'heat_venting': 0.06,  # adj
         'height': 70,
         'width': 70,
         'range': 40000,
         'turrets': [],
         'thrust_pos': [np.array([-55, 42]), np.array([55, 42]), np.array([0, -52])],
         'turret_pos': [],
         'description': 'This ship is fast',
         'bullet_pos': [np.array([-25, 13]), np.array([25, 13])],
         'missile_pos': [np.array([-15, -27]), np.array([15, -27])],  # , np.array([25, 10])],
         'emblem_pos': [(30, 31)],
         'primary': 2,
         'secondary': 2,
         'mine': 0,
         'utility': 3,
         'cargo_cap': 40,
         'cost': {},
         'draw': draw_ship,
         'name': "Velinture"}

Pelomir = {'velocity': 4.4,  # adj
           'acc': 0.2,  # adj
           'lat': 0.15,
           'rev': 0.05,
           'av': 1.25,  # adj
           'energy': 500,
           'health': 100,
           'heat_capacity': 90,
           'heat_venting': 0.02,  # adj
           'height': 30,
           'width': 30,
           'range': 15000,
           'turrets': [],
           'thrust_pos': [np.array([0, -12])],
           'turret_pos': [],
           'description': 'This ship is fast',
           'bullet_pos': [np.array([8, 2]), np.array([-8, 2])],
           'missile_pos': [],
           'emblem_pos': [(10, 6)],
           'primary': 2,
           'secondary': 0,
           'mine': 0,
           'utility': 1,
           'cargo_cap': 10,
           'cost': {},
           'draw': draw_ship,
           'name': "Pelomir"}

Harfute = {'velocity': 2,  # adj
           'acc': 0.02,  # adj
           'lat': 0.15,
           'rev': 0.05,
           'av': 0.25,
           'energy': 500,
           'health': 400,
           'heat_capacity': 300,
           'heat_venting': 0.01,  # adj
           'height': 80,
           'width': 80,
           'range': 20000,
           'turrets': ['PDC'],
           'thrust_pos': [np.array([-55, 42]), np.array([55, 42]), np.array([0, -52])],
           'turret_pos': [np.array([0, -5])],
           'description': 'This ship is fast',
           'bullet_pos': [np.array([0, 16])],
           'missile_pos': [],
           'emblem_pos': [(35, 8)],
           'primary': 1,
           'secondary': 0,
           'mine': 1,
           'utility': 2,
           'cargo_cap': 500,
           'cost': {},
           'draw': draw_ship,
           'name': "Harfute"}

Audigote = {'velocity': 1.75,  # adj
            'acc': 0.01,  # adj
            'lat': 0.15,
            'rev': 0.05,
            'av': 0.2,  # adj
            'energy': 5000,
            'health': 1200,
            'heat_capacity': 500,
            'heat_venting': 0.01,  # adj
            'height': 150,
            'width': 150,
            'range': 50000,
            'turrets': ['Rail', 'PDC', 'PDC'],
            'thrust_pos': [np.array([-55, 42]), np.array([55, 42]), np.array([0, -52])],
            'turret_pos': [np.array([0, 0]), np.array([0, 41]), np.array([0, -41])],
            'description': 'This ship is fast',
            'bullet_pos': [np.array([0, 65])],
            'missile_pos': [np.array([-24, 35]), np.array([24, 35])],
            'emblem_pos': [(70, 94)],
            'primary': 1,
            'secondary': 2,
            'mine': 1,
            'utility': 3,
            'cargo_cap': 100,
            'cost': {},
            'draw': draw_ship,
            'name': "Audigote"}

Pafonteer = {'velocity': 3.3,  # adj
             'acc': 0.10,  # adj
             'lat': 0.15,
             'rev': 0.05,
             'av': 0.5,  # adj
             'energy': 700,
             'health': 120,
             'heat_capacity': 100,
             'heat_venting': 0.2,  # adj
             'height': 40,
             'width': 40,
             'range': 40000,
             'turrets': [],
             'thrust_pos': [np.array([0, -15])],
             'turret_pos': [],
             'description': 'This ship is fast',
             'bullet_pos': [np.array([-12, 15])],
             'missile_pos': [],
             'emblem_pos': [(3, 11)],
             'primary': 1,
             'secondary': 0,
             'mine': 0,
             'utility': 1,
             'cargo_cap': 150,
             'cost': {},
             'draw': draw_ship,
             'name': "Pafonteer"}

Ontulus = {'velocity': 3.3,  # adj
           'acc': 0.1,  # adj
           'lat': 0.15,
           'rev': 0.05,
           'av': 0.5,  # adj
           'energy': 1500,
           'health': 300,
           'heat_capacity': 200,
           'heat_venting': 0.01,  # adj
           'height': 70,
           'width': 70,
           'range': 30000,
           'turrets': [],
           'thrust_pos': [np.array([-55, 42]), np.array([55, 42]), np.array([0, -52])],
           'turret_pos': [],
           'description': 'This ship is fast',
           'bullet_pos': [np.array([-22, 18])],
           'missile_pos': [np.array([22, 18])],
           'emblem_pos': [(30, 42)],
           'primary': 1,
           'secondary': 1,
           'mine': 1,
           'utility': 2,
           'cargo_cap': 20,
           'cost': {},
           'draw': draw_ship,
           'name': "Ontulus"}

Garvantex = {'velocity': 2.5,  # adj
             'acc': 0.025,  # adj
             'lat': 0.15,
             'rev': 0.05,
             'av': 0.8,  # adj
             'energy': 6000,
             'health': 1000,
             'heat_capacity': 600,
             'heat_venting': 0.2,  # adj
             'height': 90,
             'width': 90,
             'range': 35000,
             'turrets': [],
             'thrust_pos': [np.array([0, -42]), np.array([25, -22]), np.array([-25, -22])],
             'turret_pos': [],
             'description': 'This ship is fast',
             'bullet_pos': [np.array([0, 0]), np.array([-10, 10]), np.array([10, 10])],
             'missile_pos': [],
             'emblem_pos': [(31, 31), (49, 31)],
             'primary': 3,
             'secondary': 0,
             'mine': 0,
             'utility': 2,
             'cargo_cap': 30,
             'cost': {},
             'draw': draw_ship,
             'name': "Garvantex"}

Wanderer = {'velocity': 4.4,  # adj
            'acc': 0.1,  # adj
            'lat': 0.15,
            'rev': 0.05,
            'av': 0.75,  # adj
            'energy': 1300,
            'health': 175,
            'heat_capacity': 140,
            'heat_venting': 0.01,  # adj
            'height': 70,
            'width': 70,
            'range': 40000,
            'turrets': [],
            'thrust_pos': [np.array([-55, 42]), np.array([55, 42]), np.array([0, -52])],
            'turret_pos': [],
            'description': 'This ship is fast',
            'bullet_pos': [np.array([0, 25])],
            'missile_pos': [],
            'emblem_pos': [(30, 22)],
            'primary': 1,
            'secondary': 0,
            'mine': 1,
            'utility': 2,
            'cargo_cap': 20,
            'cost': {},
            'draw': draw_ship,
            'name': "Zaij's Wanderer"}

Prigozar = {'velocity': 2.2,  # adj
            'acc': 0.02,  # adj
            'lat': 0.15,
            'rev': 0.05,
            'av': 0.25,  # adj
            'energy': 3500,
            'health': 800,
            'heat_capacity': 450,
            'heat_venting': 0.02,  # adj
            'height': 110,
            'width': 110,
            'range': 50000,
            'turrets': ['PDC', 'PDC'],
            'thrust_pos': [np.array([-40, -45]), np.array([40, -45]), np.array([0, -43])],
            'turret_pos': [np.array([0, 18]), np.array([0, -16])],
            'description': 'This ship is fast',
            'bullet_pos': [np.array([-31, 45]), np.array([31, 45])],
            'missile_pos': [np.array([0, 37]), np.array([-33, -12]), np.array([33, -12])],
            'emblem_pos': [(50, 50)],
            'primary': 2,
            'secondary': 3,
            'mine': 0,
            'utility': 1,
            'cargo_cap': 70,
            'cost': {},
            'draw': draw_ship,
            'name': "Prigozar"}

Henik = {'velocity': 2,  # adj
         'acc': 0.05,  # adj
         'lat': 0.15,
         'rev': 0.05,
         'av': 0.75,  # adj
         'energy': 1800,
         'health': 300,
         'heat_capacity': 200,
         'heat_venting': 0.02,  # adj
         'height': 60,
         'width': 60,
         'range': 30000,
         'turrets': ['PDC'],
         'thrust_pos': [np.array([0, -30])],
         'turret_pos': [np.array([0, 2])],
         'description': 'This ship is fast',
         'bullet_pos': [np.array([-16, 19]), np.array([16, 19])],
         'missile_pos': [],
         'emblem_pos': [],
         'primary': 2,
         'secondary': 0,
         'mine': 0,
         'utility': 1,
         'cargo_cap': 30,
         'cost': {},
         'draw': draw_ship,
         'name': "Henik"}

Thades = {'velocity': 2.7,  # adj
          'acc': 0.05,  # adj
          'lat': 0.15,
          'rev': 0.05,
          'av': 0.5,  # adj
          'energy': 1200,
          'health': 375,
          'heat_capacity': 250,
          'heat_venting': 0.02,  # adj
          'height': 70,
          'width': 70,
          'range': 30000,
          'turrets': [],
          'thrust_pos': [np.array([0, -30])],
          'description': 'This ship is fast',
          'turret_pos': [],
          'bullet_pos': [np.array([-11, 11]), np.array([11, 11])],
          'missile_pos': [np.array([0, 10])],
          'emblem_pos': [],
          'primary': 2,
          'secondary': 1,
          'mine': 0,
          'utility': 1,
          'cargo_cap': 30,
          'cost': {},
          'draw': draw_ship,
          'name': "Thades"}

ShipNames = [Fighter, Uboat, HeavyFighter, Ghost, Pelomir, Harfute, Audigote, Pafonteer, Ontulus, Garvantex, Wanderer,
             Nasool, Prigozar, Henik, Thades, Dragonfly]

SHIPTYPES: dict[str, ShipType] = {ship['name']: ShipType(**ship) for ship in ShipNames}
