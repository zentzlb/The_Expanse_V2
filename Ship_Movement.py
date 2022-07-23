import pygame
import math


def ship_movement(keys_pressed, ship, position, max_velocity, velocity, ACC, AV, angle, WIDTH, HEIGHT, h, w, player1=True):

    if player1:
        if keys_pressed[pygame.K_q]:  # LEFT
            # VEL_Y[0] -= ACC
            angle += AV
        if keys_pressed[pygame.K_e]:  # RIGHT
            # VEL_Y[0] += ACC
            angle -= AV
        if keys_pressed[pygame.K_w]:  # UP
            velocity[0] += ACC * math.sin(angle * math.pi / 180)
            velocity[1] += ACC * math.cos(angle * math.pi / 180)
        if keys_pressed[pygame.K_s]:  # DOWN
            velocity[0] -= ACC * math.sin(angle * math.pi / 180)
            velocity[1] -= ACC * math.cos(angle * math.pi / 180)
        if keys_pressed[pygame.K_a]:  # LEFT
            velocity[1] -= ACC * math.sin(angle * math.pi / 180)  # / 2
            velocity[0] += ACC * math.cos(angle * math.pi / 180)  # / 2
        if keys_pressed[pygame.K_d]:  # RIGHT
            velocity[1] += ACC * math.sin(angle * math.pi / 180)  # / 2
            velocity[0] -= ACC * math.cos(angle * math.pi / 180)  # / 2

        if math.sqrt(velocity[0] ** 2 + velocity[1] ** 2) > max_velocity:
            velocity[0] = velocity[0] * max_velocity / math.sqrt(velocity[0] ** 2 + velocity[1] ** 2)
            velocity[1] = velocity[1] * max_velocity / math.sqrt(velocity[0] ** 2 + velocity[1] ** 2)

    else:
        if keys_pressed[pygame.K_i]:  # LEFT
            # VEL_Y[0] -= ACC
            angle += AV
        if keys_pressed[pygame.K_p]:  # RIGHT
            # VEL_Y[0] += ACC
            angle -= AV
        if keys_pressed[pygame.K_o]:  # UP
            velocity[0] += ACC * math.sin(angle * math.pi / 180)
            velocity[1] += ACC * math.cos(angle * math.pi / 180)
        if keys_pressed[pygame.K_l]:  # DOWN
            velocity[0] -= ACC * math.sin(angle * math.pi / 180)
            velocity[1] -= ACC * math.cos(angle * math.pi / 180)
        if keys_pressed[pygame.K_k]:  # LEFT
            velocity[1] -= ACC * math.sin(angle * math.pi / 180)  # / 2
            velocity[0] += ACC * math.cos(angle * math.pi / 180)  # / 2
        if keys_pressed[pygame.K_SEMICOLON]:  # RIGHT
            velocity[1] += ACC * math.sin(angle * math.pi / 180)  # / 2
            velocity[0] -= ACC * math.cos(angle * math.pi / 180)  # / 2

    """Adjust Position and Velocity"""
    if math.sqrt(velocity[0] ** 2 + velocity[1] ** 2) > max_velocity:
        velocity[0] = velocity[0] * max_velocity / math.sqrt(velocity[0] ** 2 + velocity[1] ** 2)
        velocity[1] = velocity[1] * max_velocity / math.sqrt(velocity[0] ** 2 + velocity[1] ** 2)

    position[0] += velocity[0]
    position[1] += velocity[1]

    # bounce off edge of screen
    if position[0] < 0 or position[0] > WIDTH - w:
        velocity[0] = - velocity[0]

    if position[1] < 0 or position[1] > HEIGHT - h:
        velocity[1] = - velocity[1]

    # convert real position to pixel position
    ship.x = round(position[0] + (w - h * abs(math.sin(angle * math.pi / 180)) - w * abs(math.cos(angle * math.pi / 180))) / 2)
    ship.y = round(position[1] + (h - w * abs(math.sin(angle * math.pi / 180)) - h * abs(math.cos(angle * math.pi / 180))) / 2)

    return position, velocity, angle




        # if keys_pressed[pygame.K_LEFT] and ship.x + VEL - 5 > BORDER.x:  # LEFT
        #     ship.x -= VEL
        # if keys_pressed[pygame.K_RIGHT] and ship.x + VEL < WIDTH:  # RIGHT
        #     ship.x += VEL
        # if keys_pressed[pygame.K_UP] and ship.y + VEL > 0:  # UP
        #     ship.y -= VEL
        # if keys_pressed[pygame.K_DOWN] and ship.y + VEL + ship.width < HEIGHT:  # DOWN
        #     ship.y += VEL