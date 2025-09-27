import os

if __name__ == '__main__':
    os.chdir(os.getcwd() + '\\..')

import pygame

pygame.mixer.init()

PATHS = {'AutoCannon': r"\Assets\AutoCannon_launch.mp3",
               'Missile': r"\Assets\missile_launch.mp3",
               'Plasma': r"\Assets\PA_launch.mp3",
               'Railgun': r"\Assets\railgun_launch.mp3"}


class Mixer:
    def __init__(self, **paths):
        self.sounds = {name: pygame.mixer.Sound(path) for name, path in paths.items()}

    def play(self, name: str):
        if name in self.sounds:
            self.sounds[name].play()


MIXER = Mixer(**PATHS)