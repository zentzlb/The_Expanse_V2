import pygame
import math
import numpy as np
import random as rnd
import time
from utils import FindNearest, FindMineable
from Misc import GlobalState
from Ship_Class import Ship, Base, Asteroid, Turret
from Data.Types import Entity


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = math.inf


"""NPC LOGIC"""


def Null(ship: Ship, entity_list: list[Entity], **kwargs) -> list[int]:
    commands = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    return commands


def NPControl(ship: Ship, entity_list: list[Entity], **kwargs) -> list[int]:
    commands = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    if ship.health < ship.type.health // 1000:
        ship.target = FindNearest(ship, [entity for entity in entity_list if
                                         isinstance(entity, Base) and entity.faction_name == ship.faction_name])

    elif ship.target is None or ship.target.health <= 0 or ship.counter == 60:
        ship.target = FindNearest(ship, [entity for entity in entity_list if
                                         isinstance(entity, Ship) and entity.faction_name != ship.faction_name])
        ship.counter = 0
        if ship.target is None:
            ship.target = Point(rnd.randint(0, 1000), rnd.randint(0, 1000))
            # print(ship.target)
            # print(type(ship.target) is Point)
    else:
        ship.counter += 1

    if type(ship.target) is Base:
        x = ship.target.centerx
        y = ship.target.centery

        dx = x - ship.centerx
        dy = y - ship.centery

        V = np.array([[dx], [dy]])
        V_prime = ship.Q.dot(V)
        angle2 = math.atan2(V_prime[0][0], V_prime[1][0])

        if angle2 > ship.av * math.pi / 360:  # LEFT
            commands[0] = 1
        elif angle2 < -ship.av * math.pi / 360:  # RIGHT
            commands[0] = -1

        """GO FORWARD"""
        commands[1] = 1

        """NO LATERAL ACCELERATION"""
        commands[2] = round(math.sin(ship.counter))
        """SHOOT"""
        # commands.append(0)
        # commands.append(0)

        """NO MINES"""
        # commands.append(0)

        """BOOST"""
        if ship.health < ship.type.health and ship.energy > 10:
            commands[6] = 1

        if type(ship.target) is Base:
            commands[7] = 1

        if type(ship.target) is Asteroid:
            commands[8] = 1

    elif type(ship.target) is Ship:

        bs, dx, dy, r1, angle2, in_range = find_bullet(ship)
        ms, r2 = find_missile(ship)
        # us, use = use_util(ship, gs, commands, faction)

        commands[10] = bs + 1
        commands[11] = ms + 1
        # commands[13] = us + 1

        if angle2 > ship.av * math.pi / 360:  # LEFT
            commands[0] = 1
        elif angle2 < -ship.av * math.pi / 360:  # RIGHT
            commands[0] = -1

        """GO FORWARD"""
        if (abs(angle2 * 180 / math.pi) < 80 and ship.bullet_types[bs].range < 5 * r1) or ship.bullet_types[bs].delay > 100:
            commands[1] = 1
        else:
            commands[1] = -1

        """NO LATERAL ACCELERATION"""
        commands[2] = 0  # round(math.sin(time.time()))

        if (in_range and abs(angle2) < 0.7
                and abs(r1 * math.sin(angle2)) < ship.target.height / 2
                and (ship.energy >= 50 or ship.target.heat > 0.8 * ship.target.type.heat_capacity)
                and ship.bullet_types[bs].range > r1):  # SHOOT BULLET
            commands[3] = 1

        if len(ship.missile_types) > 0 and ship.energy >= ship.missile_types[ms].energy and ship.missile_types[
            ms].range > r2:
            commands[4] = 1

        """UTIL"""
        # commands[6] = use

        """BOOST"""
        if ship.health < 20 and (
                (ship.energy > ship.bullet_types[bs].energy and ship.boost) or ship.energy > ship.bullet_types[
            bs].energy + 30):
            commands[7] = 1

    elif type(ship.target) is Point:
        # print('working')

        dx = ship.target.x - ship.centerx
        dy = ship.target.y - ship.centery

        V = np.array([[dx], [dy]])
        V_prime = ship.Q.dot(V)
        angle2 = math.atan2(V_prime[0][0], V_prime[1][0])

        if angle2 > ship.av * math.pi / 360:  # LEFT
            commands[0] = 1
        elif angle2 < -ship.av * math.pi / 360:  # RIGHT
            commands[0] = -1

        """GO FORWARD"""
        commands[1] = 1

    return commands


