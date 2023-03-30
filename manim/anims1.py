from manim import *
import manim as m  # hack for type hinting
from utils import *
from utils.utilcliparts import *

# ^ also imports manim and changes some of its defaults


class Polylogo(BasePolylogo):
    def construct(self):
        default()
        self.construct_logo()
        self.write_logo()
        self.wait()

        self.destroy_logo()
        self.wait()


soft_color = BASE02
soft_opacity = 0.0

K = 10


class Intro(Scene):
    def construct(self):
        default()
        self.next_section(skip_animations=False)

        # What if I asked you to multiply two long primes, each with n digits? That’s simple, you can just use the algorithm you know from school,

        # following numbers are primes http://compoasso.free.fr/primelistweb/page/prime/liste_online_en.php
        num1 = 51797
        num2 = 71713

        num1 = 701527
        num2 = 322351

        num1 = 3202363
        num2 = 8764867

        num1_tex = Tex(str(num1))
        num2_tex = Tex(str(num2))

        self.play(
            FadeIn(Group(num1_tex, num2_tex).arrange(RIGHT, buff=1).move_to(ORIGIN))
        )
        brace_groups = []
        for obj in [num1_tex, num2_tex]:
            brace = Brace(obj, DOWN)
            n_tex = Tex(r"$d$ digits").next_to(brace, DOWN)
            brace_groups.append(Group(brace, n_tex))

        self.play(*[FadeIn(g) for g in brace_groups])
        self.wait()
        self.play(*[FadeOut(g) for g in brace_groups])
        self.wait()

        nums_intermediate = []
        tmp = num2
        while tmp > 0:
            digit = tmp % 10
            tmp //= 10
            nums_intermediate.append(digit * num1)
        num = num1 * num2

        num_tex = Tex(str(num))
        nums_intermediate_tex = [Tex(str(n), z_index=10) for n in nums_intermediate]

        line1 = Line(
            start=num2_tex.get_left() + 0.3 * LEFT, end=num2_tex.get_right(), color=GRAY
        )
        line2 = line1.copy()
        num1_tex_target = num1_tex.copy()
        num2_tex_target = num2_tex.copy()

        objects = Group(
            num1_tex_target,
            num2_tex_target,
            line1,
            *nums_intermediate_tex,
            line2,
            num_tex,
        ).arrange_in_grid(cols=1, cell_alignment=RIGHT)
        times_tex = Tex(r"$\times$").next_to(num2_tex_target, LEFT, buff=0.1)

        for i in range(1, len(nums_intermediate_tex)):
            nums_intermediate_tex[i].align_to(
                nums_intermediate_tex[i - 1][0][-2], RIGHT
            )
        nums_intermediate_rec = [
            SurroundingRectangle(
                num,
                buff=0.1,
                color=soft_color,
                stroke_opacity=soft_opacity,
                fill_color=soft_color,
                fill_opacity=soft_opacity,
                z_index=0,
            )
            for num in nums_intermediate_tex
        ]

        objects.remove(line2)
        line2 = Line(
            end=nums_intermediate_tex[-1].get_left()[0] * RIGHT
            + line2.get_center()[1] * UP,
            start=nums_intermediate_tex[0].get_right()[0] * RIGHT
            + line2.get_center()[1] * UP,
            color=GRAY,
        )
        objects.add(line2)
        # animations

        self.play(
            Transform(num1_tex, num1_tex_target),
            Transform(num2_tex, num2_tex_target),
        )
        self.play(FadeIn(times_tex), FadeIn(line1))

        rec = SurroundingRectangle(
            num2_tex[0][-1],
            buff=0.1,
            color=soft_color,
            stroke_opacity=soft_opacity,
            fill_opacity=soft_opacity,
            fill_color=soft_color,
            z_index=0,
        )
        rec2 = nums_intermediate_rec[0]

        for i in range(len(str(num2))):
            self.add_sound(random_pop_file(), time_offset=0.1)
            if i == 0:
                self.play(
                    # FadeIn(rec),
                    FadeIn(nums_intermediate_tex[i]),
                    # FadeIn(rec2),
                    run_time=0.3,
                )
            else:
                self.play(
                    # rec.animate.move_to(num2_tex[0][-i-1].get_center()),
                    FadeIn(nums_intermediate_tex[i]),
                    # Transform(rec2, nums_intermediate_rec[i]),
                    run_time=0.3,
                )
        # self.play(FadeOut(rec), FadeOut(rec2))
        self.wait()

        self.play(Create(line2))
        for i in reversed(range(len(num_tex[0]))):
            self.add_sound(random_click_file(), time_offset=0.1)
            self.play(FadeIn(num_tex[0][i]), run_time=0.2)
        # self.add
        # self.play(
        #     Succession(
        #         *[
        #             AnimationGroup(FadeIn(let), run_time=0.2)
        #             for let in reversed(num_tex[0])
        #         ]
        #     )
        # )
        self.wait()

        # it takes only roughly n^2 steps to compute the result.

        border = SurroundingRectangle(
            Group(*nums_intermediate_tex), color=RED, fill_opacity=0.1, fill_color=RED
        )
        # brace = Brace(border, RIGHT)
        n2_tex = Tex(r"$d^2$ steps").next_to(brace, RIGHT)

        self.play(
            FadeIn(border),
            # FadeIn(brace),
            FadeIn(n2_tex),
        )
        self.wait()

        self.play(
            FadeOut(objects[2:-2]),
            FadeOut(num1_tex),
            FadeOut(num2_tex),
            FadeOut(objects[-1]),
            FadeOut(times_tex),
            FadeOut(*Group(border, n2_tex)),
        )
        self.wait()

        # But what about the opposite problem where I give you a product of two primes and ask you to find the prime factors. How do you solve that one?

        self.next_section(skip_animations=False)
        # Well, you can check whether that input number is divisible by 2,3,4,5 and so on, until you hit a factor. But if the number on input has n digits, its size is up to 10^n and hence you will need up to sqrt( 10^n) steps before you find a factor.

        sc = 1.2
        num_tex.generate_target()
        num_tex.target = Tex(num).scale(sc).to_edge(LEFT).shift(0.3 * RIGHT + 1.5 * UP)
        div_sign = Tex(r"/").scale(sc).next_to(num_tex.target, RIGHT)
        eq_sign = Tex(r"=").scale(sc).next_to(num_tex.target, RIGHT).shift(2.8 * RIGHT)

        objects = Group(num_tex)

        self.play(
            MoveToTarget(num_tex),
        )
        self.wait()
        self.play(
            FadeIn(Group(div_sign, eq_sign)),
        )

        divisors = []
        divisors += list(range(2, 10))
        for l in range(1, len(num_tex[0])):
            for _ in range(K):
                div = random.randrange(10**l, 10 ** (l + 1) - 1)
                if div < num1:
                    divisors.append(div)
        divisors.sort()

        pairs = []
        for div in divisors:
            tex1 = Tex(str(div)).scale(sc).next_to(eq_sign, LEFT)
            n = "{:.3f}".format(round(num / div, 4))
            tex2 = (
                Tex(r"{{" + n.split(".")[0] + r"}}{{." + n.split(".")[1] + r"$\dots$}}")
                .scale(sc if len(str(round(num / div))) <= 12 else 1)
                .next_to(eq_sign, RIGHT)
            )
            pairs.append([tex1, tex2])

        for pair in pairs:
            pair[1][1].set_color(RED)

        pairs.append(
            [
                Tex(str(num1)).scale(sc).next_to(eq_sign, LEFT).set_color(GREEN),
                Tex(str(num2)).scale(sc).next_to(eq_sign, RIGHT).set_color(GREEN),
            ]
        )

        def f(i):
            if i < 10:
                return (10 - i) / 10.0
            else:
                return 0.1

        self.wait(2)
        fst = True
        for i in range(len(pairs)):
            # if i < len(pairs) - 1:
            self.add_sound(random_click_file(), time_offset=f(i) / 2)
            # elif i == len(pairs) - 1:
            #     self.add_sound(
            #         "audio/polylog_success.wav",
            #         time_offset = 0.1
            #     )
            if fst == True:
                fst = False
                self.play(
                    FadeIn(Group(*pairs[i])),
                )
            else:
                g = Group(*pairs[i])
                for j in [0, 1]:
                    pairs[i][j].save_state()
                g.shift(1 * DOWN).set_color(BACKGROUND_COLOR)
                self.play(
                    Group(*pairs[i - 1])
                    .animate.shift(1 * UP)
                    .set_color(BACKGROUND_COLOR),
                    *[pairs[i][j].animate.restore() for j in [0, 1]],
                    run_time=f(i),
                )
        self.add_sound("audio/polylog_success.wav", time_offset=0.3)
        self.wait(2)

        for pair in pairs[:-1]:
            for one in pair:
                self.remove(one)

        self.wait()
        self.next_section(skip_animations=False)

        brace = Brace(num_tex, DOWN).shift(0.3 * DOWN)
        sqrt_tex = Tex(
            r"{{$d$ digits}}{{$\Rightarrow$ size up to $10^d$}}{{$\Rightarrow$ up to $\sqrt{10^d}$ steps}}"
        )
        sqrt_tex[0].next_to(brace, DOWN)
        sqrt_tex[1].next_to(sqrt_tex[0], DOWN, buff=0.5)
        sqrt_tex[2].next_to(sqrt_tex[1], DOWN, buff=0.5)

        self.play(FadeIn(brace), FadeIn(sqrt_tex[0]))
        self.wait()

        self.play(FadeIn(sqrt_tex[1]))
        self.wait()
        self.play(FadeIn(sqrt_tex[2]))
        self.wait()

        # This is much slower than the time n^2 it takes to multiply two numbers.
        formula_tex = Tex(r"{{$\sqrt{10^d}$}}{{$\gg d^2$}}").next_to(
            sqrt_tex[1], RIGHT, buff=3
        )
        self.play(
            sqrt_tex[2][5:10].copy().animate.move_to(formula_tex[0][0].get_center()),
        )
        self.play(
            FadeIn(formula_tex[1]),
        )
        self.wait(2)


