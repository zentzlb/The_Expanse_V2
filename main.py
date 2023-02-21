"""https://github.com/techwithtim/PygameForBeginners"""

import pygame
import os
import numpy as np
import math
import random as rnd
import time

from Draw_Window import draw_window
from Misc import GlobalState, MoveScreen
from Weapon_Class import Bullet
from Ship_Class import Ship, Station, Asteroid
from Control_Functions import NPControl, NPControl2, TurretControl, PlayerControl1, PlayerControl2, Null
from Explosions import ShipExplosion

PCS = 'y'
nA = 1  # number of allied ships
nE = 1  # number of enemy ships
nR = 500  # number of asteroids

# """ASK USER WHETHER TO SPAWN PLAYER CONTROLLED SHIP"""
# while PCS != 'y' and PCS != 'n':
#     PCS = input('Spawn Player Controlled Ship? (y/n)')
#
# """NUMBER OF ALLIES"""
# while nA is not int and (nA < 0 or nA > 5):
#     nA = int(input('Number of Allies:'))
#
# """NUMBER OF ENEMIES"""
# while nE is not int and (nE < 0 or nE > 5):
#     nE = int(input('Number of Enemies:'))

pygame.font.init()

WIDTH, HEIGHT = 1500, 800  # width and height of window

# WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # create window
# HUD = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # create HUD surface

pygame.display.set_caption("The Expanse")  # set window title

FONT1 = pygame.font.SysFont('Agency FB', 25)  # font type
FONT2 = pygame.font.SysFont('Agency FB', 20)  # font type
FONT3 = pygame.font.SysFont('Agency FB', 15)  # font type

COLOR = (40, 10, 35)  # define window color
BLACK = (0, 50, 0)  # BLACK
RED = (255, 0, 0)  # RED
YELLOW = (255, 255, 0)  # YELLOW

# SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space2.png')), (WIDTH, HEIGHT)).convert(HUD)  # background image
# DUST = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space_dust_new.png')), (6000, 6000)).convert(HUD)  # foreground image
# FIELD = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'middle_ground.png')), (6000, 6000)).convert(HUD)  # middle ground image

FPS = 60  # define frame rate

# YELLOW_HIT = pygame.USEREVENT + 1
# RED_HIT = pygame.USEREVENT + 2

# music_file = os.path.join('Assets', 'music.mp3')  # path to music file
pygame.init()
pygame.mixer.init()

# explosion_group = pygame.sprite.Group()  # initialize explosion group

# pygame.init()
# pygame.mixer.init()

MyGS = GlobalState(100000, 0, 0, HEIGHT, WIDTH, [FONT1, FONT2, FONT3], [[], []], [[], []], [[], []], [[], []], [], [NPControl, NPControl2])  # global state object: used to keep track of global variables


