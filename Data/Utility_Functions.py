import math
import random as rnd
import pygame
import os
from pygame.locals import BLEND_RGB_ADD
from Data.Types import Particle


class Field:
    def __init__(self, x, y, ship, vx, vy, image_key, dr, rng, faction, gs):
        self.image_key = image_key
        self.vx = vx
        self.vy = vy
        self.range = rng
        self.dr = dr
        self.r = 0
        self.width = 0
        self.height = 0
        self.timer = 1
        self.targets = []
        self.x = x
        self.y = y
        self.centerx = x
        self.centery = y
        self.fx = x
        self.fy = y
        self.faction = faction
        self.ship = ship
        self.build_target_list(gs)

    def draw(self, gs):
        image = gs.images[self.image_key][self.r-1]
        x = self.x - gs.x - image.get_width() // 2
        y = self.y - gs.y - image.get_height() // 2
        gs.WIN.blit(image, (x, y), special_flags=BLEND_RGB_ADD)
        # self.bullet_type.draw(self, gs)

    def build_target_list(self, gs):
        R2 = self.range * self.range
        for faction in range(len(gs.ships)):
            if faction != self.faction:
                for ship in gs.ships[faction]:
                    dx = self.x - ship.centerx
                    dy = self.y - ship.centery
                    r2 = dx * dx + dy * dy
                    if r2 < 9 * R2:
                        self.targets.append(ship)

    def scoot(self, gs):
        self.fx += self.vx
        self.fy += self.vy
        self.x = round(self.fx)
        self.y = round(self.fy)
        self.centerx = self.x
        self.centery = self.y

        for ship in self.targets:
            dx = ship.centerx - self.centerx
            dy = ship.centery - self.centery
            r = math.sqrt(dx * dx + dy * dy)
            if abs(r - self.r) < ship.height // 2:
                x = dx / r
                y = dy / r

                ship.vx += x * 1.0
                ship.vy = y * 1.0
                # ship.angle += rnd.randint(-1, 1) * 5

        if self.r <= self.range - self.dr:
            self.r += self.dr
            self.width = self.r
            self.height = self.r
        else:
            self.timer = 0


def auto_loader(ship, gs, commands, faction):
    if ship.missileC > 1 and ship.energy > 1:
        ship.missileC -= 1
        ship.energy -= 0.5  # adj


def use_auto_loader(ship, gs, commands, faction):
    if ship.energy > ship.type.energy * 0.4 and ship.missileC > 0:
        return 1
    else:
        return 0


def jump_drive(ship, gs, commands, faction):
    if ship.energy > ship.height * 3:
        ship.energy -= ship.height * 3
        for i in range(0, 120, 4):
            gs.particle_list.append(
                Particle(
                    ship.centerx + ship.vx * i, ship.centery + ship.vy * i, 1, rnd.randint(0, 360), 1,
                         (220, 220, 255), shrink=0.99, glow=(100, 100, 150)))
        ship.x = ship.x + ship.vx * 120  # adj
        ship.y = ship.y + ship.vy * 120  # adj


def use_jump_drive(ship, gs, commands, faction):
    if ship.energy > ship.height * 3 and ship.vx * ship.vx + ship.vy * ship.vy > 1:
        # print('called')
        R2 = 4 * ship.height * ship.width
        for f in range(len(gs.missiles)):
            if f != faction:
                for missile in gs.missiles[f]:
                    dx = ship.centerx - missile.centerx
                    dy = ship.centery - missile.centery
                    r2 = dx * dx + dy * dy
                    if r2 < R2:
                        # print('jumped missile')
                        return 1
                for bullet in gs.bullets[f]:
                    dx = ship.centerx - bullet.centerx
                    dy = ship.centery - bullet.centery
                    r2 = dx * dx + dy * dy
                    if r2 < R2:
                        # print('jumped bullet')
                        return 1
    return 0


def null(ship, gs, commands, faction):
    return 0


def cloak(ship, gs, commands, faction):
    if ship.cloaked:
        ship.cloaked = False
        ship.image.set_alpha(255)
    elif ship.energy > 100:
        ship.cloaked = True
        ship.image.set_alpha(100)
        ship.energy -= 100


def overload_reactor(ship, gs, commands, faction):
    if ship.energy < ship.type.energy:
        ship.heat += 0.25  # adj
        ship.energy += 0.25  # adj


def use_overload_reactor(ship, gs, commands, faction):
    if ship.energy < ship.type.energy * 0.9 and ship.heat < ship.type.heat_capacity * 0.8:
        return 1
    else:
        return 0


def heat_sink(ship, gs, commands, faction):
    if ship.heat < ship.type.heat_capacity and ship.energy >= 1:
        ship.heat -= 0.1  # adj
        ship.energy -= 0.5  # adj


def use_heat_sink(ship, gs, commands, faction):
    if ship.heat > ship.type.heat_capacity * 0.8 or (ship.energy < ship.type.energy * 0.9 and ship.heat > 0):
        return 1
    else:
        return 0


def repulsor(ship, gs, commands, faction):
    if ship.energy >= 200:
        wave = Field(ship.centerx, ship.centery, ship, ship.vx, ship.vy, 'GravityRepulsor', 3, 600, faction, gs)
        gs.bullets[faction].append(wave)
        ship.energy -= 200


def use_repulsor(ship, gs, commands, faction):
    return 0


