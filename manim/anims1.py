from manim import *
import manim as m  # hack for type hinting
from utils import *

# ^ also imports manim and changes some of its defaults


class Intro(Scene):
    def construct(self):
        default()

        # What if I asked you to multiply two long primes, each with n digits? That’s simple, you can just use the algorithm you know from school,

        # TODO primes
        num1 = 39847
        num2 = 39847

        num1_tex = Tex(str(num1))
        num2_tex = Tex(str(num1))

        self.play(FadeIn(Group(num1_tex, num2_tex).arrange(RIGHT).move_to(ORIGIN)))

        mult_objects, mult_anims = multiplication_animation(
            num1, num2, num1_tex, num2_tex
        )
        # mult_objects = Group(
        #     num1_tex,
        #     num2_tex,
        #     line1,
        #     *nums_intermediate_tex,
        #     num_tex,
        #     line2,
        # )

        self.play(mult_anims[0])
        self.wait()

        # it takes only roughly n^2 steps to compute the result.

        border = SurroundingRectangle(Group(*mult_objects[3:-2]), color=RED)
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

        # But what about the opposite problem where I give you a product of two primes and ask you to find the prime factors. How do you solve that one?

        div_objects, div_anims = division_animation(num1 * num2, res_tex)
        self.play(div_anims[0])
        self.wait()

        # Well, you can check whether that input number is divisible by 2,3,4,5 and so on, until you hit a factor. But if the number on input has n digits, its size is up to 10^n and hence you will need up to sqrt( 10^n) steps before you find a factor.

        brace = Brace(div_objects[0], DOWN)
        sqrt_tex = Tex(
            r"{{$n$ digits}}{{$\Rightarrow$ size up to $10^n$}}{{$\Rightarrow$ up to $\sqrt{10^n}$ steps}}"
        )
        sqrt_tex[0].next_to(brace, DOWN)
        sqrt_tex[1].next_to(sqrt_tex[0], RIGHT, buff=0.5)
        sqrt_tex[2].next_to(sqrt_tex[1], RIGHT, buff=0.5)

        self.play(FadeIn(brace), FadeIn(sqrt_tex))
        self.wait()

        # This is much slower than the time n^2 it takes to multiply two numbers.
        formula_tex = Tex(r"$n^2 \ll \sqrt{10^n}$").next_to(sqrt_tex, DOWN, buff=1)

        self.play(
            Succession(
                sqrt_tex[2][5:10]
                .copy()
                .animate.move_to(formula_tex[0][3:].get_center()),  # TODO
                FadeIn(formula_tex[0][0:3]),
            )
        )
        self.wait()

        # There were faster algorithms known for factoring, but all of them were much slower than n^2. Finding a fast classical algorithm for factoring has been one of the most important open questions of computer science for a long time. And for a good reason: an efficient factoring algorithm would break large parts of today’s cryptography.

        # TODO animace??? pridat tabulku faktorizacnich algoritmu?


class RescalablePlot(VMobject):
    def __init__(self, x_range, y_range, fns=None, *args, **kwargs):
        super().__init__(**kwargs)
        self.fns = fns if fns is not None else []
        self.x_range = x_range[:]
        self.y_range = y_range[:]
        self.scaling_factor = 1
        self.shift_direction = 0.0

        self.axes, self.plots = self.axes_and_plots()
        self.add(self.axes, *self.plots)

    def _sparsify_range(self, r):
        step = r[2]
        while 50 * step < r[1] - r[0]:
            step *= 10
        return [r[0], r[1], step]

    def axes_and_plots(self):
        axes = (
            Axes(
                x_range=self._sparsify_range(self.x_range),
                y_range=self._sparsify_range(self.y_range),
            )
            .scale(self.scaling_factor)
            .shift(self.shift_direction)
        )
        plots = []
        for fn, color in self.fns:
            plots.append(axes.plot(fn, color=color))
        return axes, plots

    def scale(self, factor, *args, **kwargs):
        self.scaling_factor = factor
        self.redraw()
        return self

    def shift(self, direction, *args, **kwargs):
        self.shift_direction = direction
        self.redraw()
        return self

    def redraw(self):
        axes, plots = self.axes_and_plots()
        self.axes.become(axes)
        for old, new in zip(self.plots, plots):
            old.become(new)
        for new in plots[len(self.plots) :]:
            self.plots.append(new)
            self.add(new)


class RescalePlot(Animation):
    def __init__(self, mobject: RescalablePlot, x_range, y_range, **kwargs):
        self.ox_range = mobject.x_range
        self.oy_range = mobject.y_range
        self.tx_range = x_range
        self.ty_range = y_range
        super().__init__(mobject, **kwargs)

    def interpolate_mobject(self, alpha: float) -> None:
        a = self.rate_func(alpha)

        def mix_up(orig, target):
            min = (1 - a) * orig[0] + a * target[0]
            max = (1 - a) * orig[1] + a * target[1]
            num_orig = (orig[1] - orig[0]) / orig[2]
            num_target = (target[1] - target[0]) / target[2]
            num = (1 - a) * num_orig + a * num_target
            density = (max - min) / num
            return [min, max, density]

        self.mobject.x_range = mix_up(self.ox_range, self.tx_range)
        self.mobject.y_range = mix_up(self.oy_range, self.ty_range)
        self.mobject.redraw()


