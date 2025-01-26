import pygame
import math
import numpy as np
import random as rnd
import os
from Explosions import ShipExplosion

from Weapon_Class import Missile, Mine
# from Misc import assign_ore, RequestUndock, GlobalState, LocalState
from Data.Types import Entity, Event, Particle, Shooter
from typing import Callable
from constants import DRAG
from Data.Types import (ShipType, BulletType, MissileType, MineType, UtilityType, TurretType, CargoClass,
                        TypeType, Vessel, FactionType, StationType)


class Ship(Shooter):

    def __init__(self,
                 control_module: Callable,
                 x: float,
                 y: float,
                 angle: float,
                 ship_type: ShipType,
                 faction: FactionType):
        super().__init__(x, y, ship_type.height, ship_type.width)
        self.faction = faction
        self.type: ShipType = ship_type
        self.bullet_types: list[BulletType] = []
        self.missile_types: list[MissileType] = []
        self.mine_types: list[MineType] = []
        self.util_types: list[UtilityType] = []

        self.heat: float = 0

        self.vx = 0
        self.vy = 0
        self.counter = 0
        self.bulletC = 0
        self.missileC = 0
        self.utilC = 0

        self.bullet_sel = 0
        self.missile_sel = 0
        self.mine_sel = 0
        self.util_sel = 0

        self.info = {}

        self.angle = angle

        self.energy = self.max_energy

        self.target = None
        self.control_module = control_module

        self.turrets = []
        self.cargo = CargoClass()
        self.forward = False
        self.boost = False
        self.cloaked = False
        self.hidden = False

        self.image = pygame.Surface((self.width, self.height))
        self.image_cloaked = self.image
        self.refresh()

    def __str__(self):
        return (f"{self.faction_name}"
                f"|{self.type.name}"
                f"|{'|'.join([bullet.name for bullet in self.bullet_types])}"
                f"|{'|'.join([missile.name for missile in self.missile_types])}")

    def __repr__(self):
        return self.__str__()

    def __sub__(self, other):
        self.health -= other
        if self.health <= 0:
            return ShipExplosion(self)
        return []

    @property
    def acc(self):
        return self.type.acc

    @property
    def lat(self):
        return self.acc * self.type.lat

    @property
    def rev(self):
        return self.acc * self.type.rev

    @property
    def heat_cap(self):
        return self.type.heat_capacity

    @property
    def is_visible(self):
        if self.cloaked and self.bulletC == 0 and self.missileC == 0 or self.hidden:
            return False
        return True

    @property
    def bullet_pos(self) -> np.ndarray:
        return self.type.bullet_pos[self.bullet_sel]

    @property
    def missile_pos(self) -> np.ndarray:
        return self.type.missile_pos[self.missile_sel]

    def concealed(self, entity_list: list[Entity]):
        if rnd.random() > 0.99:
            if self.collidelistall([asteroid for asteroid in entity_list if isinstance(asteroid, Asteroid)]):
                self.hidden = True
            else:
                self.hidden = False

    def update_turrets(self):
        self.turrets = [Turret(self.x,
                               self.y,
                               pos,
                               self.angle,
                               turret,
                               self) for pos, turret in zip(self.type.turret_pos, self.type.turrets)]

    def refresh(self):
        self.height = self.type.height
        self.width = self.type.width
        self.energy = self.type.energy
        self.health = self.type.health
        # self.image = pygame.image.load(os.path.join('Assets', f'{self.ship_type.name}', 'L1.png'))
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        self.image_cloaked = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        L1 = self.faction.ship_images[self.type.name]['L1']
        L2 = self.faction.ship_images[self.type.name]['L2']
        self.image.blit(L1, (0, 0))

        for pos, bullet in zip(self.type.bullet_pos, self.bullet_types):
            x = self.width // 2 + pos[0] - bullet.l_image.get_width() // 2
            y = self.height // 2 + pos[1] - bullet.l_image.get_height() // 2
            self.image.blit(bullet.l_image, (x, y))

        for pos, missile in zip(self.type.missile_pos, self.missile_types):
            x = self.width // 2 + pos[0] - missile.image.get_width() // 2
            y = self.height // 2 + pos[1] - missile.image.get_height() // 2
            self.image.blit(missile.image, (x, y))

        self.image.blit(L2, (0, 0))
        self.image.convert_alpha()

    def scoot(self, entity_list: list[Entity]) -> list[Event]:

        commands = self.control_module(self, entity_list)
        self.forward = False
        events = []

        self.vx *= DRAG
        self.vy *= DRAG

        """WEAPON SELECTION"""
        if commands[10] != 0:
            self.bullet_sel = commands[10] - 1

        if commands[11] != 0:
            self.missile_sel = commands[11] - 1

        if commands[12] != 0:
            self.mine_sel = commands[12] - 1

        if commands[13] != 0:
            self.util_sel = commands[13] - 1

        """MOVEMENT- THRUSTER ACCELERATION"""

        if commands[7] == 1 and commands[1] == 1 and self.energy > 0.3:  # boost
            self.boost = True
            velocity = self.velocity * 1.25
            acc = self.acc * 1.25
            av = self.av * 0.9
            self.energy -= 0.3
            self.heat += 0.03
            size = 4
        else:
            self.boost = False
            velocity = self.velocity
            acc = self.acc
            av = self.av
            size = 3

        if commands[0] == 1:  # ROTATE CCW
            self.angle += av
        elif commands[0] == -1:  # ROTATE CW
            self.angle -= av

        if commands[1] == 1:  # UP
            self.vx += acc * math.sin(self.radians)
            self.vy += acc * math.cos(self.radians)
            self.forward = True
            self.heat += 0.02

            R = 255
            G = rnd.randint(0, 255)

            events += [Particle(*(self.center + self.Qt.dot(thrust)), -rnd.randint(10, 12),
                                self.angle + rnd.randint(-15, 15), size, (R, G, 0), shrink=0.5,
                                vx=self.vx,
                                vy=self.vy,
                                glow=(R // 2, G // 2, 0)) for thrust in self.type.thrust_pos]

        elif commands[1] == -1:  # DOWN
            self.vx -= self.rev * math.sin(self.radians)
            self.vy -= self.rev * math.cos(self.radians)
            self.heat += 0.005
        if commands[2] == 1:  # LEFT
            self.vy -= self.lat * math.sin(self.radians)
            self.vx += self.lat * math.cos(self.radians)
            self.heat += 0.01
        elif commands[2] == -1:  # RIGHT
            self.vy += self.lat * math.sin(self.radians)
            self.vx -= self.lat * math.cos(self.radians)
            self.heat += 0.001

        if commands[6] == 1 and self.utilC == 0 and len(self.util_types) > 0:
            self.utility.function(self, entity_list, self.faction)
            self.utilC += self.utility.delay

        """UPDATE VELOCITY AND POSITION"""
        if self.speed > velocity:
            self.speed = velocity

        self.x += self.vx
        self.y += self.vy

        """FIRE BULLETS and MISSILES"""
        if commands[3] == 1 and len(self.bullet_types) > 0 and self.bulletC == 0:
            i, bullet_name = self.bullet_sel, self.bullet.name
            for j in range(len(self.bullet_types)):
                self.bullet_sel = j
                if self.energy >= self.bullet.energy and self.bullet.name == bullet_name:  # DOWN
                    self.energy -= self.bullet.energy
                    events += self.bullet.init(self, entity_list)
            self.bulletC = self.bullet.delay

        if commands[4] == 1 and self.missileC == 0 and len(self.missile_types) > 0 and self.target is not None:

            i, missile_name = self.missile_sel, self.missile.name
            for j in range(len(self.missile_types)):
                self.missile_sel = j
                if self.energy >= self.missile.energy and self.missile.name == missile_name:  # DOWN
                    self.energy -= self.missile.energy
                    events += self.missile.init(self, entity_list)
            self.missileC = self.missile.delay

        if commands[5] == 1 and len(self.mine_types) > 0 and self.energy >= self.mine.energy and self.missileC == 0:
            self.energy -= self.mine.energy
            self.missileC = self.mine.delay
            events += self.mine.init(self, entity_list)

        if commands[6] == 1 and self.utilC == 0 and len(self.util_types) > 0:
            self.utility.function(self, entity_list, self.faction_name)
            self.utilC += self.utility.delay

        """DOCK"""
        if commands[8] == 1:
            pass

        """MINE ASTEROID"""
        if commands[9] == 1 and type(self.target) is Asteroid and self.colliderect(
                self.target):  # harvest from asteroid
            roid = self.target  # identify specific asteroid from list
            # else:
            roid.mine(self)
            if sum(roid.ore.values()) > 0:
                events.append(Particle(self.centerx, self.centery, rnd.random(),
                                       rnd.randint(0, 360), rnd.randint(4, 6),
                                       (rnd.randint(0, 50), rnd.randint(0, 50),
                                        rnd.randint(0, 50)), 0.95))

            else:
                events.append(
                    Particle(self.centerx, self.centery, rnd.random(),
                             rnd.randint(0, 360), rnd.randint(4, 6),
                             (50, 50, 50), 0.95))

        """UPDATE ENERGY, HEALTH, AND VISIBILITY"""

        # if self.utilC == 0 and self.cloaked:
        #     self.cloaked = False
        #     self.image.set_alpha(255)

        self.concealed(entity_list)

        if not self.cloaked:
            heat_loss = 0.01 + self.type.heat_venting * (self.heat / self.heat_cap) ** 2  # adj
            if self.heat > heat_loss:
                self.heat -= heat_loss
                if self.heat > self.type.heat_capacity:
                    events += self - (self.heat - self.type.heat_capacity) / 1000
                    # self.heat = self.type.heat_capacity
            else:
                self.heat = 0

            if self.energy < self.max_energy and not self.cloaked:
                self.energy += 0.25  # adj
            if self.health < self.max_health and self.heat == 0:
                self.health += 0.025  # adj
                if self.health > self.max_health:
                    self.health = self.max_health
        if self.bulletC > 0:
            self.bulletC -= 1
        if self.missileC > 0:
            self.missileC -= 1
        if self.utilC > 0:
            self.utilC -= 1

        """UPDATE TURRET"""
        if len(self.turrets) > 0:

            for turret in self.turrets:
                xy = self.Qt.dot(turret.pos)
                turret.centerx = self.centerx + xy[0]
                turret.centery = self.centery + xy[1]
                turret.scoot(entity_list, self.faction_name)

        return events


class Turret(Shooter):
    def __init__(self, x: float, y: float, pos: np.ndarray[np.float64], angle: float,
                 turret_type: TurretType, ship: Vessel):
        # type_ = ls.TurretTypes[turret_type]
        super().__init__(x, y, turret_type.height, turret_type.width)
        self.type: TurretType = turret_type
        self.ship = ship
        self.faction = ship.faction
        self.angle = angle
        self.pos = pos
        self.health = self.max_health
        self.energy = self.max_energy
        self.targets = []
        self.vx = 0
        self.vy = 0
        self.counter = 0
        self.bulletC = 0
        self.missileC = 0
        self.target = None
        self.bullet_sel = 0
        self.missile_sel = 0

    @property
    def control_module(self):
        return self.type.control_module

    @property
    def bullet_types(self):
        return self.type.bullet_types

    @property
    def missile_types(self):
        return self.type.missile_types

    def scoot(self, entity_list: list[Entity]):

        self.vx = self.ship.vx
        self.vy = self.ship.vy

        commands = self.control_module(self, entity_list, self.faction)

        """MOVEMENT- ROTATION"""

        if commands[0] == 1:  # ROTATE CCW
            self.angle += self.av
        elif commands[0] == -1:  # ROTATE CW
            self.angle -= self.av

        """FIRE BULLETS and MISSILES"""
        if commands[1] == 1 and self.energy >= self.bullet.energy and self.bulletC == 0:
            self.energy -= self.bullet.energy
            self.bulletC = self.bullet.delay
            self.bullet.init(self, entity_list, self.faction)
        if (len(self.missile_types) > 0 and commands[2] == 1 and
                self.energy >= self.missile.energy and self.missileC == 0 and self.target is not None):
            self.energy -= self.missile.energy
            self.missileC = self.missile.delay
            missile = Missile(self.x + self.width // 2, self.y + self.height // 2 - 2,
                              self.angle, 2, 10, self.missile, self.target, self.faction)
            entity_list.append(missile)
        if self.energy < self.max_energy:
            self.energy += 0.1  # adj
        if self.health < self.max_health:
            self.health += 0.0025  # adj
        if self.bulletC > 0:
            self.bulletC -= 1
        if self.missileC > 0:
            self.missileC -= 1

    # def draw(self, surf, x_center, y_center):
    #     turret_image = pygame.transform.rotate(self.image, self.angle)
    #     x = x_center - turret_image.get_width() // 2
    #     y = y_center - turret_image.get_height() // 2
    #     surf.blit(turret_image, (x, y))


"""STATION CLASS"""


class Base(Vessel):
    def __init__(self, x: int, y: int, station_type: StationType, control_module: Callable,
                 ls: "LocalState", faction_name: str):
        station_type = ls.StationTypes[station_type]
        super().__init__(x, y, station_type.height, station_type.width)
        self.vx = 0
        self.vy = 0
        self.Health = station_type.health
        self.health = self.Health
        self.Energy = station_type.energy
        self.energy = self.Energy
        self.counter = 0
        self.angle = 0
        self.turrets = []
        self.image = station_type.image
        self.docked_ships = []
        self.docked_players = []
        self.cargo = CargoClass()
        self.faction = ls.factions[faction_name]
        self.pilots = []
        self.ship_build = None
        self.ship_cost = None

    @property
    def cargo_types(self):
        return list(self.cargo)

    def check_funds(self, item: TypeType):
        funds = True
        for ore in item.cost.keys():
            if self.cargo[ore] < item.cost[ore]:
                funds = False
        return funds

    def buy_ship(self, key: str, gs: "GlobalState", ls: "LocalState", cm: Callable):
        ship = ls.ShipTypes[key]
        funds = self.check_funds(ship)
        if funds:
            for ore in ship.cost.keys():
                self.cargo[ore] -= ship.cost[ore]
            new_ship = Ship(cm, self.turret_control, self.centerx, self.centery, 0, key, gs, ls, self.faction_name)
            return new_ship
        else:
            return None

    def scoot(self, entity_list: list[Entity]):
        for turret in self.turrets:
            turret.x = self.centerx - turret.width / 2
            turret.y = self.centery - turret.height / 2
            turret.scoot(entity_list)


"""ASTEROID CLASS"""


class Asteroid(Entity):
    def __init__(self, x, y, angle, type_):
        super().__init__(x, y, 500, 500)
        self.image = pygame.transform.rotate(
            pygame.image.load(os.path.join('Assets', 'asteroid2.png')), angle).convert_alpha()
        self.image_scaled = pygame.transform.scale(
            pygame.image.load(os.path.join('Assets', 'asteroid2.png')), (100, 100)).convert_alpha()
        self.angle = angle
        self.health = math.inf
        if type_ <= 100:
            self.ore = assign_ore('Std')
        self.ore_types = list(self.ore)

    def harvest_all(self, ore_name: str):  # method to harvest all one type of ore from an asteroid
        ore_num = self.ore[ore_name]
        self.ore[ore_name] = 0
        return ore_num  # returns the number of ore units removed from the asteroid

    def harvest(self, ore_name: str,
                quantity: float):  # method to harvest a specified amount of an ore from an asteroid
        self.ore[ore_name] -= quantity
        return quantity  # returns the number of ore units removed from the asteroid

    def draw(self, surf: pygame.Surface, x_center: int, y_center: int):
        x = x_center - self.image.get_width() // 2
        y = y_center - self.image.get_height() // 2
        surf.blit(self.image, (x, y))

    def scoot(self, *args, **kwargs) -> None:
        pass

    def mine(self, ship: Ship):
        if ship.cargo.cargo_total < ship.type.cargo_cap:
            if 'ore' in ship.info:
                ore_type = ship.info['ore']
                if ore_type in self.ore:
                    self.ore[ore_type] -= 1
                    ship.cargo[ore_type] += 1
            else:
                r = rnd.randint(0, len(self.ore_types) - 1)
                if self.ore[self.ore_types[r]] > 0:
                    self.ore[self.ore_types[r]] -= 1
                    ship.cargo[self.ore_types[r]] += 1
