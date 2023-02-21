import pygame
import math
import numpy as np
import random as rnd
import os

from Weapon_Class import Bullet, Missile, Mine
from Misc import StationTypes, assign_ore, CargoClass, RequestUndock
from Menus import StationMenu, AsteroidMenu
from Explosions import Particle


class Ship(pygame.Rect):
    def __init__(self, control_module, turret_control_module, x, y, angle, color, ship_type, gs, is_player=False):
        # ShipType = ShipTypes(ship_type, color)
        ShipType = gs.ShipTypes[ship_type]
        Turrets = []
        for i in range(len(ShipType.turrets)):
            Turrets.append(Turret(x, y, ShipType.turret_pos[i], angle, ShipType.turrets[i], turret_control_module, gs, self))
        super().__init__(x, y, ShipType.height, ShipType.width)
        self.ship_type = ShipType
        self.range = self.ship_type.range
        self.angle = angle
        self.Q = np.array([[1, 0], [0, 1]])
        self.Qt = np.transpose(self.Q)
        self.velocity = ShipType.velocity
        self.av = ShipType.av
        self.acc = ShipType.acc
        self.fx = x
        self.fy = y
        self.cx = x
        self.cy = y
        self.health = ShipType.health
        self.heat = 0
        # self.Energy = ShipType.energy
        self.energy = ShipType.energy
        self.vx = 0
        self.vy = 0
        self.counter = 0
        self.bulletC = 0
        self.missileC = 0
        self.utilC = 0
        self.target = None
        self.control_module = control_module
        self.turret_control_module = turret_control_module
        self.bullet_types = []
        self.missile_types = []
        self.mine_types = []
        self.util_types = []
        self.bullet_sel = 0
        self.missile_sel = 0
        self.mine_sel = 0
        self.util_sel = 0
        self.turrets = Turrets
        self.cargo = CargoClass()
        self.forward = False
        self.boost = False
        self.is_ship = True
        self.is_player = is_player
        self.is_visible = True
        self.cloaked = False
        self.hidden = False
        self.color = color
        self.Image = pygame.image.load(os.path.join('Assets', f'{ship_type}_{color}.png'))  # image with no flame
        # self.Imagef = pygame.image.load(os.path.join('Assets', f'{ship_type}_{color}_f.png'))  # image with flame
        self.image = self.Image
        # self.imagef = self.Imagef

        self.refresh(gs)

    def add_bullet(self, gs, key):
        if len(self.bullet_types) < self.ship_type.primary:
            self.bullet_types.append(gs.BulletTypes[key])

    def add_missile(self, gs, key):
        if len(self.missile_types) < self.ship_type.secondary:
            self.missile_types.append(gs.MissileTypes[key])

    def add_mine(self, gs, key):
        if len(self.mine_types) < self.ship_type.mine:
            self.mine_types.append(gs.MineTypes[key])

    def add_util(self, gs, key):
        if len(self.util_types) < self.ship_type.utility:
            self.util_types.append(gs.UtilTypes[key])

    def determine_visibility(self):
        if self.cloaked and self.bulletC == 0 and self.missileC == 0:
            self.is_visible = False
            self.image.set_alpha(100)
        elif self.hidden:
            self.is_visible = False
        else:
            self.is_visible = True

    def concealed(self, gs):
        if rnd.random() > 0.99:
            if self.collidelistall(gs.asteroids):
                self.hidden = True
            else:
                self.hidden = False

    def scoot(self, gs, faction):

        cos = math.cos(self.angle * math.pi / 180)
        sin = math.sin(self.angle * math.pi / 180)
        self.Q = np.array([[cos, -sin], [sin, cos]])
        self.Qt = self.Q.transpose()

        commands = self.control_module(self, gs, faction)
        self.forward = False

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

        if commands[0] == 1:  # ROTATE CCW
            self.angle += self.av
        elif commands[0] == -1:  # ROTATE CW
            self.angle -= self.av
        if commands[1] == 1:  # UP
            self.vx += self.acc * math.sin(self.angle * math.pi / 180)
            self.vy += self.acc * math.cos(self.angle * math.pi / 180)
            self.forward = True
            R = 255
            G = rnd.randint(0, 255)
            gs.particle_list.append(
                Particle(self.centerx, self.centery, -rnd.randint(10, 12), self.angle + rnd.randint(-15, 15), 3,
                         (R, G, 0), shrink=0.5, vx=self.vx, vy=self.vy, glow=(R//2, G//2, 0)))
        elif commands[1] == -1:  # DOWN
            self.vx -= self.acc * math.sin(self.angle * math.pi / 180) / 3
            self.vy -= self.acc * math.cos(self.angle * math.pi / 180) / 3
        if commands[2] == 1:  # LEFT
            self.vy -= self.acc * math.sin(self.angle * math.pi / 180) / 2
            self.vx += self.acc * math.cos(self.angle * math.pi / 180) / 2
        elif commands[2] == -1:  # RIGHT
            self.vy += self.acc * math.sin(self.angle * math.pi / 180) / 2
            self.vx -= self.acc * math.cos(self.angle * math.pi / 180) / 2

        """FIRE BULLETS and MISSILES"""
        if commands[3] == 1 and len(self.bullet_types) > 0 and self.energy >= self.bullet_types[self.bullet_sel].energy and self.bulletC == 0:  # DOWN
            self.energy -= self.bullet_types[self.bullet_sel].energy
            self.bulletC = self.bullet_types[self.bullet_sel].delay

            self.bullet_types[self.bullet_sel].init(self, gs, faction)

            # pos = self.center + self.Q.transpose().dot(self.ship_type.bullet_pos[self.bullet_sel]) - np.array([self.bullet_types[self.bullet_sel].width // 2, self.bullet_types[self.bullet_sel].height // 2])
            #
            # bullet = Bullet(pos[0], pos[1], self.angle,
            #                 self.bullet_types[self.bullet_sel], faction)
            #
            # global_state.bullets[faction].append(bullet)
        if commands[4] == 1 and self.missileC == 0 and len(self.missile_types) > 0 and self.energy >= self.missile_types[self.missile_sel].energy and self.target is not None:
            self.energy -= self.missile_types[self.missile_sel].energy
            self.missileC = self.missile_types[self.missile_sel].delay

            pos = self.center + self.Q.transpose().dot(self.ship_type.missile_pos[self.missile_sel]) - np.array(
                [self.missile_types[self.missile_sel].width // 2, self.missile_types[self.missile_sel].height // 2])
            missile = Missile(pos[0], pos[1], self.angle,
                              self.missile_types[self.missile_sel].height, self.missile_types[self.missile_sel].width,
                              self.missile_types[self.missile_sel], self.target, faction, gs)

            # missile = Missile(self.x + self.width // 2, self.y + self.height // 2 - 2, self.angle, self.missile_types[self.missile_sel].height, self.missile_types[self.missile_sel].width, self.missile_types[self.missile_sel], self.target, faction)
            gs.missiles[faction].append(missile)
        if commands[5] == 1 and len(self.mine_types) > 0 and self.energy >= self.mine_types[self.mine_sel].energy and self.missileC == 0:
            self.energy -= self.mine_types[self.mine_sel].energy
            self.missileC = self.mine_types[self.mine_sel].delay
            mine = Mine(self.centerx, self.centery, self.angle, self.mine_types[self.mine_sel].height, self.mine_types[self.mine_sel].width, self.mine_types[self.mine_sel], self.target, faction)
            gs.missiles[faction].append(mine)

        if commands[6] == 1 and self.utilC == 0 and len(self.util_types) > 0:
            self.util_types[self.util_sel].function(self, gs, faction)
            self.utilC += self.util_types[self.util_sel].delay

        if commands[7] == 1 and self.energy > 0.75:  # boost
            self.boost = True
            self.velocity = self.ship_type.velocity * 1.25
            self.acc = self.ship_type.acc * 1.25
            self.av = self.ship_type.av * 1.25
            self.energy -= 0.75
            for i in range(3):
                R = 255
                G = rnd.randint(0, 255)
                gs.particle_list.append(Particle(self.centerx, self.centery, -rnd.randint(round(2 * self.velocity), 3 * round(self.velocity)), self.angle + rnd.randint(-15, 15), 3, (R, G, 0), vx=self.vx, vy=self.vy, glow=(R // 2, G // 2, 0), shrink=0.7))
        else:
            self.boost = False
            self.velocity = self.ship_type.velocity
            self.acc = self.ship_type.acc
            self.av = self.ship_type.av

        """DOCK"""
        if commands[8] == 1:
            MyList = self.collidelistall(gs.stations[faction])
            if len(MyList) == 1:
                station = gs.stations[faction][MyList[0]]
                self.center = station.center
                self.vx = 0
                self.vy = 0
                station.docked_ships.append(self)
                gs.ships[faction].remove(self)
                gs.update()
                if self.is_player:
                    station.docked_players.append(self)
                    gs.docked = station
                    gs.menu = StationMenu()
                    gs.x = self.centerx - gs.width / 2
                    gs.y = self.centery - gs.height / 2
                    gs.cx = self.centerx
                    gs.cy = self.centery
                else:
                    for Type in self.cargo.keys():
                        cargo_transfer = self.cargo[Type]
                        station.cargo[Type] += cargo_transfer
                        self.cargo[Type] -= cargo_transfer
                    self.cargo.cargo_total = sum(self.cargo.values())

        """MINE ASTEROID"""
        if commands[9] == 1 and type(self.target) is Asteroid and self.colliderect(self.target):  # harvest from asteroid
            roid = self.target  # identify specific asteroid from list
            # if self.is_player:
            #     self.vx = 0
            #     self.vy = 0
            #     gs.ships[faction].remove(self)
            #     gs.update()
            #     gs.menu = AsteroidMenu(self, roid)
            # else:
            roid.mine(self)
            if sum(roid.ore.values()) > 0:
                gs.particle_list.append(
                    Particle(self.centerx, self.centery, rnd.random(), rnd.randint(0, 360), rnd.randint(4, 6),
                             (rnd.randint(0, 50), rnd.randint(0, 50), rnd.randint(0, 50)), 0.95))
            else:
                gs.particle_list.append(
                    Particle(self.centerx, self.centery, rnd.random(), rnd.randint(0, 360), rnd.randint(4, 6),
                             (50, 50, 50), 0.95))
            if abs(self.centerx - gs.x) < 2000 and abs(self.centery - gs.y) < 2000:
                gs.play_mining(1)

        # if commands[9] != 0:
        #     self.bullet_sel = commands[9] - 1
        #
        # if commands[10] != 0:
        #     self.missile_sel = commands[10] - 1

        """DON'T GO OVER SPEED LIMIT"""
        v2 = self.vx * self.vx + self.vy * self.vy
        if v2 > self.velocity * self.velocity:
            v = math.sqrt(v2)
            self.vx = self.vx * self.velocity / v
            self.vy = self.vy * self.velocity / v

        self.fx += self.vx
        self.fy += self.vy

        self.x = round(self.fx)
        self.y = round(self.fy)

        self.cx = round(self.x + (
                    self.width - self.height * abs(math.sin(self.angle * math.pi / 180)) - self.width * abs(math.cos(self.angle * math.pi / 180))) / 2)
        self.cy = round(self.y + (
                    self.height - self.width * abs(math.sin(self.angle * math.pi / 180)) - self.height * abs(math.cos(self.angle * math.pi / 180))) / 2)

        """UPDATE ENERGY, HEALTH, AND VISIBILITY"""

        # if self.utilC == 0 and self.cloaked:
        #     self.cloaked = False
        #     self.image.set_alpha(255)

        self.concealed(gs)
        self.determine_visibility()

        if not self.cloaked:
            heat_loss = 0.02 + self.heat * self.ship_type.heat_venting
            if self.heat > heat_loss:
                self.heat -= heat_loss
                if self.heat > self.ship_type.heat_capacity:
                    self.health -= round(self.heat - self.ship_type.heat_capacity, 1)
                    self.heat = self.ship_type.heat_capacity
            else:
                self.heat = 0

            if self.energy < self.ship_type.energy and not self.cloaked:
                self.energy += 0.5
            if self.health < self.ship_type.health and self.heat == 0:
                self.health += 0.05
        if self.bulletC > 0:
            self.bulletC -= 1
        if self.missileC > 0:
            self.missileC -= 1
        if self.utilC > 0:
            self.utilC -= 1

        """UPDATE TURRET"""
        if len(self.turrets) > 0:
            cos = math.cos(self.angle * math.pi / 180)
            sin = math.sin(self.angle * math.pi / 180)

            Q = np.array([[cos, sin], [-sin, cos]])

            for turret in self.turrets:
                turret.centerx = self.centerx + Q.dot(turret.pos)[0]
                turret.centery = self.centery + Q.dot(turret.pos)[1]
                turret.scoot(gs, faction)

        if self.is_player:
            gs.x = self.centerx - gs.width / 2
            gs.y = self.centery - gs.height / 2
            gs.cx = self.centerx
            gs.cy = self.centery

    def refresh(self, gs):
        self.height = self.ship_type.height
        self.width = self.ship_type.width
        self.energy = self.ship_type.energy
        self.health = self.ship_type.health
        self.Image = pygame.image.load(os.path.join('Assets', f'{self.ship_type.name}_{self.color}.png'))
        # self.Imagef = pygame.image.load(os.path.join('Assets', f'{self.ship_type.name}_{self.color}_f.png'))

        self.image = self.Image.copy()
        # self.imagef = self.Imagef.copy()

        for i in range(len(self.bullet_types)):
            x = self.width // 2 + self.ship_type.bullet_pos[i][0] - self.bullet_types[i].l_image.get_width() // 2
            y = self.height // 2 + self.ship_type.bullet_pos[i][1] - self.bullet_types[i].l_image.get_height() // 2
            self.image.blit(self.bullet_types[i].l_image, (x, y))
            # self.imagef.blit(self.bullet_types[i].l_image, (x, y))

        for i in range(len(self.missile_types)):
            x = self.width // 2 + self.ship_type.missile_pos[i][0]-self.missile_types[i].image.get_width() // 2
            y = self.height // 2 + self.ship_type.missile_pos[i][1]-self.missile_types[i].image.get_height() // 2
            self.image.blit(self.missile_types[i].image, (x, y))
            # self.imagef.blit(self.missile_types[i].image, (x, y))

        self.image.blit(self.Image, (0, 0))
        # self.imagef.blit(self.Imagef, (0, 0))

        self.image.convert_alpha()
        # self.imagef.convert_alpha()
        # self.image.set_alpha(100)


        Turrets = []
        # for turret in self.ship_type.turrets:
        #     Turrets.append(Turret(self.x, self.y, self. self.angle, turret, self.turret_control_module, is_player=False))
        # self.turrets = Turrets

        for i in range(len(self.ship_type.turrets)):
            Turrets.append(Turret(self.x, self.y, self.ship_type.turret_pos[i], self.angle, self.ship_type.turrets[i], self.turret_control_module, gs, self))

        self.turrets = Turrets

    # def Hide(self):  # method to turn ship invisible
    #     self.is_visible = False
    #
    # def Unhide(self):  # method to turn ship visible
    #     self.is_visible = True


"""TURRET CLASS"""


class Turret(pygame.Rect):
    def __init__(self, x, y, pos, angle, turret_type, control_module, gs, ship, is_player=False):
        TurretType = gs.TurretTypes[turret_type]
        super().__init__(x, y, TurretType.height, TurretType.width)
        self.ship = ship
        self.range = TurretType.range
        self.angle = angle
        self.av = TurretType.av
        self.fx = x
        self.fy = y
        self.cx = x
        self.cy = y
        self.pos = pos
        self.Health = TurretType.health
        self.health = self.Health
        self.Energy = TurretType.energy
        self.energy = self.Energy
        self.targets = []
        self.vx = 0
        self.vy = 0
        self.counter = 0
        self.bulletC = 0
        self.missileC = 0
        self.is_ship = False
        self.target = None
        self.control_module = control_module
        self.bullet_types = [gs.BulletTypes[TurretType.bullet_types[0]]]
        self.bullet_sel = 0
        self.missile_sel = 0
        self.turret_type = TurretType
        if TurretType.missile_type is not None:
            self.missile_types = [gs.MissileTypes[TurretType.missile_type]]
        else:
            self.missile_types = []
        self.image = TurretType.image
        self.is_player = is_player

    def scoot(self, gs, faction):

        commands = self.control_module(self, gs, faction)

        """MOVEMENT- ROTATION"""

        if commands[0] == 1:  # ROTATE CCW
            self.angle += self.av
        elif commands[0] == -1:  # ROTATE CW
            self.angle -= self.av

        """FIRE BULLETS and MISSILES"""
        if commands[1] == 1 and self.energy >= self.bullet_types[self.bullet_sel].energy and self.bulletC == 0:
            self.energy -= self.bullet_types[self.bullet_sel].energy
            self.bulletC = self.bullet_types[self.bullet_sel].delay
            self.bullet_types[self.bullet_sel].init(self, gs, faction)
            # bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2 - 2, self.angle, self.bullet_types[self.bullet_sel], faction, gs)
            # gs.bullets[faction].append(bullet)
        if len(self.missile_types) > 0 and commands[2] == 1 and self.energy >= self.missile_types[self.missile_sel].energy and self.missileC == 0 and self.target is not None:
            self.energy -= self.missile_types[self.missile_sel].energy
            self.missileC = self.missile_types[self.missile_sel].delay
            missile = Missile(self.x + self.width // 2, self.y + self.height // 2 - 2, self.angle, 2, 10, self.missile_types[self.missile_sel], self.target, faction, gs)
            gs.missiles[faction].append(missile)
        if self.energy < self.Energy:
            self.energy += 0.25
        if self.health < self.Health:
            self.health += 0.005
        if self.bulletC > 0:
            self.bulletC -= 1
        if self.missileC > 0:
            self.missileC -= 1

        self.cx = round(self.x + (self.width - self.height * abs(math.sin(self.angle * math.pi / 180)) - self.width * abs(math.cos(self.angle * math.pi / 180))) / 2)
        self.cy = round(self.y + (self.height - self.width * abs(math.sin(self.angle * math.pi / 180)) - self.height * abs(math.cos(self.angle * math.pi / 180))) / 2)

        if self.is_player:
            gs.x = self.centerx - gs.width / 2
            gs.y = self.centery - gs.height / 2
            gs.cx = self.centerx
            gs.cy = self.centery


"""STATION CLASS"""


class Station(pygame.Rect):
    def __init__(self, x, y, station_type, control_module, color, gs):
        StationType = gs.StationTypes[station_type]
        Turrets = []
        for i in range(len(StationType.turrets)):
            Turrets.append(Turret(x, y, StationType.turret_pos[i], 0, StationType.turrets[i], control_module, gs, self))
        # for turret in StationType.turrets:
        #     Turrets.append(Turret(x, y, 0, turret, control_module, is_player=False))
        super().__init__(x, y, StationType.height, StationType.width)
        self.fx = x
        self.fy = y
        self.cx = x
        self.cy = y
        self.Health = StationType.health
        self.health = self.Health
        self.Energy = StationType.energy
        self.energy = self.Energy
        self.counter = 0
        self.angle = 0
        self.turrets = Turrets
        self.image = StationType.image
        self.docked_ships = []
        self.docked_players = []
        # self.obs = None
        self.cargo = CargoClass()
        # self.ships = ['Fighter', 'Sprinter', 'Frigate']
        # self.primary = ['HV', 'PA', 'railgun']
        # self.secondary = ['HE', 'torpedo', 'swarm missile', 'smart']
        self.color = color
        self.turret_control = control_module
        self.pilots = []
        self.ship_build = None
        self.ship_cost = None
        self.cargo_types = list(self.cargo)
        self.is_visible = True

    def check_funds(self, item):
        funds = True
        for ore in item.cost.keys():
            if self.cargo[ore] < item.cost[ore]:
                funds = False
        return funds

    def buy_ship(self, key, gs, cm):
        ship = gs.ShipTypes[key]
        funds = self.check_funds(ship)
        if funds:
            for ore in ship.cost.keys():
                self.cargo[ore] -= ship.cost[ore]
            new_ship = Ship(cm, self.turret_control, self.centerx, self.centery, 0, self.color, key, gs)
            return new_ship
        else:
            return None

    def scoot(self, global_state, faction):
        # if self.obs is not None:
        #     global_state.x = self.obs.x
        #     global_state.y = self.obs.y

        if self.ship_build is None:
            i = rnd.randint(0, len(global_state.ShipTypes) - 1)
            self.ship_build = list(global_state.ShipTypes.keys())[i]
        if self.check_funds(global_state.ShipTypes[self.ship_build]):
            if self.ship_build == 'Frigate':
                cm = global_state.pilots[1]
            else:
                cm = global_state.pilots[0]
            ship = self.buy_ship(self.ship_build, global_state, cm)
            i = rnd.randint(0, len(global_state.BulletTypes) - 1)
            j = rnd.randint(0, len(global_state.MissileTypes) - 1)
            ship.add_bullet(global_state, list(global_state.BulletTypes.keys())[i])
            ship.add_missile(global_state, list(global_state.MissileTypes.keys())[j])
            self.docked_ships.append(ship)
            self.ship_build = None

        # for ship in self.docked_ships:
        for i in range(len(self.docked_ships) - 1, -1, -1):
            ship = self.docked_ships[i]
            if RequestUndock(ship, global_state, faction):
                ship.center = self.center
                ship.fx = ship.x
                ship.fy = ship.y
                ship.refresh(global_state)
                if ship not in global_state.ships[faction]:
                    global_state.ships[faction].append(ship)
                    self.docked_ships.pop(i)
                    if ship.is_player:
                        print('remove menu')
                        self.docked_players.remove(ship)
                        global_state.docked = None
                        global_state.menu = None
                    global_state.update()
                else:
                    print(f'duplicate ship in faction {faction}')

        for turret in self.turrets:
            turret.x = self.centerx - turret.width / 2
            turret.y = self.centery - turret.height / 2
            turret.scoot(global_state, faction)


"""ASTEROID CLASS"""


class Asteroid(pygame.Rect):
    def __init__(self, x, y, angle, Type):
        super().__init__(x, y, 500, 500)
        self.image = pygame.transform.rotate(pygame.image.load(os.path.join('Assets', 'asteroid2.png')), angle).convert_alpha()
        self.image_scaled = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'asteroid2.png')), (100, 100)).convert_alpha()
        self.angle = angle
        self.is_visible = True
        self.health = math.inf
        self.cx = round(self.x + (
                self.width - self.height * abs(math.sin(self.angle * math.pi / 180)) - self.width * abs(
                    math.cos(self.angle * math.pi / 180))) / 2)
        self.cy = round(self.y + (
                self.height - self.width * abs(math.sin(self.angle * math.pi / 180)) - self.height * abs(
                    math.cos(self.angle * math.pi / 180))) / 2)
        if Type <= 100:
            self.ore = assign_ore('Std')
        self.ore_types = list(self.ore)

    def harvest_all(self, ore_name):  # method to harvest all of one type of ore from an asteroid
        ore_num = self.ore[ore_name]
        self.ore[ore_name] = 0
        return ore_num  # returns the number of ore units removed from the asteroid

    def harvest(self, ore_name, quantity):  # method to harvest a specified amount of an ore from an asteroid
        self.ore[ore_name] -= quantity
        return quantity  # returns the number of ore units removed from the asteroid

    def mine(self, ship):
        if ship.cargo.cargo_total < ship.ship_type.cargo_cap:
            r = rnd.randint(0, len(self.ore_types)-1)
            if self.ore[self.ore_types[r]] > 0:
                self.ore[self.ore_types[r]] -= 1
                ship.cargo[self.ore_types[r]] += 1
                ship.cargo.cargo_total = sum(ship.cargo.values())


    # def scoot(self, bullet_list, missile_list, target_list, ally_list, global_state):