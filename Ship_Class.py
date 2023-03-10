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
            Turrets.append(Turret(x, y, ShipType.turret_pos[i], angle, ShipType.turrets[i], turret_control_module, gs))
        super().__init__(x, y, ShipType.height, ShipType.width)
        self.ship_type = ShipType
        self.range = self.ship_type.range
        self.angle = angle
        self.Q = np.array([[1, 0], [0, 1]])
        self.velocity = ShipType.velocity
        self.av = ShipType.av
        self.acc = ShipType.acc
        self.fx = x
        self.fy = y
        self.cx = x
        self.cy = y
        self.health = ShipType.health
        self.sop = 0
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
        self.is_player = is_player
        self.is_visible = True
        self.color = color
        self.Image = pygame.image.load(os.path.join('Assets', f'{ship_type}_{color}.png'))  # image with no flame
        self.Imagef = pygame.image.load(os.path.join('Assets', f'{ship_type}_{color}_f.png'))  # image with flame
        self.image = self.Image
        self.imagef = self.Imagef

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

    def scoot(self, global_state, faction):

        cos = math.cos(self.angle * math.pi / 180)
        sin = math.sin(self.angle * math.pi / 180)
        self.Q = np.array([[cos, -sin], [sin, cos]])

        commands = self.control_module(self, global_state, faction)
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
            global_state.particle_list.append(
                Particle(self.centerx, self.centery, -rnd.randint(round(self.velocity), 2*round(self.velocity)), self.angle + rnd.randint(-15, 15), 3,
                         (255, rnd.randint(0, 255), 0), shrink=0.5, vx=self.vx, vy=self.vy))
        elif commands[1] == -1:  # DOWN
            self.vx -= self.acc * math.sin(self.angle * math.pi / 180) / 3
            self.vy -= self.acc * math.cos(self.angle * math.pi / 180) / 3
        if commands[2] == 1:  # LEFT
            self.vy -= self.acc * math.sin(self.angle * math.pi / 180) / 2
            self.vx += self.acc * math.cos(self.angle * math.pi / 180) / 2
        elif commands[2] == -1:  # RIGHT
            self.vy += self.acc * math.sin(self.angle * math.pi / 180) / 2
            self.vx -= self.acc * math.cos(self.angle * math.pi / 180) / 2

        # """DON'T GO OVER SPEED LIMIT"""
        # if self.vx * self.vx + self.vy * self.vy > self.velocity * self.velocity:
        #     self.vx = self.vx * self.velocity / math.sqrt(self.vx ** 2 + self.vy ** 2)
        #     self.vy = self.vy * self.velocity / math.sqrt(self.vx ** 2 + self.vy ** 2)
        #
        # self.fx += self.vx
        # self.fy += self.vy
        #
        # self.x = round(self.fx)
        # self.y = round(self.fy)
        #
        # self.cx = round(self.x + (
        #             self.width - self.height * abs(math.sin(self.angle * math.pi / 180)) - self.width * abs(math.cos(self.angle * math.pi / 180))) / 2)
        # self.cy = round(self.y + (
        #             self.height - self.width * abs(math.sin(self.angle * math.pi / 180)) - self.height * abs(math.cos(self.angle * math.pi / 180))) / 2)

        """HIDE BEHIND ASTEROID"""
        if rnd.random() > 0.99:
            if self.collidelistall(global_state.asteroids):
                self.Hide()
            else:
                self.Unhide()

        """FIRE BULLETS and MISSILES"""
        if commands[3] == 1 and len(self.bullet_types) > 0 and self.energy >= self.bullet_types[self.bullet_sel].energy and self.bulletC == 0:  # DOWN
            self.energy -= self.bullet_types[self.bullet_sel].energy
            self.bulletC = self.bullet_types[self.bullet_sel].delay

            pos = self.center + self.Q.transpose().dot(self.ship_type.bullet_pos[self.bullet_sel]) - np.array([self.bullet_types[self.bullet_sel].width // 2, self.bullet_types[self.bullet_sel].height // 2])
            bullet = Bullet(pos[0], pos[1], self.angle,
                            self.bullet_types[self.bullet_sel], faction)

            # bullet = Bullet(self.x + self.width // 2 - self.bullet_types[self.bullet_sel].width // 2, self.y + self.height // 2 - self.bullet_types[self.bullet_sel].height // 2, self.angle, self.bullet_types[self.bullet_sel], faction)

            global_state.bullets[faction].append(bullet)
        if commands[4] == 1 and self.missileC == 0 and len(self.missile_types) > 0 and self.energy >= self.missile_types[self.missile_sel].energy and self.target is not None:
            self.energy -= self.missile_types[self.missile_sel].energy
            self.missileC = self.missile_types[self.missile_sel].delay

            pos = self.center + self.Q.transpose().dot(self.ship_type.missile_pos[self.missile_sel]) - np.array(
                [self.missile_types[self.missile_sel].width // 2, self.missile_types[self.missile_sel].height // 2])
            missile = Missile(pos[0], pos[1], self.angle,
                              self.missile_types[self.missile_sel].height, self.missile_types[self.missile_sel].width,
                              self.missile_types[self.missile_sel], self.target, faction)

            # missile = Missile(self.x + self.width // 2, self.y + self.height // 2 - 2, self.angle, self.missile_types[self.missile_sel].height, self.missile_types[self.missile_sel].width, self.missile_types[self.missile_sel], self.target, faction)
            global_state.missiles[faction].append(missile)
        if commands[5] == 1 and len(self.mine_types) > 0 and self.energy >= self.mine_types[self.mine_sel].energy and self.missileC == 0:
            self.energy -= self.mine_types[self.mine_sel].energy
            self.missileC = self.mine_types[self.mine_sel].delay
            mine = Mine(self.centerx, self.centery, self.angle, self.mine_types[self.mine_sel].height, self.mine_types[self.mine_sel].width, self.mine_types[self.mine_sel], self.target, faction)
            global_state.missiles[faction].append(mine)

        if commands[6] == 1 and self.utilC == 0 and len(self.util_types) > 0:
            self.util_types[self.util_sel].function(self, global_state)
            self.utilC += self.util_types[self.util_sel].delay

        if commands[7] == 1 and self.energy > 0.75:  # boost
            self.boost = True
            self.velocity = self.ship_type.velocity * 1.2
            self.acc = self.ship_type.acc * 1.2
            self.av = self.ship_type.av * 1.2
            self.energy -= 0.75
            for i in range(5):
                global_state.particle_list.append(Particle(self.centerx, self.centery, -rnd.randint(2*round(self.velocity), 3*round(self.velocity)), self.angle + rnd.randint(-15, 15), 4, (255, rnd.randint(0, 255), 0), shrink=0.3))
        else:
            self.boost = False
            self.velocity = self.ship_type.velocity
            self.acc = self.ship_type.acc
            self.av = self.ship_type.av

        """DOCK"""
        if commands[8] == 1:
            MyList = self.collidelistall(global_state.stations[faction])
            if len(MyList) == 1:
                station = global_state.stations[faction][MyList[0]]
                self.center = station.center
                self.vx = 0
                self.vy = 0
                station.docked_ships.append(self)
                global_state.ships[faction].remove(self)
                global_state.update()
                if self.is_player:
                    station.docked_players.append(self)
                    global_state.docked = station
                    global_state.menu = StationMenu()
                    global_state.x = self.centerx - global_state.width / 2
                    global_state.y = self.centery - global_state.height / 2
                    global_state.cx = self.centerx
                    global_state.cy = self.centery
                else:
                    for Type in self.cargo.keys():
                        cargo_transfer = self.cargo[Type]
                        station.cargo[Type] += cargo_transfer
                        self.cargo[Type] -= cargo_transfer
                    self.cargo.cargo_total = sum(self.cargo.values())

        """MINE ASTEROID"""
        if commands[9] == 1 and type(self.target) is Asteroid and self.colliderect(self.target):  # harvest from asteroid
            roid = self.target  # identify specific asteroid from list
            if self.is_player:
                self.vx = 0
                self.vy = 0
                global_state.ships[faction].remove(self)
                global_state.update()
                global_state.menu = AsteroidMenu(self, roid)
            else:
                roid.mine(self)
            if sum(roid.ore.values()) > 0:
                global_state.particle_list.append(
                    Particle(self.centerx, self.centery, rnd.random(), rnd.randint(0, 360), rnd.randint(4, 6),
                             (rnd.randint(0, 50), rnd.randint(0, 50), rnd.randint(0, 50)), 0.95))
            else:
                global_state.particle_list.append(
                    Particle(self.centerx, self.centery, rnd.random(), rnd.randint(0, 360), rnd.randint(4, 6),
                             (50, 50, 50), 0.95))
            if abs(self.centerx - global_state.x) < 2000 and abs(self.centery - global_state.y) < 2000:
                global_state.play_mining(1)

        # if commands[9] != 0:
        #     self.bullet_sel = commands[9] - 1
        #
        # if commands[10] != 0:
        #     self.missile_sel = commands[10] - 1

        """DON'T GO OVER SPEED LIMIT"""
        if self.vx * self.vx + self.vy * self.vy > self.velocity * self.velocity:
            self.vx = self.vx * self.velocity / math.sqrt(self.vx ** 2 + self.vy ** 2)
            self.vy = self.vy * self.velocity / math.sqrt(self.vx ** 2 + self.vy ** 2)

        self.fx += self.vx
        self.fy += self.vy

        self.x = round(self.fx)
        self.y = round(self.fy)

        self.cx = round(self.x + (
                    self.width - self.height * abs(math.sin(self.angle * math.pi / 180)) - self.width * abs(math.cos(self.angle * math.pi / 180))) / 2)
        self.cy = round(self.y + (
                    self.height - self.width * abs(math.sin(self.angle * math.pi / 180)) - self.height * abs(math.cos(self.angle * math.pi / 180))) / 2)

        """UPDATE ENERGY AND HEALTH"""

        if self.sop > 0.2:
            self.sop -= 0.2
            if self.sop > 50:
                self.sop = 50
        else:
            self.sop = 0

        if self.energy < self.ship_type.energy:
            self.energy += 0.5
        if self.health < self.ship_type.health and self.sop == 0:
            self.health += 0.02
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
                turret.scoot(global_state, faction)

        if self.is_player:
            global_state.x = self.centerx - global_state.width / 2
            global_state.y = self.centery - global_state.height / 2
            global_state.cx = self.centerx
            global_state.cy = self.centery

    def refresh(self, gs):
        self.height = self.ship_type.height
        self.width = self.ship_type.width
        self.energy = self.ship_type.energy
        self.health = self.ship_type.health
        self.Image = pygame.image.load(os.path.join('Assets', f'{self.ship_type.name}_{self.color}.png'))
        self.Imagef = pygame.image.load(os.path.join('Assets', f'{self.ship_type.name}_{self.color}_f.png'))

        self.image = self.Image.copy()
        self.imagef = self.Imagef.copy()

        for i in range(len(self.bullet_types)):
            x = self.width // 2 + self.ship_type.bullet_pos[i][0] - self.bullet_types[i].l_image.get_width() // 2
            y = self.height // 2 + self.ship_type.bullet_pos[i][1] - self.bullet_types[i].l_image.get_height() // 2
            self.image.blit(self.bullet_types[i].l_image, (x, y))
            self.imagef.blit(self.bullet_types[i].l_image, (x, y))

        for i in range(len(self.missile_types)):
            x = self.width // 2 + self.ship_type.missile_pos[i][0]-self.missile_types[i].image.get_width() // 2
            y = self.height // 2 + self.ship_type.missile_pos[i][1]-self.missile_types[i].image.get_height() // 2
            self.image.blit(self.missile_types[i].image, (x, y))
            self.imagef.blit(self.missile_types[i].image, (x, y))

        self.image.blit(self.Image, (0, 0))
        self.imagef.blit(self.Imagef, (0, 0))

        self.image.convert(gs.WIN2)
        self.imagef.convert(gs.WIN2)


        Turrets = []
        # for turret in self.ship_type.turrets:
        #     Turrets.append(Turret(self.x, self.y, self. self.angle, turret, self.turret_control_module, is_player=False))
        # self.turrets = Turrets

        for i in range(len(self.ship_type.turrets)):
            Turrets.append(Turret(self.x, self.y, self.ship_type.turret_pos[i], self.angle, self.ship_type.turrets[i], self.turret_control_module, gs))

        self.turrets = Turrets

    def Hide(self):  # method to turn ship invisible
        self.is_visible = False

    def Unhide(self):  # method to turn ship visible
        self.is_visible = True


"""TURRET CLASS"""


class Turret(pygame.Rect):
    def __init__(self, x, y, pos, angle, turret_type, control_module, gs, is_player=False):
        TurretType = gs.TurretTypes[turret_type]
        super().__init__(x, y, TurretType.height, TurretType.width)
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
        self.vx = 0
        self.vy = 0
        self.counter = 0
        self.bulletC = 0
        self.missileC = 0
        self.target = None
        self.control_module = control_module
        self.bullet_types = [gs.BulletTypes[TurretType.bullet_types[0]]]
        self.bullet_sel = 0
        self.missile_sel = 0
        if TurretType.missile_type is not None:
            self.missile_types = [gs.MissileTypes[TurretType.missile_type]]
        else:
            self.missile_types = []
        self.image = TurretType.image
        self.is_player = is_player

    def scoot(self, global_state, faction):

        commands = self.control_module(self, global_state, faction)

        """MOVEMENT- ROTATION"""

        if commands[0] == 1:  # ROTATE CCW
            self.angle += self.av
        elif commands[0] == -1:  # ROTATE CW
            self.angle -= self.av

        """FIRE BULLETS and MISSILES"""
        if commands[1] == 1 and self.energy >= self.bullet_types[self.bullet_sel].energy and self.bulletC == 0:
            self.energy -= self.bullet_types[self.bullet_sel].energy
            self.bulletC = self.bullet_types[self.bullet_sel].delay
            bullet = Bullet(self.x + self.width // 2, self.y + self.height // 2 - 2, self.angle, self.bullet_types[self.bullet_sel], faction)
            global_state.bullets[faction].append(bullet)
        if len(self.missile_types) > 0 and commands[2] == 1 and self.energy >= self.missile_types[self.missile_sel].energy and self.missileC == 0 and self.target is not None:
            self.energy -= self.missile_types[self.missile_sel].energy
            self.missileC = self.missile_types[self.missile_sel].delay
            missile = Missile(self.x + self.width // 2, self.y + self.height // 2 - 2, self.angle, 2, 10, self.missile_types[self.missile_sel], self.target, faction)
            global_state.missiles[faction].append(missile)
        if self.energy < self.Energy:
            self.energy += 0.2
        if self.health < self.Health:
            self.health += 0.005
        if self.bulletC > 0:
            self.bulletC -= 1
        if self.missileC > 0:
            self.missileC -= 1

        self.cx = round(self.x + (self.width - self.height * abs(math.sin(self.angle * math.pi / 180)) - self.width * abs(math.cos(self.angle * math.pi / 180))) / 2)
        self.cy = round(self.y + (self.height - self.width * abs(math.sin(self.angle * math.pi / 180)) - self.height * abs(math.cos(self.angle * math.pi / 180))) / 2)

        if self.is_player:
            global_state.x = self.centerx - global_state.width / 2
            global_state.y = self.centery - global_state.height / 2
            global_state.cx = self.centerx
            global_state.cy = self.centery


"""STATION CLASS"""


class Station(pygame.Rect):
    def __init__(self, x, y, station_type, control_module, color, gs):
        StationType = StationTypes(station_type)
        Turrets = []
        for i in range(len(StationType.turrets)):
            Turrets.append(Turret(x, y, StationType.turret_loc[i], 0, StationType.turrets[i], control_module, gs))
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
        self.turrets = Turrets
        self.image = StationType.image
        self.docked_ships = []
        self.docked_players = []
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