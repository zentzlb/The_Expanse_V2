import pygame
import os
from Misc import check_purchase, purchase


class Menu:

    def __init__(self, options):
        self.keys_pressed = pygame.key.get_pressed()
        self.mouse_pressed = pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.counter = 0
        self.button_rects = []
        self.option_list = options
        self.selected = 0
        self.hover = -1
        self.ship = None
        # self.description = description

    def draw_button(self, text, font, color, surface, center_x, center_y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (center_x - (textobj.get_width() // 2), center_y - (textobj.get_height() // 2))
        surface.blit(textobj, textrect)

    def draw_icon_button(self, menu, text, font, color, surface, center_x, center_y):
        button = pygame.Surface((280, 190))
        button_rect = button.get_rect()
        button_rect.topleft = (center_x - 140, center_y - 95)
        image = pygame.image.load(os.path.join('Assets', f'{menu}_Icon.png'))
        button.blit(image, (0, 0))  # draws the icon onto the button surface at the top left of the button
        text_surface = font.render(text, 1, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (140 - (text_surface.get_width() // 2), 165 - (text_surface.get_height() // 2))
        if len(self.button_rects) < len(self.option_list):
            self.button_rects.append(button_rect)
        button.blit(text_surface, text_rect)
        surface.blit(button, button_rect)

    def draw_menu(self, hud, gs):
        keys_pressed = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()
        edge = 50
        menuRect = pygame.Rect(edge, edge, gs.width-edge*2, gs.height-edge*2)
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)

        for i in range(len(gs.docked.docked_ships)):
            if gs.docked.docked_ships[i].is_player:
                self.ship = gs.docked.docked_ships[i]

        if keys_pressed[pygame.K_ESCAPE] and not self.keys_pressed[pygame.K_ESCAPE]:
            self.ship.refresh(gs)
            gs.ships[0].append(self.ship)
            gs.docked.docked_ships.remove(self.ship)
            gs.docked = None
            gs.menu = None

        if mouse_pressed[0] and not self.mouse_pressed[0]:
            mouse_pos = pygame.mouse.get_pos()

            for i in range(len(self.button_rects)):
                if self.button_rects[i].collidepoint(mouse_pos):
                    self.selected = i
                    if self.selected == 0:
                        gs.menu = MapMenu()
                    elif self.selected == 1:
                        gs.menu = WorkshopMenu()
                    elif self.selected == 2:
                        gs.menu = CargoMenu()
                    elif self.selected == 3:
                        gs.menu = TavernMenu()

        self.keys_pressed = keys_pressed
        self.mouse_pressed = mouse_pressed

        self.draw_button("Main Menu", gs.fonts[0], (255, 255, 255), hud, 50 + menuRect.width / 2, 100)
        self.draw_button("Press Esc to Launch", gs.fonts[0], (255, 255, 255), hud,
                         50 + menuRect.width / 2, menuRect.height - 50)

        for i in range(len(self.option_list)):
            color = (255, 255, 255)

            self.draw_icon_button(f'{self.option_list[i]}Menu', self.option_list[i], gs.fonts[0], color, hud,
                                  50 + (menuRect.width / 2) + ((-1 + (2 * (i % 2))) * 300), 200 + (300 * int(i / 2)))

        mouse_pos = pygame.mouse.get_pos()

        for i in range(len(self.button_rects)):
            if self.button_rects[i].collidepoint(mouse_pos):
                hover = i
                if self.hover == hover:
                    self.counter += 1
                    if self.counter >= 15:
                        if hover == 0:
                            menu_choice = MapMenu()
                        elif hover == 1:
                            menu_choice = WorkshopMenu()
                        elif hover == 2:
                            menu_choice = CargoMenu()
                        elif hover == 3:
                            menu_choice = TavernMenu()
                        self.draw_button(menu_choice.description, gs.fonts[0], (255, 255, 255), hud,
                                         pygame.mouse.get_pos()[0] + 75,
                                         pygame.mouse.get_pos()[1] + 25)
                else:
                    self.counter = 0
                    self.hover = hover


class StationMenu:

    def __init__(self):
        self.keys_pressed = pygame.key.get_pressed()
        self.mouse_pressed = pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.counter = 0
        self.button_rects = []
        self.option_list = ['Map', 'Workshop', 'Fleet', 'Tavern']
        self.selected = 0
        self.hover = -1
        self.ship = None
        self.description = "Return to the Main Menu"

    def draw_menu(self, hud, gs):
        keys_pressed = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()
        edge = 50
        menuRect = pygame.Rect(edge, edge, gs.width-edge*2, gs.height-edge*2)
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)

        for i in range(len(gs.docked.docked_ships)):
            if gs.docked.docked_ships[i].is_player:
                self.ship = gs.docked.docked_ships[i]

        if keys_pressed[pygame.K_ESCAPE] and not self.keys_pressed[pygame.K_ESCAPE]:
            self.ship.refresh(gs)
            gs.ships[0].append(self.ship)
            gs.docked.docked_ships.remove(self.ship)
            gs.docked = None
            gs.menu = None

        if mouse_pressed[0] and not self.mouse_pressed[0]:
            mouse_pos = pygame.mouse.get_pos()

            for i in range(len(self.button_rects)):
                if self.button_rects[i].collidepoint(mouse_pos):
                    self.selected = i
                    if self.selected == 0:
                        gs.menu = MapMenu()
                    elif self.selected == 1:
                        gs.menu = WorkshopMenu()
                    elif self.selected == 2:
                        gs.menu = CargoMenu()
                    elif self.selected == 3:
                        gs.menu = TavernMenu()

        self.keys_pressed = keys_pressed
        self.mouse_pressed = mouse_pressed

        self.draw_button("Main Menu", gs.fonts[0], (255, 255, 255), hud, 50 + menuRect.width / 2, 100)
        self.draw_button("Press Esc to Launch", gs.fonts[0], (255, 255, 255), hud,
                         50 + menuRect.width / 2, menuRect.height - 50)

        for i in range(len(self.option_list)):
            color = (255, 255, 255)

            self.draw_icon_button(f'{self.option_list[i]}Menu', self.option_list[i], gs.fonts[0], color, hud,
                                  50 + (menuRect.width / 2) + ((-1 + (2 * (i % 2))) * 300), 200 + (300 * int(i / 2)))

        mouse_pos = pygame.mouse.get_pos()

        for i in range(len(self.button_rects)):
            if self.button_rects[i].collidepoint(mouse_pos):
                hover = i
                if self.hover == hover:
                    self.counter += 1
                    if self.counter >= 150:
                        if hover == 0:
                            menu_choice = MapMenu()
                        elif hover == 1:
                            menu_choice = WorkshopMenu()
                        elif hover == 2:
                            menu_choice = CargoMenu()
                        elif hover == 3:
                            menu_choice = TavernMenu()
                        self.draw_button(menu_choice.description, gs.fonts[0], (255, 255, 255), hud,
                                         pygame.mouse.get_pos()[0] + 75,
                                         pygame.mouse.get_pos()[1] + 25)
                else:
                    self.counter = 0
                    self.hover = hover

    def draw_button(self, text, font, color, surface, center_x, center_y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (center_x - (textobj.get_width() / 2), center_y - (textobj.get_height() / 2))
        surface.blit(textobj, textrect)

    def draw_icon_button(self, menu, text, font, color, surface, center_x, center_y):
        button = pygame.Surface((280, 190))
        button_rect = button.get_rect()
        button_rect.topleft = (center_x - 140, center_y - 95)
        image = pygame.image.load(os.path.join('Assets', f'{menu}_Icon.png'))
        button.blit(image, (0, 0))  # draws the icon onto the button surface at the top left of the button
        text_surface = font.render(text, 1, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = (140 - (text_surface.get_width() / 2), 165 - (text_surface.get_height() / 2))
        if len(self.button_rects) < len(self.option_list):
            self.button_rects.append(button_rect)
        button.blit(text_surface, text_rect)
        surface.blit(button, button_rect)


"""MAP MENU"""


class MapMenu:

    def __init__(self):
        self.keys_pressed = pygame.key.get_pressed()
        self.mouse_pressed = pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.button_rects = []
        self.option_list = ['Back']
        self.selected = 0
        self.description = "View Galaxy Map"
        # self.launch_button = self.draw_button('Launch Ship', font, (255, 255, 0), hud, 100, 100)

    def draw_menu(self, hud, gs):
        # keys_pressed = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()
        edge = 50
        edge2 = 150

        H = gs.height - edge2 * 2
        W = H  # gs.width - edge2 * 2

        quad = gs.size

        menuRect = pygame.Rect(edge, edge, gs.width-edge*2, gs.height-edge*2)
        mapRect = pygame.Rect(gs.width // 2 - W // 2, gs.height // 2 - H // 2, W, H)
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)
        pygame.draw.rect(hud, (30, 70, 100, 255), mapRect)

        if mouse_pressed[0] and not self.mouse_pressed[0]:
            mouse_pos = pygame.mouse.get_pos()

            for i in range(len(self.button_rects)):
                if self.button_rects[i].collidepoint(mouse_pos):
                    self.selected = i
                    if self.selected == 0:
                        gs.menu = StationMenu()

        # if keys_pressed[pygame.K_DOWN] and not self.keys_pressed[pygame.K_DOWN]:
        #     self.selected += 1
        #     if self.selected >= len(self.option_list):
        #         self.selected = 0
        # elif keys_pressed[pygame.K_UP] and not self.keys_pressed[pygame.K_UP]:
        #     self.selected -= 1
        #     if self.selected < 0:
        #         self.selected = len(self.option_list) - 1
        # if keys_pressed[pygame.K_RETURN] and not self.keys_pressed[pygame.K_RETURN]:
        #     if self.selected == 0:
        #         gs.menu = StationMenu()
        #         gs.menu.selected = gs.menu.option_list.index('View Map')


        # self.keys_pressed = keys_pressed
        self.mouse_pressed = mouse_pressed

        for i in range(len(self.option_list)):
            if i == self.selected:
                color = (255, 255, 100)
            else:
                color = (255, 255, 255)
            self.draw_button(self.option_list[i], gs.fonts[0], color, hud, 100, 100 * (i + 1))
        # pygame.draw.circle(hud, (255, 0, 0), (500, 500), 4)
        for ship in gs.ships[0]:
            if ship.is_visible:  # only show enemy ships on station map if they're visible

                # dx = ship.centerx - gs.cx
                # dy = ship.centery - gs.cy
                # X = dx // 100 + gs.width // 2
                # Y = dy // 100 + gs.height // 2
                # pygame.draw.circle(hud, (255, 255, 0), (X, Y), 4)

                X = round(ship.centerx * (W / quad) + mapRect.x)
                Y = round(ship.centery * (H / quad) + mapRect.y)
                pygame.draw.circle(hud, (255, 255, 0), (X, Y), 4)

        for ship in gs.ships[1]:
            if ship.is_visible:  # only show enemy ships on station map if they're visible
                X = round(ship.centerx * (W / quad) + mapRect.x)
                Y = round(ship.centery * (H / quad) + mapRect.y)
                pygame.draw.circle(hud, (255, 0, 0), (X, Y), 4)

        for roid in gs.asteroids:
            X = round(roid.centerx * (W / quad) + mapRect.x)
            Y = round(roid.centery * (H / quad) + mapRect.y)
            pygame.draw.circle(hud, (255, 255, 255), (X, Y), 4)

        for station in gs.stations[0]:
            X = round(station.centerx * (W / quad) + mapRect.x)
            Y = round(station.centery * (H / quad) + mapRect.y)
            # pygame.draw.circle(hud, (255, 255, 0), (X, Y), 4)
            radarRect = pygame.Rect(X - 5, Y - 5, 10, 10)
            pygame.draw.rect(hud, (255, 255, 0), radarRect)

        for station in gs.stations[1]:
            X = round(station.centerx * (W / quad) + mapRect.x)
            Y = round(station.centery * (H / quad) + mapRect.y)
            radarRect = pygame.Rect(X - 5, Y - 5, 10, 10)
            pygame.draw.rect(hud, (255, 0, 0), radarRect)
        # pygame.draw.circle(WIN, YELLOW, (X, Y), 4)

    def draw_button(self, text, font, color, surface, center_x, center_y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (center_x - (textobj.get_width() / 2), center_y - (textobj.get_height() / 2))
        if len(self.button_rects) < len(self.option_list):
            self.button_rects.append(textrect)
        surface.blit(textobj, textrect)


"""WORKSHOP MENU"""


class WorkshopMenu:

    def __init__(self):
        self.mouse_pressed = pygame.mouse.get_pressed()
        self.mouse_pos = pygame.mouse.get_pos()
        self.counter = 0
        self.button_rects = []
        self.option_list = ['Main', 'Ships', 'Bullets', 'Missiles', 'Utility', 'Mines']
        self.selected = 0
        self.hover = -1
        self.ship = None
        self.description = "Buy Ships, Weapons, and Equipment"

    def draw_menu(self, hud, gs):
        mouse_pressed = pygame.mouse.get_pressed()
        edge = 50
        menuRect = pygame.Rect(edge, edge, gs.width - edge * 2, gs.height - edge * 2)
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)

        for i in range(len(gs.docked.docked_ships)):
            if gs.docked.docked_ships[i].is_player:
                self.ship = gs.docked.docked_ships[i]

        if mouse_pressed[0] and not self.mouse_pressed[0]:
            mouse_pos = pygame.mouse.get_pos()

            for i in range(len(self.button_rects)):
                if self.button_rects[i].collidepoint(mouse_pos):
                    self.selected = i
                    if self.selected == 0:
                        gs.menu = StationMenu()
                    elif self.selected == 1:
                        gs.menu = ShipMenu()
                    elif self.selected == 2:
                        gs.menu = WepMenu()
                    elif self.selected == 3:
                        gs.menu = WepMenu2()
                    elif self.selected == 4:
                        gs.menu = UtilMenu()
                    elif self.selected == 5:
                        gs.menu = MineMenu()

        self.mouse_pressed = mouse_pressed

        self.draw_button("Workshop", gs.fonts[0], (255, 255, 255), hud, 50 + menuRect.width / 2, 100)

        for i in range(len(self.option_list)):
            color = (255, 255, 255)

            self.draw_click_button(self.option_list[i], gs.fonts[0], color, hud,
                                  50 + (menuRect.width / 2) + ((-1 + (2 * (i % 2))) * 300), 200 +
                                   ((menuRect.height / len(self.option_list)) * int(i / 2)))

        mouse_pos = pygame.mouse.get_pos()

        for i in range(len(self.button_rects)):
            if self.button_rects[i].collidepoint(mouse_pos):
                hover = i
                if self.hover == hover:
                    self.counter += 1
                    if self.counter >= 15:
                        if hover == 0:
                            menu_choice = StationMenu()
                        elif hover == 1:
                            menu_choice = ShipMenu()
                        elif hover == 2:
                            menu_choice = WepMenu()
                        elif hover == 3:
                            menu_choice = WepMenu2()
                        elif hover == 4:
                            menu_choice = UtilMenu()
                        elif hover == 5:
                            menu_choice = MineMenu()
                        self.draw_button(menu_choice.description, gs.fonts[0], (255, 255, 255), hud,
                                         pygame.mouse.get_pos()[0] + 75,
                                         pygame.mouse.get_pos()[1] + 25)
                else:
                    self.counter = 0
                    self.hover = hover

    def draw_button(self, text, font, color, surface, center_x, center_y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (center_x - (textobj.get_width() / 2), center_y - (textobj.get_height() / 2))
        surface.blit(textobj, textrect)

    def draw_click_button(self, text, font, color, surface, center_x, center_y):
        button = pygame.Surface((200, 100))
        button.fill((20, 100, 200))
        button_rect = button.get_rect()
        button_rect.topleft = (center_x - 100, center_y - 50)
        text_surface = font.render(text, 1, color)
        text_rect = text_surface.get_rect()
        text_rect.topleft = ((text_surface.get_width() / 2), (text_surface.get_height() / 2))
        if len(self.button_rects) < len(self.option_list):
            self.button_rects.append(button_rect)
        button.blit(text_surface, text_rect)
        surface.blit(button, button_rect)



"""WEAPONS MENU"""


class WepMenu:

    def __init__(self):
        self.keys_pressed = pygame.key.get_pressed()
        self.option_list = []
        self.selected = 0
        self.ship = None
        self.description = "Buy Bullets"
        # self.launch_button = self.draw_button('Launch Ship', font, (255, 255, 0), hud, 100, 100)

    def draw_menu(self, hud,  gs):
        self.option_list = list(gs.BulletTypes)
        keys_pressed = pygame.key.get_pressed()
        edge = 50
        top_left = (300, 200)
        length = 100
        menuRect = pygame.Rect(edge, edge, gs.width-edge*2, gs.height-edge*2)
        outlineRect = pygame.Rect(top_left[0]-10, top_left[1]-10, length*10, gs.height-2*(top_left[1]-10))
        wepRect = pygame.Rect(top_left[0], top_left[1], length, length)
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)
        pygame.draw.rect(hud, (50, 30, 30, 255), outlineRect)
        pygame.draw.rect(hud, (20, 20, 20, 255), wepRect)

        for i in range(len(gs.docked.docked_ships)):
            if gs.docked.docked_ships[i].is_player:
                self.ship = gs.docked.docked_ships[i]

        if keys_pressed[pygame.K_DOWN] and not self.keys_pressed[pygame.K_DOWN]:
            self.selected += 1
            if self.selected >= len(self.option_list):
                self.selected = 0
        elif keys_pressed[pygame.K_UP] and not self.keys_pressed[pygame.K_UP]:
            self.selected -= 1
            if self.selected < 0:
                self.selected = len(self.option_list) - 1
        if keys_pressed[pygame.K_RETURN] and not self.keys_pressed[pygame.K_RETURN]:
            bullet = gs.BulletTypes[self.option_list[self.selected]]
            has_bullet = False  # this boolean will only be true if the ship already has that bullet type
            for i in range(len(self.ship.bullet_types)):
                if bullet.name == self.ship.bullet_types[i].name:
                    gs.menu = PopupMenu(self, "You already have that type of bullet equipped.")
                    has_bullet = True
            if has_bullet is False:
                if check_purchase(gs.docked, bullet):
                    purchase(gs.docked, bullet)
                    self.ship.bullet_type = bullet
                else:
                    gs.menu = PopupMenu(self, "You don't have enough ore to purchase this item.")
        if keys_pressed[pygame.K_ESCAPE] and not self.keys_pressed[pygame.K_ESCAPE]:
            gs.menu = StationMenu()
            # gs.menu.selected = gs.menu.option_list.index('Primary Weapon')


        self.keys_pressed = keys_pressed
        self.draw_button("Ship Cargo: ", gs.fonts[0], (255, 255, 255), hud, top_left[0] + 800, top_left[1])
        cargos = list(self.ship.cargo)
        for i in range(len(self.ship.cargo)):
            color = (255, 255, 255)
            self.draw_button(cargos[i], gs.fonts[0], color, hud, top_left[0] + 800, top_left[1] + ((1 + i) * (outlineRect.height / (len(self.ship.cargo) + 1))))
            self.draw_button(str(self.ship.cargo[cargos[i]]), gs.fonts[0], color, hud, top_left[0] + 900, top_left[1] + ((1 + i) * (outlineRect.height / (len(self.ship.cargo) + 1))))
        self.draw_button("Station Cargo: ", gs.fonts[0], (255, 255, 255), hud, top_left[0] + 500, top_left[1])
        station_cargo = list(gs.docked.cargo)
        for i in range(len(gs.docked.cargo)):
            color = (255, 255, 255)
            self.draw_button(station_cargo[i], gs.fonts[0], color, hud, top_left[0] + 500, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.cargo) + 1))))
            self.draw_button(str(gs.docked.cargo[station_cargo[i]]), gs.fonts[0], color, hud, top_left[0] + 600, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.cargo) + 1))))

        for i in range(len(self.option_list)):
            if i == self.selected:
                color = (255, 255, 100)
            else:
                color = (255, 255, 255)
            self.draw_button(self.option_list[i], gs.fonts[0], color, hud, 100, 100 * (i + 1))
        # pygame.draw.circle(hud, (255, 0, 0), (500, 500), 4)
        bullet_type = gs.BulletTypes[self.option_list[self.selected]]
        image = bullet_type.image  # pygame.transform.scale(type.image, (length - 20, length - 20))
        # imagex = top_left[0] + 10
        # imagey = top_left[1] + 10
        imagex = round(top_left[0] + length / 2 - bullet_type.width / 2)
        imagey = round(top_left[1] + length / 2 - bullet_type.height / 2)
        hud.blit(image, (imagex, imagey))

        self.draw_button("Cost:", gs.fonts[0], (255, 255, 255), hud, top_left[0], top_left[1] + 150)
        ore_names = list(bullet_type.cost)
        for i in range(len(bullet_type.cost)):
            color = (255, 255, 255)
            self.draw_button(ore_names[i], gs.fonts[0], color, hud, top_left[0],
                             top_left[1] + 150 + ((1 + i) * (outlineRect.height / (2 * (len(bullet_type.cost) + 1)))))
            self.draw_button(str(bullet_type.cost[ore_names[i]]), gs.fonts[0], color, hud, top_left[0] + 100,
                             top_left[1] + 150 + ((1 + i) * (outlineRect.height / (2 * (len(bullet_type.cost) + 1)))))

        bar_width = 20
        tranx = 75

        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 10),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 10), bar_width+4)
        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 15 + bar_width),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 15 + bar_width), bar_width+4)
        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 20 + 2 * bar_width),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 20 + 2 * bar_width), bar_width+4)

        pygame.draw.line(hud, (100, 0, 0), (top_left[0] + length + 5 + tranx, top_left[1] + 10), (top_left[0] + length + 5 + 4 * bullet_type.damage + tranx, top_left[1] + 10), bar_width)
        pygame.draw.line(hud, (0, 100, 0), (top_left[0] + length + 5 + tranx, top_left[1] + 15 + bar_width),
                         (top_left[0] + length + 5 + bullet_type.range // 50 + tranx, top_left[1] + 15 + bar_width), bar_width)
        pygame.draw.line(hud, (0, 0, 100), (top_left[0] + length + 5 + tranx, top_left[1] + 20 + 2 * bar_width),
                         (top_left[0] + length + 5 + 5000 // bullet_type.delay + tranx, top_left[1] + 20 + 2 * bar_width), bar_width)
        if True:  # keys_pressed[pygame.K_i]:
            damage_text = gs.fonts[1].render(f"DAMAGE", 1, (255, 255, 0))
            range_text = gs.fonts[1].render(f"RANGE", 1, (255, 255, 0))
            ROF_text = gs.fonts[1].render(f"RoF", 1, (255, 255, 0))
            hud.blit(damage_text, (top_left[0] + length + tranx - gs.fonts[1].size('DAMAGE')[0], top_left[1] - 1))
            hud.blit(range_text, (top_left[0] + length + tranx - gs.fonts[1].size('RANGE')[0], top_left[1] + 5 + bar_width - 1))
            hud.blit(ROF_text, (top_left[0] + length + tranx - gs.fonts[1].size('RoF')[0], top_left[1] + 2 * (5 + bar_width) - 1))

        # pygame.draw.circle(WIN, YELLOW, (X, Y), 4)


    def draw_button(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)

class WepMenu2:

    def __init__(self):
        self.keys_pressed = pygame.key.get_pressed()
        self.option_list = []
        self.selected = 0
        self.ship = None
        self.description = "Buy Missiles"
        # self.launch_button = self.draw_button('Launch Ship', font, (255, 255, 0), hud, 100, 100)

    def draw_menu(self, hud, gs):
        self.option_list = list(gs.MissileTypes)
        keys_pressed = pygame.key.get_pressed()
        edge = 50
        top_left = (300, 200)
        length = 100
        menuRect = pygame.Rect(edge, edge, gs.width-edge*2, gs.height-edge*2)
        outlineRect = pygame.Rect(top_left[0]-10, top_left[1]-10, length*10, gs.height-2*(top_left[1]-10))
        wepRect = pygame.Rect(top_left[0], top_left[1], length, length)
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)
        pygame.draw.rect(hud, (50, 30, 30, 255), outlineRect)
        pygame.draw.rect(hud, (20, 20, 20, 255), wepRect)

        for i in range(len(gs.docked.docked_ships)):
            if gs.docked.docked_ships[i].is_player:
                self.ship = gs.docked.docked_ships[i]

        if keys_pressed[pygame.K_DOWN] and not self.keys_pressed[pygame.K_DOWN]:
            self.selected += 1
            if self.selected >= len(self.option_list):
                self.selected = 0
        elif keys_pressed[pygame.K_UP] and not self.keys_pressed[pygame.K_UP]:
            self.selected -= 1
            if self.selected < 0:
                self.selected = len(self.option_list) - 1
        if keys_pressed[pygame.K_RETURN] and not self.keys_pressed[pygame.K_RETURN]:
            missile = gs.MissileTypes[self.option_list[self.selected]]
            has_missile = False  # this boolean will only be true if the ship already has that missile type
            for i in range(len(self.ship.missile_types)):
                if missile.name == self.ship.missile_types[i].name:
                    gs.menu = PopupMenu(self, "You already have that type of missile equipped.")
                    has_missile = True
            if has_missile is False:
                if check_purchase(gs.docked, missile):
                    purchase(gs.docked, missile)
                    self.ship.missile_type = missile
                else:
                    gs.menu = PopupMenu(self, "You don't have enough ore to purchase this item.")
        if keys_pressed[pygame.K_ESCAPE] and not self.keys_pressed[pygame.K_ESCAPE]:
            gs.menu = StationMenu()
            # gs.menu.selected = gs.menu.option_list.index('Secondary Weapon')


        self.keys_pressed = keys_pressed
        self.draw_button("Ship Cargo: ", gs.fonts[0], (255, 255, 255), hud, top_left[0] + 800, top_left[1])
        cargos = list(self.ship.cargo)
        for i in range(len(self.ship.cargo)):
            color = (255, 255, 255)
            self.draw_button(cargos[i], gs.fonts[0], color, hud, top_left[0] + 800, top_left[1] + ((1 + i) * (outlineRect.height / (len(self.ship.cargo) + 1))))
            self.draw_button(str(self.ship.cargo[cargos[i]]), gs.fonts[0], color, hud, top_left[0] + 900, top_left[1] + ((1 + i) * (outlineRect.height / (len(self.ship.cargo) + 1))))
        self.draw_button("Station Cargo: ", gs.fonts[0], (255, 255, 255), hud, top_left[0] + 500, top_left[1])
        station_cargo = list(gs.docked.cargo)
        for i in range(len(gs.docked.cargo)):
            color = (255, 255, 255)
            self.draw_button(station_cargo[i], gs.fonts[0], color, hud, top_left[0] + 500, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.cargo) + 1))))
            self.draw_button(str(gs.docked.cargo[station_cargo[i]]), gs.fonts[0], color, hud, top_left[0] + 600, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.cargo) + 1))))

        for i in range(len(self.option_list)):
            if i == self.selected:
                color = (255, 255, 100)
            else:
                color = (255, 255, 255)
            self.draw_button(self.option_list[i], gs.fonts[0], color, hud, 100, 100 * (i + 1))
        # pygame.draw.circle(hud, (255, 0, 0), (500, 500), 4)
        missile_type = gs.MissileTypes[self.option_list[self.selected]]
        image = missile_type.image  # pygame.transform.scale(type.image, (length - 20, length - 20))
        # imagex = top_left[0] + 10
        # imagey = top_left[1] + 10
        imagex = round(top_left[0] + length / 2 - missile_type.width / 2)
        imagey = round(top_left[1] + length / 2 - missile_type.height / 2)
        hud.blit(image, (imagex, imagey))

        self.draw_button("Cost:", gs.fonts[0], (255, 255, 255), hud, top_left[0], top_left[1] + 150)
        ore_names = list(missile_type.cost)
        for i in range(len(missile_type.cost)):
            color = (255, 255, 255)
            self.draw_button(ore_names[i], gs.fonts[0], color, hud, top_left[0],
                             top_left[1] + 150 + ((1 + i) * (outlineRect.height / (2 * (len(missile_type.cost) + 1)))))
            self.draw_button(str(missile_type.cost[ore_names[i]]), gs.fonts[0], color, hud, top_left[0] + 100,
                             top_left[1] + 150 + ((1 + i) * (outlineRect.height / (2 * (len(missile_type.cost) + 1)))))

        bar_width = 20
        tranx = 75

        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 10),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 10), bar_width+4)
        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 15 + bar_width),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 15 + bar_width), bar_width+4)
        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 20 + 2 * bar_width),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 20 + 2 * bar_width), bar_width+4)

        pygame.draw.line(hud, (100, 50, 0), (top_left[0] + length + 5 + tranx, top_left[1] + 10), (top_left[0] + length + 5 + 4 * (missile_type.damage + missile_type.exp_damage) + tranx, top_left[1] + 10), bar_width)
        pygame.draw.line(hud, (100, 0, 0), (top_left[0] + length + 5 + tranx, top_left[1] + 10), (top_left[0] + length + 5 + 4 * missile_type.damage + tranx, top_left[1] + 10), bar_width)
        pygame.draw.line(hud, (0, 100, 0), (top_left[0] + length + 5 + tranx, top_left[1] + 15 + bar_width),
                         (top_left[0] + length + 5 + missile_type.range // 50 + tranx, top_left[1] + 15 + bar_width), bar_width)
        pygame.draw.line(hud, (0, 0, 100), (top_left[0] + length + 5 + tranx, top_left[1] + 20 + 2 * bar_width),
                         (top_left[0] + length + 5 + 5000 // missile_type.delay + tranx, top_left[1] + 20 + 2 * bar_width), bar_width)
        if True:  # keys_pressed[pygame.K_i]:
            damage_text = gs.fonts[1].render(f"DAMAGE", 1, (255, 255, 0))
            range_text = gs.fonts[1].render(f"RANGE", 1, (255, 255, 0))
            ROF_text = gs.fonts[1].render(f"RoF", 1, (255, 255, 0))
            hud.blit(damage_text, (top_left[0] + length + tranx - gs.fonts[1].size('DAMAGE')[0], top_left[1] - 1))
            hud.blit(range_text, (top_left[0] + length + tranx - gs.fonts[1].size('RANGE')[0], top_left[1] + 5 + bar_width - 1))
            hud.blit(ROF_text, (top_left[0] + length + tranx - gs.fonts[1].size('RoF')[0], top_left[1] + 2 * (5 + bar_width) - 1))

        # pygame.draw.circle(WIN, YELLOW, (X, Y), 4)


    def draw_button(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)


class UtilMenu:

    def __init__(self):
        self.keys_pressed = pygame.key.get_pressed()
        self.option_list = []
        self.selected = 0
        self.ship = None
        self.description = "Buy Utility Items"
        # self.launch_button = self.draw_button('Launch Ship', font, (255, 255, 0), hud, 100, 100)

    def draw_menu(self, hud, gs):
        self.option_list = list(gs.MissileTypes)
        keys_pressed = pygame.key.get_pressed()
        edge = 50
        top_left = (300, 200)
        length = 100
        menuRect = pygame.Rect(edge, edge, gs.width-edge*2, gs.height-edge*2)
        outlineRect = pygame.Rect(top_left[0]-10, top_left[1]-10, length*10, gs.height-2*(top_left[1]-10))
        wepRect = pygame.Rect(top_left[0], top_left[1], length, length)
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)
        pygame.draw.rect(hud, (50, 30, 30, 255), outlineRect)
        pygame.draw.rect(hud, (20, 20, 20, 255), wepRect)

        for i in range(len(gs.docked.docked_ships)):
            if gs.docked.docked_ships[i].is_player:
                self.ship = gs.docked.docked_ships[i]

        if keys_pressed[pygame.K_DOWN] and not self.keys_pressed[pygame.K_DOWN]:
            self.selected += 1
            if self.selected >= len(self.option_list):
                self.selected = 0
        elif keys_pressed[pygame.K_UP] and not self.keys_pressed[pygame.K_UP]:
            self.selected -= 1
            if self.selected < 0:
                self.selected = len(self.option_list) - 1
        if keys_pressed[pygame.K_RETURN] and not self.keys_pressed[pygame.K_RETURN]:
            missile = gs.MissileTypes[self.option_list[self.selected]]
            has_missile = False  # this boolean will only be true if the ship already has that missile type
            for i in range(len(self.ship.missile_types)):
                if missile.name == self.ship.missile_types[i].name:
                    gs.menu = PopupMenu(self, "You already have that type of missile equipped.")
                    has_missile = True
            if has_missile is False:
                if check_purchase(gs.docked, missile):
                    purchase(gs.docked, missile)
                    self.ship.missile_type = missile
                else:
                    gs.menu = PopupMenu(self, "You don't have enough ore to purchase this item.")
        if keys_pressed[pygame.K_ESCAPE] and not self.keys_pressed[pygame.K_ESCAPE]:
            gs.menu = StationMenu()
            # gs.menu.selected = gs.menu.option_list.index('Secondary Weapon')


        self.keys_pressed = keys_pressed
        self.draw_button("Ship Cargo: ", gs.fonts[0], (255, 255, 255), hud, top_left[0] + 800, top_left[1])
        cargos = list(self.ship.cargo)
        for i in range(len(self.ship.cargo)):
            color = (255, 255, 255)
            self.draw_button(cargos[i], gs.fonts[0], color, hud, top_left[0] + 800, top_left[1] + ((1 + i) * (outlineRect.height / (len(self.ship.cargo) + 1))))
            self.draw_button(str(self.ship.cargo[cargos[i]]), gs.fonts[0], color, hud, top_left[0] + 900, top_left[1] + ((1 + i) * (outlineRect.height / (len(self.ship.cargo) + 1))))
        self.draw_button("Station Cargo: ", gs.fonts[0], (255, 255, 255), hud, top_left[0] + 500, top_left[1])
        station_cargo = list(gs.docked.cargo)
        for i in range(len(gs.docked.cargo)):
            color = (255, 255, 255)
            self.draw_button(station_cargo[i], gs.fonts[0], color, hud, top_left[0] + 500, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.cargo) + 1))))
            self.draw_button(str(gs.docked.cargo[station_cargo[i]]), gs.fonts[0], color, hud, top_left[0] + 600, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.cargo) + 1))))

        for i in range(len(self.option_list)):
            if i == self.selected:
                color = (255, 255, 100)
            else:
                color = (255, 255, 255)
            self.draw_button(self.option_list[i], gs.fonts[0], color, hud, 100, 100 * (i + 1))
        # pygame.draw.circle(hud, (255, 0, 0), (500, 500), 4)
        missile_type = gs.MissileTypes[self.option_list[self.selected]]
        image = missile_type.image  # pygame.transform.scale(type.image, (length - 20, length - 20))
        # imagex = top_left[0] + 10
        # imagey = top_left[1] + 10
        imagex = round(top_left[0] + length / 2 - missile_type.width / 2)
        imagey = round(top_left[1] + length / 2 - missile_type.height / 2)
        hud.blit(image, (imagex, imagey))

        self.draw_button("Cost:", gs.fonts[0], (255, 255, 255), hud, top_left[0], top_left[1] + 150)
        ore_names = list(missile_type.cost)
        for i in range(len(missile_type.cost)):
            color = (255, 255, 255)
            self.draw_button(ore_names[i], gs.fonts[0], color, hud, top_left[0],
                             top_left[1] + 150 + ((1 + i) * (outlineRect.height / (2 * (len(missile_type.cost) + 1)))))
            self.draw_button(str(missile_type.cost[ore_names[i]]), gs.fonts[0], color, hud, top_left[0] + 100,
                             top_left[1] + 150 + ((1 + i) * (outlineRect.height / (2 * (len(missile_type.cost) + 1)))))

        bar_width = 20
        tranx = 75

        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 10),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 10), bar_width+4)
        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 15 + bar_width),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 15 + bar_width), bar_width+4)
        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 20 + 2 * bar_width),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 20 + 2 * bar_width), bar_width+4)

        pygame.draw.line(hud, (100, 50, 0), (top_left[0] + length + 5 + tranx, top_left[1] + 10), (top_left[0] + length + 5 + 4 * (missile_type.damage + missile_type.exp_damage) + tranx, top_left[1] + 10), bar_width)
        pygame.draw.line(hud, (100, 0, 0), (top_left[0] + length + 5 + tranx, top_left[1] + 10), (top_left[0] + length + 5 + 4 * missile_type.damage + tranx, top_left[1] + 10), bar_width)
        pygame.draw.line(hud, (0, 100, 0), (top_left[0] + length + 5 + tranx, top_left[1] + 15 + bar_width),
                         (top_left[0] + length + 5 + missile_type.range // 50 + tranx, top_left[1] + 15 + bar_width), bar_width)
        pygame.draw.line(hud, (0, 0, 100), (top_left[0] + length + 5 + tranx, top_left[1] + 20 + 2 * bar_width),
                         (top_left[0] + length + 5 + 5000 // missile_type.delay + tranx, top_left[1] + 20 + 2 * bar_width), bar_width)
        if True:  # keys_pressed[pygame.K_i]:
            damage_text = gs.fonts[1].render(f"DAMAGE", 1, (255, 255, 0))
            range_text = gs.fonts[1].render(f"RANGE", 1, (255, 255, 0))
            ROF_text = gs.fonts[1].render(f"RoF", 1, (255, 255, 0))
            hud.blit(damage_text, (top_left[0] + length + tranx - gs.fonts[1].size('DAMAGE')[0], top_left[1] - 1))
            hud.blit(range_text, (top_left[0] + length + tranx - gs.fonts[1].size('RANGE')[0], top_left[1] + 5 + bar_width - 1))
            hud.blit(ROF_text, (top_left[0] + length + tranx - gs.fonts[1].size('RoF')[0], top_left[1] + 2 * (5 + bar_width) - 1))

        # pygame.draw.circle(WIN, YELLOW, (X, Y), 4)


    def draw_button(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)



class MineMenu:

    def __init__(self):
        self.keys_pressed = pygame.key.get_pressed()
        self.option_list = []
        self.selected = 0
        self.ship = None
        self.description = "Buy Mines"
        # self.launch_button = self.draw_button('Launch Ship', font, (255, 255, 0), hud, 100, 100)

    def draw_menu(self, hud, gs):
        self.option_list = list(gs.MissileTypes)
        keys_pressed = pygame.key.get_pressed()
        edge = 50
        top_left = (300, 200)
        length = 100
        menuRect = pygame.Rect(edge, edge, gs.width-edge*2, gs.height-edge*2)
        outlineRect = pygame.Rect(top_left[0]-10, top_left[1]-10, length*10, gs.height-2*(top_left[1]-10))
        wepRect = pygame.Rect(top_left[0], top_left[1], length, length)
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)
        pygame.draw.rect(hud, (50, 30, 30, 255), outlineRect)
        pygame.draw.rect(hud, (20, 20, 20, 255), wepRect)

        for i in range(len(gs.docked.docked_ships)):
            if gs.docked.docked_ships[i].is_player:
                self.ship = gs.docked.docked_ships[i]

        if keys_pressed[pygame.K_DOWN] and not self.keys_pressed[pygame.K_DOWN]:
            self.selected += 1
            if self.selected >= len(self.option_list):
                self.selected = 0
        elif keys_pressed[pygame.K_UP] and not self.keys_pressed[pygame.K_UP]:
            self.selected -= 1
            if self.selected < 0:
                self.selected = len(self.option_list) - 1
        if keys_pressed[pygame.K_RETURN] and not self.keys_pressed[pygame.K_RETURN]:
            missile = gs.MissileTypes[self.option_list[self.selected]]
            has_missile = False  # this boolean will only be true if the ship already has that missile type
            for i in range(len(self.ship.missile_types)):
                if missile.name == self.ship.missile_types[i].name:
                    gs.menu = PopupMenu(self, "You already have that type of missile equipped.")
                    has_missile = True
            if has_missile is False:
                if check_purchase(gs.docked, missile):
                    purchase(gs.docked, missile)
                    self.ship.missile_type = missile
                else:
                    gs.menu = PopupMenu(self, "You don't have enough ore to purchase this item.")
        if keys_pressed[pygame.K_ESCAPE] and not self.keys_pressed[pygame.K_ESCAPE]:
            gs.menu = StationMenu()
            # gs.menu.selected = gs.menu.option_list.index('Secondary Weapon')


        self.keys_pressed = keys_pressed
        self.draw_button("Ship Cargo: ", gs.fonts[0], (255, 255, 255), hud, top_left[0] + 800, top_left[1])
        cargos = list(self.ship.cargo)
        for i in range(len(self.ship.cargo)):
            color = (255, 255, 255)
            self.draw_button(cargos[i], gs.fonts[0], color, hud, top_left[0] + 800, top_left[1] + ((1 + i) * (outlineRect.height / (len(self.ship.cargo) + 1))))
            self.draw_button(str(self.ship.cargo[cargos[i]]), gs.fonts[0], color, hud, top_left[0] + 900, top_left[1] + ((1 + i) * (outlineRect.height / (len(self.ship.cargo) + 1))))
        self.draw_button("Station Cargo: ", gs.fonts[0], (255, 255, 255), hud, top_left[0] + 500, top_left[1])
        station_cargo = list(gs.docked.cargo)
        for i in range(len(gs.docked.cargo)):
            color = (255, 255, 255)
            self.draw_button(station_cargo[i], gs.fonts[0], color, hud, top_left[0] + 500, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.cargo) + 1))))
            self.draw_button(str(gs.docked.cargo[station_cargo[i]]), gs.fonts[0], color, hud, top_left[0] + 600, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.cargo) + 1))))

        for i in range(len(self.option_list)):
            if i == self.selected:
                color = (255, 255, 100)
            else:
                color = (255, 255, 255)
            self.draw_button(self.option_list[i], gs.fonts[0], color, hud, 100, 100 * (i + 1))
        # pygame.draw.circle(hud, (255, 0, 0), (500, 500), 4)
        missile_type = gs.MissileTypes[self.option_list[self.selected]]
        image = missile_type.image  # pygame.transform.scale(type.image, (length - 20, length - 20))
        # imagex = top_left[0] + 10
        # imagey = top_left[1] + 10
        imagex = round(top_left[0] + length / 2 - missile_type.width / 2)
        imagey = round(top_left[1] + length / 2 - missile_type.height / 2)
        hud.blit(image, (imagex, imagey))

        self.draw_button("Cost:", gs.fonts[0], (255, 255, 255), hud, top_left[0], top_left[1] + 150)
        ore_names = list(missile_type.cost)
        for i in range(len(missile_type.cost)):
            color = (255, 255, 255)
            self.draw_button(ore_names[i], gs.fonts[0], color, hud, top_left[0],
                             top_left[1] + 150 + ((1 + i) * (outlineRect.height / (2 * (len(missile_type.cost) + 1)))))
            self.draw_button(str(missile_type.cost[ore_names[i]]), gs.fonts[0], color, hud, top_left[0] + 100,
                             top_left[1] + 150 + ((1 + i) * (outlineRect.height / (2 * (len(missile_type.cost) + 1)))))

        bar_width = 20
        tranx = 75

        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 10),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 10), bar_width+4)
        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 15 + bar_width),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 15 + bar_width), bar_width+4)
        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 20 + 2 * bar_width),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 20 + 2 * bar_width), bar_width+4)

        pygame.draw.line(hud, (100, 50, 0), (top_left[0] + length + 5 + tranx, top_left[1] + 10), (top_left[0] + length + 5 + 4 * (missile_type.damage + missile_type.exp_damage) + tranx, top_left[1] + 10), bar_width)
        pygame.draw.line(hud, (100, 0, 0), (top_left[0] + length + 5 + tranx, top_left[1] + 10), (top_left[0] + length + 5 + 4 * missile_type.damage + tranx, top_left[1] + 10), bar_width)
        pygame.draw.line(hud, (0, 100, 0), (top_left[0] + length + 5 + tranx, top_left[1] + 15 + bar_width),
                         (top_left[0] + length + 5 + missile_type.range // 50 + tranx, top_left[1] + 15 + bar_width), bar_width)
        pygame.draw.line(hud, (0, 0, 100), (top_left[0] + length + 5 + tranx, top_left[1] + 20 + 2 * bar_width),
                         (top_left[0] + length + 5 + 5000 // missile_type.delay + tranx, top_left[1] + 20 + 2 * bar_width), bar_width)
        if True:  # keys_pressed[pygame.K_i]:
            damage_text = gs.fonts[1].render(f"DAMAGE", 1, (255, 255, 0))
            range_text = gs.fonts[1].render(f"RANGE", 1, (255, 255, 0))
            ROF_text = gs.fonts[1].render(f"RoF", 1, (255, 255, 0))
            hud.blit(damage_text, (top_left[0] + length + tranx - gs.fonts[1].size('DAMAGE')[0], top_left[1] - 1))
            hud.blit(range_text, (top_left[0] + length + tranx - gs.fonts[1].size('RANGE')[0], top_left[1] + 5 + bar_width - 1))
            hud.blit(ROF_text, (top_left[0] + length + tranx - gs.fonts[1].size('RoF')[0], top_left[1] + 2 * (5 + bar_width) - 1))

        # pygame.draw.circle(WIN, YELLOW, (X, Y), 4)


    def draw_button(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)


class ShipMenu:

    def __init__(self):
        self.keys_pressed = pygame.key.get_pressed()
        self.option_list = []
        self.selected = 0
        self.ship = None
        self.description = "Buy Ships"
        # self.launch_button = self.draw_button('Launch Ship', font, (255, 255, 0), hud, 100, 100)

    def draw_menu(self, hud, gs):
        self.option_list = list(gs.ShipTypes)
        keys_pressed = pygame.key.get_pressed()
        edge = 50
        top_left = (300, 200)
        length = 100
        menuRect = pygame.Rect(edge, edge, gs.width-edge*2, gs.height-edge*2)
        outlineRect = pygame.Rect(top_left[0]-10, top_left[1]-10, length*10, gs.height-2*(top_left[1]-10))
        wepRect = pygame.Rect(top_left[0], top_left[1], length, length)
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)
        pygame.draw.rect(hud, (50, 30, 30, 255), outlineRect)
        pygame.draw.rect(hud, (20, 20, 20, 255), wepRect)

        for i in range(len(gs.docked.docked_ships)):
            if gs.docked.docked_ships[i].is_player:
                self.ship = gs.docked.docked_ships[i]

        if keys_pressed[pygame.K_DOWN] and not self.keys_pressed[pygame.K_DOWN]:
            self.selected += 1
            if self.selected >= len(self.option_list):
                self.selected = 0
        elif keys_pressed[pygame.K_UP] and not self.keys_pressed[pygame.K_UP]:
            self.selected -= 1
            if self.selected < 0:
                self.selected = len(self.option_list) - 1
        if keys_pressed[pygame.K_RETURN] and not self.keys_pressed[pygame.K_RETURN]:
            ship = gs.ShipTypes[self.option_list[self.selected]]
            if self.ship.ship_type.name == ship.name:
                gs.menu = PopupMenu(self, "You already have that type of ship equipped.")
            elif check_purchase(gs.docked, ship):
                purchase(gs.docked, ship)
                self.ship.ship_type = ship
                self.ship.refresh(gs)
            else:
                gs.menu = PopupMenu(self, "You don't have enough ore to purchase this item.")
        if keys_pressed[pygame.K_ESCAPE] and not self.keys_pressed[pygame.K_ESCAPE]:
            gs.menu = StationMenu()
            # gs.menu.selected = gs.menu.option_list.index('Ships')


        self.keys_pressed = keys_pressed
        self.draw_button("Ship Cargo: ", gs.fonts[0], (255, 255, 255), hud, top_left[0] + 800, top_left[1])
        cargos = list(self.ship.cargo)
        for i in range(len(self.ship.cargo)):
            color = (255, 255, 255)
            self.draw_button(cargos[i], gs.fonts[0], color, hud, top_left[0] + 800, top_left[1] + ((1 + i) * (outlineRect.height / (len(self.ship.cargo) + 1))))
            self.draw_button(str(self.ship.cargo[cargos[i]]), gs.fonts[0], color, hud, top_left[0] + 900, top_left[1] + ((1 + i) * (outlineRect.height / (len(self.ship.cargo) + 1))))
        self.draw_button("Station Cargo: ", gs.fonts[0], (255, 255, 255), hud, top_left[0] + 500, top_left[1])
        station_cargo = list(gs.docked.cargo)
        for i in range(len(gs.docked.cargo)):
            color = (255, 255, 255)
            self.draw_button(station_cargo[i], gs.fonts[0], color, hud, top_left[0] + 500, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.cargo) + 1))))
            self.draw_button(str(gs.docked.cargo[station_cargo[i]]), gs.fonts[0], color, hud, top_left[0] + 600, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.cargo) + 1))))

        for i in range(len(self.option_list)):
            if i == self.selected:
                color = (255, 255, 100)
            else:
                color = (255, 255, 255)
            self.draw_button(self.option_list[i], gs.fonts[0], color, hud, 100, 100 * (i + 1))
        # pygame.draw.circle(hud, (255, 0, 0), (500, 500), 4)
        ship_type = gs.ShipTypes[self.option_list[self.selected]]
        ship_color = "yellow"  # leaves flexibility in case player color can be changed later
        image = pygame.image.load(os.path.join('Assets', f'{ship_type.name}_{ship_color}.png'))  # pygame.transform.scale(Type.image, (length - 20, length - 20))
        # imagex = top_left[0] + 10
        # imagey = top_left[1] + 10
        imagex = round(top_left[0] + length / 2 - ship_type.width / 2)
        imagey = round(top_left[1] + length / 2 - ship_type.height / 2)
        hud.blit(image, (imagex, imagey))
        for i in range(len(ship_type.turrets)):
            for turretKey in gs.TurretTypes.keys():
                if gs.TurretTypes[turretKey].name is ship_type.turrets[i]:
                    turretType = gs.TurretTypes[turretKey]
                    turret_image = pygame.image.load(os.path.join('Assets', f'{ship_type.turrets[i]}.png'))
                    turret_image_x = (top_left[0] + length / 2) + ship_type.turret_pos[i][0] - (turretType.width / 2)
                    turret_image_y = (top_left[1] + length / 2) + ship_type.turret_pos[i][1] - (turretType.height / 2)
                    hud.blit(turret_image, (turret_image_x, turret_image_y))

        self.draw_button("Cost:", gs.fonts[0], (255, 255, 255), hud, top_left[0], top_left[1] + 150)
        ore_names = list(ship_type.cost)
        for i in range(len(ship_type.cost)):
            color = (255, 255, 255)
            self.draw_button(ore_names[i], gs.fonts[0], color, hud, top_left[0],
                             top_left[1] + 150 + ((1 + i) * (outlineRect.height / (2 * (len(ship_type.cost) + 1)))))
            self.draw_button(str(ship_type.cost[ore_names[i]]), gs.fonts[0], color, hud, top_left[0] + 100,
                             top_left[1] + 150 + ((1 + i) * (outlineRect.height / (2 * (len(ship_type.cost) + 1)))))

        bar_width = 20
        tranx = 75

        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 10),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 10), bar_width+4)
        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 15 + bar_width),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 15 + bar_width), bar_width+4)
        pygame.draw.line(hud, (30, 30, 30), (top_left[0] + length + 5 + tranx, top_left[1] + 20 + 2 * bar_width),
                         (top_left[0] + length + 205 + tranx, top_left[1] + 20 + 2 * bar_width), bar_width+4)

        pygame.draw.line(hud, (100, 0, 0), (top_left[0] + length + 5 + tranx, top_left[1] + 10), (top_left[0] + length + 5 + ship_type.health // 3 + tranx, top_left[1] + 10), bar_width)
        pygame.draw.line(hud, (0, 100, 0), (top_left[0] + length + 5 + tranx, top_left[1] + 15 + bar_width),
                         (top_left[0] + length + 5 + ship_type.av * 100 + tranx, top_left[1] + 15 + bar_width), bar_width)
        pygame.draw.line(hud, (0, 0, 100), (top_left[0] + length + 5 + tranx, top_left[1] + 20 + 2 * bar_width),
                         (top_left[0] + length + 5 + 30 * ship_type.velocity + tranx, top_left[1] + 20 + 2 * bar_width), bar_width)
        if True:  # keys_pressed[pygame.K_i]:
            damage_text = gs.fonts[1].render(f"HEALTH", 1, (255, 255, 0))
            range_text = gs.fonts[1].render(f"TURNING", 1, (255, 255, 0))
            ROF_text = gs.fonts[1].render(f"SPEED", 1, (255, 255, 0))
            hud.blit(damage_text, (top_left[0] + length + tranx - gs.fonts[1].size('HEALTH')[0], top_left[1] - 1))
            hud.blit(range_text, (top_left[0] + length + tranx - gs.fonts[1].size('TURNING')[0], top_left[1] + 5 + bar_width - 1))
            hud.blit(ROF_text, (top_left[0] + length + tranx - gs.fonts[1].size('SPEED')[0], top_left[1] + 2 * (5 + bar_width) - 1))

        # pygame.draw.circle(WIN, YELLOW, (X, Y), 4)


    def draw_button(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)


class CargoMenu:

    def __init__(self):
        self.keys_pressed = pygame.key.get_pressed()
        self.option_list = ['Back', 'Unload Cargo']
        self.selected = 0
        self.ship = None
        self.description = "Future Home of the Fleet Liaison"

    def draw_menu(self, hud, gs):
        keys_pressed = pygame.key.get_pressed()
        edge = 50
        top_left = (300, 200)
        length = 100
        menuRect = pygame.Rect(edge, edge, gs.width-edge*2, gs.height-edge*2)
        outlineRect = pygame.Rect(top_left[0]-10, top_left[1]-10, length*10, gs.height-2*(top_left[1]-10))
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)
        pygame.draw.rect(hud, (50, 30, 30, 255), outlineRect)

        for i in range(len(gs.docked.docked_ships)):
            if gs.docked.docked_ships[i].is_player:
                self.ship = gs.docked.docked_ships[i]

        if keys_pressed[pygame.K_DOWN] and not self.keys_pressed[pygame.K_DOWN]:
            self.selected += 1
            if self.selected >= len(self.option_list):
                self.selected = 0
        elif keys_pressed[pygame.K_UP] and not self.keys_pressed[pygame.K_UP]:
            self.selected -= 1
            if self.selected < 0:
                self.selected = len(self.option_list) - 1
        if keys_pressed[pygame.K_RETURN] and not self.keys_pressed[pygame.K_RETURN]:
            if self.selected == 0:
                gs.menu = StationMenu()
                # gs.menu.selected = gs.menu.option_list.index('Cargo Hold')
            elif self.selected == 1:
                if self.ship.cargo.cargo_total == 0:
                    gs.menu = PopupMenu(self, "Error: You can't unload 0 cargo.")

                for key in self.ship.cargo:
                    gs.docked.cargo[key] += self.ship.cargo[key]
                    self.ship.cargo[key] = 0
                    self.ship.cargo.cargo_total = 0
                # for i in range(len(self.ship.cargo)):
                #     ores = list(self.ship.cargo)
                #     gs.docked.cargo[ores[i]] += self.ship.cargo[ores[i]]
                #     self.ship.cargo.cargo_total -= self.ship.cargo[ores[i]]
                #     del self.ship.cargo[ores[i]]

        self.keys_pressed = keys_pressed
        self.draw_button("Ship Cargo: ", gs.fonts[0], (255, 255, 255), hud, top_left[0], top_left[1])
        cargos = list(self.ship.cargo)
        for i in range(len(self.ship.cargo)):
            color = (255, 255, 255)
            self.draw_button(cargos[i], gs.fonts[0], color, hud, top_left[0], top_left[1] + ((1 + i) * (outlineRect.height / (len(self.ship.cargo) + 1))))
            self.draw_button(str(self.ship.cargo[cargos[i]]), gs.fonts[0], color, hud, top_left[0] + 100, top_left[1] + ((1 + i) * (outlineRect.height / (len(self.ship.cargo) + 1))))
        self.draw_button("Station Cargo: ", gs.fonts[0], (255, 255, 255), hud, top_left[0] + 400, top_left[1])
        station_cargo = list(gs.docked.cargo)
        for i in range(len(gs.docked.cargo)):
            color = (255, 255, 255)
            self.draw_button(station_cargo[i], gs.fonts[0], color, hud, top_left[0] + 400, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.cargo) + 1))))
            self.draw_button(str(gs.docked.cargo[station_cargo[i]]), gs.fonts[0], color, hud, top_left[0] + 500, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.cargo) + 1))))

        for i in range(len(self.option_list)):
            if i == self.selected:
                color = (255, 255, 100)
            else:
                color = (255, 255, 255)
            self.draw_button(self.option_list[i], gs.fonts[0], color, hud, 100, 100 * (i + 1))

    def draw_button(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)



