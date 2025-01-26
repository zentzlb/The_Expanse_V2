import pygame
import typing
import numpy as np
import math
from abc import ABC, abstractmethod
import random as rnd
from pygame.locals import BLEND_RGB_ADD

COLOR3: typing.TypeAlias = tuple[int, int, int]
COLOR4: typing.TypeAlias = tuple[int, int, int, int]


def trans_circle(display: pygame.Surface, x: float, y: float, radius: float, color: COLOR4):
    """
    creates transparent circle on surface object
    :param display: surface
    :param x: x pos
    :param y: y pos
    :param radius: circle radius
    :param color: color with alpha
    """
    surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
    pygame.draw.circle(surf, color, (radius, radius), radius)
    display.blit(surf, (x - radius, y - radius))


def glow_circle(display: pygame.Surface, x: float, y: float, radius: float, color: COLOR3 | COLOR4):
    """
    creates glow circle on surface object
    :param display: surface
    :param x: x pos
    :param y: y pos
    :param radius: circle radius
    :param color: color with alpha
    """
    surf = pygame.Surface((radius * 2, radius * 2))
    surf.set_colorkey((0, 0, 0))
    pygame.draw.circle(surf, color, (radius, radius), radius)
    display.blit(surf, (x - radius, y - radius), special_flags=BLEND_RGB_ADD)


def glow_ring(display: pygame.Surface, x: float, y: float, radius: float, color: COLOR4, width: int):
    """
    creates glow ring on surface object
    :param display: surface
    :param x: x pos
    :param y: y pos
    :param radius: circle radius
    :param color: color with alpha
    :param width: ring width
    """
    surf = pygame.Surface((radius * 2, radius * 2))
    surf.set_colorkey((0, 0, 0))
    pygame.draw.circle(surf, color, (radius, radius), radius, width=width)
    display.blit(surf, (x - radius, y - radius), special_flags=BLEND_RGB_ADD)


class Event(ABC):
    x: float
    y: float

    def __str__(self):
        return f"{self.__class__.__name__}({self.x:0.1f}, {self.y:0.1f})"

    def __repr__(self):
        return self.__str__()

    @abstractmethod
    def scoot(self) -> bool:
        """
        updates event
        """
        raise NotImplementedError

    @abstractmethod
    def draw(self, *args, **kwargs) -> None:
        """
        render event
        """
        raise NotImplementedError


class PlasmaExplosion(Event):
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.timer = 50

    def scoot(self):
        self.timer -= 1
        return self.timer > 0

    def draw(self, surf: pygame.surface, x_off: float, y_off: float):
        # save images ahead of time
        for r in range(self.timer):
            glow_circle(surf, self.x - x_off, self.y - y_off, r, (4, 0, 5))


class Beam(Event):
    def __init__(self, x: float, y: float, x2: float, y2: float, width: int, color: COLOR3):
        self.x = x
        self.y = y
        self.x2 = x2
        self.y2 = y2
        self.width = width
        self.color = color
        self.timer = 2

    def scoot(self) -> bool:
        self.timer -= 1
        return self.timer > 0

    def draw(self, surf: pygame.surface, x_off: float, y_off: float) -> None:
        x, x2 = self.x - x_off, self.x2 - x_off
        y, y2 = self.y - y_off, self.y2 - y_off

        pygame.draw.line(surf, self.color, (x, y), (x2, y2), width=self.width)
        glow_circle(surf, x2, y2, rnd.randint(5, 10), (150, 50, 0, 50))
        glow_circle(surf, x, y, rnd.randint(3, 5), (150, 50, 0, 50))


class Particle(Event):
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
        self.fx = x
        self.fy = y
        self.vx = v * math.sin(angle * math.pi / 180) + vx
        self.vy = v * math.cos(angle * math.pi / 180) + vy
        self.color = color
        self.radius = radius
        self.shrink = shrink
        self.glow = glow
        self.show = show

    @property
    def x(self):
        return round(self.fx)

    @property
    def y(self):
        return round(self.fy)

    def scoot(self):
        self.fx += self.vx
        self.fy += self.vy
        if rnd.random() > self.shrink:
            self.radius -= 1

        return self.radius > 0

    def draw(self, surf: pygame.surface, x_off: float, y_off: float):
        pygame.draw.circle(surf, self.color, (self.x - x_off, self.y - y_off), self.radius)
        if self.glow != (0, 0, 0):
            trans_circle(surf, self.x - x_off, self.y - y_off, 2 * self.radius, self.glow)