def main():


    """ASSIGN PLAYER CONTROL AND NPC CONTROL FUNCTIONS"""
    player_control = PlayerControl1
    npc_control = NPControl

    """SPAWN IN SPECIFIED SHIPS"""
    if PCS == 'y':

        yellow = Ship(PlayerControl2, TurretControl, 80000+rnd.randint(2000, 5000), rnd.randint(2000, 5000), 0, 'yellow', 'Sprinter', MyGS, is_player=True)

        yellow.add_bullet(MyGS, 'Plasma')
        yellow.add_bullet(MyGS, 'Flame Thrower')
        yellow.add_missile(MyGS, 'Smart Missile')
        yellow.add_missile(MyGS, 'EMP Missile')
        yellow.add_missile(MyGS, 'Smart Missile')
        # yellow.add_util(MyGS, 'Reactor')
        yellow.add_util(MyGS, 'Jump Drive')
        # yellow.add_mine(MyGS, 'Black Hole')
        yellow.add_mine(MyGS, 'Proximity Mine')
        MyGS.ships[0].append(yellow)


    yellow = Station(rnd.randint(2000, 5000), rnd.randint(2000, 5000), 'Partrid', TurretControl, 'yellow', MyGS)
    MyGS.stations[0].append(yellow)

    for i in range(nA):
        # yellow = Ship(NPControl2, TurretControl, rnd.randint(0, 200), rnd.randint(0, 1000), rnd.randint(0, 359), 'yellow', 'Frigate', 'HV', 'HE')
        # MyGS.ships[0].append(yellow)
        yellow = Ship(NPControl2, TurretControl, rnd.randint(2000, 5000), rnd.randint(2000, 5000), 0, 'yellow', 'Frigate', MyGS)
        yellow.add_bullet(MyGS, 'Plasma')
        yellow.add_missile(MyGS, 'EMP Missile')
        MyGS.ships[0].append(yellow)

    for i in range(nE):

        red = Ship(NPControl, TurretControl, rnd.randint(MyGS.size-2000, MyGS.size-1000), rnd.randint(2000, 5000), 0, 'red', 'Ghost', MyGS)
        red.add_bullet(MyGS, 'Plasma')
        red.add_bullet(MyGS, 'AutoCannon')
        red.add_missile(MyGS, 'Smart Missile')
        red.add_missile(MyGS, 'Swarm Missile')
        red.add_util(MyGS, 'Jump Drive')
        red.add_util(MyGS, 'Reactor')
        MyGS.ships[1].append(red)

        # red = Ship(NPControl, TurretControl, rnd.randint(MyGS.size - 2000, MyGS.size - 1000), rnd.randint(2000, 5000),
        #            0, 'red', 'Heavy Fighter', MyGS)
        # red.add_bullet(MyGS, 'Flame Thrower')
        # red.add_missile(MyGS, 'Smart Missile')
        # MyGS.ships[1].append(red)

        # red = Ship(NPControl2, TurretControl, rnd.randint(MyGS.size-2000, MyGS.size-1000), rnd.randint(MyGS.size-2000, MyGS.size-1000), 0, 'red', 'Frigate', MyGS)
        # red.add_bullet(MyGS, 'Plasma')
        # red.add_missile(MyGS, 'EMP Missile')
        # MyGS.ships[1].append(red)

        red = Station(rnd.randint(MyGS.size-5000, MyGS.size-2000), rnd.randint(MyGS.size-5000, MyGS.size-2000), 'Partrid', TurretControl, 'red', MyGS)
        # red.image.convert(HUD)
        MyGS.stations[1].append(red)

    for i in range(nR):
        roid = Asteroid(rnd.randint(1000, MyGS.size-1000), rnd.randint(1000, MyGS.size-1000), rnd.randint(0, 359), rnd.randint(0, 100))
        MyGS.asteroids.append(roid)

    """Play Music"""
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.set_num_channels(3)
    # pygame.mixer.music.load(music_file)
    # pygame.mixer.music.play()
    # pygame.event.wait()

    run = True
    clock = pygame.time.Clock()  # game clock
    winner_text = ""
    MyGS.update()

    t1 = 0
    t2 = 0
    t3 = 0
    t4 = 0

    for faction in range(len(MyGS.ships)):
        for ship in MyGS.ships[faction]:
            ship.refresh(MyGS)

    while run:  # main loop
        clock.tick(FPS)
        fps = round(clock.get_fps())

        # if 0 < fps < 110:
        #     print(f'fps: {fps}')
        #     print(f'logic: {t3-t2}')  # 0.001
        #     print(f'display: {t4-t3}')  # 0.007
        #     print(f'other: {t2 - t1}')  # 0.000
        #     print()

        t1 = time.time()
        MyGS.explosion_group.update()  # scoot all explosions
        if PCS == 'n':
            MoveScreen(MyGS)

        for event in pygame.event.get():  # look for events
            if event.type == pygame.QUIT:  # check to see if user quit game
                run = False
                print('game over!')

        # """Station Function"""
        # for faction in range(len(MyGS.stations)):
        #     for station in MyGS.stations[faction]:
        #         station.scoot(MyGS, faction)  # scoot stations

        t2 = time.time()

        """Ship Movement"""
        for faction in range(len(MyGS.ships)):

            # for ship in MyGS.ships[faction]:
            for i in range(len(MyGS.ships[faction]) - 1, -1, -1):
                ship = MyGS.ships[faction][i]
                if ship.health > 0:
                    ship.scoot(MyGS, faction)  # move ships
                    if MyGS.ships[faction].count(ship) > 1:
                        print('mobile ship error')
                        print(MyGS.ships[faction].count(ship))
                else:
                    ShipExplosion(ship, MyGS)
                    MyGS.ships[faction].pop(i)  # remove dead ships
                    MyGS.update()

        """Station Function"""
        for faction in range(len(MyGS.stations)):
            # for station in MyGS.stations[faction]:
            for i in range(len(MyGS.stations[faction]) - 1, -1, -1):
                station = MyGS.stations[faction][i]
                station.scoot(MyGS, faction)  # scoot stations

        """Bullet Movement"""
        for faction in range(len(MyGS.bullets)):
            # for bullet in MyGS.bullets[faction]:
            for i in range(len(MyGS.bullets[faction]) - 1, -1, -1):
                bullet = MyGS.bullets[faction][i]
                bullet.scoot(MyGS)  # move bullets
            MyGS.bullets[faction] = [bullet for bullet in MyGS.bullets[faction] if bullet.timer > 0]

        for faction in range(len(MyGS.missiles)):
            # for missile in MyGS.missiles[faction]:
            for i in range(len(MyGS.missiles[faction]) - 1, -1, -1):
                missile = MyGS.missiles[faction][i]
                missile.scoot(MyGS)  # move missiles
            MyGS.missiles[faction] = [missile for missile in MyGS.missiles[faction] if missile.timer > 0 and missile.health > 0]

        """Render Window"""
        t3 = time.time()
        draw_window(MyGS, fps, HEIGHT, WIDTH)
        t4 = time.time()


    pygame.quit()  # quit game
    return MyGS


if __name__ == "__main__":
    MyGS = main()
