import pygame
import os
import numpy as np
import math
import random as rnd
import time
from copy import deepcopy, copy

from Draw_Window import draw_window
from Misc import GlobalState, LocalState
# from Weapon_Class import Bullet
from Ship_Class import Ship, Base, Asteroid
from Control_Functions import NPControl, NPControl2, TurretControl, PlayerControl2, Null
from Explosions import ShipExplosion


pygame.font.init()

WIDTH, HEIGHT = 1500, 800  # width and height of window

# WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # create window
# HUD = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # create HUD surface

pygame.display.set_caption("The Expanse")  # set window title


pygame.init()
pygame.mixer.init()

# explosion_group = pygame.sprite.Group()  # initialize explosion group

gs = GlobalState((100000, 100000), [])  # global state object: used to keep track of global variables



def main():
    """ASSIGN PLAYER CONTROL AND NPC CONTROL FUNCTIONS"""
    player_control = PlayerControl2
    npc_control = NPControl




    """Play Music"""
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.set_num_channels(3)
    ls = LocalState(0, 0, HEIGHT, WIDTH)
    gs.entities.append(enemy := Ship(player_control, 1000 + rnd.randint(0, 200), 1000 + rnd.randint(rnd.randint(0, 200), 200), 180,
                                     ls.ShipTypes["Pelomir"], ls.factions['Space Pirates']))
    enemy.bullet_types.append(ls.BulletTypes['Cannon'])
    enemy.bullet_types.append(ls.BulletTypes['Cannon'])
    # enemy.bullet_types.append(ls.BulletTypes['Cannon'])

    # enemy.bullet_types.append(ls.BulletTypes['Plasma'])
    # enemy.missile_types.append(ls.MissileTypes['Sneaker'])
    # enemy.missile_types.append(ls.MissileTypes['Sneaker'])
    # enemy.mine_types.append(ls.MineTypes['Black Hole'])
    enemy.refresh()
    ls.player = enemy
    for _ in range(1):
        gs.entities.append(player := Ship(Null, rnd.randint(0, 200), 0-rnd.randint(0, 200), rnd.randint(0, 200),
                                          ls.ShipTypes["Pelomir"], ls.factions['Terminus Corporation']))
        # gs.entities.append(enemy := Ship(npc_control, 1500+rnd.randint(0, 200), 1500+rnd.randint(0, 200), rnd.randint(0, 200),
        #                                  ls.ShipTypes["Pelomir"], ls.factions['Space Pirates']))
        player.bullet_types.append(ls.BulletTypes['Plasma'])
        # player.bullet_types.append(ls.BulletTypes['Railgun'])
        # player.bullet_types.append(ls.BulletTypes['Railgun'])

        # player.bullet_types.append(ls.BulletTypes['Cannon'])
        # player.missile_types.append(ls.MissileTypes['Seeker'])
        # enemy.bullet_types.append(ls.BulletTypes['Plasma'])
        # enemy.bullet_types.append(ls.BulletTypes['Plasma'])
        player.refresh()
        # enemy.refresh()

    # pygame.mixer.music.load(music_file)
    # pygame.mixer.music.play()
    # pygame.event.wait()

    run = True
    clock = pygame.time.Clock()  # game clock

    while run:  # main loop
        clock.tick(ls.FPS)
        for event in pygame.event.get(eventtype=pygame.QUIT):  # look for events
            # if event.type == pygame.QUIT:  # check to see if user quit game
            run = False
            print('game over!')
            return
        gs.update()
        fps = round(clock.get_fps())
        gs.explosion_group.update()  # scoot all explosions


        """Render Window"""
        ls.update()
        draw_window(gs, ls, fps, HEIGHT, WIDTH)

    pygame.quit()  # quit game
    return gs


if __name__ == "__main__":
    gs = main()