class Debris(Event):
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

    def scoot(self):
        self.x += self.vx
        self.y += self.vy
        self.angle += self.av
        self.counter -= 1
        return self.counter > 0

    def draw(self, surf: pygame.surface, x_off: float, y_off: float):
        debris = pygame.transform.rotate(self.type.image, self.angle)
        surf.blit(debris, (self.x - x_off, self.y - y_off))


class BackgroundParticle:
    def __init__(self, x: float, y: float, image: pygame.Surface):
        self.x = x
        self.y = y
        self.image = image
        self.height = image.get_height()
        self.width = image.get_width()


class CargoClass(dict):  # inventory class
    def __init__(self):
        super().__init__()
        self.cargo = {}

    @property
    def cargo_total(self):
        return sum(self.cargo.values())

    def __missing__(self, key):
        return 0

    def __str__(self):
        return self.cargo

    def __repr__(self):
        return self.__str__()


class TypeType(ABC):
    name: str

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.__str__()


class ItemType(TypeType):
    cost: dict[str, int]
    draw: typing.Callable[[typing.Any, pygame.Surface, int, int], None]
    range: float


class EntityType(ItemType):
    health: float
    velocity: float


class VesselType(ItemType):
    av: float
    energy: float


class FactionType(TypeType):
    def __init__(self, **kwargs):
        """
        Faction Data
        :param kwargs:
        """
        self.color: COLOR3 = kwargs['color']
        self.name: str = kwargs['name']
        self.image: pygame.Surface = kwargs['image']
        self.ship_images: dict[str, dict[str, pygame.Surface]] = kwargs['ship_images']
        self.channel: dict = kwargs['channel']


class UtilityType(ItemType):
    def __init__(self, **kwargs):
        """
        Utility Type
        :param kwargs:
        """
        self.function: typing.Callable = kwargs['function']
        self.logic: typing.Callable = kwargs['logic']
        self.energy: str = kwargs['energy']
        self.delay: int = kwargs['delay']
        self.description: str = kwargs['description']
        self.cost: dict = kwargs['cost']
        self.name: str = kwargs['name']
        self.draw: str = kwargs['draw']


class BulletType(ItemType):
    def __init__(self, **kwargs):
        """
        Mine Type
        :param kwargs:
        """
        self.velocity: int = kwargs['velocity']
        self.damage: int = kwargs['damage']
        self.exp_damage: int = kwargs['exp_damage']
        self.exp_radius: int = kwargs['exp_radius']
        self.damage: int = kwargs['damage']
        self.energy: int = kwargs['energy']
        self.range: int = kwargs['range']
        self.delay: int = kwargs['delay']
        self.target_types: tuple[type] = kwargs['target_types']
        self.height: int = kwargs['height']
        self.width: int = kwargs['width']
        self.cost: dict = kwargs['cost']
        self.name: str = kwargs['name']
        self.image: pygame.Surface = kwargs['image']
        self.l_image: pygame.Surface = kwargs['l_image']
        self.sound: pygame.mixer.Sound = kwargs['sound']
        self.function: typing.Callable[[Entity, list[Entity], list[int]], list[Event]] = kwargs['function']
        self.init: typing.Callable = kwargs['init']
        self.draw: typing.Callable = kwargs['draw']


