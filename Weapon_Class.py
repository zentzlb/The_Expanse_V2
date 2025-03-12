import pygame
import math
import random as rnd
from utils import FindNearest
from Data.constants import DRAG, ARM
from Data.Types import (Entity, BulletType, MissileType, Event,
                        MineType, Shooter, Projectile, Guided, Particle, Vessel)
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    pass


class Bullet(Projectile):
    def __init__(self, x: float, y: float, ship: Shooter, angle: float, bullet_type: BulletType):
        self.type = bullet_type
        if bullet_type.sound is not None:
            bullet_type.sound.play()
        super().__init__(x, y, bullet_type.width, bullet_type.height)
        self.angle = angle
        self.health = 1
        self.heat = 0
        self.timer = self.range / self.velocity
        self.vx = self.velocity * math.sin(self.radians) + ship.vx
        self.vy = self.velocity * math.cos(self.radians) + ship.vy
        self.image = pygame.transform.rotate(bullet_type.image, angle)
        self.faction = ship.faction
        self.ship = ship

    def draw(self, surf: pygame.Surface, x_center: int, y_center: int):
        self.type.draw(self, surf, x_center, y_center)

    def scoot(self, entity_list: list[Entity]) -> list[Event]:
        target_list = [entity for entity in entity_list
                       if self.faction_name != entity.faction_name
                       and isinstance(entity, self.type.target_types)]
        self.x += self.vx
        self.y += self.vy
        self.timer -= 1
        if self.timer <= 0:
            self.health = 0
        elif dmg_list := self.collidelistall(target_list):
            return self.type.function(self, target_list, dmg_list)
        return []


class Missile(Guided):
    def __init__(self, x: float, y: float, ship: Shooter, angle: float,
                 missile_type: MissileType, target: "Entity", vx: float = 0, vy: float = 0):
        if missile_type.sound is not None:
            missile_type.sound.play()  # .set_volume(0.5)
        super().__init__(x, y, missile_type.width, missile_type.height)
        self.type = missile_type
        self.angle = angle
        self.vx = vx
        self.vy = vy
        self.health = missile_type.health
        self.heat = 0
        self.timer = self.range / self.velocity
        self.arm = self.range / self.velocity - ARM
        self.target = target
        self.image = missile_type.image
        self.faction = ship.faction
        self.ship = ship

    def draw(self, surf: pygame.Surface, x_center: int, y_center: int):
        self.type.draw(self, surf, x_center, y_center)

    def scoot(self, entity_list: list[Entity]) -> list[Event]:

        self.vx *= DRAG
        self.vy *= DRAG

        events = []

        targets = [ship for ship in entity_list if isinstance(ship, Vessel) and
                   ship.faction_name != self.faction_name]

        if self.target is None or self.target.health <= 0:
            self.target = FindNearest(self, targets)

        if self.target is None:
            events += self.type.explosion(self, targets, [])
            self.timer = 0
            self.health = 0
            return events

        commands: dict = self.type.guidance(self)

        if abs(commands['rotate']) >= 1:
            self.angle += self.av * commands['rotate']

        if commands['thrust']:
            self.timer -= 1
            self.vx += self.acc * math.sin(self.radians)
            self.vy += self.acc * math.cos(self.radians)
            for i in range(self.type.par_num):
                red = 255
                green = rnd.randint(0, 255)
                # if rnd.random() > 0.5:
                events = [Particle(self.centerx, self.centery, -rnd.random() - 2,
                                   self.angle + rnd.randint(-self.type.par_rnd,
                                                            self.type.par_rnd), 3, (red, green, 0),
                                   glow=(red // 2, green // 2, 0), shrink=0.85),
                          Particle(self.centerx, self.centery, -rnd.random(),
                                   self.angle + rnd.randint(-self.type.par_rnd + 5,
                                                            self.type.par_rnd + 5), 4,
                                   (80, 80, 80), shrink=0.97)]  # adj

        if self.speed > self.velocity:
            self.speed = self.velocity

        self.x += self.vx
        self.y += self.vy

        if self.timer < self.arm and (dmg_list := self.collidelistall(targets)):  # missile hits target
            events += self.type.explosion(self, targets, dmg_list)
            self.health = 0

        elif self.timer <= 1:  # missile runs out of thrust
            events += self.type.explosion(self, targets, [])
            self.health = 0
        return events


class Mine(Projectile):
    def __init__(self, x: float, y: float, ship: Shooter, angle: float, mine_type: MineType):
        if mine_type.sound is not None:
            mine_type.sound.play()
        super().__init__(x, y, mine_type.width, mine_type.height)
        # self.center = (x, y)
        self.type = mine_type
        self.angle = angle
        self.timer = mine_type.time
        self.health = self.max_health
        self.heat = 0
        self.vx = 0
        self.vy = 0
        self.image = mine_type.image
        self.faction = ship.faction
        self.ship = ship

    @property
    def arm(self):
        return self.type.time - self.type.arm

    def draw(self, surf: pygame.Surface, x_center: int, y_center: int):
        self.type.draw(self, surf, x_center, y_center)

    def scoot(self, entity_list: list[Entity]) -> list[Event]:
        events = []

        events += self.type.function(self, entity_list)

        if self.timer <= 1:  # missile runs out of thrust
            events += self.type.explosion(self, entity_list)

        self.timer -= 1

        return events
