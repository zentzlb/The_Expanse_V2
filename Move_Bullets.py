import pygame
import math
from Misc import ShipExplosion


def move_bullets(bullet_list, target_list, height, width, explosion_group):

    for bullet in bullet_list:
        bullet.scoot()
        if bullet.collidelist(target_list) != -1:  # bullet hits red
            dmgList = bullet.collidelistall(target_list)
            for i in dmgList:
                target_list[i].health -= 1
                if target_list[i].health <= 0:
                    explosion = ShipExplosion(target_list[i].centerx, target_list[i].centery)
                    explosion_group.add(explosion)
            bullet_list.remove(bullet)

            # pygame.event.post(pygame.event.Event(RED_HIT))
        elif bullet.x > width or bullet.x < 0 or bullet.y > height or bullet.y < 0:  # bullets leaves arena
            bullet_list.remove(bullet)