class MissileType(ItemType):
    def __init__(self, **kwargs):
        """
        Mine Type
        :param kwargs:
        """
        self.velocity: int = kwargs['velocity']
        self.acc: int = kwargs['acc']
        self.av: float = kwargs['av']
        self.damage: int = kwargs['damage']
        self.exp_damage: int = kwargs['exp_damage']
        self.exp_radius: int = kwargs['exp_radius']
        self.energy: int = kwargs['energy']
        self.range: int = kwargs['range']
        self.health: int = kwargs['health']
        self.delay: int = kwargs['delay']
        self.height: int = kwargs['height']
        self.width: int = kwargs['width']
        self.par_num: int = kwargs['par_num']
        self.par_rnd: int = kwargs['par_rnd']
        self.cost: dict = kwargs['cost']
        self.name: str = kwargs['name']
        self.image: pygame.Surface = kwargs['image']
        self.sound: pygame.mixer.Sound = kwargs['sound']
        self.init: typing.Callable = kwargs['init']
        self.guidance: typing.Callable = kwargs['guidance']
        self.explosion: typing.Callable = kwargs['explosion']
        self.draw: typing.Callable = kwargs['draw']


class MineType(ItemType):
    def __init__(self, **kwargs):
        """
        Mine Type
        :param kwargs:
        """
        self.damage: int = kwargs['damage']
        self.exp_damage: int = kwargs['exp_damage']
        self.exp_radius: int = kwargs['exp_radius']
        self.det_radius: int = kwargs['det_radius']
        self.energy: int = kwargs['energy']
        self.time: int = kwargs['time']
        self.delay: int = kwargs['delay']
        self.arm: int = kwargs['arm']
        self.health: int = kwargs['health']
        self.height: int = kwargs['height']
        self.width: int = kwargs['width']
        self.par_num: int = kwargs['par_num']
        self.par_rnd: int = kwargs['par_rnd']
        self.cost: dict = kwargs['cost']
        self.name: str = kwargs['name']
        self.pen: bool = kwargs['pen']
        self.emp: bool = kwargs['emp']
        self.grav: bool = kwargs['grav']
        self.image: pygame.Surface = kwargs['image']
        self.sound: pygame.mixer.Sound = kwargs['sound']
        self.init: typing.Callable = kwargs['init']
        self.function: typing.Callable = kwargs['function']
        self.explosion: typing.Callable = kwargs['explosion']
        self.draw: typing.Callable = kwargs['draw']


class TurretType(VesselType):
    def __init__(self, **kwargs):
        """
        Station Type
        :param kwargs:
        """
        self.velocity: float = kwargs['velocity']
        self.av: float = kwargs['av']
        self.energy: float = kwargs['energy']
        self.health: float = kwargs['health']
        self.height: int = kwargs['height']
        self.width: int = kwargs['width']
        self.range: float = kwargs['range']
        self.bullet_types: list[BulletType] = kwargs['bullet_types']
        self.missile_types: list[MissileType] = kwargs['missile_types']
        self.targets_missiles: bool = kwargs['targets_missiles']
        self.cost: dict = kwargs['cost']
        self.name: str = kwargs['name']
        self.image: pygame.Surface = kwargs['image']
        self.draw: str = kwargs['draw']


class ShipType(VesselType):
    def __init__(self, **kwargs):
        self.velocity: float = kwargs['velocity']
        self.acc: float = kwargs['acc']
        self.lat: float = kwargs['lat']
        self.rev: float = kwargs['rev']
        self.av: float = kwargs['av']
        self.energy: float = kwargs['energy']
        self.health: float = kwargs['health']
        self.heat_capacity: float = kwargs['heat_capacity']
        self.heat_venting: float = kwargs['heat_venting']
        self.height: int = kwargs['height']
        self.width: int = kwargs['width']
        self.range: float = kwargs['range']
        self.turrets: list = kwargs['turrets']
        self.thrust_pos: list[np.ndarray] = kwargs['thrust_pos']
        self.turret_pos: list[np.ndarray] = kwargs['turret_pos']
        self.description: str = kwargs['description']
        self.bullet_pos: list[np.ndarray] = kwargs['bullet_pos']
        self.missile_pos: list[np.ndarray] = kwargs['missile_pos']
        self.emblem_pos: list[np.ndarray] = kwargs['emblem_pos']
        self.primary: int = kwargs['primary']
        self.secondary: int = kwargs['secondary']
        self.mine: int = kwargs['mine']
        self.utility: int = kwargs['utility']
        self.cargo_cap: int = kwargs['cargo_cap']
        self.cost: dict = kwargs['cost']
        self.name: str = kwargs['name']
        self.draw: str = kwargs['draw']