"""NPC MINER LOGIC"""


def NPControl2(ship: Ship, entity_list: list[Entity], **kwargs) -> list[int]:
    commands = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    if (
            ship.cargo.cargo_total >= ship.ship_type.cargo_cap or ship.health < 0.8 * ship.ship_type.health):  # type(ship.target) is not Station and
        ship.target = FindNearest(ship, gs.stations[faction])
    elif type(ship.target) is not Asteroid and ship.cargo.cargo_total < ship.ship_type.cargo_cap:
        ship.target = FindMineable(ship, gs.asteroids)
    elif type(ship.target) is Asteroid and sum(ship.target.ore.values()) == 0:
        ship.target = FindMineable(ship, gs.asteroids)

    if ship.target is not None:

        dx = ship.target.centerx - ship.centerx
        dy = ship.target.centery - ship.centery

        V = np.array([[dx], [dy]])
        V_prime = ship.Q.dot(V)
        angle2 = math.atan2(V_prime[0][0], V_prime[1][0])

        # print(angle2)

        if angle2 > ship.av * math.pi / 360:  # LEFT
            commands[0] = 1
        elif angle2 < -ship.av * math.pi / 360:  # RIGHT
            commands[0] = -1

        """"""
        if dx * dx + dy * dy < ship.target.width * ship.target.width // 2:
            # print('close')
            v_prime = ship.Q.dot(np.array([[ship.vx], [ship.vy]]))
            if v_prime[0] > 0 or abs(angle2 * 180 / math.pi) > 80:
                commands[1] = -1
            else:
                commands[1] = 1
            if v_prime[1] > 0:
                commands[2] = 1
            else:
                commands[2] = -1
        else:
            """GO FORWARD"""
            commands[1] = 1

            """NO LATERAL ACCELERATION"""
            # commands.append(0)

        """SHOOT"""
        # commands.append(0)
        # commands.append(0)

        """MINES"""
        # commands.append(0)

        """BOOST"""
        if ship.health < ship.type.health * 0.8 and ship.energy > 10:
            commands[7] = 1

        if type(ship.target) is Base:
            commands[8] = 1

        if type(ship.target) is Asteroid:
            commands[9] = 1

    # else:
    #     commands = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    return commands


"""TURRET CONTROLS"""


