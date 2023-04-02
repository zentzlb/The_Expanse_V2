import os
import pygame
from Explosions import glow_ring, glow_circle, trans_circle


def make_wave_images(dir, max_r, color, width):
    image_list = []
    for r in range(max_r+1):
        length = 2 * (r + width)
        surf = pygame.Surface((length, length))
        surf.set_colorkey((0, 0, 0))
        w = round(1 + width * (max_r - r) / max_r)
        print(w)
        for p in range(w):
            glow_ring(surf, (r + width), (r + width), r+p, (2, 3, 5), 2*p)

        # pygame.draw.circle(surf, color, (r, r), r)
        # surf.convert_alpha()
        image_list.append(surf)
    return image_list

def make_exp_images(dir, max_r, color):
    image_list = []
    for R in range(1, max_r+1):
        length = 2 * R
        surf = pygame.Surface((length, length))
        surf.set_colorkey((0, 0, 0))
        for r in range(R):
            glow_circle(surf, R, R, r, color)
        # w = round(1 + width * (max_r - r) / max_r)
        # print(w)
        # for p in range(w):
        #     glow_ring(surf, (r + width), (r + width), r+p, (2, 3, 5), 2*p)

        # pygame.draw.circle(surf, color, (r, r), r)
        # surf.convert_alpha()
        image_list.append(surf)
    return image_list



def save_images(dir, image_list):
    os.makedirs(dir, exist_ok=True)
    for i in range(len(image_list)):
        image = image_list[i]
        pygame.image.save(image, os.path.join(dir, f'{i:0>4}.png'))




# dir = os.path.join('Assets', 'GravityRepulsor')
# image_list = make_wave_images(dir, 600, (100, 200, 255, 10), 80)

# dir = os.path.join('Assets', 'PlasmaExplosion')
# image_list = make_exp_images(dir, 50, (4, 0, 5))

dir = os.path.join('Assets', 'PhotonExplosion')
image_list = make_exp_images(dir, 60, (4, 4, 4))

save_images(dir, image_list)