class Factoring(Scene):
    def construct(self):
        default()

        mult_group = horrible_multiplication()
        num_group = mult_group[0]
        authors_tex = mult_group[1]

        t = 0.3
        self.play(
            Succession(
                AnimationGroup(FadeIn(num_group[0]), FadeIn(authors_tex)),
                Wait(t),
                FadeIn(num_group[1]),
                Wait(t),
                FadeIn(num_group[2]),
                Wait(t),
                FadeIn(num_group[3]),
                Wait(t),
                FadeIn(num_group[4]),
            )
        )
        self.wait()

        self.wait(5)


class Asymptotics(Scene):
    def construct(self):
        default()

        our_group = badge_image().shift(3 * RIGHT).set_z_index(10)
        self.add(our_group)

        your_algo = you_image().scale_to_fit_height(5).move_to(3 * LEFT).set_z_index(10)
        self.play(arrive_from(your_algo, LEFT))
        self.wait()
        self.play(our_group.animate.scale(1.3), run_time=0.5)
        self.play(our_group.animate.scale(1 / 1.3), run_time=0.5)
        self.wait()

        target_size = 0.5
        # scale_width = target_size / our_algo.width
        # scale_height = target_size / our_algo.height

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
            return x**3.5 / 2e6 * 1.2

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

        # self.play(
        #     our_algo.animate.scale(
        #         (scale_width * 1.05, scale_height * 1.05, 1)
        #     ).next_to(axes, RIGHT)
        # )
        # our_algo_placeholder = (
        #     Square(
        #         color=COLOR_GOOD,
        #         fill_opacity=1,
        #     )
        #     .scale(0.5)
        #     .scale(target_size)
        #     .move_to(our_algo)
        # )
        # self.bring_to_back(our_algo_placeholder)
        # badge = (
        #     Circle(color=ORANGE, fill_opacity=1)
        #     .scale(0.15 * target_size)
        #     .move_to(our_algo)
        #     .shift(0.15 * DOWN + 0.15 * RIGHT)
        # )
        # our_algo_full = our_algo
        # our_algo = VGroup(our_algo_placeholder, badge)
        # self.add(our_algo)

        # Asymptotic optimality means that whenever you come up with some amazing factoring algorithm, I can prove that my algorithm is either faster than yours, or if my algorithm is slower, it is slower only by a constant factor.
        # For example, perhaps my algorithm is twice as slow as yours, but it is at most twice as slow for all inputs, even very large ones.
        # your_algo = (
        #     Triangle(color=COLOR_YOURS, fill_opacity=1)
        #     .scale(0.5 * target_size)
        #     .next_to(our_algo, DOWN)
        # )
        # self.play(FadeOut(our_algo_full), FadeIn(badge), FadeIn(your_algo))

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
                obj.shift(1 * DOWN)

            return updater

        ptr_group = Group(
            our_group.copy().scale(0.2).set_stroke(BLACK, 0.8),
            MathTex(),
            your_algo.copy().scale(0.2).set_stroke(BLACK, 0.8),
        )

        sc = 0.4
        corner = Point(axes.coords_to_point(0, 0, 0))
        cornerer = make_updater(corner)
        our_group.generate_target()
        your_algo.generate_target()
        our_group.target.scale(sc).set_stroke(BLACK, 1.5)
        your_algo.target.scale(sc).set_stroke(BLACK, 1.5)
        cornerer(our_group.target)
        cornerer(your_algo.target)
        self.play(
            MoveToTarget(our_group),
            MoveToTarget(your_algo),
        )
        self.wait()

        your_algo.add_updater(make_updater(plot_yours))
        our_group.add_updater(make_updater(plot_ours))

        rate_func = rate_functions.double_smooth
        self.play(
            Write(plot_ours, rate_func=rate_func),
            Write(plot_yours, rate_func=rate_func),
            run_time=3,
        )

        zero = axes.coords_to_point(0, 0)
        arrow = Arrow(zero + DOWN, zero)
        self.play(Write(arrow))
        self.wait()

        def ptr_updater(obj):
            x = axes.point_to_coords(arrow.get_center())[0]
            x = max(x, 1e-5)
            y_ours = f_ours(x)
            y_yours = f_yours(x)
            ratio = y_ours / y_yours
            our, tex, your = obj
            tex.become(MathTex(r" = {:.2f}\times".format(ratio)))
            obj.arrange(buff=SMALL_BUFF)
            obj.next_to(arrow, RIGHT).shift(0.3 * DOWN)

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

        self.play(arrow.animate.shift(9 * RIGHT), run_time=4)
        self.wait(1)
        self.play(arrow.animate.shift(4 * LEFT), run_time=2)
        self.wait(1)

        # So it is not possible that you could come up with an algorithm such that as the input size increases, my algorithm would get slower and slower relative to yours.

        # In other words, up to constant factors, our algorithm completely nails it.

        forbidden = (
            Text("×", color=RED, font_size=80)
            .scale_to_fit_height(2)
            .move_to(2 * UP + 1 * LEFT)
        )
        self.play(
            plot_ours.animate.become(plot_bad),
            FadeIn(forbidden, scale=2, run_time=1),
        )
        self.wait()

        self.play(
            arrow.animate(run_time=4).shift(4.5 * RIGHT),
        )

        # I won’t tell you now how our algorithm works, I will explain that in a followup video that we publish in the next few days. Until then, check out our algorithm and try to understand what it is doing!
        # Or just run the algorithm on some real data! In that case be careful, our implementation is in Python, so it’s a bit slow. Good luck and see you in a few days with the follow-up video!

        self.wait(5)


