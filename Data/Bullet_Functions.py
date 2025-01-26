from Weapon_Class import Bullet
from Explosions import ExplosionDamage
import numpy as np
import random as rnd
import pygame
from pygame.locals import BLEND_RGB_ADD
from Data.Types import (Entity, State, Shooter, glow_circle, Particle,
                        FactionType, Event, PlasmaExplosion, Beam)
from utils import beam_collision
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Ship_Class import Ship, Base, Asteroid


def init_bullet(ship: Shooter, entity_list: list[Entity]) -> list[Event]:
    (x, y) = ship.center + ship.Qt.dot(ship.bullet_pos) - np.array([ship.bullet.width // 2, ship.bullet.height // 2])
    bullet = Bullet(x, y, ship, ship.angle,
                    ship.bullet)
    entity_list.append(bullet)
    return []


def init_cannon(ship: Shooter, entity_list: list[Entity]) -> list[Event]:
    (x, y) = ship.center + ship.Qt.dot(ship.bullet_pos) - np.array([ship.bullet.width // 2, ship.bullet.height // 2])
    bullet = Bullet(x, y, ship, ship.angle,
                    ship.bullet)
    entity_list.append(bullet)
    return [Particle(bullet.centerx, bullet.centery, ship.bullet.velocity+1, ship.angle + rnd.randint(-15, 15),
                     2, (255, rnd.randint(0, 255), 0),
                     shrink=0.9, vx=ship.vx, vy=ship.vy, glow=(255, 200, 0, 100)) for _ in range(5)]


def init_spray(ship: Shooter, entity_list: list[Entity]) -> list[Event]:
    if ship.is_ship:
        pos = ship.center + ship.Qt.dot(ship.type.bullet_pos[ship.bullet_sel]) - np.array(
            [ship.bullet_types[ship.bullet_sel].width // 2, ship.bullet_types[ship.bullet_sel].height // 2])
    else:
        pos = ship.center - np.array([ship.bullet_types[ship.bullet_sel].width // 2,
                                      ship.bullet_types[ship.bullet_sel].height // 2])
    bullet = Bullet(pos[0], pos[1], ship, ship.angle + rnd.randint(-15, 15),
                    ship.bullet_types[ship.bullet_sel], faction)
    entity_list.append(bullet)


def init_beam(ship: Shooter, entity_list: list[Entity]) -> list[Event]:
    x, y = ship.center + ship.Qt.dot(ship.bullet_pos)
    targets = [entity for entity in entity_list if entity.faction_name and entity.faction_name != ship.faction_name]
    (x2, y2), target = beam_collision(x, y, ship.bullet.range, ship.angle, targets)
    if target:
        heat_laser(ship, target)
    return [Beam(x, y, x2, y2, 1, (rnd.randint(200, 255), rnd.randint(0, 100), 0))]


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


def cannon(self: "Bullet", entity_list: list[Entity], dmg_list: list[int]) -> list[Event]:
    events = []
    for i in dmg_list:
        events += entity_list[i] - self.damage  # + bonus
        entity_list[i].heat += self.damage
    self.timer = 0
    return events


def he_cannon(self: Bullet, entity_list: list[Entity], dmg_list: list[int]) -> list[Event]:
    events = []
    for i in dmg_list:
        events += entity_list[i] - self.damage
        entity_list[i].heat += self.damage

    events += ExplosionDamage(self.exp_damage, self.centerx, self.centery, self.exp_radius, entity_list)
    self.timer = 0
    return events + [Particle(self.centerx, self.centery, -rnd.randint(1, self.exp_radius // 20),
                              rnd.randint(0, 360), 10,
                              ((c := rnd.randint(100, 200)) + 50, c, 100), shrink=0.5) for
                     _ in range(100)]


def heat_cannon(self: "Bullet", entity_list: list[Entity], dmg_list: list[int]) -> list[Event]:
    events = []
    for i in dmg_list:
        events += entity_list[i] - self.damage  # + bonus
        entity_list[i].heat += 3 * self.damage
    self.timer = 0
    return events


def flame(self: "Bullet", entity_list: list[Entity], dmg_list: list[int]) -> list[Event]:
    for i in dmg_list:
        # self.targets[i].health -= self.damage  # + bonus
        entity_list[i].heat += 2  # adj
    self.timer = 0
    return []
    # gs.bullets[self.faction].remove(self)


def plasma(self: "Bullet", entity_list: list[Entity], dmg_list: list[int]) -> list[Event]:
    events = []
    for i in dmg_list:
        events += entity_list[i] - self.damage
        entity_list[i].heat += self.damage
    self.timer = 0
    return events + [PlasmaExplosion(self.centerx, self.centery)]


def heat_laser(self: Shooter, target: Entity) -> list[Event]:
    if self.heat > self.heat_cap:
        heat = 1
    else:
        heat = 0.3
    target.heat += heat
    return [Particle(self.centerx, self.centery, 3,
                     rnd.randint(0, 360), 3, (255, 0, 0, 150), shrink=0.75)]


def rail(self: "Bullet", entity_list: list[Entity], dmg_list: list[int]) -> list[Particle]:
    events = []
    for i in dmg_list:
        self.events = entity_list[i] - self.damage
        entity_list[i].heat += self.damage
    return events + [Particle(self.centerx, self.centery, 2,
                              rnd.randint(0, 360), 8, (0, 223, 255), shrink=0.75) for _ in range(8)]


if __name__ == '__main__':
    print(locals())
