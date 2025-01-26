"""https://github.com/russs123/Explosion/blob/main/explosion.py"""
import pygame
import math
import os
import numpy as np
import random as rnd
from Data.Ship_Types import SHIPTYPES
from Data.Station_Types import STATIONTYPES
from Data.Turret_Types import TURRETTYPES
from Data.Bullet_Types import BULLETTYPES
from Data.Missile_Types import MISSILETYPES
from Data.Mine_Types import MINETYPES
from Data.Utility_Types import UTILITYTYPES
from Data.Debris_Types import DEBRISTYPES
from Data.Factions import FACTIONDICT
from Data.Types import Entity, State, GlobalStateInt, LocalStateInt, BackgroundParticle, Shooter
from typing import TYPE_CHECKING, Any
from Explosions import ShipExplosion

if TYPE_CHECKING:
    from Ship_Class import Ship, Base, Asteroid
    from Weapon_Class import Bullet, Missile, Mine


class GlobalState(GlobalStateInt):

    def __init__(self, size: tuple[int, int], entities: list[Entity]):
        self.radio = {}
        self.size = size
        self.entities = entities
        self.events = []
        self.lines = []  # lines in front of ship
        self.mining_sound = pygame.mixer.Sound(os.path.join('Assets', 'mining.mp3'))
        self.mining = pygame.mixer.Channel(2)
        self.explosion_group = pygame.sprite.Group()

    def __call__(self, class_: Any):
        return [entity for entity in self.entities if isinstance(entity, class_)]

    def update(self):
        self.events += [event for entity in self.entities for event in entity.scoot(self.entities)]
        self.events = [event for event in self.events if event.scoot()]
        self.entities = [entity for entity in self.entities if entity.health > 0]

    def generate_id(self, ids: set[str], celestial: Entity):
        char = type(celestial).__name__[0]
        i = 0
        while unique := f"{char}{i}" in ids:
            i += 1
        return unique


class LocalState(State):
    COLOR = (40, 10, 35)  # define window color
    BLACK = (0, 50, 0)  # BLACK
    RED = (255, 0, 0)  # RED
    YELLOW = (255, 255, 0)  # YELLOW

    FPS = 120  # define frame rate

    def __init__(self, x: int, y: int, height: int, width: int, player=None, menu=None):
        self.player: "Ship" = player
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        # self.particle_list = []  # behind ships
        # self.particle_list2 = []  # in front of ships
        self.lines = []  # lines in front of ship
        self.menu = menu
        self.mining_sound = pygame.mixer.Sound(os.path.join('Assets', 'mining.mp3'))
        self.mining = pygame.mixer.Channel(2)
        self.WIN = pygame.display.set_mode((width, height), pygame.SCALED | pygame.FULLSCREEN)  # create window
        self.images = {}
        self.misc_info = {'command prompt': False, 'command text': '', 'command history': []}
        self.fonts = [pygame.font.SysFont('Agency FB', 25),
                      pygame.font.SysFont('Agency FB', 20),
                      pygame.font.SysFont('Agency FB', 15)]
        self.factions = FACTIONDICT
        self.ShipTypes = SHIPTYPES
        for Type in list(self.ShipTypes):
            self.ShipTypes[Type].cost = assign_ship_cost(self.ShipTypes[Type])
        self.StationTypes = STATIONTYPES
        self.TurretTypes = TURRETTYPES
        self.BulletTypes = BULLETTYPES
        for Type in list(self.BulletTypes):
            self.BulletTypes[Type].cost = assign_bullet_cost(self.BulletTypes[Type])
        self.MissileTypes = MISSILETYPES
        for Type in list(self.MissileTypes):
            self.MissileTypes[Type].cost = assign_missile_cost(self.MissileTypes[Type])
        self.MineTypes = MINETYPES
        for Type in list(self.MineTypes):
            self.MineTypes[Type].cost = assign_mine_cost(self.MineTypes[Type])
        self.UtilTypes = UTILITYTYPES
        for Type in list(self.UtilTypes):
            self.UtilTypes[Type].cost = assign_util_cost(self.UtilTypes[Type])
        self.DebrisTypes = DEBRISTYPES
        # self.explosion_group = pygame.sprite.Group()  # initialize explosion group
        self.SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space2.png')),
                                            (width, height)).convert()  # background image
        self.dust = []
        self.field = []
        self.dust_images = [pygame.image.load(os.path.join('Assets', 'dust4.png')).convert_alpha(),
                            pygame.image.load(os.path.join('Assets', 'dust5.png')).convert_alpha(),
                            pygame.image.load(os.path.join('Assets', 'dust6.png')).convert_alpha()]
        for image in self.dust_images:
            image.set_alpha(100)
        # self.field_images = [pygame.image.load(os.path.join('Assets', 'asteroid80nl.png')).convert_alpha()]

        # self.DUST = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space_dust_new.png')),
        #                               (6000, 6000)).convert_alpha()  # foreground image
        self.FIELD = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'middle_ground.png')),
                                            (6000, 6000)).convert_alpha()  # middle ground image
        self.make_faction_ships()
        self.load_images('Assets')
        for i in range(300):
            self.dust.append((rnd.randint(0, 6000),
                              rnd.randint(0, 6000),
                              rnd.randint(0, len(self.dust_images) - 1)))
        for i in range(50):
            self.field.append(
                BackgroundParticle(rnd.randint(0, 24000),
                                   rnd.randint(0, 24000),
                                   self.images['Asteroids'][rnd.randint(0, len(self.images['Asteroids']) - 1)]))

    @property
    def cx(self) -> int:
        return self.x + self.width // 2

    @cx.setter
    def cx(self, value: float):
        self.x = value - self.width // 2

    @property
    def cy(self) -> int:
        return self.y + self.height // 2

    @cy.setter
    def cy(self, value: float):
        self.y = value - self.height // 2

    @property
    def faction_names(self):
        return list(self.factions.keys())

    @property
    def ship_names(self):
        return list(self.ShipTypes.keys())

    def play_mining(self, volume=1):
        if not self.mining.get_busy():
            self.mining.play(self.mining_sound)

    def load_images(self, rootdir: str) -> None:
        """
        load images from folder
        :param rootdir: path to folder
        :return:
        """
        Dirs = []
        for subdir, dirs, files in os.walk(rootdir):
            if len(dirs) != 0:
                Dirs.extend(dirs)
        for Dir in Dirs:
            directory = os.path.join(rootdir, Dir)
            image_list = []
            for file in os.listdir(directory):
                path = os.path.join(directory, file)
                image = pygame.image.load(path)
                image.convert_alpha()
                image_list.append(image)
            self.images[Dir] = image_list
            # return image_list

    def update(self):
        self.cx = self.player.centerx
        self.cy = self.player.centery
        self.player_commands()

    def make_faction_ships(self):
        """

        :return:
        """
        print('generating ship images...')
        for name in self.faction_names:
            faction = self.factions[name]
            for ship in self.ship_names:
                L1 = pygame.image.load(os.path.join('Assets', f'{ship}', 'L1.png'))
                L2 = pygame.image.load(os.path.join('Assets', f'{ship}', 'L2.png'))
                for w in range(L1.get_width()):
                    for h in range(L1.get_height()):
                        color1 = L1.get_at((w, h))
                        color2 = L2.get_at((w, h))
                        if color1 == (18, 52, 86, 255):
                            L1.set_at((w, h), faction.color)
                        if color2 == (18, 52, 86, 255):
                            L2.set_at((w, h), faction.color)

                for emblem in self.ShipTypes[ship].emblem_pos:
                    L2.blit(faction.image, emblem)
                faction.ship_images[ship] = {'L1': L1, 'L2': L2}
        print('done')

    def player_commands(self):
        if not self.misc_info['command prompt']:
            x, y = pygame.mouse.get_pos()
            dx = x - self.width // 2
            dy = y - self.height // 2
            self.player.info['V'] = np.array([[dx], [dy]])


