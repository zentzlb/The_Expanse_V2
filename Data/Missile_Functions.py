from Explosions import ExplosionDamage, PhotonExplosion, OrbExplosion
from Data.Types import Particle, glow_circle, Shooter, Entity, Event
from Weapon_Class import Missile
import numpy as np
import random as rnd
import math
import pygame


def init_missile(ship: Shooter, entity_list: list[Entity]) -> list[Event]:
    (x, y) = ship.center + ship.Qt.dot(ship.missile_pos) - np.array([ship.missile.width // 2, ship.missile.height // 2])
    missile = Missile(x, y, ship, ship.angle, ship.missile, ship.target, vx=ship.vx, vy=ship.vy)
    entity_list.append(missile)
    return []


def init_swarm(ship: Shooter, entity_list: list[Entity]) -> list[Event]:
    (x, y) = ship.center + ship.Qt.dot(ship.missile_pos) - np.array([ship.missile.width / 2, ship.missile.height / 2])
    for _ in range(4):
        v = 4 * rnd.random() + ship.missile.velocity - 4
        if ship.missile_pos[0] > 0:
            angle = math.pi / 2
        elif ship.missile_pos[0] < 0:
            angle = -math.pi / 2
        else:
            angle = (0.5 - rnd.randint(0, 1)) * math.pi

        vx = v * math.sin(ship.radians + angle)
        vy = v * math.cos(ship.radians + angle)

        missile = Missile(x, y, ship, ship.angle, ship.missile, ship.target, vx=ship.vx + vx, vy=ship.vy + vy)
        entity_list.append(missile)
    return []


def dumb_guidance(self: Missile):
    da = np.cross((math.sin(self.angle * math.pi / 180), math.cos(self.angle * math.pi / 180), 0),
                  (self.target.centerx - self.centerx, self.target.centery - self.centery, 0))[2]
    if da > 0:
        self.angle -= self.av
    else:
        self.angle += self.av
    self.vx = self.velocity * math.sin(self.angle * math.pi / 180)
    self.vy = self.velocity * math.cos(self.angle * math.pi / 180)


def drunk_guidance(self: Missile):
    da = (400 * np.cross((math.sin(self.angle * math.pi / 180), math.cos(self.angle * math.pi / 180), 0),
                         (self.target.centerx - self.centerx, self.target.centery - self.centery, 0))[2] /
          min([((self.target.centerx - self.centerx) ** 2 + (self.target.centery - self.centery) ** 2 + 1),
               (self.range / 2) ** 2]) + math.sin(self.timer / 10) + 2 * rnd.random() - 1)
    if da > 0:
        self.angle -= self.av
    else:
        self.angle += self.av
    self.vx = self.velocity * math.sin(self.angle * math.pi / 180)
    self.vy = self.velocity * math.cos(self.angle * math.pi / 180)


def smart_guidance(self: Missile):
    commands = {'thrust': True, 'rotate': 0}
    vx = self.target.vx
    vy = self.target.vy
    xo = self.target.centerx
    yo = self.target.centery
    velocity = self.velocity

    a = vx * vx + vy * vy - velocity * velocity
    b = 2 * (vx * (xo - self.centerx) + vy * (yo - self.centery))
    c = (xo - self.centerx) ** 2 + (yo - self.centery) ** 2

    t = (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    x = xo + vx * t
    y = yo + vy * t

    dx = x - self.centerx
    dy = y - self.centery

    vector = np.array([[dx], [dy]])
    vector_prime = self.Q.dot(vector)
    da = -math.atan2(vector_prime[0][0], vector_prime[1][0])
    if da > 0:
        commands['rotate'] = -1
    elif da < 0:
        commands['rotate'] = 1

    center1, center2, radius = self.blind_spots
    distance1 = math.sqrt((center1[0]-xo)**2+(center1[1]-yo)**2)
    distance2 = math.sqrt((center2[0] - xo) ** 2 + (center2[1] - yo) ** 2)

    if (distance1 <= radius or distance2 <= radius) and self.timer < self.arm:
        commands["thrust"] = False

    return commands


def sneaker_guidance(self: Missile):
    commands = {'thrust': False, 'rotate': 0}

    if self.timer == self.range / self.velocity and self.speed > self.velocity / 2:  #
        return commands
    commands['thrust'] = True

    vx = self.target.vx
    vy = self.target.vy
    xo = self.target.centerx
    yo = self.target.centery
    velocity = self.velocity

    a = vx * vx + vy * vy - velocity * velocity
    b = 2 * (vx * (xo - self.centerx) + vy * (yo - self.centery))
    c = (xo - self.centerx) ** 2 + (yo - self.centery) ** 2

    t = (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    x = xo + vx * t
    y = yo + vy * t

    dx = x - self.centerx
    dy = y - self.centery

    vector = np.array([[dx], [dy]])
    vector_prime = self.Q.dot(vector)
    da = -math.atan2(vector_prime[0][0], vector_prime[1][0])
    if da > 0:
        commands['rotate'] = -1
    elif da < 0:
        commands['rotate'] = 1
    return commands


def explosion(self: Missile, entity_list: list[Entity], dmg_list: list[int]) -> list[Event]:
    events = []
    for i in dmg_list:
        events += entity_list[i] - self.damage
        entity_list[i].heat += self.damage

    events += ExplosionDamage(self.exp_damage, self.centerx, self.centery, self.exp_radius, entity_list)

    return events + [Particle(self.centerx, self.centery, -rnd.randint(1, self.exp_radius // 20),
                              rnd.randint(0, 360), 10,
                              ((c := rnd.randint(100, 200)) + 50, c, 100), shrink=0.5) for
                     _ in range(100)]


def emp_explosion(self, gs, dmgList):
    for i in dmgList:
        self.targets[i].health -= self.damage
        self.targets[i].heat += self.damage
        self.targets[i].energy = 0
        # target_list[i].bulletC += 180
        # target_list[i].missileC += 180
        for turret in self.targets[i].turrets:
            turret.energy = 0
            turret.angle += 120 * rnd.uniform(-1, 1) / math.pi
            # turret.bulletC += 180
            # turret.missileC += 180
    for i in range(150):
        c = rnd.randint(100, 200)
        gs.particle_list2.append(Particle(self.centerx, self.centery, -rnd.randint(1, self.exp_radius // 20),
                                          rnd.randint(0, 360), 10,
                                          (c + 50, c, 100), shrink=0.5))

    ExplosionDamage(self.exp_damage, self.centerx, self.centery, self.exp_radius, self.targets, gs)


def HeatOrb(self, gs, dmgList):
    for i in dmgList:
        self.targets[i].health -= self.damage
        self.targets[i].heat += 4 * self.damage
    if len(dmgList) > 0:
        explosion = OrbExplosion(self.centerx, self.centery, gs, self.targets[dmgList[0]])
    else:
        explosion = OrbExplosion(self.centerx, self.centery, gs)
    gs.particle_list2.append(explosion)


def photon_explosion(self, gs, dmgList):
    for i in dmgList:
        self.targets[i].health -= self.damage
        self.targets[i].heat += self.damage
        dx = self.targets[i].centerx - self.centerx
        dy = self.targets[i].centery - self.centery
        r = math.sqrt(dx * dx + dy * dy)
        self.targets[i].vx += (dx * 50) / (r + 1)
        self.targets[i].vy += (dy * 50) / (r + 1)
        self.targets[i].angle += self.targets[i].av * rnd.randint(-30, 30)
    explosion = PhotonExplosion(self.centerx, self.centery, gs)
    gs.particle_list2.append(explosion)
    ExplosionDamage(self.exp_damage, self.centerx, self.centery, self.exp_radius, self.targets, gs)


def draw_missile(missile: Missile, surf: pygame.Surface, x_center: float, y_center: float):
    x = x_center - missile.image.get_width() // 2
    y = y_center - missile.image.get_height() // 2
    surf.blit(pygame.transform.rotate(missile.image, missile.angle), (x, y))


def draw_circ(missile, gs):
    x1 = missile.centerx - gs.x
    y1 = missile.centery - gs.y
    x2 = x1 + missile.width // 2
    y2 = y1 + missile.height // 2
    gs.WIN.blit(missile.image, (x1, y1))
    glow_circle(gs.WIN, x2, y2, 10, (50, 50, 100))
    glow_circle(gs.WIN, x2, y2, rnd.randint(10, 15), (50, 50, 100))


def draw_orb(missile, gs):
    x1 = missile.x - gs.x
    y1 = missile.y - gs.y
    x2 = x1 + missile.width // 2
    y2 = y1 + missile.height // 2
    image = pygame.transform.rotate(missile.image, rnd.randint(0, 360))
    gs.WIN.blit(image, (x1, y1))
    glow_circle(gs.WIN, x2, y2, rnd.randint(6, 10), (100, 80, 10))
