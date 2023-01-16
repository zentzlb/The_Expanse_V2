"""https://github.com/russs123/Explosion/blob/main/explosion.py"""
import pygame
import math
import os
import numpy as np
import random as rnd
from Ship_Types import ShipNames
from Station_Types import StationNames
from Turret_Types import TurretNames
from Bullet_Types import BulletNames
from Missile_Types import MissileNames
from Mine_Types import MineNames

# """SHIP EXPLOSION"""
#
#
# class ShipExplosion(pygame.sprite.Sprite):
#     def __init__(self, x, y, gs):
#         pygame.sprite.Sprite.__init__(self)
#         self.images = []
#         for num in range(1, 16):
#             img = pygame.image.load(f"Assets/Blast{num}.png")
#             img = pygame.transform.scale(img, (90, 90))
#             self.images.append(img)
#         self.index = 0
#         self.image = self.images[self.index]
#         self.x = x
#         self.y = y
#         self.gs = gs
#         self.rect = self.image.get_rect()
#         self.rect.center = [x - gs.x, y - gs.y]
#         self.counter = 0
#
#     def update(self):
#         explosion_speed = 2
#         self.counter += 1
#         self.rect.center = [self.x - self.gs.x, self.y - self.gs.y]
#
#         if self.counter >= explosion_speed and self.index < len(self.images) - 1:
#             self.counter = 0
#             self.index += 1
#             self.image = self.images[self.index]
#
#         if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
#             self.kill()
#
#
# """MISSILE EXPLOSION"""
#
#
# class MissileExplosion(pygame.sprite.Sprite):
#     def __init__(self, x, y, gs, exp_radius):
#         pygame.sprite.Sprite.__init__(self)
#         self.images = []
#         for num in range(1, 11):
#             img = pygame.image.load(f"Assets/smallblast{num}.png")
#             img = pygame.transform.scale(img, (exp_radius * 2, exp_radius * 2))
#             self.images.append(img)
#             gs.particle_list2.append(Particle(x, y, -rnd.randint(exp_radius // 10 - 1, exp_radius // 10 + 1),
#                                               rnd.randint(0, 360), 10,
#                                               (rnd.randint(100, 255), rnd.randint(100, 255), 100)))
#         self.index = 0
#         self.image = self.images[self.index]
#         self.x = x
#         self.y = y
#         self.gs = gs
#         self.rect = self.image.get_rect()
#         self.rect.center = [x - gs.x, y - gs.y]
#         self.counter = 0
#
#     def update(self):
#         explosion_speed = 2
#         self.counter += 1
#
#         self.rect.center = [self.x - self.gs.x, self.y - self.gs.y]
#
#         if self.counter >= explosion_speed and self.index < len(self.images) - 1:
#             self.counter = 0
#             self.index += 1
#             self.image = self.images[self.index]
#
#         if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
#             self.kill()
#
#
# """RAIL EXPLOSION"""
#
#
# class RailExplosion(pygame.sprite.Sprite):
#     def __init__(self, x, y, gs):
#         pygame.sprite.Sprite.__init__(self)
#         self.images = []
#         for num in range(1, 8):
#             img = pygame.image.load(f"Assets/railgun_blast{num}.png")
#             self.images.append(img)
#             gs.particle_list2.append(Particle(x, y, 3, rnd.randint(0, 360), 10, (0, 223, 255), shrink=0.5))
#         self.index = 0
#         self.image = self.images[self.index]
#         self.x = x
#         self.y = y
#         self.gs = gs
#         self.rect = self.image.get_rect()
#         self.rect.center = [x - gs.x, y - gs.y]
#         self.counter = 0
#
#     def update(self):
#         explosion_speed = 1
#         self.counter += 1
#         self.rect.center = [self.x - self.gs.x, self.y - self.gs.y]
#
#         if self.counter >= explosion_speed and self.index < len(self.images) - 1:
#             self.counter = 0
#             self.index += 1
#             self.image = self.images[self.index]
#
#         if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
#             self.kill()
#
#
# """PA EXPLOSION"""
#
#
# class PAExplosion(pygame.sprite.Sprite):
#     def __init__(self, x, y, gs):
#         pygame.sprite.Sprite.__init__(self)
#         self.images = []
#         for num in range(1, 14):
#             img = pygame.image.load(f"Assets/pa_blast{num}.png")
#             self.images.append(img)
#         self.index = 0
#         self.image = self.images[self.index]
#         self.x = x
#         self.y = y
#         self.gs = gs
#         self.rect = self.image.get_rect()
#         self.rect.center = [x - gs.x, y - gs.y]
#         self.counter = 0
#
#     def update(self):
#         explosion_speed = 1
#         self.counter += 1
#         self.rect.center = [self.x - self.gs.x, self.y - self.gs.y]
#
#         if self.counter >= explosion_speed and self.index < len(self.images) - 1:
#             self.counter = 0
#             self.index += 1
#             self.image = self.images[self.index]
#
#         if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
#             self.kill()
#
#
# """PARTICLE CLASS"""
#
#
# class Particle:
#     def __init__(self, x, y, v, angle, radius, color, shrink=0):
#         self.x = x
#         self.y = y
#         self.fx = x
#         self.fy = y
#         self.vx = v * math.sin(angle * math.pi / 180)
#         self.vy = v * math.cos(angle * math.pi / 180)
#         self.color = color
#         self.radius = radius
#         self.shrink = shrink
#
#     def update(self):
#         self.fx += self.vx
#         self.fy += self.vy
#         self.x = round(self.fx)
#         self.y = round(self.fy)
#         if rnd.random() > self.shrink:
#             self.radius -= 1


