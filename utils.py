import math 
from Data.Types import Entity, Vessel, Shooter, Projectile, Beam
import numpy as np
import numpy.typing as npt


def beam_collision(x: float, y: float, range_: float, angle: float, entity_list: list[Entity]) \
        -> tuple[npt.NDArray, Entity | None]:
    target = None
    dp2 = range_ * np.array([math.sin(angle * math.pi / 180), math.cos(angle * math.pi / 180)])
    R2 = range_ * range_
    root2 = math.sqrt(2)
    for entity in entity_list:
        dx = entity.centerx - x
        dy = entity.centery - y
        r2 = dx * dx + dy * dy
        if r2 < R2:
            dr = np.array([dx, dy])
            target_angle = math.acos(min((np.dot(dp2, dr) / math.sqrt(r2 * R2), 1)))
            r = math.sqrt(r2)
            if r * math.sin(target_angle) < entity.height / root2:
                target = entity
                R2 = r2
                R = r
                dp2 = R * np.array([math.sin(angle * math.pi / 180), math.cos(angle * math.pi / 180)])
    return np.array([x, y]) + dp2, target


def FindNearest(ship: Shooter | Projectile, target_list: list[Entity]) -> int | None:
    if len(target_list) > 0:
        # d = []
        ind = 0
        min_r2 = math.inf
        rng2 = ship.range * ship.range
        for target in target_list:
            dx = target.centerx - ship.centerx
            dy = target.centery - ship.centery

            r2 = dx * dx + dy * dy
            a = target.is_visible and r2 < rng2  # is uncloaked and within radar range
            b = r2 < 2250000  # is within visual range
            c = r2 < min_r2  # target.health > 0
            d = target.width > 200

            if d or c and (a or b):  # and target.health > 0:  # only add ships to the target list if they're visible
                min_r2 = r2
                ind = target
            # else:
            #     d.append(math.inf)
        if min_r2 < math.inf:
            return ind
        else:
            return None
    else:
        return None


def FindMineable(ship: Shooter, target_list: list[Entity]) -> Entity | None:
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
            a = sum(
                target.ore.values()) > 0 and r2 < rng2  # is uncloaked and within radar range  target.is_visible and  and
            # b = r2 < 2250000  # is within visual range
            c = r2 < min_r2

            if c and a:  # and target.health > 0:  # only add ships to the target list if they're visible
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


"""TARGETING COMPUTER LOGIC"""


def TargetingComputer(ship: Shooter) -> tuple[float, float, float]:
    pos = ship.Qt.dot(ship.bullet_pos) - np.array([ship.bullet.width // 2, ship.bullet.height // 2])

    if (bullet_velocity := ship.bullet.velocity) != math.inf:

        vx = ship.target.vx - ship.vx
        vy = ship.target.vy - ship.vy
        xo = ship.target.centerx - ship.centerx - pos[0]
        yo = ship.target.centery - ship.centery - pos[1]
        a = vx * vx + vy * vy - bullet_velocity * bullet_velocity
        b = 2 * (vx * xo + vy * yo)
        c = xo * xo + yo * yo

        if a < 0:
            t = (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)
        elif a > 0 and b * b - 4 * a * c > 0:
            t1 = (-b + math.sqrt(b * b - 4 * a * c)) / (2 * a)
            t2 = (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)
            t_list = [t1, t2, math.inf]
            val = min([t for t in t_list if t > 0])
            if val != math.inf:
                t = val
            else:
                t = -1
        elif b != 0:
            t = -c / b
        else:
            t = -1

        if t > 0:
            x = xo + vx * t
            y = yo + vy * t
            r = math.sqrt(x * x + y * y)
        else:
            x = math.inf
            y = math.inf
            r = math.inf

    else:
        x = ship.target.centerx - pos[0] - ship.centerx
        y = ship.target.centery - pos[1] - ship.centery
        r = math.sqrt(x * x + y * y)

    if r < ship.bullet_types[ship.bullet_sel].range:
        angle2 = math.atan2(y, x)
        in_rng = True
    else:
        angle2 = math.atan2(ship.target.centery - ship.centery, ship.target.centerx - ship.centerx)
        in_rng = False

    return angle2, in_rng, r
