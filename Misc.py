"""https://github.com/russs123/Explosion/blob/main/explosion.py"""
import os
import random as rnd
from functools import partial
from typing import TYPE_CHECKING, Any

import numpy as np
import pygame

from Control_Functions import PlayerControl2, NPControl
from Data.Bullet_Types import BULLETTYPES, BULLETMETA
from Data.Debris_Types import DEBRISTYPES
from Data.Factions import FACTIONDICT, FactionType
from Data.Mine_Types import MINETYPES
from Data.Missile_Types import MISSILETYPES, MISSILEMETA
from Data.Ship_Types import SHIPTYPES, SHIPMETA
from Data.Station_Types import STATIONTYPES
from Data.Turret_Types import TURRETTYPES
from Data.Types import Entity, State, GameStateInt, BackgroundParticle, get_attr
from Data.Utility_Types import UTILITYTYPES
from Data.constants import *
from Menus2 import Button
from Ship_Class import Ship

if TYPE_CHECKING:
    pass


class GameState(GameStateInt):

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
        self.events = [e for event in self.events for e in event.scoot(self.entities)]
        self.entities = [entity for entity in self.entities if entity.health > 0]

    def generate_id(self, ids: set[str], celestial: Entity):
        char = type(celestial).__name__[0]
        i = 0
        while unique := f"{char}{i}" in ids:
            i += 1
        return unique


