import pygame
from pygame.locals import *
import os
import numpy as np
import math
import time
from Misc import TargetingComputer
from Menus import StationMenu
from Ship_Class import Ship, Asteroid
from Explosions import trans_circle, glow_circle
from Control_Functions import Point
from Text_Commands import unpack_str, complete_str


def draw_window(gs, fps, HEIGHT, WIDTH):

    keys_pressed = pygame.key.get_pressed()

    player_ship = None
    # gs.WIN2.fill((0, 0, 0, 0))
    gs.WIN.fill((10, 10, 20))
    rr = 100  # radar radius
    hbh = 30  # health bar height
    bt = 3
    rng = 0



    COLOR = (40, 10, 35)  # define window color
    BLACK = (0, 50, 0)  # BLACK
    RED = (255, 0, 0)  # RED
    YELLOW = (255, 255, 0)  # YELLOW
    GREEN = (0, 255, 0)  # green
    BLUE = (75, 75, 255)  # blue
    SILVER = (200, 200, 255)  # silver

    # gs.WIN.blit(gs.SPACE, (0, 0))  # draw background

    # gs.WIN.blit(gs.DUST, (-2000 - gs.x % 2000, -2000 - gs.y % 2000))  # draw foreground

    # gs.WIN.blit(gs.FIELD, (-2000 - (gs.x / 5) % 2000, -2000 - (gs.y / 5) % 2000))  # draw foreground

    for dust in gs.dust:
        x = (dust[0] - gs.x) % 6000 - 1000
        y = (dust[1] - gs.y) % 6000 - 1000
        gs.WIN.blit(gs.dust_images[dust[2]], (x, y))

    for roid in gs.field:
        x = (roid.x - gs.x) / 4 % 6000 - 1000
        y = (roid.y - gs.y) / 4 % 6000 - 1000
        if x < WIDTH and x + roid.width > 0 and y < HEIGHT and y + roid.height > 0:
            gs.WIN.blit(roid.image, (x, y))

    if keys_pressed[pygame.K_PERIOD]:
        gs.show_bars = True
    elif keys_pressed[pygame.K_COMMA]:
        gs.show_bars = False
    t1 = time.time()
    for roid in gs.asteroids:
        if (roid.x - gs.x < WIDTH and roid.x - gs.x + roid.width > 0) and (roid.y - gs.y < HEIGHT and roid.y - gs.y + roid.height > 0):
            gs.WIN.blit(roid.image, (roid.cx - gs.x, roid.cy - gs.y))

    # for i in range(len(gs.particle_list) - 1, -1, -1):
    #     p = gs.particle_list[i]
    #     p.scoot()
    #     if (p.x - gs.x - p.radius < WIDTH and p.x - gs.x + p.radius > 0) and (
    #             p.y - gs.y - p.radius < WIDTH and p.y - gs.y + p.radius > 0):
    #         p.draw(gs)
    #         # pygame.draw.circle(gs.WIN, p.color, (p.x - gs.x, p.y - gs.y), p.radius)
    #         # if p.glow != (0, 0, 0):
    #         #     glow_circle(gs.WIN, p.x - gs.x, p.y - gs.y, 2*p.radius, p.glow)
    #     if p.radius <= 0:
    #         gs.particle_list.pop(i)

    for p in gs.particle_list:
        p.scoot()
        if (p.x - gs.x - p.radius < WIDTH and p.x - gs.x + p.radius > 0) and (
                p.y - gs.y - p.radius < WIDTH and p.y - gs.y + p.radius > 0):
            p.draw(gs)

    gs.particle_list = [p for p in gs.particle_list if p.radius > 0]

    for faction in range(len(gs.ships)):

        for station in gs.stations[faction]:
            if (station.x - gs.x < WIDTH and station.x - gs.x + station.width > 0) and (station.y - gs.y < HEIGHT and station.y - gs.y + station.height > 0):
                gs.WIN.blit(station.image, (station.cx - gs.x, station.cy - gs.y))
                for turret in station.turrets:
                    TURRET = pygame.transform.rotate(turret.image, turret.angle)
                    gs.WIN.blit(TURRET, (turret.cx - gs.x, turret.cy - gs.y))

        for ship in gs.ships[faction]:
            if ship.health > 0 and (ship.x - gs.x < WIDTH and ship.x - gs.x + ship.width > 0) and (ship.y - gs.y < HEIGHT and ship.y - gs.y + ship.height > 0):
                # if ship.forward:
                #     SHIP = pygame.transform.rotate(ship.imagef, ship.angle)  # display with thrusters active
                # else:

                SHIP = pygame.transform.rotate(ship.image, ship.angle)  # display without thrusters
                gs.WIN.blit(SHIP, (ship.cx - gs.x, ship.cy - gs.y))

                if ship.heat > 0 and not ship.cloaked:
                    opacity = 50 * (ship.heat / ship.ship_type.heat_capacity)
                    # trans_circle(gs.WIN, ship.centerx - gs.x, ship.centery - gs.y, math.sqrt(2) * ship.width // 2, (0, 0, 255, round(opacity)))
                    glow_circle(gs.WIN, ship.centerx - gs.x, ship.centery - gs.y, math.sqrt(2) * ship.width // 2, (0, 0, round(opacity)))

                for turret in ship.turrets:
                    TURRET = pygame.transform.rotate(turret.image, turret.angle)
                    gs.WIN.blit(TURRET, (turret.cx - gs.x, turret.cy - gs.y))

                if not ship.is_player and gs.show_bars:  # ship is not player controlled
                    """HEALTH BAR"""
                    pygame.draw.line(gs.WIN, GREEN, (ship.x - gs.x, ship.y - gs.y - 5), (
                        ship.x + 100 * ship.health / ship.ship_type.energy - gs.x, ship.y - gs.y - 5), bt)

                    """ENERGY BAR"""
                    pygame.draw.line(gs.WIN, BLUE, (ship.x - gs.x, ship.y - bt - gs.y - 5), (ship.x + 100 * ship.energy / ship.ship_type.energy - gs.x, ship.y - bt - gs.y - 5), bt)

                elif ship.is_player:  # player controlled ship
                    """DRAW INFO BOX"""
                    player_ship = ship


        """DISPLAY BULLETS AND MISSILES"""
        for bullet in gs.bullets[faction]:
            if (bullet.x - gs.x < WIDTH and bullet.x - gs.x + bullet.width > 0) and (bullet.y - gs.y < HEIGHT and bullet.y - gs.y + bullet.height > 0):
                # gs.WIN.blit(bullet.image, (bullet.x - gs.x, bullet.y - gs.y))
                bullet.draw(gs)
        for missile in gs.missiles[faction]:
            if (missile.x - gs.x < WIDTH and missile.x - gs.x + missile.width > 0) and (missile.y - gs.y < HEIGHT and missile.y - gs.y + missile.height > 0):
                missile.draw(gs)
                # if missile.angle == 0:
                #     MISSILE = missile.image
                # else:
                #     MISSILE = pygame.transform.rotate(missile.image, missile.angle)
                # gs.WIN.blit(MISSILE, (missile.x - gs.x, missile.y - gs.y))

    gs.explosion_group.draw(gs.WIN)

    for p in gs.particle_list2:
        p.scoot()
        if (p.x - gs.x - p.radius < WIDTH and p.x - gs.x + p.radius > 0) and (p.y - gs.y - p.radius < WIDTH and p.y - gs.y + p.radius > 0):
            p.draw(gs)

    gs.particle_list2 = [p for p in gs.particle_list2 if p.radius > 0]

    for line in gs.lines:
        line.draw(gs)
    gs.lines = []

    if player_ship is not None:
        draw_hud(gs, player_ship, keys_pressed, fps)
        draw_textbox(gs, player_ship, keys_pressed, fps)
    elif gs.menu is not None:
        gs.menu.draw_menu(gs.WIN, gs)


    # gs.WIN.blit(gs.WIN2, (0, 0))
    # gs.WIN.blit(gs.WIN, (0, 0))

    pygame.display.update()  # scoot window



def draw_hud(gs, player_ship, keys_pressed, fps):
    COLOR = (40, 10, 35)  # define window color
    BLACK = (0, 50, 0)  # BLACK
    RED = (255, 0, 0)  # RED
    YELLOW = (255, 255, 0)  # YELLOW
    GREEN = (0, 255, 0)  # green
    BLUE = (75, 75, 255)  # blue
    SILVER = (200, 200, 255)  # silver

    rr = 100  # radar radius
    hbh = 30  # health bar height
    bt = 3
    rng = 0
    box1_pos = (0, 2 * rr + hbh / 2)
    box2_pos = (0, 2 * rr + bt * hbh / 2 + bt)
    box3_pos = (0, 2 * rr + 5 * hbh / 2 + 5)
    bw = bt + 2 * rr + bt + 1
    bh = hbh + bt + 2

    box_tl = (0, box3_pos[1] + hbh + bt - 1)
    length = 2 * rr + 7
    rect1 = pygame.Rect(box_tl[0], box_tl[1], length, length)
    rect2 = pygame.Rect(box_tl[0], box_tl[1] + length - bt, length, length)
    center = rect1.center

    HUD = pygame.Surface((length, gs.height), pygame.SRCALPHA)
    # HUD.set_colorkey((0,0,0))
    """PUT STUFF HERE"""

    """DRAW HEALTH AND ENERGY BARS"""
    # hbc = (255 * min((player_ship.heat, player_ship.ship_type.heat_capacity)) // player_ship.ship_type.heat_capacity, 255, 0, 60)

    pygame.draw.line(HUD, (0, 255, 0, 60), (bt, 2 * rr + hbh),
                     (bt + 2 * rr * player_ship.health / player_ship.ship_type.health, 2 * rr + hbh), hbh)
    pygame.draw.line(HUD, (80, 100, 255, 60), (bt, 2 * rr + 2 * hbh + bt),
                     (bt + 2 * rr * player_ship.energy / player_ship.ship_type.energy, 2 * rr + 2 * hbh + bt), hbh)
    pygame.draw.line(HUD, (255, 100, 0, 60), (bt, 2 * rr + 3 * hbh + 2 * bt),
                     (bt + 2 * rr * player_ship.heat / player_ship.ship_type.heat_capacity, 2 * rr + 3 * hbh + 2 * bt),
                     hbh)

    pygame.draw.rect(HUD, SILVER, (box1_pos[0], box1_pos[1], bw, bh), bt)
    pygame.draw.rect(HUD, SILVER, (box2_pos[0], box2_pos[1], bw, bh), bt)
    pygame.draw.rect(HUD, SILVER, (box3_pos[0], box3_pos[1], bw, bh), bt)

    # pygame.draw.line(HUD, SILVER, (0, 2 * rr + hbh / 2), (bt + 2 * rr + bt, 2 * rr + hbh / 2), bt)
    # pygame.draw.line(HUD, SILVER, (0, 2 * rr + bt * hbh / 2 + 2), (bt + 2 * rr + bt, 2 * rr + bt * hbh / 2 + 2), bt)
    # pygame.draw.line(HUD, SILVER, (0, 2 * rr + 5 * hbh / 2 + 5), (bt + 2 * rr + bt, 2 * rr + 5 * hbh / 2 + 5), bt)
    # pygame.draw.line(HUD, SILVER, (1, 2 * rr + hbh / 2), (1, 2 * rr + 5 * hbh / 2 + 5), bt)
    # pygame.draw.line(HUD, SILVER, (bt + 2 * rr + 2, 2 * rr + hbh / 2), (bt + 2 * rr + 2, 2 * rr + 5 * hbh / 2 + 5),
    #                  bt)

    """DRAW TARGET WINDOW"""

    health_text = gs.fonts[0].render(
        f"{fps} Shields: {100 * player_ship.health / player_ship.ship_type.health:0.0f}%", 1,
        YELLOW)
    energy_text = gs.fonts[0].render(f"Energy: {100 * player_ship.energy / player_ship.ship_type.energy:0.0f}%", 1,
                                     YELLOW)
    heat_text = gs.fonts[0].render(f"Heat: {100 * player_ship.heat / player_ship.ship_type.heat_capacity:0.0f}%", 1,
                                   YELLOW)

    HUD.blit(health_text, (7, 2 * rr + hbh / 2))  # display health
    HUD.blit(energy_text, (7, 2 * rr + 3 * hbh / 2 + bt))  # display energy
    HUD.blit(heat_text, (7, 2 * rr + 5 * hbh / 2 + 2 * bt))  # display energy

    if type(player_ship.target) is Ship and player_ship.target.health > 0:
        MyAngle, in_rng, r = TargetingComputer(player_ship)
        # print(MyAngle)
        angle = -((player_ship.angle % 360) * math.pi / 180 - math.pi/2)
        if MyAngle-angle > math.pi:
            angle += 2 * math.pi
        elif MyAngle - angle < -math.pi:
            MyAngle += 2 * math.pi
        # print(angle)
        # da = (ship_angle-MyAngle) % (math.pi / 2)
        # print(da)
        # print()
        # angle = da + MyAngle
        angle2 = MyAngle - angle
        if not in_rng:
            MyColor1 = (255, 0, 0, 50)
            MyColor2 = (255, 0, 0, 15)
        elif abs(angle2) < 0.7 and abs(r * math.sin(angle2)) < player_ship.target.height / 2:#abs(MyAngle - angle) < player_ship.av * math.pi / 180:
            MyColor1 = (0, 255, 0, 100)
            MyColor2 = (0, 255, 0, 15)
        else:
            MyColor1 = (255, 255, 255, 50)
            MyColor2 = (255, 255, 255, 15)

        # make surface


        # x and y positions
        l1 = player_ship.width
        l2 = player_ship.width + 20

        width = 2 * l2
        height = 2 * l2

        TC = pygame.Surface((width, height), pygame.SRCALPHA)

        xo = width // 2
        yo = height // 2

        angles = (-angle, -MyAngle)
        pygame.draw.arc(TC, MyColor2, TC.get_rect(), min(angles), max(angles), width=10)
        x1 = round(xo + l1 * math.cos(MyAngle))
        y1 = round(yo + l1 * math.sin(MyAngle))
        x2 = round(xo + l2 * math.cos(MyAngle))
        y2 = round(yo + l2 * math.sin(MyAngle))
        pygame.draw.line(TC, MyColor1, (x1, y1), (x2, y2), bt)
        x1 = round(xo + l1 * math.cos(angle))
        y1 = round(yo + l1 * math.sin(angle))
        x2 = round(xo + l2 * math.cos(angle))
        y2 = round(yo + l2 * math.sin(angle))
        pygame.draw.line(TC, MyColor1, (x1, y1), (x2, y2), bt)
        gs.WIN.blit(TC, (gs.width//2-xo, gs.height//2-yo))


        """DRAW TARGET"""

        dx = player_ship.target.cx - player_ship.cx
        dy = player_ship.target.cy - player_ship.cy

        # target_rect = pygame.Rect(box_tl[0] + 2, box_tl[1] + 2, box_tr[0] - box_tl[0] - 3, box_bl[1] - box_tl[1] - 3)
        pygame.draw.rect(HUD, (255, 0, 0, 15), rect1)

        SHIP = pygame.transform.rotate(player_ship.target.image, player_ship.target.angle)
        adjust_x = (player_ship.target.width - player_ship.target.height * abs(
            math.sin(player_ship.target.angle * math.pi / 180)) - player_ship.target.width * abs(
            math.cos(player_ship.target.angle * math.pi / 180))) / 2
        adjust_y = (player_ship.target.height - player_ship.target.width * abs(
            math.sin(player_ship.target.angle * math.pi / 180)) - player_ship.target.height * abs(
            math.cos(player_ship.target.angle * math.pi / 180))) / 2
        HUD.blit(SHIP,
                 (center[0] - player_ship.target.width // 2 + adjust_x,
                  center[1] - player_ship.target.height // 2 + adjust_y))
        # cos = math.cos(player_ship.target.angle * math.pi / 180)
        # sin = math.sin(player_ship.target.angle * math.pi / 180)
        # Q = np.array([[cos, sin], [-sin, cos]])
        Q = player_ship.target.Qt
        for turret in player_ship.target.turrets:
            target_turret = pygame.transform.rotate(turret.image, turret.angle)
            adjust_turret_x = (turret.width - turret.height * abs(
                math.sin(turret.angle * math.pi / 180)) - turret.width * abs(
                math.cos(turret.angle * math.pi / 180))) / 2
            adjust_turret_y = (turret.height - turret.width * abs(
                math.sin(turret.angle * math.pi / 180)) - turret.height * abs(
                math.cos(turret.angle * math.pi / 180))) / 2
            target_turret_x = (center[0] - turret.width // 2 + adjust_turret_x) + Q.dot(turret.pos)[0]
            target_turret_y = (center[1] - turret.height // 2 + adjust_turret_y) + Q.dot(turret.pos)[1]
            HUD.blit(target_turret, (target_turret_x, target_turret_y))
        health_text = gs.fonts[2].render(
            f"Shields: {100 * player_ship.target.health / player_ship.target.ship_type.health:0.0f}%",
            True, SILVER)
        energy_text = gs.fonts[2].render(
            f"Energy: {100 * player_ship.target.energy / player_ship.target.ship_type.energy:0.0f}%", True, SILVER)
        heat_text = gs.fonts[2].render(
            f"Heat: {100 * player_ship.target.heat / player_ship.target.ship_type.heat_capacity:0.0f}%", True, SILVER)
        range_text = gs.fonts[2].render(
            f"Range: {math.sqrt(dx * dx + dy * dy):0.0f}", True, SILVER)
        HUD.blit(health_text, (7, box_tl[1] + 1))
        HUD.blit(energy_text, (7, box_tl[1] + 1 + gs.fonts[2].get_height()))
        HUD.blit(heat_text, (7, box_tl[1] + 1 + 2 * gs.fonts[2].get_height()))
        HUD.blit(range_text, (7, box_tl[1] + 1 + 3 * gs.fonts[2].get_height()))
    elif type(player_ship.target) is Asteroid:
        """DRAW TARGET"""

        # target_rect = pygame.Rect(box_tl[0] + 2, box_tl[1] + 2, box_tr[0] - box_tl[0] - 3, box_bl[1] - box_tl[1] - 3)
        pygame.draw.rect(HUD, (255, 255, 255, 15), rect1)

        # ROID = pygame.transform.scale(ship.target.image, (1000, 1000))
        adjust_x = (player_ship.target.width - player_ship.target.height * abs(
            math.sin(player_ship.target.angle * math.pi / 180)) - player_ship.target.width * abs(
            math.cos(player_ship.target.angle * math.pi / 180))) / 2
        adjust_y = (player_ship.target.height - player_ship.target.width * abs(
            math.sin(player_ship.target.angle * math.pi / 180)) - player_ship.target.height * abs(
            math.cos(player_ship.target.angle * math.pi / 180))) / 2
        HUD.blit(player_ship.target.image_scaled, (center[0] - 50, center[1] - 50))
        for i in range(len(player_ship.target.ore_types)):
            ore_text = gs.fonts[2].render(
                f"{player_ship.target.ore_types[i]}: {player_ship.target.ore[player_ship.target.ore_types[i]]}",
                True, SILVER)
            HUD.blit(ore_text, (7, box_tl[1] + 1 + i * gs.fonts[2].get_height()))
        # health_text = global_state.fonts[2].render(ship.target.ore_types[i]
        #     f"Shields: {100 * ship.target.health / ship.target.ship_type.health:0.0f}%", True, SILVER)
        # energy_text = global_state.fonts[2].render(
        #     f"Energy: {100 * ship.target.energy / ship.target.ship_type.energy:0.0f}%", True, SILVER)
        # HUD.blit(health_text, (7, box_tl[1] + 1))
        # HUD.blit(energy_text, (7, box_tl[1] + 1 + global_state.fonts[2].get_height()))
    pygame.draw.rect(HUD, SILVER, rect1, bt)

    if keys_pressed[pygame.K_p]:
        quad = gs.size
        Length = length - 2 * bt
        x = rect2.x + bt
        y = rect2.y + bt
        pygame.draw.rect(HUD, (30, 70, 100, 100), rect2)

        X = round(player_ship.centerx * (Length / quad) + x)
        Y = round(player_ship.centery * (Length / quad) + y)
        pygame.draw.circle(HUD, (0, 255, 0), (X, Y), 2)
        for roid in gs.asteroids:
            X = round(roid.centerx * (Length / quad) + x)
            Y = round(roid.centery * (Length / quad) + y)
            pygame.draw.circle(HUD, (255, 255, 255), (X, Y), 2)
        for station in gs.stations[0]:
            X = round(station.centerx * (Length / quad) + x)
            Y = round(station.centery * (Length / quad) + y)
            # pygame.draw.circle(hud, (255, 255, 0), (X, Y), 4)
            radarRect = pygame.Rect(X - 2, Y - 2, 4, 4)
            pygame.draw.rect(HUD, (255, 255, 0), radarRect)
        for station in gs.stations[1]:
            X = round(station.centerx * (Length / quad) + x)
            Y = round(station.centery * (Length / quad) + y)
            # pygame.draw.circle(hud, (255, 255, 0), (X, Y), 4)
            radarRect = pygame.Rect(X - 2, Y - 2, 4, 4)
            pygame.draw.rect(HUD, (255, 0, 0), radarRect)
    else:
        th = gs.fonts[2].get_height()
        c = 0

        for i in range(len(player_ship.bullet_types)):
            if i == player_ship.bullet_sel:
                COLOR = YELLOW
            else:
                COLOR = SILVER
            text = gs.fonts[2].render(f"{c + 1}. {player_ship.bullet_types[i].name}", True, COLOR)
            HUD.blit(text, (7, rect2.y + 4 + c * th))
            c += 1
        for i in range(len(player_ship.missile_types)):
            if i == player_ship.missile_sel:
                COLOR = YELLOW
            else:
                COLOR = SILVER
            text = gs.fonts[2].render(f"{c + 1}. {player_ship.missile_types[i].name}", True, COLOR)
            HUD.blit(text, (7, rect2.y + 4 + c * th))
            c += 1
        for i in range(len(player_ship.mine_types)):
            if i == player_ship.mine_sel:
                COLOR = YELLOW
            else:
                COLOR = SILVER
            text = gs.fonts[2].render(f"{c + 1}. {player_ship.mine_types[i].name}", True, COLOR)
            HUD.blit(text, (7, rect2.y + 4 + c * th))
            c += 1
        for i in range(len(player_ship.util_types)):
            if i == player_ship.util_sel:
                COLOR = YELLOW
            else:
                COLOR = SILVER
            text = gs.fonts[2].render(f"{c + 1}. {player_ship.util_types[i].name}", True, COLOR)
            HUD.blit(text, (7, rect2.y + 4 + c * th))
            c += 1

    pygame.draw.rect(HUD, SILVER, rect2, bt)

    """RADAR"""
    rng = player_ship.ship_type.range
    pygame.draw.circle(HUD, (0, 0, 255, 50), (rr + bt, rr + bt), rr)
    pygame.draw.circle(HUD, (0, 150, 255, 75), (rr + bt, rr + bt), 50 * time.time() % rr, width=bt)
    pygame.draw.circle(HUD, (200, 200, 255), (rr + bt, rr + bt), rr + bt, width=bt)
    # HUD.blit(HUD, (0, 0))
    pygame.draw.circle(HUD, GREEN, (rr + 3, rr + 3), 6)

    rr2 = (rr - 2 * bt)

    c = rr2 / (math.log((rng ** 2) / (1000 + rng) + 1) ** 2)

    if player_ship.target is not None and type(player_ship.target) is not Point:
        dx = player_ship.target.centerx - gs.cx
        dy = player_ship.target.centery - gs.cy
        d = math.sqrt(dx * dx + dy * dy)
        r = c * math.log((d * d) / (1000 + d) + 1) ** 2
        if r < rr2:
            angle = math.atan2(dy, dx)
            X = rr + r * math.cos(angle) + 3
            Y = rr + r * math.sin(angle) + 3
            pygame.draw.circle(HUD, (255, 255, 0), (X, Y), 5)

    for roid in gs.asteroids:
        dx = roid.centerx - gs.cx
        dy = roid.centery - gs.cy
        d = math.sqrt(dx * dx + dy * dy)
        r = c * math.log((d * d) / (1000 + d) + 1) ** 2
        if r < rr2:
            angle = math.atan2(dy, dx)
            X = rr + r * math.cos(angle) + 3
            Y = rr + r * math.sin(angle) + 3
            pygame.draw.circle(HUD, (255, 255, 255), (X, Y), 4)

    for faction in range(len(gs.ships)):
        if faction == 0:
            MyColor = GREEN
        else:
            MyColor = RED
        for ship in gs.ships[faction]:
            if ship.is_visible:  # only show uncloaked ships on radar
                dx = ship.centerx - gs.cx
                dy = ship.centery - gs.cy
                d = math.sqrt(dx * dx + dy * dy)
                r = c * math.log((d * d) / (1000 + d) + 1) ** 2
                if r < rr2:
                    angle = math.atan2(dy, dx)
                    X = rr + r * math.cos(angle) + 3
                    Y = rr + r * math.sin(angle) + 3
                    pygame.draw.circle(HUD, MyColor, (X, Y), 3)

        for station in gs.stations[faction]:
            dx = station.centerx - gs.cx
            dy = station.centery - gs.cy
            d = math.sqrt(dx * dx + dy * dy)
            r = c * math.log((d * d) / (1000 + d) + 1) ** 2
            if r < rr2:
                angle = math.atan2(dy, dx)
                X = rr + r * math.cos(angle) + 3
                Y = rr + r * math.sin(angle) + 3
                radarRect = pygame.Rect(X - 5, Y - 5, 10, 10)
                pygame.draw.rect(HUD, MyColor, radarRect)
                # pygame.draw.circle(HUD, YELLOW, (X, Y), 4)

        for missile in gs.missiles[faction]:
            dx = missile.centerx - gs.cx
            dy = missile.centery - gs.cy
            d = math.sqrt(dx * dx + dy * dy)
            r = c * math.log((d * d) / (1000 + d) + 1) ** 2
            if r < rr2:
                angle = math.atan2(dy, dx)
                X = rr + r * math.cos(angle) + 3
                Y = rr + r * math.sin(angle) + 3
                pygame.draw.circle(HUD, MyColor, (X, Y), 1)

    gs.WIN.blit(HUD, (0, 0))

def draw_textbox(gs, player_ship, keys_pressed, fps):

    if keys_pressed[pygame.K_ESCAPE]:
        gs.misc_info['command prompt'] = False
        gs.misc_info['command text'] = ''

    if gs.misc_info['command prompt']:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    gs.misc_info['command text'] = gs.misc_info['command text'][:-1]
                elif event.key == pygame.K_RETURN:
                    if len(gs.misc_info['command text']) > 0:
                        gs.misc_info['command history'].append(gs.misc_info['command text'])
                        if len(gs.misc_info['command history']) > 30:
                            gs.misc_info['command history'] = gs.misc_info['command history'][-30:]
                        unpack_str(gs.misc_info['command text'], gs, player_ship)
                    gs.misc_info['command text'] = ''
                elif event.key == pygame.K_TAB:
                    if len(gs.misc_info['command text']) > 0:
                        complete_str(gs.misc_info['command text'], gs, player_ship)
                elif event.unicode.isprintable() and len(gs.misc_info['command text']) < 40:
                    gs.misc_info['command text'] += event.unicode

        text = gs.misc_info['command text']
        text_surface = gs.fonts[2].render(text, True, (255, 255, 255))
        tw = text_surface.get_width()
        th = text_surface.get_height()
        sw = 300
        sh = th * (len(gs.misc_info['command history'])+1) + 10
        surf = pygame.Surface((sw, sh))
        for i in range(len(gs.misc_info['command history'])):
            txt = gs.misc_info['command history'][i]
            txt_surface = gs.fonts[2].render(txt, True, (200, 200, 200))
            surf.blit(txt_surface, (5, 5+i*th))
        surf.blit(text_surface, (5, sh-th-5))
        surf.set_alpha(100)
        gs.WIN.blit(surf, (gs.width-sw, gs.height-sh))
    else:
        pygame.event.clear()

    if keys_pressed[pygame.K_TAB]:
        gs.misc_info['command prompt'] = True