class GlobalState:
    def __init__(self, size, x, y, height, width, fonts, stations, ships, bullets, missiles, asteroids, pilots,
                 docked=None, menu=None):
        self.size = size
        self.x = x
        self.y = y
        self.stations = stations
        self.ships = ships
        self.bullets = bullets
        self.missiles = missiles
        self.asteroids = asteroids
        self.cx = x + width / 2
        self.cy = y + height / 2
        self.height = height
        self.width = width
        self.show_bars = False
        self.particle_list = []  # behind ships
        self.particle_list2 = []  # in front of ships
        self.fonts = fonts
        self.docked = docked
        self.menu = menu
        self.targets = []
        self.pilots = pilots
        self.mining_sound = pygame.mixer.Sound(os.path.join('Assets', 'mining.mp3'))
        self.mining = pygame.mixer.Channel(2)
        self.ShipTypes = make_dict(ShipNames)
        self.StationTypes = make_dict(StationNames)
        self.TurretTypes = make_dict(TurretNames)
        self.BulletTypes = make_dict(BulletNames)
        self.MissileTypes = make_dict(MissileNames)
        self.MineTypes = make_dict(MineNames)
        self.explosion_group = pygame.sprite.Group()  # initialize explosion group
        self.update()

    def update(self):
        self.targets = []
        for i in range(len(self.ships)):
            self.targets.append([])
            for j in range(len(self.ships)):
                if j != i:
                    self.targets[i].extend(self.ships[j])

    def play_mining(self, volume=1):
        if not self.mining.get_busy():
            self.mining.play(self.mining_sound)


def make_dict(List):
    Dict = {}
    for D in List:
        Dict[D['name']] = Dict2Object(D)
    return Dict


class Dict2Object:
    def __init__(self, dic):
        print(dic['name'])
        print(dic.keys())
        print()
        for key in dic.keys():
            exec(f"self.{key} = dic['{key}']")

"""WEAPON TYPES"""


