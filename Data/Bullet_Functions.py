import math
import typing

from Weapon_Class import Bullet
from Explosions import ExplosionDamage
import numpy as np
import random as rnd
import pygame
from pygame.locals import BLEND_RGB_ADD
from Data.Types import Entity, State, Shooter, glow_circle, FactionType, Effect, COLOR3
from Data.Effects import Particle, PlasmaExplosion, Beam
from Data.constants import PULSE_DURATION
from utils import beam_collision
from typing import TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from Ship_Class import Ship, Base, Asteroid


def distance(e1: Entity, e2: Entity) -> float:
    return math.sqrt((e1.centerx - e2.centerx) ** 2 + (e1.centery - e2.centery) ** 2)


class Pulse(Effect):
    duration = PULSE_DURATION

    def __init__(self, ship: Shooter, pos: np.ndarray[int, int], func: Callable,
                 width: int, color: COLOR3, shrink: float = 1):
        self.ship = ship
        self.pos = pos
        self.function = func
        self.width: float = width
        self.color = color
        self.shrink = shrink
        self.timer = self.duration
        self.x2 = 0
        self.y2 = 0

    @property
    def origin(self) -> tuple[float, float]:
        return self.ship.center + self.ship.Qt.dot(self.pos)

    @property
    def x(self) -> float:
        return self.origin[0]

    @property
    def y(self) -> float:
        return self.origin[1]


    def scoot(self, entity_list: list[Entity]) -> list[Effect]:
        effects = []
        targets = [entity for entity in entity_list if
                   entity.faction_name and entity.faction_name != self.ship.faction_name]
        x, y = self.origin
        (self.x2, self.y2), target = beam_collision(x, y, self.ship.bullet.range, self.ship.angle,
                                              targets)
        if target and self.timer == self.duration:
            effects += self.function(self.ship, target)

        self.timer -= 1
        if self.timer > 0:
            effects.append(self)
        return effects

    def draw(self, surf: pygame.surface, x_off: float, y_off: float) -> None:

        ox, oy = self.origin
        x, x2 = ox - x_off, self.x2 - x_off
        y, y2 = oy - y_off, self.y2 - y_off

        pygame.draw.line(surf, self.color, (x, y), (x2, y2),
                         width=round(self.width * self.timer / self.duration) + 1)
        glow_circle(surf, x2, y2, rnd.randint(5, 10), (150, 50, 0, 50))
        glow_circle(surf, x, y, rnd.randint(3, 5), (150, 50, 0, 50))



