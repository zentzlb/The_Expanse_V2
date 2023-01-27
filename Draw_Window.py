import pygame
import os
import numpy as np
import math
import time
from Misc import TargetingComputer
from Menus import StationMenu
from Ship_Class import Ship, Asteroid


def draw_window(gs, fps, HEIGHT, WIDTH):

    keys_pressed = pygame.key.get_pressed()

    gs.WIN2.fill((0, 0, 0, 0))
    gs.HUD.fill((0, 0, 0, 0))
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

    gs.WIN.blit(gs.SPACE, (0, 0))  # draw background

    gs.WIN.blit(gs.DUST, (-2000 - gs.x % 2000, -2000 - gs.y % 2000))  # draw foreground
    gs.WIN.blit(gs.FIELD, (-2000 - (gs.x / 5) % 2000, -2000 - (gs.y / 5) % 2000))  # draw foreground

    if keys_pressed[pygame.K_PERIOD]:
        gs.show_bars = True
    elif keys_pressed[pygame.K_COMMA]:
        gs.show_bars = False
    t1 = time.time()
    for roid in gs.asteroids:
        if (roid.x - gs.x < WIDTH and roid.x - gs.x + roid.width > 0) and (roid.y - gs.y < HEIGHT and roid.y - gs.y + roid.height > 0):
            gs.WIN.blit(roid.image, (roid.cx - gs.x, roid.cy - gs.y))


    for i in range(len(gs.particle_list) - 1, -1, -1):
        p = gs.particle_list[i]
        p.update()
        if (p.x - gs.x - p.radius < WIDTH and p.x - gs.x + p.radius > 0) and (
                p.y - gs.y - p.radius < WIDTH and p.y - gs.y + p.radius > 0):
            pygame.draw.circle(gs.WIN, p.color, (p.x - gs.x, p.y - gs.y), p.radius)
        if p.radius <= 0:
            gs.particle_list.pop(i)

    for faction in range(len(gs.ships)):

        for station in gs.stations[faction]:
            if (station.x - gs.x < WIDTH and station.x - gs.x + station.width > 0) and (station.y - gs.y < HEIGHT and station.y - gs.y + station.height > 0):
                gs.WIN.blit(station.image, (station.cx - gs.x, station.cy - gs.y))
                for turret in station.turrets:
                    TURRET = pygame.transform.rotate(turret.image, turret.angle)
                    gs.WIN.blit(TURRET, (turret.cx - gs.x, turret.cy - gs.y))

        for ship in gs.ships[faction]:
            if ship.health > 0 and (ship.x - gs.x < WIDTH and ship.x - gs.x + ship.width > 0) and (ship.y - gs.y < HEIGHT and ship.y - gs.y + ship.height > 0):
                if ship.forward:
                    SHIP = pygame.transform.rotate(ship.imagef, ship.angle)  # display with thrusters active
                else:
                    SHIP = pygame.transform.rotate(ship.image, ship.angle)  # display without thrusters
                gs.WIN.blit(SHIP, (ship.cx - gs.x, ship.cy - gs.y))
                sop = ship.sop
                if sop > 0:
                    pygame.draw.circle(gs.WIN2, (0, 0, 255, round(sop)), (ship.centerx - gs.x, ship.centery - gs.y), math.sqrt(2) * ship.width // 2)

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

                    # translatex = 1000
                    # translatey = 25
                    #
                    #
                    # box_tl = (1 + translatex, 2 * rr + 5 * hbh / 2 + 5 + translatey)
                    # box_bl = (1 + translatex, 4 * rr + 5 * hbh / 2 + 10 + translatey)
                    # box_tr = (5 + 2 * rr + translatex, 2 * rr + 5 * hbh / 2 + 5 + translatey)
                    # box_br = (5 + 2 * rr + translatex, 4 * rr + 5 * hbh / 2 + 10 + translatey)
                    #
                    # pygame.draw.line(gs.HUD, SILVER, box_tl, box_tr, 3)  # top line
                    # pygame.draw.line(gs.HUD, SILVER, box_tl, box_bl, 3)  # left line
                    # pygame.draw.line(gs.HUD, SILVER, box_tr, box_br, 3)  # right line
                    # pygame.draw.line(gs.HUD, SILVER, box_bl, box_br, 3)  # bottom line

                    """DRAW HEALTH AND ENERGY BARS"""
                    pygame.draw.line(gs.HUD, (0, 255, 0, 60), (bt, 2 * rr + hbh), (bt + 2 * rr * ship.health / ship.ship_type.health, 2 * rr + hbh), hbh)
                    pygame.draw.line(gs.HUD, (80, 100, 255, 60), (bt, 2 * rr + 2 * hbh + bt), (bt + 2 * rr * ship.energy / ship.ship_type.energy, 2 * rr + 2 * hbh + bt), hbh)
                    pygame.draw.line(gs.HUD, SILVER, (0, 2 * rr + hbh / 2), (bt + 2 * rr + bt, 2 * rr + hbh / 2), bt)
                    pygame.draw.line(gs.HUD, SILVER, (0, 2 * rr + bt * hbh / 2 + 2), (bt + 2 * rr + bt, 2 * rr + bt * hbh / 2 + 2), bt)
                    pygame.draw.line(gs.HUD, SILVER, (0, 2 * rr + 5 * hbh / 2 + 5), (bt + 2 * rr + bt, 2 * rr + 5 * hbh / 2 + 5), bt)
                    pygame.draw.line(gs.HUD, SILVER, (1, 2 * rr + hbh / 2), (1, 2 * rr + 5 * hbh / 2 + 5), bt)
                    pygame.draw.line(gs.HUD, SILVER, (bt + 2 * rr + 2, 2 * rr + hbh / 2), (bt + 2 * rr + 2, 2 * rr + 5 * hbh / 2 + 5), bt)

                    """DRAW TARGET gs.WINDOW"""
                    box_tl = (0, 2 * rr + 5 * hbh / 2 + 5)
                    length = 2 * rr + 7
                    rect1 = pygame.Rect(box_tl[0], box_tl[1], length, length)
                    rect2 = pygame.Rect(box_tl[0], box_tl[1]+length-bt, length, length)
                    center = rect1.center


                    health_text = gs.fonts[0].render(f"{fps} Shields: {100 * ship.health / ship.ship_type.health:0.0f}%", 1, YELLOW)
                    energy_text = gs.fonts[0].render(f"Energy: {100 * ship.energy / ship.ship_type.energy:0.0f}%", 1, YELLOW)

                    gs.HUD.blit(health_text, (7, 2 * rr + hbh / 2))  # display health
                    gs.HUD.blit(energy_text, (7, 2 * rr + 3 * hbh / 2 + bt))  # display energy

                    if type(ship.target) is Ship and ship.target.health > 0:
                        MyAngle = TargetingComputer(ship)
                        # print([90 - MyAngle * 180 / math.pi, yellow.angle, MyAngle * 180 / math.pi - yellow.angle])
                        if abs(90 - MyAngle * 180 / math.pi - ship.angle) < ship.av:
                            MyColor = GREEN
                        else:
                            MyColor = RED
                        pygame.draw.line(gs.WIN, MyColor, (round(ship.centerx - gs.x + 25 * math.cos(MyAngle)), round(ship.centery - gs.y + 25 * math.sin(MyAngle))), (round(ship.centerx - gs.x + 50 * math.cos(MyAngle)), round(ship.centery - gs.y + 50 * math.sin(MyAngle))), bt)

                        """DRAW TARGET"""

                        dx = ship.target.cx - ship.cx
                        dy = ship.target.cy - ship.cy

                        # target_rect = pygame.Rect(box_tl[0] + 2, box_tl[1] + 2, box_tr[0] - box_tl[0] - 3, box_bl[1] - box_tl[1] - 3)
                        pygame.draw.rect(gs.HUD, (255, 0, 0, 15), rect1)

                        SHIP = pygame.transform.rotate(ship.target.image, ship.target.angle)
                        adjust_x = (ship.target.width - ship.target.height * abs(math.sin(ship.target.angle * math.pi / 180)) - ship.target.width * abs(math.cos(ship.target.angle * math.pi / 180))) / 2
                        adjust_y = (ship.target.height - ship.target.width * abs(math.sin(ship.target.angle * math.pi / 180)) - ship.target.height * abs(math.cos(ship.target.angle * math.pi / 180))) / 2
                        gs.HUD.blit(SHIP, (center[0] - ship.target.width // 2 + adjust_x, center[1] - ship.target.height // 2 + adjust_y))
                        cos = math.cos(ship.target.angle * math.pi / 180)
                        sin = math.sin(ship.target.angle * math.pi / 180)
                        Q = np.array([[cos, sin], [-sin, cos]])
                        for turret in ship.target.turrets:
                            target_turret = pygame.transform.rotate(turret.image, turret.angle)
                            adjust_turret_x = (turret.width - turret.height * abs(math.sin(turret.angle * math.pi / 180)) - turret.width * abs(math.cos(turret.angle * math.pi / 180))) / 2
                            adjust_turret_y = (turret.height - turret.width * abs(math.sin(turret.angle * math.pi / 180)) - turret.height * abs(math.cos(turret.angle * math.pi / 180))) / 2
                            target_turret_x = (center[0] - turret.width // 2 + adjust_turret_x) + Q.dot(turret.pos)[0]
                            target_turret_y = (center[1] - turret.height // 2 + adjust_turret_y) + Q.dot(turret.pos)[1]
                            gs.HUD.blit(target_turret, (target_turret_x, target_turret_y))
                        health_text = gs.fonts[2].render(f"Shields: {100 * ship.target.health / ship.target.ship_type.health:0.0f}%", True, SILVER)
                        energy_text = gs.fonts[2].render(
                            f"Energy: {100 * ship.target.energy / ship.target.ship_type.energy:0.0f}%", True, SILVER)
                        range_text = gs.fonts[2].render(
                            f"Range: {math.sqrt(dx * dx + dy * dy):0.0f}", True, SILVER)
                        gs.HUD.blit(health_text, (7, box_tl[1] + 1))
                        gs.HUD.blit(energy_text, (7, box_tl[1] + 1 + gs.fonts[2].get_height()))
                        gs.HUD.blit(range_text, (7, box_tl[1] + 1 + 2 * gs.fonts[2].get_height()))
                    elif type(ship.target) is Asteroid:
                        """DRAW TARGET"""

                        # target_rect = pygame.Rect(box_tl[0] + 2, box_tl[1] + 2, box_tr[0] - box_tl[0] - 3, box_bl[1] - box_tl[1] - 3)
                        pygame.draw.rect(gs.HUD, (255, 255, 255, 15), rect1)

                        # ROID = pygame.transform.scale(ship.target.image, (1000, 1000))
                        adjust_x = (ship.target.width - ship.target.height * abs(
                            math.sin(ship.target.angle * math.pi / 180)) - ship.target.width * abs(
                            math.cos(ship.target.angle * math.pi / 180))) / 2
                        adjust_y = (ship.target.height - ship.target.width * abs(
                            math.sin(ship.target.angle * math.pi / 180)) - ship.target.height * abs(
                            math.cos(ship.target.angle * math.pi / 180))) / 2
                        gs.HUD.blit(ship.target.image_scaled, (center[0] - 50, center[1] - 50))
                        for i in range(len(ship.target.ore_types)):
                            ore_text = gs.fonts[2].render(f"{ship.target.ore_types[i]}: {ship.target.ore[ship.target.ore_types[i]]}", True, SILVER)
                            gs.HUD.blit(ore_text, (7, box_tl[1] + 1 + i * gs.fonts[2].get_height()))
                        # health_text = global_state.fonts[2].render(ship.target.ore_types[i]
                        #     f"Shields: {100 * ship.target.health / ship.target.ship_type.health:0.0f}%", True, SILVER)
                        # energy_text = global_state.fonts[2].render(
                        #     f"Energy: {100 * ship.target.energy / ship.target.ship_type.energy:0.0f}%", True, SILVER)
                        # gs.HUD.blit(health_text, (7, box_tl[1] + 1))
                        # gs.HUD.blit(energy_text, (7, box_tl[1] + 1 + global_state.fonts[2].get_height()))
                    pygame.draw.rect(gs.HUD, SILVER, rect1, bt)

                    if keys_pressed[pygame.K_p]:
                        quad = gs.size
                        Length = length - 2 * bt
                        x = rect2.x + bt
                        y = rect2.y + bt
                        pygame.draw.rect(gs.HUD, (30, 70, 100, 100), rect2)

                        X = round(ship.centerx * (Length / quad) + x)
                        Y = round(ship.centery * (Length / quad) + y)
                        pygame.draw.circle(gs.HUD, (0, 255, 0), (X, Y), 2)
                        for roid in gs.asteroids:
                            X = round(roid.centerx * (Length / quad) + x)
                            Y = round(roid.centery * (Length / quad) + y)
                            pygame.draw.circle(gs.HUD, (255, 255, 255), (X, Y), 2)
                        for station in gs.stations[0]:
                            X = round(station.centerx * (Length / quad) + x)
                            Y = round(station.centery * (Length / quad) + y)
                            # pygame.draw.circle(hud, (255, 255, 0), (X, Y), 4)
                            radarRect = pygame.Rect(X - 2, Y - 2, 4, 4)
                            pygame.draw.rect(gs.HUD, (255, 255, 0), radarRect)
                        for station in gs.stations[1]:
                            X = round(station.centerx * (Length / quad) + x)
                            Y = round(station.centery * (Length / quad) + y)
                            # pygame.draw.circle(hud, (255, 255, 0), (X, Y), 4)
                            radarRect = pygame.Rect(X - 2, Y - 2, 4, 4)
                            pygame.draw.rect(gs.HUD, (255, 0, 0), radarRect)
                    else:
                        th = gs.fonts[2].get_height()
                        c = 0

                        for i in range(len(ship.bullet_types)):
                            if i == ship.bullet_sel:
                                COLOR = YELLOW
                            else:
                                COLOR = SILVER
                            text = gs.fonts[2].render(f"{c + 1}. {ship.bullet_types[i].name}", True, COLOR)
                            gs.HUD.blit(text, (7, rect2.y + 4 + c * th))
                            c += 1
                        for i in range(len(ship.missile_types)):
                            if i == ship.missile_sel:
                                COLOR = YELLOW
                            else:
                                COLOR = SILVER
                            text = gs.fonts[2].render(f"{c + 1}. {ship.missile_types[i].name}", True, COLOR)
                            gs.HUD.blit(text, (7, rect2.y + 4 + c * th))
                            c += 1
                        for i in range(len(ship.mine_types)):
                            if i == ship.mine_sel:
                                COLOR = YELLOW
                            else:
                                COLOR = SILVER
                            text = gs.fonts[2].render(f"{c + 1}. {ship.mine_types[i].name}", True, COLOR)
                            gs.HUD.blit(text, (7, rect2.y + 4 + c * th))
                            c += 1
                        for i in range(len(ship.util_types)):
                            if i == ship.util_sel:
                                COLOR = YELLOW
                            else:
                                COLOR = SILVER
                            text = gs.fonts[2].render(f"{c + 1}. {ship.util_types[i].name}", True, COLOR)
                            gs.HUD.blit(text, (7, rect2.y + 4 + c * th))
                            c += 1

                    pygame.draw.rect(gs.HUD, SILVER, rect2, bt)

                    rng = ship.ship_type.range


        """DISPLAY BULLETS AND MISSILES"""
        for bullet in gs.bullets[faction]:
            if (bullet.x - gs.x < WIDTH and bullet.x - gs.x + bullet.width > 0) and (bullet.y - gs.y < HEIGHT and bullet.y - gs.y + bullet.height > 0):
                gs.WIN.blit(bullet.image, (bullet.x - gs.x, bullet.y - gs.y))
        for missile in gs.missiles[faction]:
            if (missile.x - gs.x < WIDTH and missile.x - gs.x + missile.width > 0) and (missile.y - gs.y < HEIGHT and missile.y - gs.y + missile.height > 0):
                if missile.angle == 0:
                    MISSILE = missile.image
                else:
                    MISSILE = pygame.transform.rotate(missile.image, missile.angle)
                gs.WIN.blit(MISSILE, (missile.x - gs.x, missile.y - gs.y))


    gs.explosion_group.draw(gs.WIN)

    for i in range(len(gs.particle_list2) - 1, -1, -1):
        p = gs.particle_list2[i]
        p.update()
        if (p.x - gs.x - p.radius < WIDTH and p.x - gs.x + p.radius > 0) and (p.y - gs.y - p.radius < WIDTH and p.y - gs.y + p.radius > 0):
            pygame.draw.circle(gs.WIN, p.color, (p.x - gs.x, p.y - gs.y), p.radius)
        if p.radius <= 0:
            gs.particle_list2.pop(i)

    """RADAR"""
    if gs.menu is None and rng != 0:
        pygame.draw.circle(gs.HUD, (0, 0, 255, 50), (rr + bt, rr + bt), rr)
        pygame.draw.circle(gs.HUD, (0, 150, 255, 75), (rr + bt, rr + bt), 50 * time.time() % rr, width=bt)
        pygame.draw.circle(gs.HUD, (200, 200, 255), (rr + bt, rr + bt), rr + bt, width=bt)
        # gs.WIN.blit(gs.HUD, (0, 0))
        pygame.draw.circle(gs.HUD, GREEN, (rr + 3, rr + 3), 6)

        rr2 = (rr - 2 * bt)

        c = rr2 / (math.log((rng ** 2) / (1000 + rng) + 1) ** 2)

        for faction in range(len(gs.ships)):
            if faction == 0:
                MyColor = YELLOW
            else:
                MyColor = RED
            for ship in gs.ships[faction]:
                if ship.is_visible:  # only show uncloaked ships on radar
                    dx = ship.centerx - gs.cx
                    dy = ship.centery - gs.cy
                    d = math.sqrt(dx ** 2 + dy ** 2)
                    r = c * math.log((d ** 2) / (1000 + d) + 1) ** 2
                    if r < rr2:
                        angle = math.atan2(dy, dx)
                        X = rr + r * math.cos(angle) + 3
                        Y = rr + r * math.sin(angle) + 3
                        pygame.draw.circle(gs.HUD, MyColor, (X, Y), 3)

            for station in gs.stations[faction]:
                dx = station.centerx - gs.cx
                dy = station.centery - gs.cy
                d = math.sqrt(dx ** 2 + dy ** 2)
                r = c * math.log((d ** 2) / (1000 + d) + 1) ** 2
                if r < rr2:
                    angle = math.atan2(dy, dx)
                    X = rr + r * math.cos(angle) + 3
                    Y = rr + r * math.sin(angle) + 3
                    radarRect = pygame.Rect(X - 5, Y - 5, 10, 10)
                    pygame.draw.rect(gs.HUD, MyColor, radarRect)
                    # pygame.draw.circle(gs.WIN, YELLOW, (X, Y), 4)

            for missile in gs.missiles[faction]:
                dx = missile.centerx - gs.cx
                dy = missile.centery - gs.cy
                d = math.sqrt(dx ** 2 + dy ** 2)
                r = c * math.log((d ** 2) / (1000 + d) + 1) ** 2
                if r < rr2:
                    angle = math.atan2(dy, dx)
                    X = rr + r * math.cos(angle) + 3
                    Y = rr + r * math.sin(angle) + 3
                    pygame.draw.circle(gs.HUD, MyColor, (X, Y), 1)

        for roid in gs.asteroids:
            dx = roid.centerx - gs.cx
            dy = roid.centery - gs.cy
            d = math.sqrt(dx ** 2 + dy ** 2)
            r = c * math.log((d ** 2) / (1000 + d) + 1) ** 2
            if r < rr2:
                angle = math.atan2(dy, dx)
                X = rr + r * math.cos(angle) + 3
                Y = rr + r * math.sin(angle) + 3
                pygame.draw.circle(gs.HUD, (255, 255, 255), (X, Y), 4)

    elif gs.menu is not None:
        gs.menu.draw_menu(gs.HUD, gs)

    gs.WIN.blit(gs.WIN2, (0, 0))
    gs.WIN.blit(gs.HUD, (0, 0))

    pygame.display.update()  # update window