from Data.Types import Vessel
import pygame

def draw_turret(self: Vessel, surf: pygame.Surface, x_center: float, y_center: float):
    turret_image = pygame.transform.rotate(self.image, self.angle)
    x = x_center - turret_image.get_width() // 2
    y = y_center - turret_image.get_height() // 2
    surf.blit(turret_image, (x, y))