class LocalState(State):
    menu_names = ['faction selection', 'ship selection', 'weapon selection']
    FPS = 120  # define frame rate

    def __init__(self, x: int, y: int, height: int, width: int, player=None, menu=None):
        self.player: "Ship" = player
        self.x = x
        self.y = y
        self.height = height
        self.width = width
        self.menu = menu
        self.selected = None
        # self.particle_list = []  # behind ships
        # self.particle_list2 = []  # in front of ships
        self.lines = []  # lines in front of ship
        self.buttons: list[Button] = []
        self.mining_sound = pygame.mixer.Sound(os.path.join('Assets', 'mining.mp3'))
        self.mining = pygame.mixer.Channel(2)
        self.WIN = pygame.display.set_mode((width, height),
                                           pygame.SCALED | pygame.FULLSCREEN)  # create window
        self.images = {}
        # self.menu_names = {'faction selection', 'ship selection', 'weapon selection'}
        self.menu_name = 'faction selection'

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
        self.FIELD = pygame.transform.scale(
            pygame.image.load(os.path.join('Assets', 'middle_ground.png')),
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
                                   self.images['Asteroids'][
                                       rnd.randint(0, len(self.images['Asteroids']) - 1)]))

    @property
    def full_size(self):
        return self.height / 2

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

    @property
    def faction(self):
        if self.player:
            return self.player.faction
        return None

    def set_ship(self, faction: FactionType, ship_name: str, **kwargs):
        self.player = Ship(PlayerControl2, self.x, self.y, 0, self.ShipTypes[ship_name],
                           faction)
        self.player.refresh()

    def set_attr(self, slot_type: str, i: int, type_, **kwargs):
        self.player.__getattribute__(slot_type)[i].type = type_
        self.player.refresh()

    def select(self, value: Any, **kwargs):
        if self.selected == value:
            self.selected = None
        else:
            self.selected = value

    def next(self, *args, **kwargs):
        self.selected = None
        if self.menu_name in self.menu_names:
            i = self.menu_names.index(self.menu_name)
            if i < len(self.menu_names) - 1:
                self.menu_name = self.menu_names[i + 1]

    def last(self, *args, **kwargs):
        self.selected = None
        if self.menu_name in self.menu_names:
            i = self.menu_names.index(self.menu_name)
            if i > 0:
                self.menu_name = self.menu_names[i - 1]

    def exit_menu(self, *args, **kwargs):
        self.menu_name = ''

    def menu_buttons(self):
        spacing = 20
        mx, my = pygame.mouse.get_pos()
        nav_buttons = [Button(rect := (spacing, self.height - 60, 50, 200),
                              color=YELLOW if pygame.Rect(rect).collidepoint(mx, my)
                              else SILVER,
                              func=self.last),
                       Button(rect := (self.width - spacing - 200, self.height - 60, 50, 200),
                              color=YELLOW if pygame.Rect(rect).collidepoint(mx, my)
                              else (SILVER, BLUE)[self.menu_name == 'weapon selection'],
                              func=self.exit_menu if self.menu_name == 'weapon selection' else
                       self.next)
                       ]
        match self.menu_name:
            case 'faction selection':
                size = 200
                x = np.linspace(0, self.width, len(self.factions) + 2)[1:-1]
                return [Button(rect := (float(x[i]) - size / 2,
                                        (self.height - size) / 2,
                                        size + spacing,
                                        size + spacing),
                               pygame.transform.scale(faction.image, (size, size)),
                               func=partial(self.set_ship, faction, 'Corpus 9'),
                               color=YELLOW if pygame.Rect(rect).collidepoint(mx, my)
                               else (SILVER, GREEN)[self.faction is not None and faction.name ==
                        self.faction.name])
                        for i, faction in enumerate(self.factions.values())] + nav_buttons
            case 'ship selection':
                size = 160
                x = np.linspace(0, self.width, self.width // size)[1:-1]
                mx, my = pygame.mouse.get_pos()
                return [Button(rect := (float(x[i % len(x)]) - size / 2,
                                        spacing + (size + 2 * spacing) * (i // len(x)),
                                        size + spacing,
                                        size + spacing),
                               self.factions[self.faction.name].ship_images[ship]['L1'],
                               func=partial(self.set_ship, self.faction, ship),
                               rect_width=5,
                               color=YELLOW if pygame.Rect(rect).collidepoint(mx, my)
                               else (COLOR, GREEN)[ship == self.player.type.name])
                        for i, ship in enumerate(self.faction.ship_images)] + nav_buttons
            case 'weapon selection':
                buttons = []
                scale = self.full_size / self.player.image.get_width()
                size = 15 * scale
                for i, pos in enumerate(self.player.type.bullet_pos):
                    x = float(self.width / 2 + scale * pos[0] - size / 2)
                    y = float(self.height / 2 + scale * pos[1] - size / 2)
                    buttons.append(Button(rect := (x, y, size, size),
                                          rect_width=round(scale),
                                          func=partial(self.select, ('bullet_slots', i)),
                                          color=YELLOW if pygame.Rect(rect).collidepoint(mx, my)
                                          else (BLUE, GREEN)[self.selected == ('bullet_slots', i)]
                                          ))

                for i, pos in enumerate(self.player.type.missile_pos):
                    x = float(self.width / 2 + scale * pos[0] - size / 2)
                    y = float(self.height / 2 + scale * pos[1] - size / 2)
                    buttons.append(Button(rect := (x, y, size, size),
                                          rect_width=round(scale),
                                          func=partial(self.select, ('missile_slots', i)),
                                          color=YELLOW if pygame.Rect(rect).collidepoint(mx, my)
                                          else (BLUE, GREEN)[self.selected == ('missile_slots', i)]
                                          ))

                if type(self.selected) is tuple:
                    size = 40
                    x = spacing
                    y = np.linspace(spacing, self.height - size, len(self.BulletTypes) + 1)[:-1]
                    if self.selected[0] == 'bullet_slots':
                        buttons += [Button(rect := (x,
                                                    float(y[i]),
                                                    size + spacing,
                                                    size + spacing),
                                           pygame.transform.scale(bul.l_image, (size, size)),
                                           func=partial(self.set_attr, 'bullet_slots', self.selected[1],
                                                        bul),
                                           rect_width=5,
                                           color=YELLOW if pygame.Rect(rect).collidepoint(mx, my)
                                           else (BLACK, GREEN)[
                                               self.player.bullet_slots[self.selected[1]].type
                                               == bul])
                                    for i, bul in enumerate(self.BulletTypes.values())]
                    elif self.selected[0] == 'missile_slots':
                        buttons += [Button(rect := (x,
                                                    float(y[i]),
                                                    size + spacing,
                                                    size + spacing),
                                           pygame.transform.scale(mis.image, (size, size)),
                                           func=partial(self.set_attr, 'missile_slots',
                                                        self.selected[1],
                                                        mis),
                                           rect_width=5,
                                           color=YELLOW if pygame.Rect(rect).collidepoint(mx, my)
                                           else (BLACK, GREEN)[
                                               self.player.missile_slots[self.selected[1]].type
                                               == mis])
                                    for i, mis in enumerate(self.MissileTypes.values())]
                return buttons + nav_buttons

        # 'faction selection', 'ship selection', 'weapon selection'

    def draw(self):
        """
        draws buttons on surf
        :param surf: game window
        """

        match self.menu_name:
            case 'faction selection':
                self.WIN.fill((10, 10, 20))
            case 'ship selection':
                self.WIN.fill((10, 10, 20))
                height = self.fonts[2].get_height()
                y = [self.height / 2 + i * (height * 1.1) + 20 for i in range(len(SHIPMETA))]
                text_len = 100
                bar_len = 300
                x = self.width / 2 + 100

                text_surface = self.fonts[1].render(self.player.name,
                                                    antialias=True,
                                                    color=BLUE,
                                                    wraplength=text_len)
                self.WIN.blit(text_surface, (x, y[0] - self.fonts[1].get_height()))

                for i, (key, value) in enumerate(SHIPMETA.items()):
                    ratio = (get_attr(*value['args'], obj=self.player.type,
                                      func=value['func']) / value['max'])

                    color = ratio * np.array(GREEN) + (1 - ratio) * np.array(RED)

                    text_surface = self.fonts[2].render(key,
                                                        antialias=True,
                                                        color=SILVER,
                                                        wraplength=text_len)
                    self.WIN.blit(text_surface, (x, y[i]))
                    pygame.draw.rect(self.WIN,
                                     COLOR,
                                     (x + text_len, y[i], bar_len, height))
                    pygame.draw.rect(self.WIN,
                                     color,
                                     (x + text_len, y[i], bar_len * ratio, height))

            case 'weapon selection':
                self.WIN.fill(COLOR)
                image = pygame.transform.scale(self.player.image,
                                               (self.full_size, self.full_size))
                self.WIN.blit(image, (self.width / 2 - self.full_size / 2,
                                      self.height / 2 - self.full_size / 2))
                if (type(self.selected) is tuple and
                        self.selected[0] == 'bullet_slots' and
                        (slot := self.player.bullet_slots[self.selected[1]])):
                    height = self.fonts[2].get_height()
                    y = [round(self.height / 2 + i * (height * 1.1) + 20)
                         for i in range(len(BULLETMETA))]
                    text_len = 100
                    bar_len = 300
                    x = self.width - bar_len - text_len - 20

                    text_surface = self.fonts[1].render(slot.type.name,
                                                        antialias=True,
                                                        color=BLUE,
                                                        wraplength=text_len)
                    self.WIN.blit(text_surface, (x, y[0] - self.fonts[1].get_height()))

                    for i, (key, value) in enumerate(BULLETMETA.items()):
                        ratio = (get_attr(*value['args'],
                                          obj=slot.type,
                                          func=value['func']) / value['max'])

                        color = ratio * np.array(GREEN) + (1 - ratio) * np.array(RED)

                        text_surface = self.fonts[2].render(key,
                                                            antialias=True,
                                                            color=SILVER,
                                                            wraplength=text_len)
                        self.WIN.blit(text_surface, (x, y[i]))
                        pygame.draw.rect(self.WIN,
                                         BLACK,
                                         (x + text_len, y[i], bar_len, height))
                        pygame.draw.rect(self.WIN,
                                         color,
                                         (x + text_len, y[i], bar_len * ratio, height))
                elif (type(self.selected) is tuple and
                        self.selected[0] == 'missile_slots' and
                        (slot := self.player.missile_slots[self.selected[1]])):
                    height = self.fonts[2].get_height()
                    y = [round(self.height / 2 + i * (height * 1.1) + 20) for i in
                         range(len(MISSILEMETA))]
                    text_len = 100
                    bar_len = 300
                    x = self.width - bar_len - text_len - 20

                    text_surface = self.fonts[1].render(slot.type.name,
                                                        antialias=True,
                                                        color=BLUE,
                                                        wraplength=text_len)
                    self.WIN.blit(text_surface, (x, y[0] - self.fonts[1].get_height()))

                    for i, (key, value) in enumerate(MISSILEMETA.items()):
                        ratio = (get_attr(*value['args'],
                                          obj=slot.type,
                                          func=value['func']) / value['max'])

                        color = ratio * np.array(GREEN) + (1 - ratio) * np.array(RED)

                        text_surface = self.fonts[2].render(key,
                                                            antialias=True,
                                                            color=SILVER,
                                                            wraplength=text_len)
                        self.WIN.blit(text_surface, (x, y[i]))
                        pygame.draw.rect(self.WIN,
                                         BLACK,
                                         (x + text_len, y[i], bar_len, height))
                        pygame.draw.rect(self.WIN,
                                         color,
                                         (x + text_len, y[i], bar_len * ratio, height))

        for button in self.buttons:
            button.draw(self.WIN)
        pygame.display.update()

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
        if self.player:
            self.cx = self.player.centerx
            self.cy = self.player.centery
            self.player_commands()
        if self.menu_name:
            self.buttons = self.menu_buttons()
        else:
            self.buttons = []

        return self.menu_name == ''

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


def assign_util_cost(
        util):  # in case we want util costs to be formulaic later when utils are better fleshed out
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