"""TAVERN MENU"""



class TavernMenu:

    def __init__(self):
        self.keys_pressed = pygame.key.get_pressed()
        self.option_list = ['Back', 'Unload Cargo']
        self.selected = 0
        self.ship = None
        self.description = "Future Home of the Tavern Menu"

    def draw_menu(self, hud, gs):
        keys_pressed = pygame.key.get_pressed()
        edge = 50
        top_left = (300, 200)
        length = 100
        menuRect = pygame.Rect(edge, edge, gs.width-edge*2, gs.height-edge*2)
        outlineRect = pygame.Rect(top_left[0]-10, top_left[1]-10, length*10, gs.height-2*(top_left[1]-10))
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)
        pygame.draw.rect(hud, (50, 30, 30, 255), outlineRect)

        for i in range(len(gs.docked.docked_ships)):
            if gs.docked.docked_ships[i].is_player:
                self.ship = gs.docked.docked_ships[i]

        if keys_pressed[pygame.K_DOWN] and not self.keys_pressed[pygame.K_DOWN]:
            self.selected += 1
            if self.selected >= len(self.option_list):
                self.selected = 0
        elif keys_pressed[pygame.K_UP] and not self.keys_pressed[pygame.K_UP]:
            self.selected -= 1
            if self.selected < 0:
                self.selected = len(self.option_list) - 1
        if keys_pressed[pygame.K_RETURN] and not self.keys_pressed[pygame.K_RETURN]:
            if self.selected == 0:
                gs.menu = StationMenu()
                # gs.menu.selected = gs.menu.option_list.index('Cargo Hold')
            elif self.selected == 1:
                if self.ship.cargo.cargo_total == 0:
                    gs.menu = PopupMenu(self, "Error: You can't unload 0 cargo.")

                for key in self.ship.cargo:
                    gs.docked.cargo[key] += self.ship.cargo[key]
                    self.ship.cargo[key] = 0
                    self.ship.cargo.cargo_total = 0
                # for i in range(len(self.ship.cargo)):
                #     ores = list(self.ship.cargo)
                #     gs.docked.cargo[ores[i]] += self.ship.cargo[ores[i]]
                #     self.ship.cargo.cargo_total -= self.ship.cargo[ores[i]]
                #     del self.ship.cargo[ores[i]]

        self.keys_pressed = keys_pressed
        self.draw_button("Ship Cargo: ", gs.fonts[0], (255, 255, 255), hud, top_left[0], top_left[1])
        cargos = list(self.ship.cargo)
        for i in range(len(self.ship.cargo)):
            color = (255, 255, 255)
            self.draw_button(cargos[i], gs.fonts[0], color, hud, top_left[0], top_left[1] + ((1 + i) * (outlineRect.height / (len(self.ship.cargo) + 1))))
            self.draw_button(str(self.ship.cargo[cargos[i]]), gs.fonts[0], color, hud, top_left[0] + 100, top_left[1] + ((1 + i) * (outlineRect.height / (len(self.ship.cargo) + 1))))
        self.draw_button("Station Cargo: ", gs.fonts[0], (255, 255, 255), hud, top_left[0] + 400, top_left[1])
        station_cargo = list(gs.docked.cargo)
        for i in range(len(gs.docked.cargo)):
            color = (255, 255, 255)
            self.draw_button(station_cargo[i], gs.fonts[0], color, hud, top_left[0] + 400, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.cargo) + 1))))
            self.draw_button(str(gs.docked.cargo[station_cargo[i]]), gs.fonts[0], color, hud, top_left[0] + 500, top_left[1] + ((1 + i) * (outlineRect.height / (len(gs.docked.cargo) + 1))))

        for i in range(len(self.option_list)):
            if i == self.selected:
                color = (255, 255, 100)
            else:
                color = (255, 255, 255)
            self.draw_button(self.option_list[i], gs.fonts[0], color, hud, 100, 100 * (i + 1))

    def draw_button(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)


