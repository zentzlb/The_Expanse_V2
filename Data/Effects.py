import math
import random as rnd

from Types import pygame, Effect, glow_circle, COLOR3, Entity, Shooter


class PlasmaExplosion(Effect):
    max_timer = 50

    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.timer = self.max_timer

    def scoot(self, entity_list: list["Effect"]) -> list[Effect]:
        self.timer -= 1
        if self.timer > 0:
            return [self]
        return []

    def draw(self, surf: pygame.surface, x_off: float, y_off: float):
        # save images ahead of time
        for r in range(self.timer):
            glow_circle(surf, self.x - x_off, self.y - y_off, r, (4, 0, 5))


class Beam(Effect):
    __slots__ = 'x', 'y', 'x2', 'y2', 'width', 'color', 'shrink', 'timer'

    def __init__(self, x: float, y: float, x2: float, y2: float, width: int, color: COLOR3,
                 shrink: float = 1):
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.width: float = width
        self.color = color
        self.shrink = shrink
        self.timer = 2

    def scoot(self, entity_list: list["Effect"]) -> list[Effect]:
        self.timer -= 1
        if self.timer > 0:
            return [self]
        return []
        # self.width -= self.shrink
        # return self.width > 0

    def draw(self, surf: pygame.surface, x_off: float, y_off: float) -> None:
        x, x2 = self.x - x_off, self.x2 - x_off
        y, y2 = self.y - y_off, self.y2 - y_off

        pygame.draw.line(surf, self.color, (x, y), (x2, y2),
                         width=round(self.width))
        glow_circle(surf, x2, y2, rnd.randint(5, 10), (150, 50, 0, 50))
        glow_circle(surf, x, y, rnd.randint(3, 5), (150, 50, 0, 50))


class Particle(Effect):
    __slots__ = 'x', 'y', 'v', 'angle', 'radius', 'color', 'shrink', 'vx', 'vy', 'glow', 'show'

    def __init__(self,
                 x: float,
                 y: float,
                 v: float,
                 angle: float,
                 radius: int,
                 color,
                 shrink: float = 0,
                 vx: float = 0,
                 vy: float = 0,
                 glow=(0, 0, 0),
                 show=True):
        self.x = x
        self.y = y
        self.vx = v * math.sin(angle * math.pi / 180) + vx
        self.vy = v * math.cos(angle * math.pi / 180) + vy
        self.color = color
        self.radius = radius
        self.shrink = shrink
        self.glow = glow
        self.show = show

    def scoot(self, entity_list: list["Effect"]) -> list[Effect]:
        self.x += self.vx
        self.y += self.vy
        if rnd.random() > self.shrink:
            self.radius -= 1

        if self.radius > 0:
            return [self]
        return []

    def draw(self, surf: pygame.surface, x_off: float, y_off: float):
        if self.show:
            pygame.draw.circle(surf, self.color, (self.x - x_off, self.y - y_off), self.radius)
            if self.glow != (0, 0, 0):
                glow_circle(surf, self.x - x_off, self.y - y_off, 2 * self.radius, self.glow)


class Chaff(Particle):

    def __init__(self, x: float, y: float, v: float,
                 angle: float, radius: int, color, ship: "Entity", entity_list: list["Entity"]):
        super().__init__(x, y, v, angle, radius, color)
        for entity in entity_list:
            if type(Entity) is Shooter and rnd.random() > 0.6:
                pass


class Debris(Effect):
    def __init__(self, x, y, v, angle, debris_type, time, av, vx=0, vy=0, show=True):
        self.x = x
        self.y = y
        self.vx = v * math.sin(angle * math.pi / 180) + vx
        self.vy = v * math.cos(angle * math.pi / 180) + vy
        self.type = debris_type
        self.height = debris_type.image.get_height()
        self.width = debris_type.image.get_width()
        self.angle = rnd.randint(-180, 180)
        self.av = av
        self.show = show
        self.counter = time
        # print(self.av)

    def scoot(self, entity_list: list["Effect"]) -> list[Effect]:
        self.x += self.vx
        self.y += self.vy
        self.angle += self.av
        self.counter -= 1
        if self.counter > 0:
            return [self]
        return []

    def draw(self, surf: pygame.surface, x_off: float, y_off: float):
        debris = pygame.transform.rotate(self.type.image, self.angle)
        surf.blit(debris, (self.x - x_off, self.y - y_off))