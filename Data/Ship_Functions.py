from Data.Types import Vessel
import pygame


def draw_ship(self: Vessel, surf: pygame.Surface, x_center: int, y_center: int):
    if len(self.turrets) == 0:
        ship_image = pygame.transform.rotate(self.image, self.angle)
        x = x_center - ship_image.get_width() // 2
        y = y_center - ship_image.get_height() // 2
        surf.blit(ship_image, (x, y))
    else:
        ship_image = self.image.copy()
        for turret in self.turrets:
            turret_image = pygame.transform.rotate(turret.image, turret.angle - self.angle)
            x = self.width // 2 + turret.pos[0] - turret_image.get_width() // 2
            y = self.height // 2 + turret.pos[1] - turret_image.get_height() // 2
            ship_image.blit(turret_image, (x, y))

        ship_image = pygame.transform.rotate(ship_image, self.angle)
        x = x_center - ship_image.get_width() // 2
        y = y_center - ship_image.get_height() // 2
        surf.blit(ship_image, (x, y))
