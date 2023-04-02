import os
import pygame
import random as rnd
import math
from Explosions import Particle, ExplosionDamage, trans_circle, glow_circle, PhotonExplosion, PAExplosion, OrbExplosion

pygame.mixer.init()


def explosion(self, gs, dmgList):
    for i in dmgList:
        self.targets[i].health -= self.damage
        self.targets[i].heat += self.damage

    for i in range(100):
        c = rnd.randint(100, 200)
        gs.particle_list2.append(Particle(self.centerx, self.centery, -rnd.randint(1, self.er // 20),
                                          rnd.randint(0, 360), 10,
                                          (c + 50, c, 100), shrink=0.5))

    ExplosionDamage(self.exp_damage, self.centerx, self.centery, self.er, self.targets, gs)


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
        gs.particle_list2.append(Particle(self.centerx, self.centery, -rnd.randint(1, self.er // 20),
                                          rnd.randint(0, 360), 10,
                                          (c + 50, c, 100), shrink=0.5))

    ExplosionDamage(self.exp_damage, self.centerx, self.centery, self.er, self.targets, gs)


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
    ExplosionDamage(self.exp_damage, self.centerx, self.centery, self.er, self.targets, gs)


def draw_missile(missile, gs):
    image = pygame.transform.rotate(missile.image, missile.angle)
    gs.WIN.blit(image, (missile.x - gs.x, missile.y - gs.y))


def draw_circ(missile, gs):
    x1 = missile.x - gs.x
    y1 = missile.y - gs.y
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


Seeker = {'velocity': 5.25,  # adj
          'av': 0.4,  # adj
          'damage': 10,
          'exp_damage': 20,
          'exp_radius': 100,
          'energy': 200,
          'range': 8000,
          'health': 3,
          'delay': 400,  # adj
          'height': 12,
          'width': 12,
          'drunk': False,
          'smart': False,
          'par_num': 1,
          'par_rnd': 0,
          'cost': {},
          'name': "Seeker",
          'image': pygame.image.load(os.path.join('Assets', 'smallmissile1.png')),
          'sound': pygame.mixer.Sound('Assets//missile_launch.mp3'),
          'explosion': explosion,
          'draw': draw_missile}

EMPMissile = {'velocity': 4.25,  # adj
              'av': 0.25,  # adj
              'damage': 10,
              'exp_damage': 85,
              'exp_radius': 200,
              'energy': 250,
              'range': 3000,
              'health': 10,
              'delay': 500,  # adj
              'height': 15,
              'width': 15,
              'drunk': False,
              'smart': False,
              'par_num': 2,
              'par_rnd': 70,
              'cost': {},
              'name': "EMP Missile",
              'image': pygame.image.load(os.path.join('Assets', 'torpedo.png')),
              'sound': pygame.mixer.Sound('Assets//missile_launch.mp3'),
              'explosion': emp_explosion,
              'draw': draw_missile}

SwarmMissile = {'velocity': 4.5,  # adj
                'av': 1.25,  # adj
                'damage': 15,
                'exp_damage': 10,
                'exp_radius': 50,
                'energy': 180,
                'range': 4500,
                'health': 4,
                'delay': 180,  # adj
                'height': 10,
                'width': 10,
                'drunk': True,
                'smart': False,
                'par_num': 1,
                'par_rnd': 40,
                'cost': {},
                'name': "Swarm Missile",
                'image': pygame.image.load(os.path.join('Assets', 'swarm_missile.png')),
                'sound': pygame.mixer.Sound('Assets//missile_launch.mp3'),
                'explosion': explosion,
                'draw': draw_missile}

SmartMissile = {'velocity': 5.5,
                'av': 0.3,  # adj
                'damage': 10,
                'exp_damage': 15,
                'exp_radius': 80,
                'energy': 220,
                'range': 15000,
                'health': 3,
                'delay': 480,  # adj
                'height': 12,
                'width': 12,
                'drunk': False,
                'smart': True,
                'par_num': 1,
                'par_rnd': 0,
                'cost': {},
                'name': "Smart Missile",
                'image': pygame.image.load(os.path.join('Assets', 'smartmissile.png')),
                'sound': pygame.mixer.Sound('Assets//missile_launch.mp3'),
                'explosion': explosion,
                'draw': draw_missile}

IonOrb = {'velocity': 4.5,  # adj
          'av': 1,  # adj
          'damage': 20,
          'exp_damage': 0,
          'exp_radius': 0,
          'energy': 180,
          'range': 4000,
          'health': 3,
          'delay': 360,  # adj
          'height': 10,
          'width': 10,
          'drunk': False,
          'smart': False,
          'par_num': 0,
          'par_rnd': 0,
          'cost': {},
          'name': "Ion Orb",
          'image': pygame.image.load(os.path.join('Assets', 'Ion_Orb.png')),
          'sound': pygame.mixer.Sound('Assets//missile_launch.mp3'),
          'explosion': HeatOrb,
          'draw': draw_orb}

PhotonTorpedo = {'velocity': 4,  # adj
                 'av': 1.2,  # adj
                 'damage': 20,
                 'exp_damage': 5,
                 'exp_radius': 50,
                 'energy': 180,
                 'range': 3250,
                 'health': 3,
                 'delay': 360,  # adj
                 'height': 10,
                 'width': 10,
                 'drunk': False,
                 'smart': False,
                 'par_num': 0,
                 'par_rnd': 0,
                 'cost': {},
                 'name': "Photon Torpedo",
                 'image': pygame.image.load(os.path.join('Assets', 'photon_torpedo.png')),
                 'sound': pygame.mixer.Sound('Assets//missile_launch.mp3'),
                 'explosion': photon_explosion,
                 'draw': draw_circ}

MissileNames = [Seeker, EMPMissile, SwarmMissile, SmartMissile, IonOrb, PhotonTorpedo]
