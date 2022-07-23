import math
from matplotlib import pyplot as plt


import pygame
pygame.init()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255, 10)  # This color contains an extra integer. It's the alpha value.
PURPLE = (255, 0, 255)

screen = pygame.display.set_mode((200, 325))
screen.fill(WHITE)  # Make the background white. Remember that the screen is a Surface!
clock = pygame.time.Clock()

size = (50, 50)
red_image = pygame.Surface(size)
green_image = pygame.Surface(size)
blue_image = pygame.Surface(size, pygame.SRCALPHA)  # Contains a flag telling pygame that the Surface is per-pixel alpha
purple_image = pygame.Surface(size)

red_image.set_colorkey(BLACK)
green_image.set_alpha(50)
# For the 'blue_image' it's the alpha value of the color that's been drawn to each pixel that determines transparency.
purple_image.set_colorkey(BLACK)
purple_image.set_alpha(50)

pygame.draw.rect(red_image, RED, red_image.get_rect(), 10)
pygame.draw.rect(green_image, GREEN, green_image.get_rect(), 10)
pygame.draw.rect(blue_image, BLUE, blue_image.get_rect(), 10)
pygame.draw.rect(purple_image, PURPLE, purple_image.get_rect(), 10)


c = 10
while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                screen.blit(red_image, (75, c))
                c += 1
            elif event.key == pygame.K_2:
                screen.blit(green_image, (75, 100))
            elif event.key == pygame.K_3:
                screen.blit(blue_image, (75, 175))
            elif event.key == pygame.K_4:
                screen.blit(purple_image, (75, 250))

    pygame.display.update()

# dx = 100000
# dy = 0
#
# d = math.sqrt(dx ** 2 + dy ** 2)
# r = 2.5 * math.log((d ** (3/2)) / (1000 + d) + 1) ** 2
# print(r)

"""DAMAGE TEST"""
# x = []
# y = []
# max_damage = 4
# r = 50 / math.sqrt(2)
# exp = 30
#
# for d in range(200):
#     x.append(d)
#     y.append(round(max_damage / (1 + (d / (r + exp)) ** 3)))
#
# plt.plot(x, y)
# plt.show()

# plt.plot(x, y)
# plt.show()

# vx = 2
# vy = 0
# bullet_velocity = 7
# Xo = 0
# Yo = 0
# xo = 10
# yo = 10
#
# a = vx ** 2 + vy ** 2 - bullet_velocity ** 2
# b = 2 * (vx * (xo - Xo) + vy * (yo - Yo))
# c = (xo - Xo) ** 2 + (yo - Yo) ** 2
#
# t = (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
#
# x = xo + vx * t
# y = yo + vy * t
#
# dx = x - Xo
# dy = y - Yo
#
# print(dx)
# print(dy)

# cos = math.cos(self.angle * math.pi / 180)
# sin = math.sin(self.angle * math.pi / 180)
#
# Q = np.array([[cos, sin], [-sin, cos]])
# V = np.array([[dx], [dy]])
# print(V)
# V_prime = Q.dot(V)
# angle2 = math.atan2(V_prime[0][0], V_prime[1][0])