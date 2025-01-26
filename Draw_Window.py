import pygame
from pygame.locals import *
import os
import numpy as np
import math
import time
from Misc import GlobalState, LocalState
from utils import TargetingComputer
from Menus import StationMenu
from Ship_Class import Ship, Asteroid, Base
from Weapon_Class import Bullet, Missile
from Data.Types import glow_circle
from Control_Functions import Point
from Text_Commands import unpack_str, complete_str


def draw_window(gs: GlobalState, ls: LocalState, fps: int, HEIGHT: int, WIDTH: int):
    keys_pressed = pygame.key.get_pressed()

    # ls.WIN2.fill((0, 0, 0, 0))
    ls.WIN.fill((10, 10, 20))
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

    # ls.WIN.blit(gs.SPACE, (0, 0))  # draw background

    # ls.WIN.blit(gs.DUST, (-2000 - ls.x % 2000, -2000 - ls.y % 2000))  # draw foreground

    # ls.WIN.blit(gs.FIELD, (-2000 - (ls.x / 5) % 2000, -2000 - (ls.y / 5) % 2000))  # draw foreground

    for dust in ls.dust:
        x = (dust[0] - ls.x) % 6000 - 1000
        y = (dust[1] - ls.y) % 6000 - 1000
        ls.WIN.blit(ls.dust_images[dust[2]], (x, y))

    for roid in ls.field:
        x = (roid.x - ls.x) / 4 % 6000 - 1000
        y = (roid.y - ls.y) / 4 % 6000 - 1000
        if x < WIDTH and x + roid.width > 0 and y < HEIGHT and y + roid.height > 0:
            ls.WIN.blit(roid.image, (x, y))

    for entity in gs.entities:
        # pygame.draw.rect(ls.WIN, (0, 200, 0, 100), (entity.x-ls.x, entity.y-ls.y, entity.width, entity.height), width=3)
        entity.draw(ls.WIN, entity.centerx - ls.x, entity.centery - ls.y)

    for event in gs.events:
        event.draw(ls.WIN, ls.x, ls.y)

    for line in gs.lines:
        line.draw(ls)
    gs.lines = []

    if ls.player is not None:
        draw_hud(gs, ls, keys_pressed, fps)
        draw_textbox(gs, ls, keys_pressed, fps)
    elif ls.menu is not None:
        ls.menu.draw_menu(ls.WIN, gs)

    # ls.WIN.blit(ls.WIN2, (0, 0))
    # ls.WIN.blit(ls.WIN, (0, 0))

    pygame.display.update()  # scoot window


