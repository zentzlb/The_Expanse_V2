import pygame
import os
import numpy as np
import math
import random as rnd
import time
# from copy import deepcopy, copy

from Draw_Window import draw_window
from Misc import GameState, LocalState
# from Weapon_Class import Bullet
from Ship_Class import Ship, Base, Asteroid
from Control_Functions import NPControl, NPControl2, TurretControl, PlayerControl2, Null
from Explosions import ShipExplosion

# changes
pygame.font.init()

WIDTH, HEIGHT = 1500, 850  # width and height of window

# WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # create window
# HUD = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)  # create HUD surface

pygame.display.set_caption("The Expanse")  # set window title


pygame.init()
pygame.mixer.init()

# explosion_group = pygame.sprite.Group()  # initialize explosion group

gs = GameState((100000, 100000), [])  # global state object: used to keep track of global variables


def main():
    """ASSIGN PLAYER CONTROL AND NPC CONTROL FUNCTIONS"""
    player_control = PlayerControl2
    npc_control = NPControl




    """Play Music"""
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.set_num_channels(3)
    ls = LocalState(0, 0, HEIGHT, WIDTH)
    ls.menu_name = 'faction selection'
    # gs.entities.append(enemy := Ship(NPControl, 1000 + rnd.randint(0, 200), 1000 +
    #                                  rnd.randint(rnd.randint(0, 200), 200), 170,
    #                                  ls.ShipTypes["Corpus 9"], ls.factions['Space Pirates']))
    # enemy.bullet_slots[0].type = ls.BulletTypes['AP AutoCannon']
    # enemy.bullet_slots[1].type = ls.BulletTypes['Flame Thrower']
    # enemy.missile_slots[0].type = ls.MissileTypes['Seeker']
    # enemy.util_slots[0].type = ls.UtilTypes['Reactor']

    # gs.entities.append(enemy := Ship(player_control, 1000 + rnd.randint(0, 200), 1000 +
    #                                  rnd.randint(rnd.randint(0, 200), 200), 170,
    #                                  ls.ShipTypes["Dragonfly"], ls.factions['Space Pirates']))
    # enemy.bullet_slots[0].type = ls.BulletTypes['Beam Laser']
    # enemy.missile_slots[0].type = ls.MissileTypes['Seeker']
    # enemy.missile_slots[1].type = ls.MissileTypes['Seeker']

    # enemy.refresh()
    # ls.player = enemy
    for _ in range(3):
        gs.entities.append(player := Ship(NPControl, 5000+rnd.randint(0, 200), 0-rnd.randint(0,
                                                                                             200),
                                          rnd.randint(0, 200),
                                          ls.ShipTypes["Pafonteer"], ls.factions['Terminus '
                                                                            'Corporation']))


        player.bullet_slots[0].type = ls.BulletTypes['Plasma']
        # player.bullet_slots[1].type = ls.BulletTypes['Plasma']

        # player.missile_slots[0].type = ls.MissileTypes['Seeker']
        # player.missile_slots[1].type = ls.MissileTypes['Seeker']
        # player.bullet_slots[0].type = ls.BulletTypes['Plasma']
        # player.bullet_slots[1].type = ls.BulletTypes['Plasma']
        # player.missile_slots[0].type = ls.MissileTypes['Seeker']
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
    counter = 0

    while run:  # main loop
        clock.tick(ls.FPS)
        for event in pygame.event.get():  # look for events
            if event.type == pygame.QUIT:  # check to see if user quit game
                run = False
                print('game over!')
                return
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                for button in ls.buttons:
                    if button.collidepoint(mx, my):
                        button()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    ls.menu_name = 'faction selection'

        if not ls.menu_name:
            if ls.player is not None and ls.player not in gs.entities:
                if ls.player.health > 0:
                    gs.entities.append(ls.player)

            gs.update()
            gs.explosion_group.update()  # scoot all explosions
            ls.update()
            fps = round(clock.get_fps())
            draw_window(gs, ls, fps, HEIGHT, WIDTH)
        else:
            ls.update()
            ls.draw()




        """Render Window"""


    pygame.quit()  # quit game
    return gs


if __name__ == "__main__":
    gs = main()