def TurretControl(turret: Ship, entity_list: list[Entity], **kwargs) -> list[int]:
    commands = [0, 0, 0]

    if turret.counter == 30:
        turret.targets = []
        R2 = 9 * turret.range * turret.range
        for f in range(len(gs.ships)):
            if f != faction:
                if turret.turret_type.targets_missiles:
                    # print('Looking for missiles')
                    for missile in gs.missiles[f]:
                        dx = turret.centerx - missile.centerx
                        dy = turret.centerx - missile.centerx
                        r2 = dx * dx + dy * dy
                        if r2 < R2:
                            turret.targets.append(missile)
                for ship in gs.ships[f]:
                    dx = turret.centerx - ship.centerx
                    dy = turret.centerx - ship.centerx
                    r2 = dx * dx + dy * dy
                    if r2 < R2:
                        turret.targets.append(ship)
        turret.counter = 0

    if turret.target is None or turret.target.health <= 0 or turret.counter == 10:
        turret.target = FindNearest(turret, turret.targets)

    turret.counter += rnd.randint(0, 1)

    if turret.target is not None:

        vx = turret.target.vx - turret.vx
        vy = turret.target.vy - turret.vy
        xo = turret.target.centerx - turret.centerx
        yo = turret.target.centery - turret.centery
        bullet_velocity = turret.bullet_types[turret.bullet_sel].velocity

        a = vx * vx + vy * vy - bullet_velocity * bullet_velocity
        b = 2 * (vx * xo + vy * yo)
        c = xo * xo + yo * yo

        if a < 0:
            t = (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)
        elif a > 0 and b * b - 4 * a * c > 0:
            t1 = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
            t2 = (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)
            t_list = [t1, t2, math.inf]
            val = min([t for t in t_list if t > 0])
            if val != math.inf:
                t = val
            else:
                t = -1
        elif b != 0:
            t = -c / b
        else:
            t = -1

        if t > 0:
            x = xo + vx * t
            y = yo + vy * t

            V = np.array([x, y])
            V_prime = turret.Q.dot(V)
            angle2 = math.atan2(V_prime[0], V_prime[1])
            r = math.sqrt(x * x + y * y)

        else:
            angle2 = math.atan2(turret.target.centerx - turret.centerx, turret.target.centery - turret.centery)
            r = math.inf


        if angle2 > turret.av * math.pi / 360:  # LEFT
            commands[0] = 1
        elif angle2 < -turret.av * math.pi / 360:  # RIGHT
            commands[0] = -1

        """SHOOT"""
        if abs(angle2) < 0.7 and abs(r * math.sin(angle2)) < turret.target.height / 2 and turret.bullet_types[
            turret.bullet_sel].range > r:  # SHOOT BULLET
            commands[1] = 1

        if len(turret.missile_types) > 0 and (
                turret.energy >= turret.missile_types[turret.missile_sel].energy and turret.missile_types[
            turret.missile_sel].range > r):
            commands[2] = 1

    else:


        V = np.array([[math.sin(turret.ship.angle * math.pi / 180)], [math.cos(turret.ship.angle * math.pi / 180)]])
        V_prime = turret.Q.dot(V)
        angle2 = math.atan2(V_prime[0][0], V_prime[1][0])

        if angle2 > turret.av * math.pi / 360:  # LEFT
            commands[0] = 1
        elif angle2 < -turret.av * math.pi / 360:  # RIGHT
            commands[0] = -1

    return commands


"""PLAYER KEYBOARD CONTROLS"""


def PlayerControl2(ship: Ship, entity_list: list[Entity], **kwargs) -> list[int]:

    commands = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    keys_pressed = pygame.key.get_pressed()
    mouse_pressed = pygame.mouse.get_pressed()

    if keys_pressed[pygame.K_l]:  # LOCK ONTO THE NEAREST TARGET
        ship.target = FindNearest(ship, [entity for entity in entity_list if
                                         isinstance(entity, Ship) and entity.faction_name != ship.faction_name])
    elif keys_pressed[pygame.K_o]:
        ship.target = FindMineable(ship, [entity for entity in entity_list if isinstance(entity, Asteroid)])
    elif keys_pressed[pygame.K_SEMICOLON]:  # REMOVE TARGET LOCK
        ship.target = None

    """MOVEMENT"""

    if 'V' in ship.info:
        V = ship.info['V']
    else:
        V = np.array([[0], [0]])

    V_prime = ship.Q.dot(V)
    angle2 = math.atan2(V_prime[0][0], V_prime[1][0])

    # print(angle2)

    if angle2 > ship.av * math.pi / 360:  # LEFT
        commands[0] = 1
    elif angle2 < -ship.av * math.pi / 360:  # RIGHT
        commands[0] = -1

    if keys_pressed[pygame.K_w]:  # UP
        commands[1] = 1
    elif keys_pressed[pygame.K_s]:  # DOWN
        commands[1] = -1

    if keys_pressed[pygame.K_a]:  # LEFT
        commands[2] = 1
    elif keys_pressed[pygame.K_d]:  # RIGHT
        commands[2] = -1

    if mouse_pressed[0]:  # fire bullet
        commands[3] = 1

    if mouse_pressed[2]:  # fire missile
        commands[4] = 1

    if keys_pressed[pygame.K_SPACE]:  # fire mine
        commands[5] = 1

    if mouse_pressed[1]:  # utility
        commands[6] = 1

    if keys_pressed[pygame.K_LSHIFT]:  # boost
        commands[7] = 1

    if keys_pressed[pygame.K_u]:  # dock
        commands[8] = 1

    if keys_pressed[pygame.K_h]:  # mine
        commands[9] = 1

    for i in range(1, 10):
        if eval(f'keys_pressed[pygame.K_{i}]'):
            if i <= len(ship.bullet_types):
                commands[10] = i
                # print(f"command 10: {commands[10]}")
            elif i <= len(ship.bullet_types) + len(ship.missile_types):
                commands[11] = i - len(ship.bullet_types)
                # print(f"command 11: {commands[11]}")
            elif i <= len(ship.bullet_types) + len(ship.missile_types) + len(ship.mine_types):
                commands[12] = i - len(ship.bullet_types) - len(ship.missile_types)
                # print(f"command 12: {commands[12]}")
            elif i <= len(ship.bullet_types) + len(ship.missile_types) + len(ship.mine_types) + len(ship.util_types):
                commands[13] = i - len(ship.bullet_types) - len(ship.missile_types) - len(ship.mine_types)
                # print(f"command 13: {commands[13]}")

    return commands