def draw_hud(gs: GlobalState, ls: LocalState, keys_pressed, fps: float):
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

    HUD = pygame.Surface((length, ls.height), pygame.SRCALPHA)
    # HUD.set_colorkey((0,0,0))
    """PUT STUFF HERE"""

    """DRAW HEALTH AND ENERGY BARS"""
    # hbc = (255 * min((ls.player.heat, ls.player.ship_type.heat_capacity)) // ls.player.ship_type.heat_capacity, 255, 0, 60)

    pygame.draw.line(HUD, (0, 255, 0, 60), (bt, 2 * rr + hbh),
                     (bt + 2 * rr * ls.player.health / ls.player.type.health, 2 * rr + hbh), hbh)
    pygame.draw.line(HUD, (80, 100, 255, 60), (bt, 2 * rr + 2 * hbh + bt),
                     (bt + 2 * rr * ls.player.energy / ls.player.type.energy, 2 * rr + 2 * hbh + bt), hbh)
    pygame.draw.line(HUD, (255, 100, 0, 60), (bt, 2 * rr + 3 * hbh + 2 * bt),
                     (bt + 2 * rr * ls.player.heat / ls.player.type.heat_capacity, 2 * rr + 3 * hbh + 2 * bt),
                     hbh)

    pygame.draw.rect(HUD, SILVER, (box1_pos[0], box1_pos[1], bw, bh), bt)
    pygame.draw.rect(HUD, SILVER, (box2_pos[0], box2_pos[1], bw, bh), bt)
    pygame.draw.rect(HUD, SILVER, (box3_pos[0], box3_pos[1], bw, bh), bt)

    """DRAW TARGET WINDOW"""

    health_text = ls.fonts[0].render(
        f"{fps} Shields: {100 * ls.player.health / ls.player.type.health:0.0f}%", 1,
        YELLOW)
    energy_text = ls.fonts[0].render(f"Energy: {100 * ls.player.energy / ls.player.type.energy:0.0f}%", 1,
                                     YELLOW)
    heat_text = ls.fonts[0].render(f"Heat: {100 * ls.player.heat / ls.player.type.heat_capacity:0.0f}%", 1,
                                   YELLOW)

    HUD.blit(health_text, (7, 2 * rr + hbh / 2))  # display health
    HUD.blit(energy_text, (7, 2 * rr + 3 * hbh / 2 + bt))  # display energy
    HUD.blit(heat_text, (7, 2 * rr + 5 * hbh / 2 + 2 * bt))  # display energy

    if type(ls.player.target) is Ship and ls.player.target.health > 0:
        MyAngle, in_rng, r = TargetingComputer(ls.player)
        # print(MyAngle)
        angle = -((ls.player.angle % 360) * math.pi / 180 - math.pi / 2)
        if MyAngle - angle > math.pi:
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
        elif abs(angle2) < 0.7 and abs(r * math.sin(
                angle2)) < ls.player.target.height / 2:  # abs(MyAngle - angle) < ls.player.av * math.pi / 180:
            MyColor1 = (0, 255, 0, 100)
            MyColor2 = (0, 255, 0, 15)
        else:
            MyColor1 = (255, 255, 255, 50)
            MyColor2 = (255, 255, 255, 15)

        # make surface

        # x and y positions
        l1 = ls.player.width
        l2 = ls.player.width + 20

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
        ls.WIN.blit(TC, (ls.width // 2 - xo, ls.height // 2 - yo))

        """DRAW TARGET"""

        dx = ls.player.target.centerx - ls.player.centerx
        dy = ls.player.target.centery - ls.player.centery

        # target_rect = pygame.Rect(box_tl[0] + 2, box_tl[1] + 2, box_tr[0] - box_tl[0] - 3, box_bl[1] - box_tl[1] - 3)
        pygame.draw.rect(HUD, (255, 0, 0, 15), rect1)

        SHIP = pygame.transform.rotate(ls.player.target.image, ls.player.target.angle)
        adjust_x = (ls.player.target.width - ls.player.target.height * abs(
            math.sin(ls.player.target.angle * math.pi / 180)) - ls.player.target.width * abs(
            math.cos(ls.player.target.angle * math.pi / 180))) / 2
        adjust_y = (ls.player.target.height - ls.player.target.width * abs(
            math.sin(ls.player.target.angle * math.pi / 180)) - ls.player.target.height * abs(
            math.cos(ls.player.target.angle * math.pi / 180))) / 2
        HUD.blit(SHIP,
                 (center[0] - ls.player.target.width // 2 + adjust_x,
                  center[1] - ls.player.target.height // 2 + adjust_y))
        # cos = math.cos(ls.player.target.angle * math.pi / 180)
        # sin = math.sin(ls.player.target.angle * math.pi / 180)
        # Q = np.array([[cos, sin], [-sin, cos]])
        Q = ls.player.target.Qt
        for turret in ls.player.target.turrets:
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
        health_text = ls.fonts[2].render(
            f"Shields: {100 * ls.player.target.health / ls.player.target.type.health:0.0f}%",
            True, SILVER)
        energy_text = ls.fonts[2].render(
            f"Energy: {100 * ls.player.target.energy / ls.player.target.type.energy:0.0f}%", True, SILVER)
        heat_text = ls.fonts[2].render(
            f"Heat: {100 * ls.player.target.heat / ls.player.target.type.heat_capacity:0.0f}%", True, SILVER)
        range_text = ls.fonts[2].render(
            f"Range: {math.sqrt(dx * dx + dy * dy):0.0f}", True, SILVER)
        HUD.blit(health_text, (7, box_tl[1] + 1))
        HUD.blit(energy_text, (7, box_tl[1] + 1 + ls.fonts[2].get_height()))
        HUD.blit(heat_text, (7, box_tl[1] + 1 + 2 * ls.fonts[2].get_height()))
        HUD.blit(range_text, (7, box_tl[1] + 1 + 3 * ls.fonts[2].get_height()))
    elif type(ls.player.target) is Asteroid:
        """DRAW TARGET"""

        # target_rect = pygame.Rect(box_tl[0] + 2, box_tl[1] + 2, box_tr[0] - box_tl[0] - 3, box_bl[1] - box_tl[1] - 3)
        pygame.draw.rect(HUD, (255, 255, 255, 15), rect1)

        # ROID = pygame.transform.scale(ship.target.image, (1000, 1000))
        adjust_x = (ls.player.target.width - ls.player.target.height * abs(
            math.sin(ls.player.target.angle * math.pi / 180)) - ls.player.target.width * abs(
            math.cos(ls.player.target.angle * math.pi / 180))) / 2
        adjust_y = (ls.player.target.height - ls.player.target.width * abs(
            math.sin(ls.player.target.angle * math.pi / 180)) - ls.player.target.height * abs(
            math.cos(ls.player.target.angle * math.pi / 180))) / 2
        HUD.blit(ls.player.target.image_scaled, (center[0] - 50, center[1] - 50))
        for i in range(len(ls.player.target.ore_types)):
            ore_text = ls.fonts[2].render(
                f"{ls.player.target.ore_types[i]}: {ls.player.target.ore[ls.player.target.ore_types[i]]}",
                True, SILVER)
            HUD.blit(ore_text, (7, box_tl[1] + 1 + i * ls.fonts[2].get_height()))
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

        X = round(ls.player.centerx * (Length / quad) + x)
        Y = round(ls.player.centery * (Length / quad) + y)
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
        th = ls.fonts[2].get_height()
        c = 0

        for i in range(len(ls.player.bullet_types)):
            if i == ls.player.bullet_sel:
                COLOR = YELLOW
            else:
                COLOR = SILVER
            text = ls.fonts[2].render(f"{c + 1}. {ls.player.bullet_types[i].name}", True, COLOR)
            HUD.blit(text, (7, rect2.y + 4 + c * th))
            c += 1
        for i in range(len(ls.player.missile_types)):
            if i == ls.player.missile_sel:
                COLOR = YELLOW
            else:
                COLOR = SILVER
            text = ls.fonts[2].render(f"{c + 1}. {ls.player.missile_types[i].name}", True, COLOR)
            HUD.blit(text, (7, rect2.y + 4 + c * th))
            c += 1
        for i in range(len(ls.player.mine_types)):
            if i == ls.player.mine_sel:
                COLOR = YELLOW
            else:
                COLOR = SILVER
            text = ls.fonts[2].render(f"{c + 1}. {ls.player.mine_types[i].name}", True, COLOR)
            HUD.blit(text, (7, rect2.y + 4 + c * th))
            c += 1
        for i in range(len(ls.player.util_types)):
            if i == ls.player.util_sel:
                COLOR = YELLOW
            else:
                COLOR = SILVER
            text = ls.fonts[2].render(f"{c + 1}. {ls.player.util_types[i].name}", True, COLOR)
            HUD.blit(text, (7, rect2.y + 4 + c * th))
            c += 1

    pygame.draw.rect(HUD, SILVER, rect2, bt)

    """RADAR"""
    rng = ls.player.type.range
    pygame.draw.circle(HUD, (0, 0, 255, 50), (rr + bt, rr + bt), rr)
    pygame.draw.circle(HUD, (0, 150, 255, 75), (rr + bt, rr + bt), 50 * time.time() % rr, width=bt)
    pygame.draw.circle(HUD, (200, 200, 255), (rr + bt, rr + bt), rr + bt, width=bt)
    # HUD.blit(HUD, (0, 0))
    pygame.draw.circle(HUD, GREEN, (rr + 3, rr + 3), 6)

    rr2 = (rr - 2 * bt)

    c = rr2 / (math.log((rng ** 2) / (1000 + rng) + 1) ** 2)

    if ls.player.target is not None and type(ls.player.target) is not Point:
        dx = ls.player.target.centerx - ls.cx
        dy = ls.player.target.centery - ls.cy
        d = math.sqrt(dx * dx + dy * dy)
        r = c * math.log((d * d) / (1000 + d) + 1) ** 2
        if r < rr2:
            angle = math.atan2(dy, dx)
            X = rr + r * math.cos(angle) + 3
            Y = rr + r * math.sin(angle) + 3
            pygame.draw.circle(HUD, (255, 255, 0), (X, Y), 5)

    for roid in gs(Asteroid):
        dx = roid.centerx - ls.cx
        dy = roid.centery - ls.cy
        d = math.sqrt(dx * dx + dy * dy)
        r = c * math.log((d * d) / (1000 + d) + 1) ** 2
        if r < rr2:
            angle = math.atan2(dy, dx)
            X = rr + r * math.cos(angle) + 3
            Y = rr + r * math.sin(angle) + 3
            pygame.draw.circle(HUD, (255, 255, 255), (X, Y), 4)

    for ship in gs(Ship):
        if ship.is_visible:  # only show uncloaked ships on radar
            if ship.faction_name == ls.player.faction_name:
                my_color = GREEN
            else:
                my_color = RED
            dx = ship.centerx - ls.cx
            dy = ship.centery - ls.cy
            d = math.sqrt(dx * dx + dy * dy)
            r = c * math.log((d * d) / (1000 + d) + 1) ** 2
            if r < rr2:
                angle = math.atan2(dy, dx)
                X = rr + r * math.cos(angle) + 3
                Y = rr + r * math.sin(angle) + 3
                pygame.draw.circle(HUD, my_color, (X, Y), 3)

    for station in gs(Base):
        if station.faction_name == ls.player.faction_name:
            my_color = GREEN
        else:
            my_color = RED
        dx = station.centerx - ls.cx
        dy = station.centery - ls.cy
        d = math.sqrt(dx * dx + dy * dy)
        r = c * math.log((d * d) / (1000 + d) + 1) ** 2
        if r < rr2:
            angle = math.atan2(dy, dx)
            X = rr + r * math.cos(angle) + 3
            Y = rr + r * math.sin(angle) + 3
            radarRect = pygame.Rect(X - 5, Y - 5, 10, 10)
            pygame.draw.rect(HUD, my_color, radarRect)
            # pygame.draw.circle(HUD, YELLOW, (X, Y), 4)

    for missile in gs(Missile):
        if missile.faction_name == ls.player.faction_name:
            my_color = GREEN
        else:
            my_color = RED
        dx = missile.centerx - ls.cx
        dy = missile.centery - ls.cy
        d = math.sqrt(dx * dx + dy * dy)
        r = c * math.log((d * d) / (1000 + d) + 1) ** 2
        if r < rr2:
            angle = math.atan2(dy, dx)
            X = rr + r * math.cos(angle) + 3
            Y = rr + r * math.sin(angle) + 3
            pygame.draw.circle(HUD, my_color, (X, Y), 1)

    ls.WIN.blit(HUD, (0, 0))


def draw_textbox(gs, ls, keys_pressed, fps):
    if keys_pressed[pygame.K_ESCAPE]:
        ls.misc_info['command prompt'] = False
        ls.misc_info['command text'] = ''

    if ls.misc_info['command prompt']:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    ls.misc_info['command text'] = ls.misc_info['command text'][:-1]
                elif event.key == pygame.K_RETURN:
                    if len(ls.misc_info['command text']) > 0:
                        ls.misc_info['command history'].append(ls.misc_info['command text'])
                        if len(ls.misc_info['command history']) > 30:
                            ls.misc_info['command history'] = ls.misc_info['command history'][-30:]
                        unpack_str(ls.misc_info['command text'], gs, ls.player)
                    ls.misc_info['command text'] = ''
                elif event.key == pygame.K_TAB:
                    if len(ls.misc_info['command text']) > 0:
                        complete_str(ls.misc_info['command text'], ls, ls.player)
                elif event.unicode.isprintable() and len(ls.misc_info['command text']) < 40:
                    ls.misc_info['command text'] += event.unicode

        text = ls.misc_info['command text']
        text_surface = ls.fonts[2].render(text, True, (255, 255, 255))
        tw = text_surface.get_width()
        th = text_surface.get_height()
        sw = 300
        sh = th * (len(ls.misc_info['command history']) + 1) + 10
        surf = pygame.Surface((sw, sh))
        for i in range(len(ls.misc_info['command history'])):
            txt = ls.misc_info['command history'][i]
            txt_surface = ls.fonts[2].render(txt, True, (200, 200, 200))
            surf.blit(txt_surface, (5, 5 + i * th))
        surf.blit(text_surface, (5, sh - th - 5))
        surf.set_alpha(100)
        ls.WIN.blit(surf, (ls.width - sw, ls.height - sh))
    else:
        pygame.event.clear()

    if keys_pressed[pygame.K_TAB]:
        ls.misc_info['command prompt'] = True