# class BulletTypes:
#     def __init__(self, bullet_type):
#         if bullet_type == 'HV':
#             self.velocity = 12
#             self.damage = 4
#             self.energy = 14
#             self.range = 3000
#             self.delay = 25
#             self.height = 10
#             self.width = 10
#             self.cost = {"Iron": 10, "Nickel": 10, "Platinum": 1, "Gold": 0}
#             self.name = "HV"
#             self.pen = False
#             self.exptype = None
#             self.image = pygame.image.load(os.path.join('Assets', 'bullet.png'))  # bullet
#             self.sound = None
#         elif bullet_type == 'PA':
#             self.velocity = 8
#             self.damage = 50
#             self.energy = 110
#             self.range = 1500
#             self.delay = 150
#             self.height = 15
#             self.width = 15
#             self.cost = {"Iron": 10, "Nickel": 5, "Platinum": 5, "Gold": 10}
#             self.name = "PA"
#             self.pen = False
#             self.exptype = PAExplosion
#             self.image = pygame.image.load(os.path.join('Assets', 'Plasma.png'))  # bullet
#             self.sound = None
#         elif bullet_type == 'railgun':
#             self.velocity = 25
#             self.damage = 10
#             self.energy = 250
#             self.range = 8000
#             self.delay = 240
#             self.height = 30
#             self.width = 30
#             self.cost = {"Iron": 10, "Nickel": 25, "Platinum": 10, "Gold": 1}
#             self.name = "railgun"
#             self.pen = True
#             self.exptype = RailExplosion
#             self.image = pygame.image.load(os.path.join('Assets', 'railgun.png'))  # bullet
#             self.sound = pygame.mixer.Sound(os.path.join('Assets', 'railgun_launch.mp3'))
#
#
# class MissileTypes:
#     def __init__(self, missile_type):
#         self.name = missile_type
#         if missile_type == 'HE':
#             self.height = 12
#             self.width = 12
#             self.velocity = 10
#             self.angular_velocity = 0.75
#             self.damage = 13
#             self.explosion_damage = 7
#             self.energy = 150
#             self.range = 7000
#             self.delay = 120
#             self.explosion_radius = 100
#             self.emp = False
#             self.drunk = False
#             self.smart = False
#             self.par_str = 1
#             self.par_rnd = 0
#             self.cost = {"Iron": 100, "Nickel": 125, "Platinum": 10, "Gold": 10}
#             self.image = pygame.image.load(os.path.join('Assets', 'smallmissile1.png'))  # missile
#             self.sound = pygame.mixer.Sound('Assets//missile_launch.mp3')
#         if missile_type == 'torpedo':
#             self.height = 15
#             self.width = 15
#             self.velocity = 7.5
#             self.angular_velocity = 0.5
#             self.damage = 10
#             self.explosion_damage = 65
#             self.energy = 230
#             self.range = 2000
#             self.delay = 250
#             self.explosion_radius = 200
#             self.emp = True
#             self.drunk = False
#             self.smart = False
#             self.par_str = 4
#             self.par_rnd = 70
#             self.cost = {"Iron": 100, "Nickel": 50, "Platinum": 15, "Gold": 50}
#             self.image = pygame.image.load(os.path.join('Assets', 'torpedo.png'))  # missile
#             self.sound = pygame.mixer.Sound('Assets//missile_launch.mp3')
#         if missile_type == 'swarm missile':
#             self.height = 10
#             self.width = 10
#             self.velocity = 8
#             self.angular_velocity = 2.5
#             self.damage = 10
#             self.explosion_damage = 5
#             self.energy = 120
#             self.range = 4000
#             self.delay = 40
#             self.explosion_radius = 50
#             self.emp = False
#             self.drunk = True
#             self.smart = False
#             self.par_str = 2
#             self.par_rnd = 30
#             self.cost = {"Iron": 100, "Nickel": 50, "Platinum": 15, "Gold": 50}
#             self.image = pygame.image.load(os.path.join('Assets', 'swarm_missile.png'))  # missile
#             self.sound = pygame.mixer.Sound('Assets//missile_launch.mp3')
#         if missile_type == 'smart':
#             self.height = 12
#             self.width = 12
#             self.velocity = 10.5
#             self.angular_velocity = 0.5
#             self.damage = 10
#             self.explosion_damage = 5
#             self.energy = 220
#             self.range = 15000
#             self.delay = 240
#             self.explosion_radius = 60
#             self.emp = False
#             self.drunk = False
#             self.smart = True
#             self.par_str = 1
#             self.par_rnd = 0
#             self.cost = {"Iron": 100, "Nickel": 125, "Platinum": 10, "Gold": 10}
#             self.image = pygame.image.load(os.path.join('Assets', 'smartmissile.png'))  # missile
#             self.sound = pygame.mixer.Sound('Assets//missile_launch.mp3')
#
#
# class MineTypes:
#     def __init__(self, mine_type):
#         self.name = mine_type
#
#         if mine_type == 'black hole':
#             self.height = 19
#             self.width = 19
#             self.damage = 1
#             self.energy = 200
#             self.delay = 150
#             self.explosion_radius = 60
#             self.emp = False
#             self.grav = True
#             self.pen = True
#             self.par_str = 30
#             self.par_rnd = 0
#             self.time = 2000
#             self.cost = {"Iron": 100, "Nickel": 125, "Platinum": 10, "Gold": 10}
#             self.image = pygame.image.load(os.path.join('Assets', 'black_hole.png'))  # missile
#             self.sound = pygame.mixer.Sound('Assets//missile_launch.mp3')
#
#
# class ShipTypes:
#     def __init__(self, ship_type, color):
#         crg = CargoClass()
#         if ship_type == 'Fighter':
#             self.velocity = 5
#             self.acc = 0.3
#             self.av = 2
#             self.energy = 500
#             self.health = 125
#             self.height = 50
#             self.width = 50
#             self.range = 20000
#             self.turrets = []
#             self.turret_loc = []
#             self.cargo_cap = 50
#             self.cost = {"Iron": 100, "Nickel": 25, "Platinum": 25, "Gold": 5}
#             self.name = "Fighter"
#         if ship_type == 'Sprinter':
#             self.velocity = 6
#             self.acc = 0.45
#             self.av = 1.75
#             self.energy = 250
#             self.health = 100
#             self.height = 30
#             self.width = 30
#             self.range = 15000
#             self.turrets = []
#             self.turret_loc = []
#             self.cargo_cap = 10
#             self.cost = {"Iron": 50, "Nickel": 30, "Platinum": 30, "Gold": 10}
#             self.name = "Sprinter"
#         if ship_type == 'Frigate':
#             self.velocity = 3
#             self.acc = 0.25
#             self.av = 0.5
#             self.energy = 2000
#             self.health = 350
#             self.height = 80
#             self.width = 80
#             self.range = 30000
#             self.turrets = ['PDC']
#             self.turret_loc = [np.array([0, 0])]
#             self.cargo_cap = 1000
#             self.cost = {"Iron": 300, "Nickel": 50, "Platinum": 40, "Gold": 30}
#             self.name = "Frigate"
#         if ship_type == 'Destroyer':
#             self.velocity = 2.5
#             self.acc = 0.15
#             self.av = 0.2
#             self.energy = 10000
#             self.health = 1000
#             self.height = 150
#             self.width = 150
#             self.range = 50000
#             self.turrets = ['Rail', 'PDC', 'PDC']
#             self.turret_loc = [np.array([0, 0]), np.array([0, 41]), np.array([0, -41])]
#             self.cargo_cap = 1000
#             self.cost = {"Iron": 300, "Nickel": 50, "Platinum": 40, "Gold": 30}
#             self.name = "Frigate"
#         self.image = pygame.image.load(os.path.join('Assets', f'{ship_type}_{color}.png'))  # image with no flame
#         self.imagef = pygame.image.load(os.path.join('Assets', f'{ship_type}_{color}_f.png'))  # image with flame


