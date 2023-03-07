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


class Asymptotics(Scene):
    def construct(self):
        default()

        # TODO riso pls nakodi tohle

        # So, ladies and gentlemen, it is with utmost pride that, today, we, the polylog team, can present to you a simple algorithm for factoring numbers for which we can also prove that its time complexity is asymptotically optimal! [tadá zvuk?]
        our_algo_img = m.ImageMobject("img/program3x_placeholder.png").scale_to_fit_width(14.2) # TODO nezapomenout vyprintscreenovat final verzi v solarized barvach
        #our_algo.width = 16 * 0.75
        self.play(
            FadeIn(our_algo_img),
        )
        self.wait()
        
        badge_img = ImageMobject("img/badge_downscaled.png").scale_to_fit_width(6)
        badge_tex = Tex(r"Asymptotically \\ optimal!", color = RED).shift(1*UP)
        badge_group = Group(badge_img, badge_tex)


        badge_group.generate_target()
        badge_group.target.scale(0.7).align_to(our_algo_img, DR).shift(1*DOWN)

        our_algo = Group(
            our_algo_img,
            badge_group
        )

        # TODO double check it is ok to use this image: https://gallery.yopriceville.com/Free-Clipart-Pictures/Badges-and-Labels-PNG/Green_Classic_Seal_Badge_PNG_Clipart#.ZAaV6dLMJkg
        
        self.play(
            FadeIn(badge_group)
        )
        self.wait()
        self.play(
            MoveToTarget(badge_group)
        )
        self.wait()

        target_size = 0.5
        scale_width = target_size / our_algo.width
        scale_height = target_size / our_algo.height

        COLOR_GOOD = "#002b36"
        COLOR_BAD = COLOR_GOOD
        COLOR_YOURS = RED
        COLOR_OURS = COLOR_GOOD

        def make_range(max):
            return [0, max, max / 10]

        x_range, y_range = make_range(2e3), make_range(2e5)

        def f_good(x):
            return x**1.5 * 2

        def f_bad(x):
            return x**4 / 4e7

        def f_yours(x):
            return x**1.5

        axes = (
            Axes(
                x_range=x_range,
                y_range=y_range,
            )
            .scale(0.9)
            .shift(LEFT)
        )
        labels = axes.get_axis_labels(
            x_label=r"\text{input size}", y_label=r"\text{time}"
        )

        self.play(
            our_algo.animate.scale(
                (scale_width * 1.05, scale_height * 1.05, 1)
            ).next_to(axes, RIGHT)
        )
        our_algo_placeholder = (
            Square(
                color=COLOR_GOOD,
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
        our_algo = VGroup(our_algo_placeholder, badge)
        self.add(our_algo)

        # Asymptotic optimality means that whenever you come up with some amazing factoring algorithm, I can prove that my algorithm is either faster than yours, or if my algorithm is slower, it is slower only by a constant factor.
        # For example, perhaps my algorithm is twice as slow as yours, but it is at most twice as slow for all inputs, even very large ones.

        your_algo = (
            Triangle(color=COLOR_YOURS, fill_opacity=1)
            .scale(0.5 * target_size)
            .next_to(our_algo, DOWN)
        )
        self.play(FadeOut(our_algo_full), FadeIn(badge), FadeIn(your_algo))

        self.play(Write(axes), Write(labels))

        plot_good = axes.plot(f_good, color=COLOR_GOOD)
        plot_bad = axes.plot(f_bad, color=COLOR_BAD)
        plot_yours = axes.plot(f_yours, color=COLOR_YOURS)
        plot_ours = plot_good.copy()

        def f_ours(x):
            zero = plot_good.get_top()[1]
            one = plot_bad.get_top()[1]
            alpha = (plot_ours.get_top()[1] - zero) / (one - zero)
            return (1 - alpha) * f_good(x) + alpha * f_bad(x)

        def make_updater(plot):
            def updater(obj):
                obj.next_to(plot, RIGHT + UP)
                obj.shift(0.4 * DOWN)

            return updater

        ptr_group = VGroup(
            our_algo.copy().scale(0.7), MathTex(), your_algo.copy().scale(0.7)
        )
        your_algo.add_updater(make_updater(plot_yours))
        our_algo.add_updater(make_updater(plot_ours))

        self.play(Write(plot_ours), Write(plot_yours))

        zero = axes.coords_to_point(0, 0)
        arrow = Arrow(zero + DOWN, zero)
        self.play(Write(arrow))

        def ptr_updater(obj):
            x = axes.point_to_coords(arrow.get_center())[0]
            x = max(x, 1e-5)
            y_ours = f_ours(x)
            y_yours = f_yours(x)
            ratio = y_ours / y_yours
            our, tex, your = obj
            tex.become(MathTex(r" = {:.2f}\times".format(ratio)))
            obj.arrange()
            obj.next_to(arrow, RIGHT)

        def lines_updater(obj):
            ctp = axes.coords_to_point
            x = axes.point_to_coords(arrow.get_center())[0]
            x = max(x, 1e-5)
            y_ours = f_ours(x)
            y_yours = f_yours(x)
            line, point_ours, point_yours = obj
            line.put_start_and_end_on(
                ctp(x, 0),
                ctp(x, max(y_ours, y_yours)),
            )
            # print(len(plot_ours.get_all_points()))
            point_ours.move_to(ctp(x, y_ours))
            point_yours.move_to(ctp(x, y_yours))

        lines_group = VGroup(
            DashedLine(stroke_width=1), Dot(color=COLOR_OURS), Dot(color=COLOR_YOURS)
        )
        ptr_updater(ptr_group)
        lines_updater(lines_group)
        self.remove(ptr_group, lines_group)
        self.play(FadeIn(ptr_group), FadeIn(lines_group))
        ptr_group.add_updater(ptr_updater)
        lines_group.add_updater(lines_updater)

        self.play(arrow.animate.shift(10 * RIGHT), run_time=2)
        self.wait(1)
        self.play(arrow.animate.shift(5 * LEFT))
        self.wait(1)

        # So it is not possible that you could come up with an algorithm such that as the input size increases, my algorithm would get slower and slower relative to yours.

        # In other words, up to constant factors, our algorithm completely nails it.

        self.play(plot_ours.animate.become(plot_bad))

        self.play(arrow.animate.shift(5 * LEFT))
        self.play(arrow.animate.shift(10 * RIGHT), run_time=4)

        # I won’t tell you now how our algorithm works, I will explain that in a followup video that we publish in the next few days. Until then, check out our algorithm and try to understand what it is doing!
        # Or just run the algorithm on some real data! In that case be careful, our implementation is in Python, so it’s a bit slow. Good luck and see you in a few days with the follow-up video!

        self.wait(5)


class Factoring(Scene):
    def construct(self):
        default()

        mult_group = horrible_multiplication()

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