class StationType(VesselType):
    def __init__(self, **kwargs):
        """
        Station Type
        :param kwargs:
        """
        self.velocity: int = kwargs['velocity']
        self.energy: int = kwargs['energy']
        self.health: int = kwargs['health']
        self.height: int = kwargs['height']
        self.width: int = kwargs['width']
        self.turrets: list = kwargs['turrets']
        self.turret_pos: list = kwargs['turret_pos']
        self.image: pygame.Surface = kwargs['image']
        self.cost: dict = kwargs['cost']
        self.name: str = kwargs['name']
        self.draw: str = kwargs['draw']


class DebrisType(TypeType):
    def __init__(self, **kwargs):
        """
        Debris Type
        :param kwargs:
        """
        self.av: int = kwargs['av']
        self.time: int = kwargs['time']
        self.image: pygame.Surface = kwargs['image']
        self.name: str = kwargs['name']


class State(ABC):

    @abstractmethod
    def update(self, *arg, **kwargs):
        """Updates State object by frame."""
        raise NotImplementedError


class Entity(pygame.FRect):
    health: float
    heat: float
    vx: float
    vy: float
    angle: float
    id: str
    type: EntityType

    def __sub__(self, other: float) -> list[Event]:
        self.health -= other
        return []

    @property
    def name(self) -> str:
        """
        returns name of type
        """
        return self.type.name

    @property
    def max_health(self):
        return self.type.health

    @property
    def velocity(self):
        return self.type.velocity

    @abstractmethod
    def scoot(self, entity_list: list[typing.Self]) -> list[Event]:
        """Updates Entity's position and status by frame."""
        raise NotImplementedError

    @abstractmethod
    def draw(self, *args, **kwargs) -> None:
        """
        Draws object on game window.
        """
        raise NotImplementedError

    @property
    def speed(self):
        """
        speed of projectile
        :return:
        """
        return math.sqrt(self.vx * self.vx + self.vy * self.vy)

    @speed.setter
    def speed(self, value: float):
        ratio = value / self.speed
        self.vx *= ratio
        self.vy *= ratio

    @property
    def radians(self):
        return self.angle * math.pi / 180

    @property
    def Q(self) -> np.ndarray:
        """
        forward transformation matrix
        :return: array
        """
        cos = math.cos(self.radians)
        sin = math.sin(self.radians)
        return np.array([[cos, -sin], [sin, cos]])

    @property
    def Qt(self) -> np.ndarray:
        """
        reverse transformation matrix
        :return: array
        """
        return self.Q.transpose()

    @property
    def cx(self) -> int:
        """
        integer center x
        :return: int
        """
        return round(self.centerx)

    @property
    def cy(self) -> int:
        """
        integer center x
        :return: int
        """
        return round(self.centery)

    @property
    def ix(self) -> int:
        """
        integer x position
        :return: int
        """
        return round(self.x)

    @property
    def iy(self) -> int:
        """
        integer y position
        :return: int
        """
        return round(self.y)

    @property
    def iwidth(self) -> int:
        """
        integer width
        :return: int
        """
        return round(self.width)

    @property
    def iheight(self) -> int:
        """
        integer height
        :return: int
        """
        return round(self.height)

    @property
    def range(self):
        return self.type.range

    @property
    def is_visible(self):
        return True

    @property
    def faction_name(self) -> str:
        """
        returns name of faction allegiance
        """
        return ''


class GlobalStateInt(State):
    radio: dict
    size: tuple[int, int]
    entities: list[Entity]
    events: list[Event]
    lines: list
    explosion_group = pygame.sprite.Group

    @abstractmethod
    def generate_id(self, ids: set[str], celestial: Entity):
        """
        generates IDs
        :param ids: set of IDs
        :param celestial: object
        """
        raise NotImplementedError


