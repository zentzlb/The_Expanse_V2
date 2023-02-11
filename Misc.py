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
from Utility_Types import UtilityNames


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
        self.WIN = pygame.display.set_mode((width, height), pygame.SCALED | pygame.FULLSCREEN)  # create window
        # self.WIN.set_alpha(255)
        # self.WIN2 = pygame.Surface((width, height), pygame.SRCALPHA)  # create transparent surface
        # self.HUD = pygame.Surface((width, height), pygame.SRCALPHA)  # create HUD surface
        self.ShipTypes = make_dict(ShipNames)
        for Type in list(self.ShipTypes):
            self.ShipTypes[Type].cost = assign_ship_cost(self.ShipTypes[Type])
        self.StationTypes = make_dict(StationNames)
        self.TurretTypes = make_dict(TurretNames)
        self.BulletTypes = make_dict(BulletNames)
        for Type in list(self.BulletTypes):
            self.BulletTypes[Type].cost = assign_bullet_cost(self.BulletTypes[Type])
        self.MissileTypes = make_dict(MissileNames)
        for Type in list(self.MissileTypes):
            self.MissileTypes[Type].cost = assign_missile_cost(self.MissileTypes[Type])
        self.MineTypes = make_dict(MineNames)
        for Type in list(self.MineTypes):
            self.MineTypes[Type].cost = assign_mine_cost(self.MineTypes[Type])
        self.UtilTypes = make_dict(UtilityNames)
        for Type in list(self.UtilTypes):
            self.UtilTypes[Type].cost = assign_util_cost(self.UtilTypes[Type])
        self.explosion_group = pygame.sprite.Group()  # initialize explosion group
        self.SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space2.png')),
                                       (width, height)).convert_alpha()  # background image
        self.dust = []
        self.dust_images = [pygame.image.load(os.path.join('Assets', 'dust4.png')).convert_alpha(), pygame.image.load(os.path.join('Assets', 'dust5.png')).convert_alpha(), pygame.image.load(os.path.join('Assets', 'dust6.png')).convert_alpha()]
        for i in range(250):
            self.dust.append((rnd.randint(0, 6000), rnd.randint(0, 6000), rnd.randint(0, 2)))
        # self.DUST = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space_dust_new.png')),
        #                               (6000, 6000)).convert_alpha()  # foreground image
        self.FIELD = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'middle_ground.png')),
                                       (6000, 6000)).convert_alpha()  # middle ground image
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


def assign_ship_cost(ship):
    cost = {"Iron": int(ship.height*3), "Nickel": int(ship.velocity*20), "Platinum": int(ship.energy/50), "Gold": int(ship.av*50)}
    return cost


def assign_bullet_cost(bullet):
    cost = {"Iron": bullet.height, "Nickel": int(bullet.range/300), "Platinum": int(bullet.delay/12), "Gold": int(bullet.damage/5)}
    return cost


def assign_missile_cost(missile):
    cost = {"Iron": int(missile.height*10), "Nickel": int(missile.range/100), "Platinum": int(missile.delay/20), "Gold": missile.exp_damage}
    return cost


def assign_mine_cost(mine):
    cost = {"Iron": int(mine.height*5), "Nickel": int(mine.time/20), "Platinum": int(mine.delay/20), "Gold": int(mine.arm/10)}
    return cost


def assign_util_cost(util):  # in case we want util costs to be formulaic later when utils are better fleshed out
    cost = {"Iron": 50, "Nickel": 50, "Platinum": 20, "Gold": 10}
    return cost


class Dict2Object:
    def __init__(self, dic):
        # print(dic['name'])
        # print(dic.keys())
        # print()
        for key in dic.keys():
            exec(f"self.{key} = dic['{key}']")
        if hasattr(self, 'image'):
            # print(self.name)
            self.image.convert_alpha()


class CargoClass(dict):  # inventory class
    def __init__(self):
        super().__init__()
        self.cargo = {}
        self.cargo_total = 0

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


def FindNearest(ship, target_list):
    if len(target_list) > 0:
        # d = []
        ind = 0
        min_r2 = math.inf
        rng2 = ship.range * ship.range
        for target in target_list:
            dx = target.centerx - ship.centerx
            dy = target.centery - ship.centery

            r2 = dx * dx + dy * dy
            a = target.is_visible and r2 < rng2  # is uncloaked and within radar range
            b = r2 < 2250000  # is within visual range
            c = r2 < min_r2 and target.health > 0

            if c and (a or b):  # and target.health > 0:  # only add ships to the target list if they're visible
                min_r2 = r2
                ind = target
            # else:
            #     d.append(math.inf)
        if min_r2 < math.inf:
            return ind
        else:
            return None
    else:
        return None


def FindMineable(ship, target_list):
    if len(target_list) > 0:
        # d = []
        ind = 0
        min_r2 = math.inf
        rng2 = ship.range * ship.range
        for i in range(len(target_list)):
            target = target_list[i]
            dx = target.centerx - ship.centerx
            dy = target.centery - ship.centery

            r2 = dx * dx + dy * dy
            a = sum(target.ore.values()) > 0 and r2 < rng2  # is uncloaked and within radar range  target.is_visible and  and
            # b = r2 < 2250000  # is within visual range
            c = r2 < min_r2

            if c and a:  # and target.health > 0:  # only add ships to the target list if they're visible
                min_r2 = r2
                ind = i
            # else:
            #     d.append(math.inf)
        if min_r2 < math.inf:
            return target_list[ind]
        else:
            return None
    else:
        return None



    # if len(target_list) > 0:
    #     d = []
    #     for target in target_list:
    #         r = math.sqrt((target.centerx - xo) ** 2 + (target.centery - yo) ** 2)  # distance to target
    #         if sum(target.ore.values()) > 0:  # only look for asteroid with ore
    #             d.append(r)
    #         else:
    #             d.append(math.inf)
    #     if len(d) > 0 and min(d) < math.inf:
    #         ind = d.index(min(d))
    #         return target_list[ind]
    #     else:
    #         return None
    # else:
    #     return None


# """EXPLOSION DAMAGE CALCULATION"""
#
#
# def ExplosionDamage(max_damage, xo, yo, exp, target_list, gs):
#     for target in target_list:
#         d = (math.sqrt((target.centerx - xo) ** 2 + (target.centery - yo) ** 2))
#         r = math.sqrt(target.height * target.width)
#         if d < exp + r:
#             damage = round(2 * max_damage / (1 + math.exp((d + 1) / (r + exp + 1))))
#             target.health -= damage
#             target.sop += 2 * damage


"""TARGETING COMPUTER LOGIC"""


def TargetingComputer(ship):
    pos = ship.Q.transpose().dot(ship.ship_type.bullet_pos[ship.bullet_sel]) - np.array(
        [ship.bullet_types[ship.bullet_sel].width // 2, ship.bullet_types[ship.bullet_sel].height // 2])

    vx = ship.target.vx
    vy = ship.target.vy
    xo = ship.target.centerx - pos[0]
    yo = ship.target.centery - pos[1]

    a = vx ** 2 + vy ** 2 - ship.bullet_types[ship.bullet_sel].velocity ** 2
    b = 2 * (vx * (xo - ship.centerx) + vy * (yo - ship.centery))
    c = (xo - ship.centerx) ** 2 + (yo - ship.centery) ** 2

    t = (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    x = xo + vx * t
    y = yo + vy * t

    dx = x - ship.centerx
    dy = y - ship.centery

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



