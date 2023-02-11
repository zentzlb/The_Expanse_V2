import pygame
import math
import numpy as np
import random as rnd
import time
# from Misc import FindNearest
from Explosions import Particle, ExplosionDamage

"""BULLET CLASS"""

class Bullet(pygame.Rect):
    def __init__(self, x, y, angle, bullet_type, faction, gs):
        self.bullet_type = bullet_type
        if bullet_type.sound is not None:
            bullet_type.sound.play()
        super().__init__(x, y, bullet_type.width, bullet_type.height)
        self.angle = angle
        self.velocity = bullet_type.velocity
        self.range = bullet_type.range
        self.damage = bullet_type.damage
        self.targets = []
        self.timer = self.range / self.velocity
        self.fx = x
        self.fy = y
        self.image = pygame.transform.rotate(bullet_type.image, angle)
        self.faction = faction
        self.build_target_list(gs)

    def draw(self, gs):
        self.bullet_type.draw(self, gs)

    def build_target_list(self, gs):
        R2 = self.range * self.range
        for faction in range(len(gs.ships)):
            if faction != self.faction:
                if self.bullet_type.targets_missiles:
                    for missile in gs.missiles[faction]:
                        dx = self.centerx - missile.centerx
                        dy = self.centerx - missile.centerx
                        r2 = dx * dx + dy * dy
                        if r2 < 9 * R2:
                            self.targets.append(missile)
                for ship in gs.ships[faction]:
                    dx = self.centerx - ship.centerx
                    dy = self.centerx - ship.centerx
                    r2 = dx * dx + dy * dy
                    if r2 < 9 * R2:
                        self.targets.append(ship)

    def scoot(self, gs):
        self.fx += self.velocity * math.sin(self.angle * math.pi / 180)
        self.fy += self.velocity * math.cos(self.angle * math.pi / 180)

        self.x = round(self.fx)
        self.y = round(self.fy)

        # if self.collidelist(gs.targets[self.faction]) != -1:  # bullet hits red
        if self.collidelist(self.targets) != -1:
            dmgList = self.collidelistall(self.targets)
            self.bullet_type.function(self, gs, dmgList)
        # elif self.timer > self.range / self.velocity:  # missile runs out of thrust
        #     gs.bullets[self.faction].remove(self)
        self.timer -= 1


"""MISSILE CLASS"""