class Asymptotics(Scene):
    def construct(self):
        default()

        # TODO riso pls nakodi tohle

        # So, ladies and gentlemen, it is with utmost pride that, today, we, the polylog team, can present to you a simple algorithm for factoring numbers for which we can also prove that its time complexity is asymptotically optimal! [tadá zvuk?]
        our_algo = m.ImageMobject("img/program3x_placeholder.png")
        our_algo.width = 16 * 0.75
        self.play(FadeIn(our_algo))
        target_size = 0.5
        scale_width = target_size / our_algo.width
        scale_height = target_size / our_algo.height

        COLOR_OURS = "#002b36"
        COLOR_OURS_BAD = CYAN
        COLOR_YOURS = RED

        def make_ranges(max_x, max_y):
            return (
                [0, max_x, 1],
                [0, max_y, 1],
            )

        x_range1, y_range1 = make_ranges(1e2, 1e5)
        x_range2, y_range2 = make_ranges(1e3, 1e6)
        x_range3, y_range3 = make_ranges(5e3, 5e7)

        def f_ours_good(x):
            return x**2 * 2

        def f_ours_bad(x):
            return x**3 / 1e3

        def f_yours(x):
            return x**2

        plot = (
            RescalablePlot(
                x_range=x_range1,
                y_range=y_range1,
                fns=[(f_yours, COLOR_YOURS), (f_ours_good, COLOR_OURS)],
            )
            .scale(0.9)
            .shift(LEFT)
        )
        # labels = axes1.get_axis_labels(x_label="input size", y_label="time")

        self.play(
            our_algo.animate.scale((scale_width, scale_height, 1)).next_to(plot, RIGHT)
        )
        our_algo_placeholder = (
            Square(
                color=COLOR_OURS,
                fill_opacity=1,
            )
            .scale(0.5)
            .scale(target_size)
            .move_to(our_algo)
        )
        self.bring_to_back(our_algo_placeholder)
        badge = (
            Circle(color=ORANGE, fill_opacity=1)
            .scale(0.15 * target_size)
            .move_to(our_algo)
            .shift(0.15 * DOWN + 0.15 * RIGHT)
        )
        our_algo_full = our_algo
        our_algo = VGroup(badge, our_algo_placeholder)
        # our_algo = our_algo_placeholder

        your_algo = (
            Triangle(color=COLOR_YOURS, fill_opacity=1)
            .scale(0.5 * target_size)
            .next_to(our_algo, DOWN)
        )
        self.play(FadeOut(our_algo_full), FadeIn(badge), FadeIn(your_algo))

        self.play(Write(plot))

        self.play(RescalePlot(plot, x_range=x_range2, y_range=y_range2, run_time=4))
        self.wait(1)
        # self.play(RescalePlot(plot, x_range=x_range3, y_range=y_range3, run_time=2))

        plot.fns.pop()
        plot.fns.append((f_ours_bad, COLOR_OURS_BAD))
        self.play(plot.animate.redraw())
        self.wait(1)
        self.play(RescalePlot(plot, x_range=x_range3, y_range=y_range3, run_time=4))

        # Asymptotic optimality means that whenever you come up with some amazing factoring algorithm, I can prove that my algorithm is either faster than yours, or if my algorithm is slower, it is slower only by a constant factor.
        # For example, perhaps my algorithm is twice as slow as yours, but it is at most twice as slow for all inputs, even very large ones.

        # So it is not possible that you could come up with an algorithm such that as the input size increases, my algorithm would get slower and slower relative to yours.

        # In other words, up to constant factors, our algorithm completely nails it.

        # I won’t tell you now how our algorithm works, I will explain that in a followup video that we publish in the next few days. Until then, check out our algorithm and try to understand what it is doing!
        # Or just run the algorithm on some real data! In that case be careful, our implementation is in Python, so it’s a bit slow. Good luck and see you in a few days with the follow-up video!

        self.wait(5)


class Factoring(Scene):
    def construct(self):
        default()

        authors_tex = Tex(
            "[Boudot, Gaudry, Guillevic, Heninger, Thomé, Zimmermann], $~3000$ CPU years"
        )
        authors_tex.scale(0.4)

        def allow_breaks(s):
            return "\hskip 0pt{}".join(s)

        n_tex, a_tex, b_tex = [
            Tex("\\hsize=9cm{}" + allow_breaks(str(n)), tex_environment=None).scale(0.8)
            for n in horrible_multiplication()
        ]
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

        self.play(FadeIn(mult_group))
        self.wait()

        self.wait(5)


class Polylog(Scene):
    def construct(self):
        default()
        authors = Tex(
            r"\textbf{Richard Hladík, Filip Hlásek, Václav Rozhoň, Václav Volhejn}",
            color=text_color,
            font_size=40,
        ).shift(3 * DOWN + 0 * LEFT)

        channel_name = Tex(r"polylog", color=text_color)
        channel_name.scale(4).shift(1 * UP)
        channel_name_without_o = Tex(r"p\hskip 5.28pt lylog", color=text_color)
        channel_name_without_o.scale(4).shift(1 * UP)

        logo_solarized = (
            SVGMobject("img/logo-solarized.svg")
            .scale(0.55)
            .move_to(2 * LEFT + 0.95 * UP + 0.49 * RIGHT)
        )
        self.play(
            Write(authors),
            Write(channel_name),
        )
        self.play(FadeIn(logo_solarized))
        self.add(channel_name_without_o)
        self.remove(channel_name)

        self.wait()

        self.play(*[FadeOut(o) for o in self.mobjects])
        self.wait()
