import pygame
import os
import math

pygame.font.init()

WIDTH, HEIGHT = 1500, 800  # width and height of window

WIN = pygame.display.set_mode((WIDTH, HEIGHT))  # create window
pygame.display.set_caption("The Expanse")  # set window title

FONT = pygame.font.SysFont('comicsans', 40)

COLOR = (40, 10, 35)  # define window color
BLACK = (0, 50, 0)  # BLACK
RED = (255, 0, 0)  # RED
YELLOW = (255, 255, 0)  # YELLOW

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

FPS = 30  # define frame rate
VEL = 4  # ship velocity
BULLET_VEL = 7  # bullet velocity
MAX_BULLETS = 3  # max number of bullets
ACC = .1  # ship acceleration

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

VEL_Y = [0, 0]
VEL_R = [0, 0]

POS_Y = [100, HEIGHT // 2]
POS_R = [WIDTH - 100, HEIGHT // 2]

ANG_Y = 0
ANG_R = 0
AV = 3

spaceship_height, spaceship_width = 50, 50
Y_SHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))  # yellow spaceship
Y_SHIP = pygame.transform.rotate(pygame.transform.scale(Y_SHIP_IMAGE, (spaceship_height, spaceship_width)), ANG_Y)
R_SHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))  # red spaceship
R_SHIP = pygame.transform.rotate(pygame.transform.scale(R_SHIP_IMAGE, (spaceship_height, spaceship_width)), ANG_R)


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    # WIN.fill(COLOR)  # fill window with color
    pygame.draw.rect(WIN, BLACK, BORDER)

    red_health_text = FONT.render(f"Health: {red_health}", 1, RED)
    yellow_health_text = FONT.render(f"Health: {yellow_health}", 1, YELLOW)
    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))  # display red health
    WIN.blit(yellow_health_text, (yellow_health_text.get_width() - 10, 10))  # display yellow health

    Y_SHIP = pygame.transform.rotate(pygame.transform.scale(Y_SHIP_IMAGE, (spaceship_height, spaceship_width)), ANG_Y)
    WIN.blit(Y_SHIP, (yellow.x, yellow.y))
    WIN.blit(R_SHIP, (red.x, red.y))

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update()  # update window


def yellow_movement(keys_pressed, yellow):
    global ANG_Y
    if keys_pressed[pygame.K_q]:  # LEFT
        # VEL_Y[0] -= ACC
        ANG_Y += AV
    if keys_pressed[pygame.K_e]:  # RIGHT
        # VEL_Y[0] += ACC
        ANG_Y -= AV
    if keys_pressed[pygame.K_w]:  # UP
        VEL_Y[0] += ACC * math.sin(ANG_Y * math.pi / 180)
        VEL_Y[1] += ACC * math.cos(ANG_Y * math.pi / 180)
    if keys_pressed[pygame.K_s]:  # DOWN
        VEL_Y[0] -= ACC * math.sin(ANG_Y * math.pi / 180)
        VEL_Y[1] -= ACC * math.cos(ANG_Y * math.pi / 180)
    if keys_pressed[pygame.K_a]:  # LEFT
        VEL_Y[1] -= ACC * math.sin(ANG_Y * math.pi / 180) / 4
        VEL_Y[0] += ACC * math.cos(ANG_Y * math.pi / 180) / 4
    if keys_pressed[pygame.K_d]:  # RIGHT
        VEL_Y[1] += ACC * math.sin(ANG_Y * math.pi / 180) / 4
        VEL_Y[0] -= ACC * math.cos(ANG_Y * math.pi / 180) / 4

    if math.sqrt(VEL_Y[0] ** 2 + VEL_Y[1] ** 2) > VEL:
        VEL_Y[0] = VEL_Y[0] * VEL / math.sqrt(VEL_Y[0] ** 2 + VEL_Y[1] ** 2)
        VEL_Y[1] = VEL_Y[1] * VEL / math.sqrt(VEL_Y[0] ** 2 + VEL_Y[1] ** 2)

    POS_Y[0] += VEL_Y[0]
    POS_Y[1] += VEL_Y[1]

    # if POS_Y

    yellow.x = round(POS_Y[0])
    yellow.y = round(POS_Y[1])
    # yellow.x += round(VEL_Y[0])
    # yellow.y += round(VEL_Y[1])


def red_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x + VEL - 5 > BORDER.x:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL < WIDTH:  # RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y + VEL > 0:  # UP
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.width < HEIGHT:  # DOWN
        red.y += VEL


def move_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):  # bullet hits red
            yellow_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(RED_HIT))
        elif bullet.x > WIDTH or bullet.x < 0 or bullet.y > HEIGHT or bullet.y < 0:  # bullets leaves arena
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):  # bullet hits yellow
            red_bullets.remove(bullet)
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
        elif bullet.x > WIDTH or bullet.x < 0 or bullet.y > HEIGHT or bullet.y < 0:  # bullets leaves arena
            red_bullets.remove(bullet)


def main():
    red = pygame.Rect(POS_R[0], POS_R[1], spaceship_width, spaceship_height)
    yellow = pygame.Rect(POS_Y[0], POS_Y[1], spaceship_width, spaceship_height)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    run = True
    clock = pygame.time.Clock()  # game clock
    winner_text = ""

    while run:  # main loop
        clock.tick(FPS)
        for event in pygame.event.get():  # look for events
            if event.type == pygame.QUIT:  # check to see if user quit game
                run = False
                print('game over!')
            if event.type == pygame.KEYDOWN:  # fire bullets
                if event.key == pygame.K_LCTRL:  # and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 2, 2)
                    yellow_bullets.append(bullet)
                if event.key == pygame.K_RCTRL:  # and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 3, 3)
                    red_bullets.append(bullet)
            if event.type == RED_HIT:
                red_health -= 1
                if red_health >= 0:
                    winner_text = "yellow won"
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                if yellow_health >= 0:
                    winner_text = "red won"

        keys_pressed = pygame.key.get_pressed()  # list of keys that are pressed

        yellow_movement(keys_pressed, yellow)
        red_movement(keys_pressed, red)

        move_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    pygame.quit()  # quit game


if __name__ == "__main__":
    main()
