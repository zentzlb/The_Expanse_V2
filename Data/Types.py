import pygame
import typing
import numpy as np
import math
from abc import ABC, abstractmethod
import random as rnd
from collections import defaultdict
from pygame.locals import BLEND_RGB_ADD

COLOR3: typing.TypeAlias = tuple[int, int, int]
COLOR4: typing.TypeAlias = tuple[int, int, int, int]


def get_attr(*args: str, obj: object, func: typing.Callable) -> float:
    """
    calculates quantity from object attributes and function
    :param args: attribute names
    :param obj: object with attributes
    :param func: function to calculate desired quantity
    :return: desired quantity
    """
    return func(*[obj.__getattribute__(arg) for arg in args])


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


def glow_ring(display: pygame.Surface, x: float, y: float, radius: float, color: COLOR4,
              width: int):
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


class Effect(ABC):
    x: float
    y: float

    def __str__(self):
        return f"{self.__class__.__name__}({self.x:0.1f}, {self.y:0.1f})"

    def __repr__(self):
        return self.__str__()

    @property
    def sound(self):
        return ''

    @abstractmethod
    def scoot(self, entity_list: list["Effect"]) -> list[typing.Self]:
        """
        updates event
        """
        raise NotImplementedError

    @abstractmethod
    def draw(self, *args, **kwargs) -> None:
        """
        render event
        """
        pass


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


class SlotType(ItemType):
    energy: float
    delay: int
    spin_up: int
    function: typing.Callable
    init: typing.Callable

    def __bool__(self):
        return True


class UtilityType(SlotType):
    def __init__(self, **kwargs):
        """
        Utility Type
        :param kwargs:
        """
        self.function: typing.Callable = kwargs['function']
        self.logic: typing.Callable = kwargs['logic']
        self.energy: float = kwargs['energy']
        self.delay: int = kwargs['delay']
        self.description: str = kwargs['description']
        self.cost: dict = kwargs['cost']
        self.name: str = kwargs['name']
        self.draw: str = kwargs['draw']
    @property
    def spin_up(self):
        return 0


class BulletType(SlotType):
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
        self.spin_up: int = kwargs['spin_up']
        self.target_types: tuple[type] = kwargs['target_types']
        self.height: int = kwargs['height']
        self.width: int = kwargs['width']
        self.cost: dict = kwargs['cost']
        self.name: str = kwargs['name']
        self.image: pygame.Surface = kwargs['image']
        self.l_image: pygame.Surface = kwargs['l_image']
        self.sound: pygame.mixer.Sound = kwargs['sound']
        self.function: typing.Callable[
            [Entity, list[Entity], list[int]], list[Effect]] = kwargs['function']
        self.init: typing.Callable = kwargs['init']
        self.draw: typing.Callable = kwargs['draw']


class MissileType(SlotType):
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
        self.ammo: int = kwargs['ammo']
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

    @property
    def spin_up(self):
        return 0


class MineType(SlotType):
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
    @property
    def spin_up(self):
        return 0


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

    def __sub__(self, other: float) -> list[Effect]:
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
    def scoot(self, entity_list: list[typing.Self]) -> list[Effect]:
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

    @radians.setter
    def radians(self, value: float):
        self.angle = value * 180 / math.pi


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
    events: list[Effect]
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

    def scoot(self, entity_list: list[Entity]) -> tuple[Effect]:
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

    def scoot(self, entity_list: list[Entity]) -> tuple[Effect]:
        """
        updates vessel by frame
        :param entity_list: list of other game entities
        :return: list of events
        """
        pass

    def draw(self, *args, **kwargs) -> None:
        self.type.draw(self, *args, **kwargs)


class NullSlot:
    def __init__(self):
        pass
    def __getattr__(self, item):
        return None
    def __bool__(self):
        return False


class Slot:
    def __init__(self, type_: SlotType | None):
        self.type: SlotType | NullSlot = type_ if type_ else NullSlot()
        self.counter: int = 0
        if hasattr(type_, 'ammo'):
            self.ammo = type_.ammo
        else:
            self.ammo: int | float = math.inf

    def __getattr__(self, item):
        return object.__getattribute__(self if item in self.__dict__ else self.type, item)

    def __bool__(self):
        return bool(self.type)

    def __setattr__(self, key, value):
        if key == 'type':
            if hasattr(value, 'ammo'):
                self.ammo = value.ammo
            else:
                self.ammo: int | float = math.inf
        object.__setattr__(self, key, value)

    @property
    def ready(self) -> bool:
        return self.counter + self.type.spin_up <= 0 < self.ammo

    def use(self, shooter: Vessel, entity_list: list[Entity]) -> list[Effect]:
        if type(self.type) is NullSlot:
            return []
        if self.ready and self.energy <= shooter.energy:
            self.ammo -= 1
            shooter.energy -= self.energy
            self.counter = self.delay
            return self.init(shooter, entity_list)
        elif 0 >= self.counter > -self.type.spin_up:
            self.counter -= 2
        return []


class BulletSlot(Slot):
    type: BulletType


class MissileSlot(Slot):
    type: MissileType


class MineSlot(Slot):
    type: MineType


class UtilitySlot(Slot):
    type: UtilityType


class Shooter(Vessel):
    counter: int

    bullet_sel: int
    missile_sel: int
    mine_sel: int
    util_sel: int

    bullet_slots: dict[int, BulletSlot]
    missile_slots: dict[int, MissileSlot]
    mine_slots: dict[int, MineSlot]
    util_slots: dict[int, UtilitySlot]

    @property
    def bullet(self) -> BulletSlot:
        return self.bullet_slots[self.bullet_sel]

    @property
    def missile(self) -> MissileSlot:
        return self.missile_slots[self.missile_sel]

    @property
    def mine(self) -> MineSlot:
        return self.mine_slots[self.mine_sel]

    @property
    def utility(self) -> UtilitySlot:
        return self.util_slots[self.util_sel]

    @property
    def bullet_pos(self) -> np.ndarray:
        return np.array([0, 0])

    @property
    def missile_pos(self) -> np.ndarray:
        return np.array([0, 0])

