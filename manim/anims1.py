from utils.utilgeneral import *
from utils.util import *
from manim import *

class Polylog(Scene):
    def construct(self):
        default()
        authors = Tex(
            r"\textbf{Richard Hladík, Filip Hlásek, Václav Rozhoň, Václav Volhejn}", 
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
        default()
        
        #TODO primes
        num1 = 398473984793874
        num2 = 398473934343344
        mult_objects, mult_anims = multiplication_animation(num1, num2)

        self.play(
            mult_anims[0]
        )
        self.wait()
        self.play(
            mult_anims[1]
        )