class FinalScene(Scene):
    def construct(self):
        default()
        code_img = (
            ImageMobject("img/program_placeholder.png" if DRAFT else "img/program.png")
            .scale_to_fit_width(14.2)
            .align_to(Dot().to_edge(DOWN), UP)
        )
        self.play(
            code_img.animate.to_edge(DOWN),
            run_time=20,
            rate_func=linear,
        )
        self.wait()


class LadiesandGentlemen(Scene):
    def construct(self):
        default()
        code_img = (
            ImageMobject(
                "img/program_placeholder.png" if DRAFT else "img/program.png",
                z_index=-2,
            )
            .scale_to_fit_width(14.2)
            .align_to(Dot().to_edge(DOWN), UP)
        )

        levin_img = ImageMobject("img/levin.jpg").scale_to_fit_width(3)
        name_txt = Tex("Leonid Levin").scale(0.7).next_to(levin_img, DOWN)
        levin_back = SurroundingRectangle(
            Group(levin_img, name_txt),
            fill_color=BACKGROUND_COLOR,
            fill_opacity=1,
            z_index=-1,
            color=BACKGROUND_COLOR,
        )
        levin_group = Group(levin_back, levin_img, name_txt).shift(3 * LEFT)

        badge_img = badge_image().shift(3 * RIGHT)
        badge_back = SurroundingRectangle(
            badge_img,
            fill_color=BACKGROUND_COLOR,
            fill_opacity=1,
            z_index=-1,
            color=BACKGROUND_COLOR,
        )
        badge = Group(badge_img)

        time_badge = 20
        badge_runtime = 0.8
        self.add_sound("audio/tada_success.mp3", time_offset=time_badge)

        self.play(
            code_img.animate(rate_func=linear, run_time=20).to_edge(DOWN),
            Succession(
                Wait(15),
                FadeIn(levin_group),
            ),
            Succession(
                Wait(time_badge),
                FadeIn(badge, scale=2, run_time=badge_runtime),
            ),
        )
        self.play(FadeOut(code_img), FadeOut(levin_img), FadeOut(name_txt))
        self.wait(5)