def assign_ship_cost(ship):
    cost = {"Iron": int(ship.height * 3),
            "Nickel": int(ship.velocity * 20),
            "Platinum": int(ship.energy / 50),
            "Gold": int(ship.av * 50)}
    return cost


def assign_bullet_cost(bullet):
    cost = {"Iron": bullet.height,
            "Nickel": int(bullet.range / 300),
            "Platinum": int(bullet.delay / 12),
            "Gold": int(bullet.damage / 5)}
    return cost


def assign_missile_cost(missile):
    cost = {"Iron": int(missile.height * 10),
            "Nickel": int(missile.range / 100),
            "Platinum": int(missile.delay / 20),
            "Gold": missile.exp_damage}
    return cost


def assign_mine_cost(mine):
    cost = {"Iron": int(mine.height * 5),
            "Nickel": int(mine.time / 20),
            "Platinum": int(mine.delay / 20),
            "Gold": int(mine.arm / 10)}
    return cost


def assign_util_cost(util):  # in case we want util costs to be formulaic later when utils are better fleshed out
    cost = {"Iron": 50,
            "Nickel": 50,
            "Platinum": 20,
            "Gold": 10}
    return cost


# class Dict2Object:
#     def __init__(self, dic):
#         for key in dic.keys():
#             exec(f"self.{key} = dic['{key}']")
#         if hasattr(self, 'image'):
#             # print(self.name)
#             self.image.convert_alpha()


class StationTypes:
    def __init__(self, station_type):
        if station_type == 'Partrid':
            self.energy = 500
            self.health = 100
            self.height = 250
            self.width = 250
            self.turrets = ['PDC']
            self.turret_loc = [np.array([0, 0])]
            self.image = pygame.image.load(
                os.path.join('Assets', f'{station_type}.png'))  # image with no flame


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
        self.image = pygame.image.load(
            os.path.join('Assets', f'{turret_type}.png'))
        if turret_type == 'Rail':
            self.av = 0.3
            self.energy = 1000
            self.health = 200
            self.height = 29
            self.width = 29
            self.bullet_type = 'railgun'
            self.missile_type = None
        self.image = pygame.image.load(
            os.path.join('Assets', f'{turret_type}.png'))


"""FIND NEAREST ENTITY IN LIST"""





def assign_ore(name):
    if name == 'Std':  # standard asteroid with iron, nickel, platinum, and gold
        return {"Iron": rnd.randint(200, 300),
                "Nickel": rnd.randint(100, 200),
                "Platinum": rnd.randint(25, 125),
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
