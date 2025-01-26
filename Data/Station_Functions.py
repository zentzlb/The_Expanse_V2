from Data.Types import Vessel
import pygame


def draw_station(self: Vessel, surf: pygame.Surface, x_center: float, y_center: float):
    if len(self.turrets) == 0:
        station_image = pygame.transform.rotate(self.image, self.angle)
        x = x_center - station_image.get_width() // 2
        y = y_center - station_image.get_height() // 2
        surf.blit(station_image, (x, y))
    else:
        station_image = self.image.copy()
        for turret in self.turrets:
            turret_image = pygame.transform.rotate(turret.image, turret.angle - self.angle)
            x = self.width // 2 + turret.pos[0] - turret_image.get_width() // 2
            y = self.height // 2 + turret.pos[1] - turret_image.get_height() // 2
            station_image.blit(turret_image, (x, y))

        station_image = pygame.transform.rotate(station_image, self.angle)
        x = x_center - station_image.get_width() // 2
        y = y_center - station_image.get_height() // 2
        surf.blit(station_image, (x, y))