class Missile(pygame.Rect):
    def __init__(self, x, y, angle, height, width, missile_type, target, faction, gs):
        if missile_type.sound is not None:
            missile_type.sound.play()#.set_volume(0.5)
        super().__init__(x, y, width, height)
        self.angle = angle
        self.velocity = missile_type.velocity
        self.range = missile_type.range
        self.damage = missile_type.damage
        self.exp_damage = missile_type.exp_damage
        self.av = missile_type.av
        self.fx = x
        self.fy = y
        self.vx = 0
        self.vy = 0
        self.health = missile_type.health
        self.targets = []
        self.heat = 0
        self.er = missile_type.exp_radius
        self.timer = self.range / self.velocity
        self.arm = self.range / self.velocity - 60
        self.target = target
        self.is_visible = True
        # self.emp = missile_type.emp
        self.image = missile_type.image
        self.missile_type = missile_type
        self.faction = faction

        self.build_target_list(gs)

    def build_target_list(self, gs):
        R2 = 9 * self.range * self.range
        for faction in range(len(gs.ships)):
            if faction != self.faction:
                for ship in gs.ships[faction]:
                    dx = self.centerx - ship.centerx
                    dy = self.centerx - ship.centerx
                    r2 = dx * dx + dy * dy
                    if r2 < R2:
                        self.targets.append(ship)

    def scoot(self, gs):

        for i in range(self.missile_type.par_num):
            R = 255
            G = rnd.randint(0, 255)
            gs.particle_list.append(Particle(self.centerx, self.centery, -rnd.randint(3, 5), self.angle + rnd.randint(-self.missile_type.par_rnd, self.missile_type.par_rnd), 3, (R, G, 0), glow=(R//2, G//2, 0), shrink=0.5))
            gs.particle_list.append(Particle(self.centerx, self.centery, -rnd.randint(2, 3), self.angle + rnd.randint(-self.missile_type.par_rnd+5, self.missile_type.par_rnd+5), 5, (80, 80, 80), shrink=0.9))

        if self.target is None or self.target.health <= 0:
            self.target = FindNearest(self, self.targets)

        if self.target is None:
            # explosion = MissileExplosion(self.centerx, self.centery, gs, self.er)
            # explosion_group.add(explosion)
            self.missile_type.explosion(self, gs, [])
            self.timer = 0
            # gs.missiles[self.faction].remove(self)

        else:
            if self.missile_type.smart:
                vx = self.target.vx
                vy = self.target.vy
                xo = self.target.centerx
                yo = self.target.centery
                velocity = self.velocity

                a = vx ** 2 + vy ** 2 - velocity ** 2
                b = 2 * (vx * (xo - self.centerx) + vy * (yo - self.centery))
                c = (xo - self.centerx) ** 2 + (yo - self.centery) ** 2

                t = (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
                x = xo + vx * t
                y = yo + vy * t

                dx = x - self.centerx
                dy = y - self.centery

                cos = math.cos(self.angle * math.pi / 180)
                sin = math.sin(self.angle * math.pi / 180)

                Q = np.array([[cos, -sin], [sin, cos]])
                V = np.array([[dx], [dy]])
                V_prime = Q.dot(V)
                da = -math.atan2(V_prime[0][0], V_prime[1][0])

            elif self.missile_type.drunk:
                da = 400 * np.cross((math.sin(self.angle * math.pi / 180), math.cos(self.angle * math.pi / 180), 0),
                              (self.target.centerx - self.centerx, self.target.centery - self.centery, 0))[2] / min([((self.target.centerx - self.centerx) ** 2 + (self.target.centery - self.centery) ** 2 + 1), (self.range / 2) ** 2]) + math.sin(self.timer / 10) + 2 * rnd.random() - 1
                # print(min([((self.target.centerx - self.centerx) ** 2 + (self.target.centery - self.centery) ** 2 + 1), self.range ** 2]))
            else:
                da = np.cross((math.sin(self.angle * math.pi / 180), math.cos(self.angle * math.pi / 180), 0),
                                      (self.target.centerx - self.centerx, self.target.centery - self.centery, 0))[2]
            if da > 0:
                self.angle -= self.av
            else:
                self.angle += self.av

        self.vx = self.velocity * math.sin(self.angle * math.pi / 180)
        self.vy = self.velocity * math.cos(self.angle * math.pi / 180)

        self.fx += self.vx
        self.fy += self.vy

        self.x = round(self.fx)
        self.y = round(self.fy)

        if self.collidelist(self.targets) != -1 and self.timer < self.arm:  # missile hits target
            dmgList = self.collidelistall(self.targets)
            self.missile_type.explosion(self, gs, dmgList)
            self.health = 0
            # ExplosionDamage(self.exp_damage, self.centerx, self.centery, self.er, gs.targets[self.faction], gs)
            # gs.missiles[self.faction].remove(self)

        elif self.timer <= 1:  # missile runs out of thrust
            # explosion = MissileExplosion(self.centerx, self.centery, gs, self.er)
            # explosion_group.add(explosion)
            self.missile_type.explosion(self, gs, [])
            # ExplosionDamage(self.exp_damage, self.centerx, self.centery, self.er, gs.targets[self.faction], gs)
            # gs.missiles[self.faction].remove(self)
        self.timer -= 1

class Mine(pygame.Rect):
    def __init__(self, x, y, angle, height, width, mine_type, target, faction):
        if mine_type.sound is not None:
            mine_type.sound.play()
        super().__init__(x, y, mine_type.width, mine_type.height)
        self.center = (x, y)
        self.damage = mine_type.damage
        self.er = mine_type.exp_radius
        self.exp_damage = mine_type.exp_damage
        self.pen = mine_type.pen
        self.timer = mine_type.time
        self.arm = mine_type.time - mine_type.arm
        self.health = mine_type.health
        self.heat = 0
        self.exptype = None
        self.is_visible = True
        self.grav = True
        self.fx = x
        self.fy = y
        self.vx = 0
        self.vy = 0
        self.angle = 0
        self.image = mine_type.image
        self.mine_type = mine_type
        self.faction = faction

    def scoot(self, gs):

        self.mine_type.function(self, gs)

        if self.timer <= 1:  # missile runs out of thrust
            # gs.missiles[self.faction].remove(self)
            if self.mine_type.explosion is not None:
                self.mine_type.explosion(self, gs)

        self.timer -= 1


def FindNearest(ship, target_list):
    if len(target_list) > 0:
        # d = []
        ind = 0
        min_r2 = math.inf
        rng2 = ship.range * ship.range
        for i in range(len(target_list)):
            target = target_list[i]
            dx = target.centerx - ship.centerx
            dy = target.centery - ship.centery

            r2 = dx * dx + dy * dy
            a = target.is_visible and r2 < rng2  # is uncloaked and within radar range
            b = r2 < 2250000  # is within visual range
            c = r2 < min_r2


            if c and (a or b):  # and target.health > 0:  # only add ships to the target list if they're visible
                min_r2 = r2
                ind = i
            # else:
            #     d.append(math.inf)
        if min_r2 < math.inf:
            return target_list[ind]
        else:
            return None
    else:
        return None
