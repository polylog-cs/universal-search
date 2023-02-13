from random import randrange
from re import I
from unittest import skip
from manim import config as global_config

from utils.util import *


class Polylog(Scene):
    def construct(self):
        default()
        authors = Tex(
            r"\textbf{Filip Hlásek, Václav Rozhoň, Václav Volhejn}", 
            color=text_color,
            font_size = 40,
        ).shift(
            3*DOWN + 0*LEFT
        )

        channel_name = Tex(r"polylog", color=text_color)
        channel_name.scale(4).shift(1 * UP)

        logo_solarized = ImageMobject("img/logo-solarized.png").scale(0.032).move_to(2 * LEFT + 1 * UP + 0.455 * RIGHT)
        self.play(
           Write(authors),
           Write(channel_name), 
        )
        self.play(
            FadeIn(logo_solarized)
        )

        self.wait()

        self.play(
            *[FadeOut(o) for o in self.mobjects]
        )
        self.wait()


class Explore(Scene):
    def construct(self):
        pass

