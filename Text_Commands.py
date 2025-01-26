from Ship_Class import Ship, Base, Asteroid
from utils import FindNearest


def clear_text(gs, ship, args):
    gs.misc_info['command history'] = []


def clear_ore(gs, ship, args):
    if 'ore' in ship.info:
        del ship.info['ore']


def clear_cargo(gs, ship, args):
    if args in ship.cargo:
        del ship.cargo[args]
    ship.cargo.cargo_total = sum(ship.cargo.values())


def set_ore(gs, ship, args):
    ship.info['ore'] = args


def target_ship(gs, ship, args):
    if args == 'f':
        target_list = gs.ships[0]
        ship.target = FindNearest(ship, target_list)


def target_missile(gs, ship, args):
    pass


def target_station(gs, ship, args):
    pass


def target_asteroid(gs, ship, args):
    pass


def target_next(gs, ship, args):
    pass


def check_cargo(ls, ship, args):
    ls.misc_info['command history'].append('_____________________________')
    for key in ship.cargo.keys():
        ls.misc_info['command history'].append(f'{key}: {ship.cargo[key]}')
    if len(ls.misc_info['command history']) > 30:
        ls.misc_info['command history'] = ls.misc_info['command history'][-30:]


def check_ore(ls, ship, args):
    ls.misc_info['command history'].append('_____________________________')
    if 'ore' in ship.info:
        ls.misc_info['command history'].append(f"ore type: {ship.info['ore']}")
    else:
        ls.misc_info['command history'].append('no ore type set')
    if len(ls.misc_info['command history']) > 30:
        ls.misc_info['command history'] = ls.misc_info['command history'][-30:]


def check_target(ls, ship, args):
    ls.misc_info['command history'].append('_____________________________')
    if type(ship.target) is Ship:
        target = ship.target
        ls.misc_info['command history'].append(f"health: {target.health}")
        ls.misc_info['command history'].append(f"heat: {target.heat}")
        ls.misc_info['command history'].append(f"energy: {target.energy}")

        ls.misc_info['command history'].append(f"")
        ls.misc_info['command history'].append(f"primary weapons:")
        for bullet in target.bullet_types:
            ls.misc_info['command history'].append(f"{bullet.name}")

        ls.misc_info['command history'].append(f"")
        ls.misc_info['command history'].append(f"secondary weapons:")
        for missile in target.missile_types:
            ls.misc_info['command history'].append(f"{missile.name}")

        ls.misc_info['command history'].append(f"")
        ls.misc_info['command history'].append(f"mines:")
        for mine in target.mine_types:
            ls.misc_info['command history'].append(f"{mine.name}")

        ls.misc_info['command history'].append(f"")
        ls.misc_info['command history'].append(f"utilities:")
        for util in target.util_types:
            ls.misc_info['command history'].append(f"{util.name}")

        ls.misc_info['command history'].append(f"")
        ls.misc_info['command history'].append(f"turrets:")
        for turret in ship.turrets:
            ls.misc_info['command history'].append(f"{turret.turret_type.name}")
            ls.misc_info['command history'].append(f"turret energy: {turret.energy}")

        if len(ls.misc_info['command history']) > 30:
            ls.misc_info['command history'] = ls.misc_info['command history'][-30:]


def check_status(ls, ship, args):
    ls.misc_info['command history'].append('_____________________________')
    target = ship
    ls.misc_info['command history'].append(f"health: {target.health}")
    ls.misc_info['command history'].append(f"heat: {target.heat}")
    ls.misc_info['command history'].append(f"energy: {target.energy}")

    ls.misc_info['command history'].append(f"")
    ls.misc_info['command history'].append(f"primary weapons:")
    for bullet in target.bullet_types:
        ls.misc_info['command history'].append(f"{bullet.name}")

    ls.misc_info['command history'].append(f"")
    ls.misc_info['command history'].append(f"secondary weapons:")
    for missile in target.missile_types:
        ls.misc_info['command history'].append(f"{missile.name}")

    ls.misc_info['command history'].append(f"")
    ls.misc_info['command history'].append(f"mines:")
    for mine in target.mine_types:
        ls.misc_info['command history'].append(f"{mine.name}")

    ls.misc_info['command history'].append(f"")
    ls.misc_info['command history'].append(f"utilities:")
    for util in target.util_types:
        ls.misc_info['command history'].append(f"{util.name}")

    ls.misc_info['command history'].append(f"")
    ls.misc_info['command history'].append(f"turrets:")
    for turret in ship.turrets:
        ls.misc_info['command history'].append(f"{turret.turret_type.name}")
        ls.misc_info['command history'].append(f"turret energy: {turret.energy}")

    if len(ls.misc_info['command history']) > 30:
        ls.misc_info['command history'] = ls.misc_info['command history'][-30:]



target_dict = {'ship': target_ship,
               'missile': target_missile,
               'station': target_station,
               'asteroid': target_asteroid,
               'next': target_next}

set_dict = {'ore': set_ore}

clear_dict = {'ore': clear_ore,
              'text': clear_text,
              'cargo': clear_cargo}

check_dict = {'cargo': check_cargo,
              'target': check_target,
              'ore': check_ore,
              'status': check_status}

main_dict = {'set': set_dict,
             'clear': clear_dict,
             'check': check_dict,
             'target': target_dict}


def list2str(mylist: list):
    string = ''
    for word in mylist:
        string += word
        string += ' '
    return string


def unpack_str(string: str, gs, ship):
    cmd_list = string.split(' ')
    d = main_dict
    for cmd in cmd_list:
        if cmd in d:
            if callable(d[cmd]):
                fn = d[cmd]
                args = cmd_list[-1]
                fn(gs, ship, args)
            elif type(d[cmd]) is dict:
                d = d[cmd]


def complete_str(string: str, ls, ship):
    cmd_list = string.split(' ')
    d = main_dict
    for cmd in cmd_list:
        if cmd in d:
            if type(d[cmd]) is dict:
                d = d[cmd]
        else:
            lets = len(cmd)
            comp_list = []
            for key in d.keys():
                if len(key) >= lets and key[:lets] == cmd:
                    comp_list.append(key)
            if len(comp_list) == 1:
                # print(cmd_list)
                new_list = cmd_list[:cmd_list.index(cmd)]
                new_list.append(comp_list[0])
                # print(new_list)
                new_string = list2str(new_list)
                ls.misc_info['command text'] = new_string
            elif len(comp_list) > 1:
                ls.misc_info['command history'].append('_____________________________')
                for comp in comp_list:
                    ls.misc_info['command history'].append(comp)
                ls.misc_info['command history'].append('_____________________________')
