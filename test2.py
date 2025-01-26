# Essential imports
import sys
from entity2 import Entity2
import pygame

# Pygame setup
pygame.init()
WIDTH = 800
HEIGHT = 450
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Window")
clock = pygame.time.Clock()
mouse_position = (0, 0)
current_x = 0
current_y = 0

# List of players & projectiles (entity objects)
players = []
projectiles = []

# Create entity
player1 = Entity2(0, WIDTH / 8, (255, 255, 255), 10, 10, WIDTH * 1 / 20, WIDTH * 1 / 20)
players.append(player1)

# Create gravity variable and projectile force variable
gravity = 0.5
projectile_force = 100


# Entity jumps with gravity var
def jump(index: int):
    """
    :param index: Grabs integer index of players and switches their velocity to -15
    """
    players[index].y_velocity = -15


# Moving variables
moving_left = False
moving_right = False

# Main display loop
while True:
    screen.fill((0, 0, 0))
    pygame.draw.rect(screen, (0, 0, 255), (0, HEIGHT * 0.75, WIDTH, HEIGHT * 0.25))
    for event in pygame.event.get():
        if event.type == pygame.MOUSEMOTION:
            mouse_position = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            projectiles.append(Entity2(players[0].x, players[0].y, (255, 0, 0), 0, 0, 20, 20))
            current_x = mouse_position[0]
            current_y = mouse_position[1]
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_w:
                if 295 < players[0].y <= 300:
                    jump(0)
                else:
                    pass
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
    for player in players:
        if moving_left:
            players[0].x -= 5
        if moving_right:
            players[0].x += 5
        player.y_velocity += gravity
        pygame.draw.rect(screen, player.color, (player.x, player.y, player.width, player.height))
        if player.x <= 0:
            player.x = 0
        if player.x >= 760:
            player.x = 760
        if player.y >= (HEIGHT * 0.75)-player.height and player.y_velocity >= 0:
            player.y = (HEIGHT * 0.75)-player.height
        else:
            player.y += player.y_velocity
    for projectile in projectiles:
        projectile.move(current_x, current_y)
        projectile.draw(screen)

    projectiles = [projectile for projectile in projectiles if projectile.speed > 1]
    pygame.display.flip()
    clock.tick(60)

