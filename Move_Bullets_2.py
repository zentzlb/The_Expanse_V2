import pygame
import math
import numpy as np


def move_bullets(yellow_bullets, red_bullets, yellow, red, BULLET_VEL, HEIGHT, WIDTH, RED_HIT, YELLOW_HIT):

    for bullet in yellow_bullets:
        """MISSILE TRACKING"""
        da = np.cross((math.sin(bullet[1] * math.pi / 180), math.cos(bullet[1] * math.pi / 180), 0), (red.x + red.width / 2 - bullet[0].x, red.y + red.height / 2 - bullet[0].y, 0))[2]
        if da > 0:
            bullet[1] -= 1.5
        else:
            bullet[1] += 1.5

        """CHANGE POSITION"""
        bullet[0].x += round(BULLET_VEL * math.sin(bullet[1] * math.pi / 180))
        bullet[0].y += round(BULLET_VEL * math.cos(bullet[1] * math.pi / 180))
        if red.colliderect(bullet[0]):  # bullet hits red
            yellow_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(RED_HIT))
        elif bullet[0].x > WIDTH or bullet[0].x < 0 or bullet[0].y > HEIGHT or bullet[0].y < 0:  # bullets leaves arena
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet[0].x += round(BULLET_VEL * math.sin(bullet[1] * math.pi / 180))
        bullet[0].y += round(BULLET_VEL * math.cos(bullet[1] * math.pi / 180))
        if yellow.colliderect(bullet[0]):  # bullet hits yellow
            red_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
        elif bullet[0].x > WIDTH or bullet[0].x < 0 or bullet[0].y > HEIGHT or bullet[0].y < 0:  # bullets leaves arena
            red_bullets.remove(bullet)
