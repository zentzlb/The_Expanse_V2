import math
import random as rnd
from Explosions import ExplosionDamage
import pygame
from typing import TYPE_CHECKING
from Data.Types import Particle, Entity, Vessel, Event, Shooter
from Weapon_Class import Mine

if TYPE_CHECKING:
    from Misc import GlobalState, LocalState


def init_mine(ship: Shooter, entity_list: list[Entity]) -> list[Event]:
    (x, y) = ship.center
    missile = Mine(x, y, ship, ship.angle, ship.mine)
    entity_list.append(missile)
    return []


def draw_mine(mine: Mine, surf: pygame.Surface, x_center: float, y_center: float):
    x = x_center - mine.image.get_width() // 2
    y = y_center - mine.image.get_height() // 2
    surf.blit(pygame.transform.rotate(mine.image, mine.angle), (x, y))


def explosion(self: Mine, gs: "GlobalState"):
    for i in range(100):
        c = rnd.randint(100, 200)
        gs.particle_list2.append(Particle(self.centerx, self.centery, -rnd.randint(1, self.er // 20),
                                          rnd.randint(0, 360), 10,
                                          (c + 50, c, 100), shrink=0.5))

    ExplosionDamage(self.exp_damage, self.centerx, self.centery, self.er, gs.targets[self.faction], gs)


def proximity(self: Mine, gs: "GlobalState"):
    if self.timer < self.arm:
        dr2 = self.type.det_radius * self.type.det_radius
        for target in gs.targets[self.faction]:
            dx = target.centerx - self.centerx
            dy = target.centery - self.centery
            if dx * dx + dy * dy < dr2:
                explosion(self, gs)
                self.health = 0
                break


def black_hole(self: Mine, entity_list: list[Entity]):
    events = []
    if self.timer < self.arm:
        for i in range(self.type.par_num):
            angle = rnd.randint(-180, 180)
            r = rnd.randint(95, 105)
            x = self.centerx + r * math.sin(math.pi * angle / 180)
            y = self.centery + r * math.cos(math.pi * angle / 180)
            events.append(
                Particle(x, y, 10, angle + 180, 10,
                         (rnd.randint(0, 30), 0, rnd.randint(0, 100))))

        targets = [ship for ship in entity_list if isinstance(ship, Vessel) and
                   ship.faction_name != self.faction_name]

        for ship in targets:
            dx = ship.centerx - self.centerx
            dy = ship.centery - self.centery
            r2 = dx * dx + dy * dy
            if r2 < 1000000:
                ship.vx -= (dx * 50) / (r2 + 1)
                ship.vy -= (dy * 50) / (r2 + 1)
                if ship.vx * ship.vx + ship.vy * ship.vy > ship.velocity * ship.velocity:
                    ship.vx = ship.vx * ship.velocity / math.sqrt(ship.vx * ship.vx + ship.vy * ship.vy)
                    ship.vy = ship.vy * ship.velocity / math.sqrt(ship.vx * ship.vx + ship.vy * ship.vy)

                if r2 < (self.height + ship.height) ** 2:
                    events += ship - self.damage

    else:
        for i in range(10):
            angle = rnd.randint(-180, 180)
            r = rnd.randint(1, 100)
            x = self.centerx + r * math.sin(math.pi * angle / 180)
            y = self.centery + r * math.cos(math.pi * angle / 180)
            events.append(
                Particle(x, y, 0, 0, 10, (rnd.randint(0, 30), 0, rnd.randint(0, 100))))

    return events