# def minmax(mylist, rng):
#     temp = []
#     for r in mylist:
#         if r * 0.8 > rng:
#             temp.append(r)
#         else:
#             temp.append(math.inf)
#     if min(temp) < math.inf:
#         return temp.index(min(temp))
#     else:
#         return mylist.index(max(mylist))


def find_bullet(ship: Ship):
    ind = -1
    rng = math.inf
    R = math.inf
    X = math.inf
    Y = math.inf
    for bs in range(len(ship.bullet_types)):

        pos = ship.Qt.dot(ship.type.bullet_pos[bs]) - np.array(
            [ship.bullet_types[bs].width // 2, ship.bullet_types[bs].height // 2])

        if ship.bullet_types[bs].velocity != math.inf:

            vx = ship.target.vx - ship.vx
            vy = ship.target.vy - ship.vy
            xo = ship.target.centerx - ship.centerx - pos[0]
            yo = ship.target.centery - ship.centery - pos[1]
            bullet_velocity = ship.bullet_types[bs].velocity
            a = vx * vx + vy * vy - bullet_velocity * bullet_velocity
            b = 2 * (vx * xo + vy * yo)
            c = xo * xo + yo * yo

            if a < 0:
                t = (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)
            elif a > 0 and b * b - 4 * a * c > 0:
                t1 = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
                t2 = (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)
                t_list = [t1, t2, math.inf]
                val = min([t for t in t_list if t > 0])
                if val != math.inf:
                    t = val
                else:
                    t = -1
            elif b != 0:
                t = -c / b
            else:
                t = -1

            if t > 0:
                x = xo + vx * t
                y = yo + vy * t
                r = math.sqrt(x * x + y * y)
            else:
                x = math.inf
                y = math.inf
                r = math.inf

        else:
            x = ship.target.centerx - pos[0] - ship.centerx
            y = ship.target.centery - pos[1] - ship.centery
            r = math.sqrt(x * x + y * y)

        if rng > ship.bullet_types[bs].range > r or ind == -1 or (r > rng and ship.bullet_types[bs].range > rng):
            rng = ship.bullet_types[bs].range
            ind = bs
            X = x
            Y = y
            R = r

    if R != math.inf:
        V = np.array([[X], [Y]])
        V_prime = ship.Q.dot(V)
        angle2 = math.atan2(V_prime[0][0], V_prime[1][0])
        in_range = True
    else:
        angle2 = math.atan2(ship.target.centerx - ship.centerx, ship.target.centery - ship.centery)
        in_range = False

    return ind, X, Y, R, angle2, in_range


def find_missile(ship: Ship):
    ind = -1
    rng = math.inf
    dx = ship.target.centerx - ship.centerx
    dy = ship.target.centery - ship.centery
    r = math.sqrt(dx * dx + dy * dy)

    for ms in range(len(ship.missile_types)):
        if rng > ship.missile_types[ms].range > r or ind == -1 or (r > rng and ship.missile_types[ms].range > rng):
            rng = ship.missile_types[ms].range
            ind = ms
    return ind, r


def use_util(ship: Ship, gs: GlobalState, commands: list[int], faction: str):
    for us in range(len(ship.util_types)):
        use = ship.util_types[us].logic(ship, gs, commands, faction)
        if use == 1:
            return us, 1
    return 0, 0