class CargoClass(dict):
    def __init__(self):
        super().__init__()
        self.cargo = assign_ore('Cargo')

    def __missing__(self, key):
        return 0


class StationTypes:
    def __init__(self, station_type):
        if station_type == 'Partrid':
            self.energy = 500
            self.health = 100
            self.height = 250
            self.width = 250
            self.turrets = ['PDC']
            self.turret_loc = [np.array([0, 0])]
            self.image = pygame.image.load(os.path.join('Assets', f'{station_type}.png'))  # image with no flame


class TurretTypes:
    def __init__(self, turret_type):
        if turret_type == 'PDC':
            self.av = 1.5
            self.energy = 200
            self.health = 100
            self.height = 20
            self.width = 20
            self.bullet_type = 'HV'
            self.missile_type = None
        self.image = pygame.image.load(os.path.join('Assets', f'{turret_type}.png'))
        if turret_type == 'Rail':
            self.av = 0.3
            self.energy = 1000
            self.health = 200
            self.height = 29
            self.width = 29
            self.bullet_type = 'railgun'
            self.missile_type = None
        self.image = pygame.image.load(os.path.join('Assets', f'{turret_type}.png'))


"""FIND NEAREST ENTITY IN LIST"""


def FindNearest(xo, yo, target_list):
    if len(target_list) > 0:
        d = []
        for target in target_list:
            dx = target.centerx - xo
            dy = target.centery - yo
            # r = math.sqrt((target.centerx - xo) ** 2 + (target.centery - yo) ** 2)  # distance to target
            r2 = dx * dx + dy * dy
            a = target.is_visible  # is uncloaked
            # b = r < 1500  # is within visual range
            b = r2 < 2250000
            if a or b:  # and target.health > 0:  # only add ships to the target list if they're visible
                d.append(r2)
            else:
                d.append(math.inf)
        if len(d) > 0:
            ind = d.index(min(d))
            return target_list[ind]
        else:
            return None
    else:
        return None


