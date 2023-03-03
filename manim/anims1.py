from utils.utilgeneral import *
from utils.util import *
from manim import *


class Intro(Scene):
    def construct(self):
        default()
        
        #What if I asked you to multiply two long primes, each with n digits? That’s simple, you can just use the algorithm you know from school, 

        #TODO primes
        num1 = 39847
        num2 = 39847

        num1_tex = Tex(str(num1))
        num2_tex = Tex(str(num1))

        self.play(
            FadeIn(Group(num1_tex, num2_tex).arrange(RIGHT).move_to(ORIGIN))
        )

        mult_objects, mult_anims = multiplication_animation(num1, num2, num1_tex, num2_tex)
        #mult_objects = Group(
        #     num1_tex,
        #     num2_tex,
        #     line1,
        #     *nums_intermediate_tex,
        #     num_tex,
        #     line2,
        # )


        self.play(
            mult_anims[0]
        )
        self.wait()

        # it takes only roughly n^2 steps to compute the result. 

        border = SurroundingRectangle(Group(*mult_objects[3:-2]), color = RED)
        brace = Brace(border, RIGHT)
        n2_tex = Tex(r"$n^2$ operations").next_to(brace, RIGHT)

        self.play(
            FadeIn(border),
            FadeIn(brace),
            FadeIn(n2_tex),
        )
        self.wait()

        res_tex = mult_objects[-2].copy()
        self.add(res_tex)

        self.play(
            mult_anims[1],
            FadeOut(*Group(border, brace, n2_tex)),
        )
        self.wait()

        
        #But what about the opposite problem where I give you a product of two primes and ask you to find the prime factors. How do you solve that one? 
        
        div_objects, div_anims = division_animation(num1 * num2, res_tex)
        self.play(div_anims[0])
        self.wait()

        # Well, you can check whether that input number is divisible by 2,3,4,5 and so on, until you hit a factor. But if the number on input has n digits, its size is up to 10^n and hence you will need up to sqrt( 10^n) steps before you find a factor. 
        
        brace = Brace(div_objects[0], DOWN)
        sqrt_tex = Tex(r"{{$n$ digits}}{{$\Rightarrow$ size up to $10^n$}}{{$\Rightarrow$ up to $\sqrt{10^n}$ steps}}")
        sqrt_tex[0].next_to(brace, DOWN)
        sqrt_tex[1].next_to(sqrt_tex[0], RIGHT, buff = 0.5)
        sqrt_tex[2].next_to(sqrt_tex[1], RIGHT, buff = 0.5)

        self.play(
            FadeIn(brace),
            FadeIn(sqrt_tex)
        )
        self.wait()
        
        # This is much slower than the time n^2 it takes to multiply two numbers. 
        formula_tex = Tex(r"$n^2 \ll \sqrt{10^n}$").next_to(sqrt_tex, DOWN, buff = 1)
        
        self.play(
            Succession(
                sqrt_tex[2][5:10].copy().animate.move_to(formula_tex[0][3:].get_center()), # TODO 
                FadeIn(formula_tex[0][0:3])           
            )
        )
        self.wait()
        
        
        # There were faster algorithms known for factoring, but all of them were much slower than n^2. Finding a fast classical algorithm for factoring has been one of the most important open questions of computer science for a long time. And for a good reason: an efficient factoring algorithm would break large parts of today’s cryptography. 

        # TODO animace??? pridat tabulku faktorizacnich algoritmu?

        #So, ladies and gentlemen, it is with utmost pride that, today, we, the polylog team, can present to you a simple algorithm for factoring numbers for which we can also prove that its time complexity is asymptotically optimal! [tadá zvuk?] Asymptotic optimality means that whenever you come up with some amazing factoring algorithm, I can prove that my algorithm is either faster than yours, or if my algorithm is slower, it is slower only by a constant factor. 
        # For example, perhaps my algorithm is twice as slow as yours, but it is at most twice as slow for all inputs, even very large ones. 

        # So it is not possible that you could come up with an algorithm such that as the input size increases, my algorithm would get slower and slower relative to yours. 

    
        #In other words, up to constant factors, our algorithm completely nails it. 
        
        # I won’t tell you now how our algorithm works, I will explain that in a followup video that we publish in the next few days. Until then, check out our algorithm and try to understand what it is doing! 
        #Or just run the algorithm on some real data! In that case be careful, our implementation is in Python, so it’s a bit slow. Good luck and see you in a few days with the follow-up video!


class Factoring(Scene):
    def construct(self):
        default()

        authors_tex = Tex("{{[Boudot, Gaudry, Guillevic, Heninger, Thomé, Zimmermann]\\}}{{$~3000$ CPU years}}")
        authors_tex[0].scale(0.4)
        authors_tex[1].scale(0.4)

        n_tex, a_tex, b_tex = [Tex(str(n)) for n in horrible_multiplication()]
        eq_tex = Tex(str(r"="))
        times_tex = Tex(str(r"$\times$"))

        mult_group = Group(
            authors_tex,
            n_tex,
            eq_tex, 
            a_tex,
            times_tex,
            b_tex,
        ).arrange(DOWN)

        self.play(
            FadeIn(mult_group)
        )
        self.wait()



        self.wait(5)


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




