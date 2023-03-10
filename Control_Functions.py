import pygame
import math
import numpy as np
import random as rnd
import time

from Misc import FindNearest, FindMineable
from Ship_Class import Ship, Station, Asteroid

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.health = math.inf


"""NPC LOGIC"""


def Null(ship, global_state, faction):
    commands = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    return commands


def NPControl(ship, gs, faction):

    commands = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    if ship.health < ship.ship_type.health // 10:
        ship.target = FindNearest(ship, gs.stations[faction])

    elif ship.target is None or ship.target.health <= 0 or ship.counter == 60:
        ship.target = FindNearest(ship, gs.targets[faction])
        ship.counter = 0
        if ship.target is None:
            ship.target = Point(rnd.randint(0, gs.size), rnd.randint(0, gs.size))
            # print(ship.target)
            # print(type(ship.target) is Point)
    else:
        ship.counter += 1

    if type(ship.target) is Station:
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
        if ship.health < ship.ship_type.health and ship.energy > 10:
            commands[6] = 1

        if type(ship.target) is Station:
            commands[7] = 1

        if type(ship.target) is Asteroid:
            commands[8] = 1

    elif type(ship.target) is Ship:

        pos = ship.Q.transpose().dot(ship.ship_type.bullet_pos[ship.bullet_sel]) - np.array([ship.bullet_types[ship.bullet_sel].width // 2, ship.bullet_types[ship.bullet_sel].height // 2])

        vx = ship.target.vx
        vy = ship.target.vy
        xo = ship.target.centerx - pos[0]
        yo = ship.target.centery - pos[1]
        bullet_velocity = ship.bullet_types[ship.bullet_sel].velocity

        a = vx ** 2 + vy ** 2 - bullet_velocity ** 2
        b = 2 * (vx * (xo - ship.centerx) + vy * (yo - ship.centery))
        c = (xo - ship.centerx) ** 2 + (yo - ship.centery) ** 2

        t = (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)

        x = xo + vx * t
        y = yo + vy * t

        dx = x - ship.centerx
        dy = y - ship.centery

        cos = math.cos(ship.angle * math.pi / 180)
        sin = math.sin(ship.angle * math.pi / 180)

        Q = np.array([[cos, -sin], [sin, cos]])
        V = np.array([[dx], [dy]])
        V_prime = Q.dot(V)
        angle2 = math.atan2(V_prime[0][0], V_prime[1][0])

        # print(angle2)

        if angle2 > ship.av * math.pi / 360:  # LEFT
            commands[0] = 1
        elif angle2 < -ship.av * math.pi / 360:  # RIGHT
            commands[0] = -1

        """GO FORWARD"""
        if angle2 < math.pi / 180:
            commands[1] = 1
        else:
            commands[1] = -1

        """NO LATERAL ACCELERATION"""
        commands[2] = round(math.sin(time.time()))

        """SHOOT"""
        if abs(angle2 * 180 / math.pi) < ship.av and ship.energy >= 30 and ship.bullet_types[ship.bullet_sel].range * ship.bullet_types[ship.bullet_sel].range > dx * dx + dy * dy:  # SHOOT BULLET
            commands[3] = 1

        if len(ship.missile_types) > 0 and ship.energy >= ship.missile_types[ship.missile_sel].energy and ship.missile_types[ship.missile_sel].range > math.sqrt(dx ** 2 + dy ** 2):
            commands[4] = 1

        """MINES"""
        # commands.append(0)

        """BOOST"""
        if ship.health < 20 and ((ship.energy > ship.bullet_types[ship.bullet_sel].energy and ship.boost) or ship.energy > ship.bullet_types[ship.bullet_sel].energy + 30):
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


def NPControl2(ship, global_state, faction):

    commands = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    if (ship.cargo.cargo_total >= ship.ship_type.cargo_cap or ship.health < 0.8 * ship.ship_type.health):  # type(ship.target) is not Station and
        ship.target = FindNearest(ship, global_state.stations[faction])
    elif type(ship.target) is not Asteroid and ship.cargo.cargo_total < ship.ship_type.cargo_cap:
        ship.target = FindMineable(ship, global_state.asteroids)
    elif type(ship.target) is Asteroid and sum(ship.target.ore.values()) == 0:
        ship.target = FindMineable(ship, global_state.asteroids)

    if ship.target is not None:

        # rewrite

        x = ship.target.centerx
        y = ship.target.centery

        dx = x - ship.centerx
        dy = y - ship.centery

        # cos = math.cos(ship.angle * math.pi / 180)
        # sin = math.sin(ship.angle * math.pi / 180)
        #
        # Q = np.array([[cos, -sin], [sin, cos]])
        V = np.array([[dx], [dy]])
        V_prime = ship.Q.dot(V)
        angle2 = math.atan2(V_prime[0][0], V_prime[1][0])



        # print(angle2)

        if angle2 > ship.av * math.pi / 360:  # LEFT
            commands[0] = 1
        elif angle2 < -ship.av * math.pi / 360:  # RIGHT
            commands[0] = -1

        """"""
        if dx * dx + dy * dy < ship.target.width * ship.target.width // 4:
            # print('close')
            v_prime = ship.Q.dot(np.array([[ship.vx], [ship.vy]]))
            if v_prime[0] > 0:
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
        if ship.health < ship.ship_type.health * 0.8 and ship.energy > 10:
            commands[7] = 1

        if type(ship.target) is Station:
            commands[8] = 1

        if type(ship.target) is Asteroid:
            commands[9] = 1

    # else:
    #     commands = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    return commands


"""TURRET CONTROLS"""

def TurretControl(ship, gs, faction):

    commands = []

    if ship.target is None or ship.target.health >= 0 or ship.counter == 60:
        ship.target = FindNearest(ship, gs.targets[faction])
        ship.counter = 0
    else:
        ship.counter += 1

    if ship.target is not None:
        vx = ship.target.vx
        vy = ship.target.vy
        xo = ship.target.centerx
        yo = ship.target.centery
        bullet_velocity = ship.bullet_types[ship.bullet_sel].velocity

        a = vx ** 2 + vy ** 2 - bullet_velocity ** 2
        b = 2 * (vx * (xo - ship.centerx) + vy * (yo - ship.centery))
        c = (xo - ship.centerx) ** 2 + (yo - ship.centery) ** 2

        t = (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
        x = xo + vx * t
        y = yo + vy * t

        dx = x - ship.centerx
        dy = y - ship.centery

        cos = math.cos(ship.angle * math.pi / 180)
        sin = math.sin(ship.angle * math.pi / 180)

        Q = np.array([[cos, -sin], [sin, cos]])
        V = np.array([[dx], [dy]])
        V_prime = Q.dot(V)
        angle2 = math.atan2(V_prime[0][0], V_prime[1][0])

        if angle2 > ship.av * math.pi / 360:  # LEFT
            commands.append(1)
        elif angle2 < -ship.av * math.pi / 360:  # RIGHT
            commands.append(-1)
        else:
            commands.append(0)

        """SHOOT"""
        if abs(angle2 * 180 / math.pi) < ship.av and ship.energy >= 30 and ship.bullet_types[ship.bullet_sel].range * ship.bullet_types[ship.bullet_sel].range > dx * dx + dy * dy:  # SHOOT BULLET
            commands.append(1)
        else:
            commands.append(0)
        if len(ship.missile_types) > 0 and (ship.energy >= ship.missile_types[ship.missile_sel].energy and ship.missile_types[ship.missile_sel].range > math.sqrt(dx ** 2 + dy ** 2)):
            commands.append(1)
        else:
            commands.append(0)

    else:
        commands = [0, 0, 0]



    return commands


"""PLAYER KEYBOARD CONTROLS"""


def PlayerControl1(ship, global_state, faction):

    keys_pressed = pygame.key.get_pressed()
    commands = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    if keys_pressed[pygame.K_l]:  # LOCK ONTO THE NEAREST TARGET
        target_list = []
        for i in range(len(global_state.ships)):
            if i != faction:
                target_list.extend(global_state.ships[i])
        ship.target = FindNearest(ship, target_list)
    elif keys_pressed[pygame.K_o]:
        ship.target = FindMineable(ship, global_state.asteroids)
    elif keys_pressed[pygame.K_SEMICOLON]:  # REMOVE TARGET LOCK
        ship.target = None


    """MOVEMENT"""
    if keys_pressed[pygame.K_q]:  # LEFT
        commands[0] = 1
    elif keys_pressed[pygame.K_e]:  # RIGHT
        commands[0] = -1

    if keys_pressed[pygame.K_w]:  # UP
        commands[1] = 1
    elif keys_pressed[pygame.K_s]:  # DOWN
        commands[1] = -1

    if keys_pressed[pygame.K_a]:  # LEFT
        commands[2] = 1
    elif keys_pressed[pygame.K_d]:  # RIGHT
        commands[2] = -1

    if keys_pressed[pygame.K_SPACE]:  # fire bullet
        commands[3] = 1

    if keys_pressed[pygame.K_m]:  # fire missile
        commands[4] = 1

    if keys_pressed[pygame.K_n]:  # fire mine
        commands[5] = 1

    if keys_pressed[pygame.K_k]:  # utility
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


def minmax(mylist, rng):
    temp = []
    for r in mylist:
        if r * 0.8 > rng:
            temp.append(r)
        else:
            temp.append(math.inf)
    if min(temp) < math.inf:
        return temp.index(min(temp))
    else:
        return mylist.index(max(mylist))


