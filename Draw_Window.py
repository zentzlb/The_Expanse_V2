import pygame
import os
import math
import time
from Misc import TargetingComputer
from Menus import StationMenu
from Ship_Class import Ship, Asteroid


def draw_window(WIN, HUD, SPACE, DUST, FIELD, global_state, fps, HEIGHT, WIDTH):

    keys_pressed = pygame.key.get_pressed()

    HUD.fill((0, 0, 0, 0))
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

    # t1 =time.time()
    WIN.blit(SPACE, (0, 0))  # draw background
    # t2 = time.time()
    # print(f"ship subroutine: {t2 - t1}")

    # print([global_state.x % 2000, global_state.y % 2000])


    WIN.blit(DUST, (-2000 - global_state.x % 2000, -2000 - global_state.y % 2000))  # draw foreground
    WIN.blit(FIELD, (-2000 - (global_state.x / 5) % 2000, -2000 - (global_state.y / 5) % 2000))  # draw foreground


    # MISSILE_IMAGE = pygame.image.load(os.path.join('Assets', 'smallmissile1.png'))  # missile
    # BULLET_IMAGE = pygame.image.load(os.path.join('Assets', 'bullet.png'))  # bullet

    # WIN.fill(COLOR)  # fill window with color
    # pygame.draw.rect(WIN, BLACK, BORDER)

    # if len(red_ships) > 0:
    #     red_health_text = FONT.render(f"Health: {red_ships[0].health} Energy: {red_ships[0].energy}", 1, RED)
    # else:
    #     red_health_text = FONT.render(f"ALL SHIPS DESTROYED", 1, RED)
    #
    # if len(yellow_ships) > 0:
    #     yellow_health_text = FONT.render(f"Health: {yellow_ships[0].health} Energy: {yellow_ships[0].energy}", 1, YELLOW)
    # else:
    #     yellow_health_text = FONT.render(f"ALL SHIPS DESTROYED", 1, YELLOW)

    # WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))  # display red health
    # WIN.blit(yellow_health_text, (yellow_health_text.get_width() - 10, 10))  # display yellow health
    if keys_pressed[pygame.K_PERIOD]:
        global_state.show_bars = True
    elif keys_pressed[pygame.K_COMMA]:
        global_state.show_bars = False
    t1 = time.time()
    for roid in global_state.asteroids:
        if (roid.cx - global_state.x > WIDTH or roid.cx - global_state.x + roid.width * 1.5 > 0) and (
                roid.cy - global_state.y > HEIGHT or roid.cy - global_state.y + roid.height * 1.5 > 0):
            # ROID = pygame.transform.rotate(roid.image, roid.angle)
            # pygame.draw.rect(WIN, GREEN, roid)
            WIN.blit(roid.image, (roid.cx - global_state.x, roid.cy - global_state.y))
    # t2 = time.time()
    # print()
    # print(t2-t1)
    # print()

    for i in range(len(global_state.particle_list)-1, -1, -1):
        p = global_state.particle_list[i]
        p.update()
        pygame.draw.circle(WIN, p.color, (p.x - global_state.x, p.y - global_state.y), p.radius)
        if p.radius <= 0:
            global_state.particle_list.remove(p)


    for faction in range(len(global_state.ships)):

        for station in global_state.stations[faction]:
            if (station.cx - global_state.x > WIDTH or station.cx - global_state.x + station.width * 1.5 > 0) and (station.cy - global_state.y > HEIGHT or station.cy - global_state.y + station.height * 1.5 > 0):
                WIN.blit(station.image, (station.cx - global_state.x, station.cy - global_state.y))
                for turret in station.turrets:
                    TURRET = pygame.transform.rotate(turret.image, turret.angle)
                    WIN.blit(TURRET, (turret.cx - global_state.x, turret.cy - global_state.y))

        for ship in global_state.ships[faction]:
            if ship.sop > 0:
                ship.sop -= 0.5
                if ship.sop > 50:
                    ship.sop = 50
            if ship.health > 0 and (ship.cx - global_state.x > WIDTH or ship.cx - global_state.x + ship.width * 1.5 > 0) and (ship.cy - global_state.y > HEIGHT or ship.cy - global_state.y + ship.height * 1.5 > 0):
                if ship.forward:
                    SHIP = pygame.transform.rotate(ship.imagef, ship.angle)  # display with thrusters active
                else:
                    SHIP = pygame.transform.rotate(ship.image, ship.angle)  # display without thrusters
                # pygame.draw.rect(WIN, GREEN, yellow)
                WIN.blit(SHIP, (ship.cx - global_state.x, ship.cy - global_state.y))
                sop = ship.sop
                pygame.draw.circle(HUD, (0, 0, 255, round(sop)), (ship.centerx - global_state.x, ship.centery - global_state.y), ship.width // 2)

                for turret in ship.turrets:
                    TURRET = pygame.transform.rotate(turret.image, turret.angle)
                    WIN.blit(TURRET, (turret.cx - global_state.x, turret.cy - global_state.y))

                if not ship.is_player and global_state.show_bars:  # ship is not player controlled
                    """HEALTH BAR"""
                    pygame.draw.line(WIN, GREEN, (ship.x - global_state.x, ship.y - global_state.y - 5), (
                    ship.x + 100 * ship.health / ship.ship_type.energy - global_state.x, ship.y - global_state.y - 5), bt)

                    """ENERGY BAR"""
                    pygame.draw.line(WIN, BLUE, (ship.x - global_state.x, ship.y - bt - global_state.y - 5), (ship.x + 100 * ship.energy / ship.ship_type.energy - global_state.x, ship.y - bt - global_state.y - 5), bt)

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
                    # pygame.draw.line(HUD, SILVER, box_tl, box_tr, 3)  # top line
                    # pygame.draw.line(HUD, SILVER, box_tl, box_bl, 3)  # left line
                    # pygame.draw.line(HUD, SILVER, box_tr, box_br, 3)  # right line
                    # pygame.draw.line(HUD, SILVER, box_bl, box_br, 3)  # bottom line

                    """DRAW HEALTH AND ENERGY BARS"""
                    pygame.draw.line(HUD, (0, 255, 0, 60), (bt, 2 * rr + hbh), (bt + 2 * rr * ship.health / ship.ship_type.health, 2 * rr + hbh), hbh)
                    pygame.draw.line(HUD, (80, 100, 255, 60), (bt, 2 * rr + 2 * hbh + bt), (bt + 2 * rr * ship.energy / ship.ship_type.energy, 2 * rr + 2 * hbh + bt), hbh)
                    pygame.draw.line(HUD, SILVER, (0, 2 * rr + hbh / 2), (bt + 2 * rr + bt, 2 * rr + hbh / 2), bt)
                    pygame.draw.line(HUD, SILVER, (0, 2 * rr + bt * hbh / 2 + 2), (bt + 2 * rr + bt, 2 * rr + bt * hbh / 2 + 2), bt)
                    pygame.draw.line(HUD, SILVER, (0, 2 * rr + 5 * hbh / 2 + 5), (bt + 2 * rr + bt, 2 * rr + 5 * hbh / 2 + 5), bt)
                    pygame.draw.line(HUD, SILVER, (1, 2 * rr + hbh / 2), (1, 2 * rr + 5 * hbh / 2 + 5), bt)
                    pygame.draw.line(HUD, SILVER, (bt + 2 * rr + 2, 2 * rr + hbh / 2), (bt + 2 * rr + 2, 2 * rr + 5 * hbh / 2 + 5), bt)

                    """DRAW TARGET WINDOW"""
                    box_tl = (0, 2 * rr + 5 * hbh / 2 + 5)
                    length = 2 * rr + 7
                    rect1 = pygame.Rect(box_tl[0], box_tl[1], length, length)
                    rect2 = pygame.Rect(box_tl[0], box_tl[1]+length-bt, length, length)
                    center = rect1.center


                    health_text = global_state.fonts[0].render(f"{fps} Shields: {100 * ship.health / ship.ship_type.health:0.0f}%", 1, YELLOW)
                    energy_text = global_state.fonts[0].render(f"Energy: {100 * ship.energy / ship.ship_type.energy:0.0f}%", 1, YELLOW)

                    HUD.blit(health_text, (7, 2 * rr + hbh / 2))  # display health
                    HUD.blit(energy_text, (7, 2 * rr + 3 * hbh / 2 + bt))  # display energy

                    if type(ship.target) is Ship and ship.target.health > 0:
                        MyAngle = TargetingComputer(ship)
                        # print([90 - MyAngle * 180 / math.pi, yellow.angle, MyAngle * 180 / math.pi - yellow.angle])
                        if abs(90 - MyAngle * 180 / math.pi - ship.angle) < ship.av:
                            MyColor = GREEN
                        else:
                            MyColor = RED
                        pygame.draw.line(WIN, MyColor, (round(ship.centerx - global_state.x + 25 * math.cos(MyAngle)), round(ship.centery - global_state.y + 25 * math.sin(MyAngle))), (round(ship.centerx - global_state.x + 50 * math.cos(MyAngle)), round(ship.centery - global_state.y + 50 * math.sin(MyAngle))), bt)

                        """DRAW TARGET"""

                        dx = ship.target.cx - ship.cx
                        dy = ship.target.cy - ship.cy

                        # target_rect = pygame.Rect(box_tl[0] + 2, box_tl[1] + 2, box_tr[0] - box_tl[0] - 3, box_bl[1] - box_tl[1] - 3)
                        pygame.draw.rect(HUD, (255, 0, 0, 15), rect1)

                        SHIP = pygame.transform.rotate(ship.target.image, ship.target.angle)
                        adjust_x = (ship.target.width - ship.target.height * abs(math.sin(ship.target.angle * math.pi / 180)) - ship.target.width * abs(math.cos(ship.target.angle * math.pi / 180))) / 2
                        adjust_y = (ship.target.height - ship.target.width * abs(math.sin(ship.target.angle * math.pi / 180)) - ship.target.height * abs(math.cos(ship.target.angle * math.pi / 180))) / 2
                        HUD.blit(SHIP, (center[0] - ship.target.width // 2 + adjust_x, center[1] - ship.target.height // 2 + adjust_y))
                        health_text = global_state.fonts[2].render(f"Shields: {100 * ship.target.health / ship.target.ship_type.health:0.0f}%", True, SILVER)
                        energy_text = global_state.fonts[2].render(
                            f"Energy: {100 * ship.target.energy / ship.target.ship_type.energy:0.0f}%", True, SILVER)
                        range_text = global_state.fonts[2].render(
                            f"Range: {math.sqrt(dx * dx + dy * dy):0.0f}", True, SILVER)
                        HUD.blit(health_text, (7, box_tl[1] + 1))
                        HUD.blit(energy_text, (7, box_tl[1] + 1 + global_state.fonts[2].get_height()))
                        HUD.blit(range_text, (7, box_tl[1] + 1 + 2 * global_state.fonts[2].get_height()))
                    elif type(ship.target) is Asteroid:
                        """DRAW TARGET"""

                        # target_rect = pygame.Rect(box_tl[0] + 2, box_tl[1] + 2, box_tr[0] - box_tl[0] - 3, box_bl[1] - box_tl[1] - 3)
                        pygame.draw.rect(HUD, (255, 255, 255, 15), rect1)

                        # ROID = pygame.transform.scale(ship.target.image, (1000, 1000))
                        adjust_x = (ship.target.width - ship.target.height * abs(
                            math.sin(ship.target.angle * math.pi / 180)) - ship.target.width * abs(
                            math.cos(ship.target.angle * math.pi / 180))) / 2
                        adjust_y = (ship.target.height - ship.target.width * abs(
                            math.sin(ship.target.angle * math.pi / 180)) - ship.target.height * abs(
                            math.cos(ship.target.angle * math.pi / 180))) / 2
                        HUD.blit(ship.target.image_scaled, (center[0] - 50, center[1] - 50))
                        for i in range(len(ship.target.ore_types)):
                            ore_text = global_state.fonts[2].render(f"{ship.target.ore_types[i]}: {ship.target.ore[ship.target.ore_types[i]]}", True, SILVER)
                            HUD.blit(ore_text, (7, box_tl[1] + 1 + i * global_state.fonts[2].get_height()))
                        # health_text = global_state.fonts[2].render(ship.target.ore_types[i]
                        #     f"Shields: {100 * ship.target.health / ship.target.ship_type.health:0.0f}%", True, SILVER)
                        # energy_text = global_state.fonts[2].render(
                        #     f"Energy: {100 * ship.target.energy / ship.target.ship_type.energy:0.0f}%", True, SILVER)
                        # HUD.blit(health_text, (7, box_tl[1] + 1))
                        # HUD.blit(energy_text, (7, box_tl[1] + 1 + global_state.fonts[2].get_height()))
                    pygame.draw.rect(HUD, SILVER, rect1, bt)

                    if keys_pressed[pygame.K_p]:
                        quad = global_state.size
                        Length = length - 2 * bt
                        x = rect2.x + bt
                        y = rect2.y + bt
                        pygame.draw.rect(HUD, (30, 70, 100, 100), rect2)

                        X = round(ship.centerx * (Length / quad) + x)
                        Y = round(ship.centery * (Length / quad) + y)
                        pygame.draw.circle(HUD, (0, 255, 0), (X, Y), 2)
                        for roid in global_state.asteroids:
                            X = round(roid.centerx * (Length / quad) + x)
                            Y = round(roid.centery * (Length / quad) + y)
                            pygame.draw.circle(HUD, (255, 255, 255), (X, Y), 2)
                        for station in global_state.stations[0]:
                            X = round(station.centerx * (Length / quad) + x)
                            Y = round(station.centery * (Length / quad) + y)
                            # pygame.draw.circle(hud, (255, 255, 0), (X, Y), 4)
                            radarRect = pygame.Rect(X - 2, Y - 2, 4, 4)
                            pygame.draw.rect(HUD, (255, 255, 0), radarRect)
                        for station in global_state.stations[1]:
                            X = round(station.centerx * (Length / quad) + x)
                            Y = round(station.centery * (Length / quad) + y)
                            # pygame.draw.circle(hud, (255, 255, 0), (X, Y), 4)
                            radarRect = pygame.Rect(X - 2, Y - 2, 4, 4)
                            pygame.draw.rect(HUD, (255, 0, 0), radarRect)
                    else:
                        th = global_state.fonts[2].get_height()
                        c = 0

                        for i in range(len(ship.bullet_types)):
                            if i == ship.bullet_sel:
                                COLOR = YELLOW
                            else:
                                COLOR = SILVER
                            text = global_state.fonts[2].render(f"{c+1}. {ship.bullet_types[i].name}", True, COLOR)
                            HUD.blit(text, (7, rect2.y + 4 + c * th))
                            c += 1
                        for i in range(len(ship.missile_types)):
                            if i == ship.missile_sel:
                                COLOR = YELLOW
                            else:
                                COLOR = SILVER
                            text = global_state.fonts[2].render(f"{c+1}. {ship.missile_types[i].name}", True, COLOR)
                            HUD.blit(text, (7, rect2.y + 4 + c * th))
                            c += 1

                        # for i in range(len(global_state.stations[0][0].docked_ships)):
                        #     text = global_state.fonts[2].render(f"{global_state.stations[0][0].docked_ships[i].ship_type.name}", True, SILVER)
                        #     HUD.blit(text, (7, rect2.y + 4 + i * th))


                        # primary_text = global_state.fonts[2].render(
                        #     f"Primary: {ship.bullet_types[ship.bullet_sel].name}", True, SILVER)
                        # secondary_text = global_state.fonts[2].render(
                        #     f"Secondary: {ship.missile_types[ship.missile_sel].name}", True, SILVER)
                        # cargo_text = global_state.fonts[2].render(
                        #     f"Cargo: {ship.cargo_total}", True, SILVER)
                        # HUD.blit(primary_text, (7, rect2.y + 4))
                        # HUD.blit(secondary_text, (7, rect2.y + 4 + global_state.fonts[2].get_height()))
                        # HUD.blit(cargo_text, (7, rect2.y + 4 + 2 * global_state.fonts[2].get_height()))


                    pygame.draw.rect(HUD, SILVER, rect2, bt)

                    rng = ship.ship_type.range


        """DISPLAY BULLETS AND MISSILES"""
        for bullet in global_state.bullets[faction]:
            if (bullet.x - global_state.x > WIDTH or bullet.x - global_state.x + bullet.width > 0) and (bullet.y - global_state.y > HEIGHT or bullet.y - global_state.y + bullet.height > 0):
                WIN.blit(bullet.image, (bullet.x - global_state.x, bullet.y - global_state.y))
        for missile in global_state.missiles[faction]:
            if (missile.x - global_state.x > WIDTH or missile.x - global_state.x + missile.width > 0) and (missile.y - global_state.y > HEIGHT or missile.y - global_state.y + missile.height > 0):
                MISSILE = pygame.transform.rotate(missile.image, missile.angle)
                WIN.blit(MISSILE, (missile.x - global_state.x, missile.y - global_state.y))

    # for i in global_state.particle_list:
    #     i.update()
    #     pygame.draw.circle(WIN, i.color, (i.x - global_state.x, i.y - global_state.y), i.radius)
    #
    # for i in global_state.particle_list:
    #     if i.radius <= 0:
    #         global_state.particle_list.remove(i)


    global_state.explosion_group.draw(WIN)

    for i in range(len(global_state.particle_list2)-1, -1, -1):
        p = global_state.particle_list2[i]
        p.update()
        pygame.draw.circle(WIN, p.color, (p.x - global_state.x, p.y - global_state.y), p.radius)
        if p.radius <= 0:
            global_state.particle_list2.remove(p)

    """RADAR"""
    if global_state.menu is None and rng != 0:
        pygame.draw.circle(HUD, (0, 0, 255, 50), (rr + bt, rr + bt), rr)
        pygame.draw.circle(HUD, (0, 150, 255, 75), (rr + bt, rr + bt), 50 * time.time() % rr, width=bt)
        pygame.draw.circle(HUD, (200, 200, 255), (rr + bt, rr + bt), rr + bt, width=bt)
        # WIN.blit(HUD, (0, 0))
        pygame.draw.circle(HUD, GREEN, (rr + 3, rr + 3), 6)

        rr2 = (rr - 2 * bt)

        c = rr2 / (math.log((rng ** 2) / (1000 + rng) + 1) ** 2)

        for faction in range(len(global_state.ships)):
            if faction == 0:
                MyColor = YELLOW
            else:
                MyColor = RED
            for ship in global_state.ships[faction]:
                if ship.is_visible:  # only show uncloaked ships on radar
                    dx = ship.centerx - global_state.cx
                    dy = ship.centery - global_state.cy
                    d = math.sqrt(dx ** 2 + dy ** 2)
                    r = c * math.log((d ** 2) / (1000 + d) + 1) ** 2
                    if r < rr2:
                        angle = math.atan2(dy, dx)
                        X = rr + r * math.cos(angle) + 3
                        Y = rr + r * math.sin(angle) + 3
                        pygame.draw.circle(HUD, MyColor, (X, Y), 3)

            for station in global_state.stations[faction]:
                dx = station.centerx - global_state.cx
                dy = station.centery - global_state.cy
                d = math.sqrt(dx ** 2 + dy ** 2)
                r = c * math.log((d ** 2) / (1000 + d) + 1) ** 2
                if r < rr2:
                    angle = math.atan2(dy, dx)
                    X = rr + r * math.cos(angle) + 3
                    Y = rr + r * math.sin(angle) + 3
                    radarRect = pygame.Rect(X - 5, Y - 5, 10, 10)
                    pygame.draw.rect(HUD, MyColor, radarRect)
                    # pygame.draw.circle(WIN, YELLOW, (X, Y), 4)

            for missile in global_state.missiles[faction]:
                dx = missile.centerx - global_state.cx
                dy = missile.centery - global_state.cy
                d = math.sqrt(dx ** 2 + dy ** 2)
                r = c * math.log((d ** 2) / (1000 + d) + 1) ** 2
                if r < rr2:
                    angle = math.atan2(dy, dx)
                    X = rr + r * math.cos(angle) + 3
                    Y = rr + r * math.sin(angle) + 3
                    pygame.draw.circle(HUD, MyColor, (X, Y), 1)

        for roid in global_state.asteroids:
            dx = roid.centerx - global_state.cx
            dy = roid.centery - global_state.cy
            d = math.sqrt(dx ** 2 + dy ** 2)
            r = c * math.log((d ** 2) / (1000 + d) + 1) ** 2
            if r < rr2:
                angle = math.atan2(dy, dx)
                X = rr + r * math.cos(angle) + 3
                Y = rr + r * math.sin(angle) + 3
                pygame.draw.circle(HUD, (255, 255, 255), (X, Y), 4)


    elif global_state.menu is not None:

        global_state.menu.draw_menu(HUD, global_state)




    WIN.blit(HUD, (0, 0))

    pygame.display.update()  # update window
