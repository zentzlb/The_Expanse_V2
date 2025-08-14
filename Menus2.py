"""

"""
import pygame
import typing
from Data.Types import COLOR3
from Data.Ship_Types import SHIPTYPES
from Data.Bullet_Types import BULLETTYPES


class Button(pygame.FRect):
    """
    generic button
    """

    def __init__(self,
                 rect: tuple[float, float, float, float],
                 # fonts: dict[str, pygame.font.Font],
                 # text: str = '',
                 image: pygame.Surface | None = None,
                 rect_width: int = 0,
                 # text_color: COLOR3 = (0, 0, 0),
                 color: COLOR3 = (100, 100, 100),
                 func: typing.Callable = lambda *args, **kwargs: None):
        super().__init__(rect)
        self.color = color
        self.rect_width = rect_width
        # self.text_color = text_color
        # self.text = text
        self.image = image
        # self.fonts = fonts
        self.func = func


    def draw(self, surf: pygame.Surface) -> None:
        """
        draw_game button on a surface
        :param surf: surface
        :return:
        """
        pygame.draw.rect(surf, self.color, self, width=self.rect_width)
        if self.image:
            self.draw_image(surf)
        # else:
        #     self.draw_text(surf)

    def draw_outline(self, surf: pygame.Surface, width: int = 2) -> None:
        """
        draw_game button on a surface
        :param surf: surface
        :param width: outline width
        :return:
        """
        pygame.draw.rect(surf, self.color, (self.x-width, self.y-width, self.width+2*width,
                                                self.height+2*width), width=width)

    # def draw_text(self, surf: pygame.Surface) -> None:
    #     """
    #     blits text onto surface centered on centerx, centery
    #     :param surf: surface to blit onto
    #     """
    #     # if self.text_color != (0, 0, 0):
    #     #     print(self.text_color)
    #     if self.text:
    #         text_surface = self.fonts['large'].render(self.text,
    #                                                   True,
    #                                                   self.text_color)
    #         xt = self.centerx - text_surface.get_width() / 2
    #         yt = self.centery - text_surface.get_height() / 2
    #         surf.blit(text_surface, (xt, yt))

    def draw_image(self, surf: pygame.Surface):
        """
        blits image onto surface centered on centerx, centery
        :param surf: surface to blit onto
        """
        xt = self.centerx - self.image.get_width() / 2
        yt = self.centery - self.image.get_height() / 2
        surf.blit(self.image, (xt, yt))

    def __call__(self, *args, **kwargs):
        kwargs['button'] = self
        return self.func(*args, **kwargs)

    def __str__(self):
        return f"Button: {self.color}"

    def __repr__(self):
        return self.__str__()


class Menu:
    def __init__(self, buttons: list[Button]):
        self.buttons = buttons
        self.info = {}

    def draw(self, surf: pygame.Surface):
        for button in self.buttons:
            button.draw(surf)