"""ASTEROID MENU"""


class AsteroidMenu:

    def __init__(self, ship, asteroid):
        self.keys_pressed = pygame.key.get_pressed()
        self.option_list = ['Launch', 'Harvest']  # can add options later (Build Station, Build Turret, etc)
        self.selected = 0
        self.ship = ship
        self.asteroid = asteroid

    def draw_menu(self, hud, gs):
        keys_pressed = pygame.key.get_pressed()
        edge = 50
        menuRect = pygame.Rect(edge, edge, gs.width - edge * 2, gs.height - edge * 2)
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)

        if keys_pressed[pygame.K_DOWN] and not self.keys_pressed[pygame.K_DOWN]:
            self.selected += 1
            if self.selected >= len(self.option_list):
                self.selected = 0
        elif keys_pressed[pygame.K_UP] and not self.keys_pressed[pygame.K_UP]:
            self.selected -= 1
            if self.selected < 0:
                self.selected = len(self.option_list) - 1
        if keys_pressed[pygame.K_RETURN] and not self.keys_pressed[pygame.K_RETURN]:
            if self.selected == 0:
                gs.ships[0].append(self.ship)
                gs.menu = None
            elif self.selected == 1:
                gs.menu = AsteroidMenu2(self.ship, self.asteroid)

        self.keys_pressed = keys_pressed

        for i in range(len(self.option_list)):
            if i == self.selected:
                color = (255, 255, 100)
            else:
                color = (255, 255, 255)
            self.draw_button(self.option_list[i], gs.fonts[0], color, hud, 100, 100 * (i + 1))

    def draw_button(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)