def init_bullet(ship: Shooter, entity_list: list[Entity]) -> list[Effect]:
    (x, y) = ship.center + ship.Qt.dot(ship.bullet_pos) - np.array(
        [ship.bullet.width // 2, ship.bullet.height // 2])
    bullet = Bullet(x, y, ship, ship.angle,
                    ship.bullet.type)
    entity_list.append(bullet)
    return []


def init_cannon(ship: Shooter, entity_list: list[Entity]) -> list[Effect]:
    (x, y) = ship.center + ship.Qt.dot(ship.bullet_pos) - np.array(
        [ship.bullet.width // 2, ship.bullet.height // 2])
    bullet = Bullet(x, y, ship, ship.angle,
                    ship.bullet.type)
    entity_list.append(bullet)
    return [Particle(bullet.centerx, bullet.centery, ship.bullet.velocity - 1,
                     ship.angle + rnd.randint(-25, 25),
                     2, (255, rnd.randint(0, 255), 0),
                     shrink=0.8, vx=ship.vx, vy=ship.vy, glow=(100, 50, 0)) for _ in range(5)]


def init_spray(ship: Shooter, entity_list: list[Entity]) -> list[Effect]:
    (x, y) = ship.center + ship.Qt.dot(ship.bullet_pos) - np.array(
        [ship.bullet.width // 2, ship.bullet.height // 2])
    bullet = Bullet(x, y, ship, ship.angle + rnd.randint(-15, 15),
                    ship.bullet.type)
    entity_list.append(bullet)
    return []


def init_beam(ship: Shooter, entity_list: list[Entity]) -> list[Effect]:
    x, y = ship.center + ship.Qt.dot(ship.bullet_pos)
    targets = [entity for entity in entity_list if entity.faction_name and
               entity.faction_name != ship.faction_name]
    (x2, y2), target = beam_collision(x, y, ship.bullet.range, ship.angle, targets)
    if target:
        heat_laser(ship, target)
        effects = [Particle(x2, y2, 1, rnd.randint(0, 360),
                           1, (255, 0, 0), shrink=0.9)
                  for _ in range(10)]
    else:
        effects = []
    return effects + [Beam(x, y, x2, y2, 2,
                          (rnd.randint(200, 255), rnd.randint(0, 100), 0))]


def init_pulse(ship: Shooter, entity_list: list[Entity]) -> list[Effect]:

    return [Pulse(ship, ship.bullet_pos, ship.bullet.type.function, 5,
             (rnd.randint(0, 100), rnd.randint(200, 255), 0), shrink=0.5)]


def draw_bullet(bullet: Bullet, surf: pygame.Surface, x_center: float, y_center: float):
    x = x_center - bullet.image.get_width() // 2
    y = y_center - bullet.image.get_height() // 2
    surf.blit(bullet.image, (x, y))


def draw_flame(bullet, surf: pygame.Surface, x_center: float, y_center: float):
    scale = (bullet.range / bullet.velocity - bullet.timer) / 40
    radius1 = 2 + round(scale)
    r = 255 / (1 + scale)
    g = rnd.randint(0, 200) / (1 + scale)
    color1 = (r, g, 0)
    surf2 = pygame.Surface((radius1 * 2, radius1 * 2))
    surf2.set_colorkey((0, 0, 0))
    pygame.draw.circle(surf2, color1, (radius1, radius1), radius1)
    surf.blit(surf2, (x_center - radius1, y_center - radius1), special_flags=BLEND_RGB_ADD)


# def draw_beam(beam, surf: pygame.Surface, x_center: float, y_center: float):
#     shift = np.array([x_center, y_center], dtype=np.float64)
#     p1 = beam.p1 - shift
#     p2 = beam.p2 - shift
#     if beam.overcharged:
#         w = 2
#     else:
#         w = 1
#     pygame.draw.line(surf, beam.color, p1, p2, width=w)
#     glow_circle(surf, p2[0], p2[1], rnd.randint(5, 10), (150, 50, 0, 50))
#     glow_circle(surf, p1[0], p1[1], rnd.randint(3, 5), (150, 50, 0, 50))


def cannon(self: "Bullet", entity_list: list[Entity], dmg_list: list[int]) -> list[Effect]:
    effects = []
    for i in dmg_list:
        effects += entity_list[i] - self.damage  # + bonus
        entity_list[i].heat += self.damage
    self.timer = 0
    return effects


def he_cannon(self: Bullet, entity_list: list[Entity], dmg_list: list[int]) -> list[Effect]:
    effects = []
    for i in dmg_list:
        effects += entity_list[i] - self.damage
        entity_list[i].heat += self.damage

    effects += ExplosionDamage(self.exp_damage, self.centerx, self.centery, self.exp_radius,
                              entity_list)
    self.timer = 0
    return effects + [Particle(self.centerx, self.centery, -rnd.randint(1, self.exp_radius // 20),
                              rnd.randint(0, 360), 10,
                              ((c := rnd.randint(100, 200)) + 50, c, 100), shrink=0.5) for
                     _ in range(100)]


def heat_cannon(self: "Bullet", entity_list: list[Entity], dmg_list: list[int]) -> list[Effect]:
    effects = []
    for i in dmg_list:
        effects += entity_list[i] - self.damage  # + bonus
        entity_list[i].heat += 3 * self.damage
    self.timer = 0
    return effects


def flame(self: "Bullet", entity_list: list[Entity], dmg_list: list[int]) -> list[Effect]:
    for i in dmg_list:
        # self.targets[i].health -= self.damage  # + bonus
        entity_list[i].heat += 2  # adj
    self.timer = 0
    return []
    # gs.bullets[self.faction].remove(self)


def plasma(self: "Bullet", entity_list: list[Entity], dmg_list: list[int]) -> list[Effect]:
    effects = []
    # for i in dmg_list:
    #     effects += entity_list[i] - self.damage
    #     entity_list[i].heat += self.damage
    # self.timer = 0
    for entity in entity_list:
        if isinstance(entity, Shooter) and distance(self, entity) < 25 + entity.height / 2:
            effects += entity - self.damage
            entity.heat += self.damage
    self.timer = 0
    return effects + [PlasmaExplosion(self.centerx, self.centery)]


def heat_laser(self: Shooter, target: Entity) -> list[Effect]:
    if self.heat > self.heat_cap:
        heat = 1
        color = (0, 0, 255, 150)
    else:
        heat = 0.4
        color = (255, 0, 0, 150)
    target.heat += heat
    return [Particle(self.centerx, self.centery, 3,
                     rnd.randint(0, 360), 3, color, shrink=0.75)]


def pulse_laser(damage: int, self: Shooter, target: Entity) -> list[Effect]:
    target.heat += damage
    effects = target - damage

    return effects + [Particle(target.centerx, target.centery, 2,
                              rnd.randint(0, 360), 3, (0, 255, 0),
                              shrink=0.9, glow=(0, 80, 0)) for _ in range(10)]


def rail(self: "Bullet", entity_list: list[Entity], dmg_list: list[int]) -> list[Particle]:
    effects = []
    for i in dmg_list:
        self.effects = entity_list[i] - self.damage
        entity_list[i].heat += self.damage
    return effects + [Particle(self.centerx, self.centery, 2,
                              rnd.randint(0, 360), 8, (0, 223, 255),
                              shrink=0.75) for _ in range(8)]


if __name__ == '__main__':
    print(locals())