def FindMineable(xo, yo, target_list):
    if len(target_list) > 0:
        d = []
        for target in target_list:
            r = math.sqrt((target.centerx - xo) ** 2 + (target.centery - yo) ** 2)  # distance to target
            if sum(target.ore.values()) > 0:  # only look for asteroid with ore
                d.append(r)
            else:
                d.append(math.inf)
        if len(d) > 0 and min(d) < math.inf:
            ind = d.index(min(d))
            return target_list[ind]
        else:
            return None
    else:
        return None


"""EXPLOSION DAMAGE CALCULATION"""


def ExplosionDamage(max_damage, xo, yo, exp, target_list, gs):
    for target in target_list:
        d = (math.sqrt((target.centerx - xo) ** 2 + (target.centery - yo) ** 2))
        r = math.sqrt(target.height * target.width)
        if d < exp + r:
            damage = round(2 * max_damage / (1 + math.exp((d + 1) / (r + exp + 1))))
            target.health -= damage
            target.sop += 2 * damage
            # if target.health <= 0:
            #     explosion = ShipExplosion(target.centerx, target.centery, gs)
            #     explosion_group.add(explosion)


"""TARGETING COMPUTER LOGIC"""


def TargetingComputer(ship):
    vx = ship.target.vx
    vy = ship.target.vy
    xo = ship.target.centerx
    yo = ship.target.centery

    a = vx ** 2 + vy ** 2 - ship.bullet_types[ship.bullet_sel].velocity ** 2
    b = 2 * (vx * (xo - ship.centerx) + vy * (yo - ship.centery))
    c = (xo - ship.centerx) ** 2 + (yo - ship.centery) ** 2

    t = (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    x = xo + vx * t
    y = yo + vy * t

    dx = x - ship.centerx
    dy = y - ship.centery

    # cos = math.cos(ship.angle * math.pi / 180)
    # sin = math.sin(ship.angle * math.pi / 180)
    #
    # Q = np.array([[cos, -sin], [sin, cos]])
    # V = np.array([[dx], [dy]])
    # V_prime = Q.dot(V)
    # angle2 = math.atan2(V_prime[0][0], V_prime[1][0])

    angle2 = math.atan2(dy, dx)

    return angle2


def MoveScreen(gs):
    keys_pressed = pygame.key.get_pressed()
    if keys_pressed[pygame.K_UP]:  # UP
        gs.y -= 15
        gs.cy -= 15
    elif keys_pressed[pygame.K_DOWN]:  # DOWN
        gs.y += 15
        gs.cy += 15
    if keys_pressed[pygame.K_RIGHT]:  # RIGHT
        gs.x += 15
        gs.cx += 15
    elif keys_pressed[pygame.K_LEFT]:  # LEFT
        gs.x -= 15
        gs.cx -= 15


def assign_ore(name):
    if name == 'Std':  # standard asteroid with iron, nickel, platinum, and gold
        return {"Iron": rnd.randint(200, 300), "Nickel": rnd.randint(100, 200), "Platinum": rnd.randint(25, 125),
                "Gold": rnd.randint(0, 75)}
    if name == 'Cargo':  # shortcut to assign empty cargo to new ships
        return {"Iron": 0, "Nickel": 0, "Platinum": 0, "Gold": 0}


def check_purchase(station, target):
    for i in range(len(target.cost)):
        ore_names = list(target.cost)
        if station.cargo[ore_names[i]] < target.cost[ore_names[i]]:
            return False
    return True


def purchase(station, target):
    for i in range(len(target.cost)):
        ore_names = list(target.cost)
        station.cargo[ore_names[i]] -= target.cost[ore_names[i]]


def RequestUndock(ship, global_state, faction):
    if ship.is_player:
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_b]:
            return True
    elif rnd.random() > 0.999:
        return True
    else:
        return False


"""UTILITY SLOTS"""


def auto_loader(ship, gs):
    if ship.missileC > 1 and ship.energy > 1:
        ship.missileC -= 1
        ship.energy -= 1
