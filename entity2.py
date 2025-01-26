import pygame
import math


class Entity2(pygame.FRect):
    def __init__(self,
                 x: float,
                 y: float,
                 color: tuple,
                 x_velocity: float,
                 y_velocity: float,
                 width: float,
                 height: float):

        super().__init__(x, y, width, height)
        self.color = color
        self.y_velocity = x_velocity
        self.x_velocity = y_velocity

    @property
    def speed(self):
        """
        speed of projectile
        :return:
        """
        return math.sqrt(self.x_velocity * self.x_velocity + self.y_velocity * self.y_velocity)

    @speed.setter
    def speed(self, value: float):
        ratio = value / self.speed
        self.x_velocity *= ratio
        self.y_velocity *= ratio

    def move(self, x: float, y: float):
        """
        update position
        :param x: mouse x position
        :param y: mouse y position
        :return:
        """
        self.x_velocity = (x - self.x) / 5
        self.y_velocity = (y - self.y) / 5
        self.x += self.x_velocity
        self.y += self.y_velocity

    def draw(self, screen: pygame.Surface):
        """
        draw projectile on screen
        :param screen:
        :return:
        """
        pygame.draw.rect(screen, self.color, self)


if __name__ == '__main__':
    e = Entity2(1, 2, (255, 255, 255), 3, 4, 10, 10)
    print(e.x_velocity, e.y_velocity, e.speed)
    e.speed = 20
    print(e.x_velocity, e.y_velocity, e.speed)