class LocalStateInt(State):
    player: Entity | None
    x: int
    y: int
    cx: int
    cy: int
    height: int
    width: int
    lines: list
    fonts: list[pygame.font.SysFont]
    menu: typing.Any
    mining_sound: pygame.mixer.Sound
    mining: pygame.mixer.Channel
    WIN: pygame.Surface
    images: dict[str, pygame.Surface]
    misc_info: dict
    Factions: dict[FactionType]
    faction_names: list[str]
    ShipTypes: dict[str, ShipType]
    ship_names: list[str]
    StationTypes: dict[str, StationType]
    TurretTypes: dict[str, TurretType]
    BulletTypes: dict[str, BulletType]
    MissileTypes: dict[str, MissileType]
    MineTypes: dict[str, MineType]
    UtilTypes: dict[str, UtilityType]
    DebrisTypes: dict[str, DebrisType]
    SPACE: pygame.Surface
    dust: list[pygame.Surface]
    field: list[pygame.Surface]
    dust_images: list[pygame.Surface]
    FIELD: list[pygame.Surface]

    @abstractmethod
    def play_mining(self, volume: float = 1.0):
        """
        plays mining sound
        :param volume: volume
        """
        raise NotImplementedError

    @abstractmethod
    def load_images(self, rootdir: str):
        """
        load images from rootdir
        :param rootdir: root directory
        """
        raise NotImplementedError

    @abstractmethod
    def make_faction_ships(self):
        """
        makes ships
        """
        raise NotImplementedError

    @abstractmethod
    def player_commands(self):
        """
        gets player commands
        """
        raise NotImplementedError


class Projectile(Entity):
    type: BulletType | MissileType | MineType
    faction: FactionType
    image: pygame.Surface

    def scoot(self, entity_list: list[Entity]) -> tuple[Event]:
        """
        updates vessel by frame
        :param entity_list: list of other game entities
        :return: list of events
        """
        pass

    @property
    def damage(self):
        return self.type.damage

    @property
    def exp_damage(self):
        return self.type.exp_damage

    @property
    def exp_radius(self):
        return self.type.exp_radius

    @property
    def faction_name(self) -> str:
        """
        returns name of faction allegiance
        """
        return self.faction.name

    def draw(self, *args, **kwargs) -> None:
        self.type.draw(self, *args, **kwargs)


class Guided(Projectile):
    type: MissileType

    @property
    def av(self):
        return self.type.av

    @property
    def acc(self):
        return self.type.acc


class Vessel(Entity):
    type: VesselType
    heat: float
    av: float
    acc: float
    energy: float
    target: Entity | None
    image: pygame.Surface
    turrets: typing.Self
    faction: FactionType

    @property
    def max_energy(self):
        return self.type.energy

    @property
    def heat_cap(self):
        return 1

    @property
    def av(self):
        return self.type.av

    @property
    def faction_name(self) -> str:
        """
        returns name of faction allegiance
        """
        return self.faction.name

    def refresh(self):
        """
        updates Vessel
        """
        pass

    def scoot(self, entity_list: list[Entity]) -> tuple[Event]:
        """
        updates vessel by frame
        :param entity_list: list of other game entities
        :return: list of events
        """
        pass

    def draw(self, *args, **kwargs) -> None:
        self.type.draw(self, *args, **kwargs)


class Shooter(Vessel):
    counter: int
    bulletC: int
    missileC: int
    utilC: int

    bullet_sel: int
    missile_sel: int
    mine_sel: int
    util_sel: int

    bullet_types: list[BulletType]
    missile_types: list[MissileType]
    mine_types: list[MineType]
    util_types: list[UtilityType]

    @property
    def bullet(self) -> BulletType:
        return self.bullet_types[self.bullet_sel]

    @property
    def missile(self) -> MissileType:
        return self.missile_types[self.missile_sel]

    @property
    def mine(self) -> MineType:
        return self.mine_types[self.mine_sel]

    @property
    def utility(self) -> UtilityType:
        return self.util_types[self.util_sel]

    @property
    def bullet_pos(self) -> np.ndarray:
        return np.array([0, 0])

    @property
    def missile_pos(self) -> np.ndarray:
        return np.array([0, 0])

