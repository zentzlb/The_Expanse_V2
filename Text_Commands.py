from Ship_Class import Ship, Station, Asteroid
from Misc import FindNearest


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


def check_cargo(gs, ship, args):
    gs.misc_info['command history'].append('_____________________________')
    for key in ship.cargo.keys():
        gs.misc_info['command history'].append(f'{key}: {ship.cargo[key]}')
    if len(gs.misc_info['command history']) > 30:
        gs.misc_info['command history'] = gs.misc_info['command history'][-30:]


def check_ore(gs, ship, args):
    gs.misc_info['command history'].append('_____________________________')
    if 'ore' in ship.info:
        gs.misc_info['command history'].append(f"ore type: {ship.info['ore']}")
    else:
        gs.misc_info['command history'].append('no ore type set')
    if len(gs.misc_info['command history']) > 30:
        gs.misc_info['command history'] = gs.misc_info['command history'][-30:]


def check_target(gs, ship, args):
    gs.misc_info['command history'].append('_____________________________')
    if type(ship.target) is Ship:
        target = ship.target
        gs.misc_info['command history'].append(f"health: {target.health}")
        gs.misc_info['command history'].append(f"heat: {target.heat}")
        gs.misc_info['command history'].append(f"energy: {target.energy}")

        gs.misc_info['command history'].append(f"")
        gs.misc_info['command history'].append(f"primary weapons:")
        for bullet in target.bullet_types:
            gs.misc_info['command history'].append(f"{bullet.name}")

        gs.misc_info['command history'].append(f"")
        gs.misc_info['command history'].append(f"secondary weapons:")
        for missile in target.missile_types:
            gs.misc_info['command history'].append(f"{missile.name}")

        gs.misc_info['command history'].append(f"")
        gs.misc_info['command history'].append(f"mines:")
        for mine in target.mine_types:
            gs.misc_info['command history'].append(f"{mine.name}")

        gs.misc_info['command history'].append(f"")
        gs.misc_info['command history'].append(f"utilities:")
        for util in target.util_types:
            gs.misc_info['command history'].append(f"{util.name}")

        gs.misc_info['command history'].append(f"")
        gs.misc_info['command history'].append(f"turrets:")
        for turret in ship.turrets:
            gs.misc_info['command history'].append(f"{turret.turret_type.name}")
            gs.misc_info['command history'].append(f"turret energy: {turret.energy}")

        if len(gs.misc_info['command history']) > 30:
            gs.misc_info['command history'] = gs.misc_info['command history'][-30:]

def check_status(gs, ship, args):
    gs.misc_info['command history'].append('_____________________________')
    target = ship
    gs.misc_info['command history'].append(f"health: {target.health}")
    gs.misc_info['command history'].append(f"heat: {target.heat}")
    gs.misc_info['command history'].append(f"energy: {target.energy}")

    gs.misc_info['command history'].append(f"")
    gs.misc_info['command history'].append(f"primary weapons:")
    for bullet in target.bullet_types:
        gs.misc_info['command history'].append(f"{bullet.name}")

    gs.misc_info['command history'].append(f"")
    gs.misc_info['command history'].append(f"secondary weapons:")
    for missile in target.missile_types:
        gs.misc_info['command history'].append(f"{missile.name}")

    gs.misc_info['command history'].append(f"")
    gs.misc_info['command history'].append(f"mines:")
    for mine in target.mine_types:
        gs.misc_info['command history'].append(f"{mine.name}")

    gs.misc_info['command history'].append(f"")
    gs.misc_info['command history'].append(f"utilities:")
    for util in target.util_types:
        gs.misc_info['command history'].append(f"{util.name}")

    gs.misc_info['command history'].append(f"")
    gs.misc_info['command history'].append(f"turrets:")
    for turret in ship.turrets:
        gs.misc_info['command history'].append(f"{turret.turret_type.name}")
        gs.misc_info['command history'].append(f"turret energy: {turret.energy}")

    if len(gs.misc_info['command history']) > 30:
        gs.misc_info['command history'] = gs.misc_info['command history'][-30:]



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


def list2str(list):
    string = ''
    for word in list:
        string += word
        string += ' '
    return string


def unpack_str(string, gs, ship):
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


def complete_str(string, gs, ship):
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
                gs.misc_info['command text'] = new_string
            elif len(comp_list) > 1:
                gs.misc_info['command history'].append('_____________________________')
                for comp in comp_list:
                    gs.misc_info['command history'].append(comp)
                gs.misc_info['command history'].append('_____________________________')