class AsteroidMenu2:

    def __init__(self, ship, asteroid):
        self.keys_pressed = pygame.key.get_pressed()
        self.option_list = ['Back']
        self.selected = 0
        self.ship = ship
        self.asteroid = asteroid
        for i in range(len(asteroid.ore)):
            self.option_list.append('Harvest All/Max')
            self.option_list.append('Harvest 10')

    def draw_menu(self, hud, gs):
        keys_pressed = pygame.key.get_pressed()
        ores = list(self.asteroid.ore)
        cargos = list(self.ship.cargo)
        edge = 50
        top_left = (300, 100)
        length = 100
        menuRect = pygame.Rect(edge, edge, gs.width - edge * 2, gs.height - edge * 2)
        outlineRect = pygame.Rect(top_left[0] - 10, top_left[1] + (menuRect.height - 100) / len(self.option_list), length * 2, (len(self.option_list) - 2) * (menuRect.height - 100) / len(self.option_list) + 25)
        playerRect = pygame.Rect(top_left[0] + 350, top_left[1] + (menuRect.height - 100) / len(self.option_list), length * 2, (len(self.option_list) - 2) * (menuRect.height - 100) / len(self.option_list) + 25)
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)
        pygame.draw.rect(hud, (50, 30, 30, 225), outlineRect)
        pygame.draw.rect(hud, (50, 30, 30, 225), playerRect)

        if keys_pressed[pygame.K_DOWN] and not self.keys_pressed[pygame.K_DOWN]:
            self.selected += 1
            if self.selected >= len(self.option_list):
                self.selected = 0
        elif keys_pressed[pygame.K_UP] and not self.keys_pressed[pygame.K_UP]:
            self.selected -= 1
            if self.selected < 0:
                self.selected = len(self.option_list) - 1
        if keys_pressed[pygame.K_RETURN] and not self.keys_pressed[pygame.K_RETURN]:
            if self.selected == 0:
                gs.menu = AsteroidMenu(self.ship, self.asteroid)
            elif self.selected >= 0:
                if self.selected % 2 != 0:  # odd number = Harvest All/Max for some ore
                    ores_index = self.selected // 2
                    if self.asteroid.ore[ores[ores_index]] == 0:
                        gs.menu = PopupMenu(self, "Error: You can't harvest 0 ore.")
                    elif (self.ship.cargo.cargo_total + self.asteroid.ore[ores[ores_index]]) < self.ship.ship_type.cargo_cap:
                        added_cargo = self.asteroid.harvest_all(ores[ores_index])
                        self.ship.cargo.cargo_total += added_cargo
                        self.ship.cargo[ores[ores_index]] += added_cargo
                        cargos = list(self.ship.cargo)
                    elif self.ship.cargo.cargo_total < self.ship.ship_type.cargo_cap:
                        added_cargo = self.ship.ship_type.cargo_cap - self.ship.cargo.cargo_total
                        self.asteroid.harvest(ores[ores_index], added_cargo)
                        self.ship.cargo.cargo_total += added_cargo
                        self.ship.cargo[ores[ores_index]] += added_cargo
                        cargos = list(self.ship.cargo)
                    else:
                        gs.menu = PopupMenu(self, "Error: Harvest All/Max failed. Cargo full.")
                if self.selected % 2 == 0:  # even number = Harvest 10 for some ore
                    ores_index = int(self.selected / 2 - 1)
                    if self.asteroid.ore[ores[ores_index]] < 10:
                        gs.menu = PopupMenu(self, "Error: You can't harvest 10 of this ore.")
                    elif (self.ship.cargo.cargo_total + 10) <= self.ship.ship_type.cargo_cap:
                        self.ship.cargo.cargo_total += 10
                        self.ship.cargo[ores[ores_index]] += self.asteroid.harvest(ores[ores_index], 10)
                        cargos = list(self.ship.cargo)
                    else:
                        gs.menu = PopupMenu(self, "Error: Harvest 10 failed. Cargo full.")

        self.keys_pressed = keys_pressed
        self.draw_button("Ship Cargo: ", gs.fonts[0], (255, 255, 255), hud, 650, 100)

        for i in range(len(self.option_list)):
            if i == self.selected:
                color = (255, 255, 100)
            else:
                color = (255, 255, 255)
            self.draw_button(self.option_list[i], gs.fonts[0], color, hud, 100, 100 + (((menuRect.height - 100) * i) / len(self.option_list)))
        for i in range(len(self.asteroid.ore)):
            color = (255, 255, 255)
            self.draw_button(ores[i], gs.fonts[0], color, hud, top_left[0], 100 + (1.5 * (menuRect.height - 100) / len(self.option_list)) + ((2 * (menuRect.height - 100) * i) / len(self.option_list)))
            self.draw_button(str(self.asteroid.ore[ores[i]]), gs.fonts[0], color, hud, top_left[0] + 100, 100 + (1.5 * (menuRect.height - 100) / len(self.option_list)) + ((2 * (menuRect.height - 100) * i) / len(self.option_list)))
        for i in range(len(self.ship.cargo)):
            color = (255, 255, 255)
            self.draw_button(cargos[i], gs.fonts[0], color, hud, top_left[0] + 360, 100 + (1.5 * (menuRect.height - 100) / len(self.option_list)) + ((2 * (menuRect.height - 100) * i) / len(self.option_list)))
            self.draw_button(str(self.ship.cargo[cargos[i]]), gs.fonts[0], color, hud, top_left[0] + 460, 100 + (1.5 * (menuRect.height - 100) / len(self.option_list)) + ((2 * (menuRect.height - 100) * i) / len(self.option_list)))

    def draw_button(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)


class PopupMenu:

    def __init__(self, menu, text):
        self.keys_pressed = pygame.key.get_pressed()
        self.menu = menu
        self.text = text

    def draw_menu(self, hud, gs):
        keys_pressed = pygame.key.get_pressed()
        edge = 50
        color = (255, 255, 255)
        menuRect = pygame.Rect(edge, edge, gs.width - edge * 2, gs.height - edge * 2)
        pygame.draw.rect(hud, (30, 30, 30, 225), menuRect)

        if keys_pressed[pygame.K_p] and not self.keys_pressed[pygame.K_p]:
            gs.menu = self.menu

        self.keys_pressed = keys_pressed

        self.draw_button(self.text, gs.fonts[0], color, hud, 550, 350)
        self.draw_button("Press p to return to previous menu.", gs.fonts[0], color, hud, 550, 400)

    def draw_button(self, text, font, color, surface, x, y):
        textobj = font.render(text, 1, color)
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        surface.blit(textobj, textrect)
