import math

from manim import *

from .utilgeneral import *


def multiplication_animation(scene, num1, num2, obj1, obj2):
    # TODO dá se získat text v obj1?
    # create objects

    nums_intermediate = []
    tmp = num2
    while tmp > 0:
        digit = tmp % 10
        tmp //= 10
        nums_intermediate.append(digit * num1)
    num = num1 * num2

    num1_tex, num2_tex, num_tex = [Tex(str(n)) for n in [num1, num2, num]]
    nums_intermediate_tex = [Tex(str(n)) for n in nums_intermediate]
    num2_tex = Tex(r"$\times$" + str(num2))

    line1 = Line(start=num2_tex.get_left(), end=num2_tex.get_right(), color=GRAY)
    line2 = line1.copy()

    objects = Group(
        num1_tex,
        num2_tex,
        line1,
        *nums_intermediate_tex,
        line2,
        num_tex,
    ).arrange_in_grid(cols=1, cell_alignment=RIGHT)

    for i in range(1, len(nums_intermediate_tex)):
        nums_intermediate_tex[i].align_to(nums_intermediate_tex[i - 1][0][-2], RIGHT)

    objects.remove(line2)
    line2 = Line(
            start=nums_intermediate_tex[-1].get_left()[0] * RIGHT
            + line2.get_center()[1] * UP,
            end=nums_intermediate_tex[0].get_right()[0] * RIGHT
            + line2.get_center()[1] * UP,
            color=GRAY,
        )
    objects.add(line2)
    # animations

    
    anims1 = [
        ReplacementTransform(obj1, num1_tex),
        ReplacementTransform(obj2, num2_tex),
        FadeIn(line1)
    ]

    rec = SurroundingRectangle(num2_tex[0][-1], buff = 0.1, color = RED)
    print(len(str(num2)))
    for i in range(len(str(num2))):
        if i == 0:
            anims1.append(
                AnimationGroup(
                    FadeIn(rec),
                    FadeIn(nums_intermediate_tex[i]),
                )
            )
        else:
            anims1.append(
                AnimationGroup(
                    rec.animate.move_to(num2_tex[0][-i-1].get_center()),
                    FadeIn(nums_intermediate_tex[i])
                )
            )
            rec.move_to(num2_tex[0][-i-1].get_center()),
    anims1.append(
        FadeOut(rec)
    )
    anims1.append(Wait())
    rec.move_to(num2_tex[0][-1].get_center())

    anims2 = AnimationGroup(
        FadeOut(objects),
    )

    return objects, [Succession(*anims1), anims2]


def division_animation(num, obj):
    sc = 1.5
    num_tex = Tex(num).scale(sc).to_edge(LEFT)
    div_sign = Tex(r"/").scale(sc).next_to(num_tex, RIGHT)
    eq_sign = Tex(r"=").scale(sc).next_to(num_tex, RIGHT).shift(4 * RIGHT)

    objects = Group(num_tex)

    # animations
    anims1 = Succession(
        ReplacementTransform(obj, num_tex),
        FadeIn(Group(div_sign, eq_sign)),
    )

    anims2 = AnimationGroup(FadeOut(num_tex))

    return objects, [anims1, anims2]


def horrible_multiplication():
    authors_tex = Tex(
        "\\hsize=20cm{} [Boudot, Gaudry, Guillevic, Heninger, Thomé, Zimmermann 2020], RSA Factoring Challenge"
    )
    authors_tex.scale(0.4).to_corner(DR)

    def allow_breaks(s):
        return "\hskip 0pt{}".join(s)

    n = 2140324650240744961264423072839333563008614715144755017797754920881418023447140136643345519095804679610992851872470914587687396261921557363047454770520805119056493106687691590019759405693457452230589325976697471681738069364894699871578494975937497937
    a = 64135289477071580278790190170577389084825014742943447208116859632024532344630238623598752668347708737661925585694639798853367
    b = 33372027594978156556226010605355114227940760344767554666784520987023841729210037080257448673296881877565718986258036932062711

    n_tex, a_tex, b_tex = [
        Tex("\\hsize=9cm{}" + allow_breaks(str(k)), tex_environment=None).scale(0.8)
        for k in [n, a, b]
    ]
    eq_tex = Tex(str(r"="))
    times_tex = Tex(str(r"$\times$"))

    mult_group = Group(
        n_tex,
        eq_tex,
        a_tex,
        times_tex,
        b_tex,
    ).arrange(DOWN)

    return Group(mult_group, authors_tex)


class CollapsibleAsymptotics(VMobject):
    def __init__(self, tex, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tex = MathTex(*[t if t else "{}" for t in tex])
        self.immovable = self.tex[1]
        self.add(self.tex)

    def collapse(self):
        fake_tex = Group(
            MathTex("\mathcal{O}("),
            MathTex(self.immovable.get_tex_string()),
            MathTex(")"),
        )
        fake_tex[0].next_to(self.tex, LEFT, buff=SMALL_BUFF)
        fake_tex[1].shift(self.immovable.get_center() - fake_tex[1].get_center())
        fake_tex[2].next_to(self.tex, RIGHT, buff=SMALL_BUFF)

        new_tex = MathTex("\mathcal{O}(", self.immovable.get_tex_string(), ")")
        new_tex.shift(self.immovable.get_center() - new_tex[1].get_center())
        return AnimationGroup(
            *(FadeIn(new_tex[i], target_position=fake_tex[i]) for i in range(3)),
            FadeOut(self.tex[0], target_position=self.tex[1], scale=(0, 1, 0)),
            FadeOut(self.tex[2], target_position=self.tex[1], scale=(0, 1, 0)),
        )


class ProgramInvocation(VMobject):
    def _make_code(text):
        return Code(
            code=text,
            language="Python",
            tab_width=4,
            style="solarized-light",
            font="monospace",
            insert_line_no=False,
            font_size=24,
            margin=0.2,
        )

    def __init__(self, code, stdin, stdout, ok, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.wheels = 0
        self.code = ProgramInvocation._make_code(code)
        arrow = MathTex(r"\Rightarrow")
        font_size = 24
        self.stdin = VGroup(
            Text(stdin, font="monospace", font_size=font_size), arrow.copy()
        ).arrange()
        color = RED if "Error" in stdout else TEXT_COLOR
        self.stdout = VGroup(
            arrow.copy(),
            Text(stdout, font="monospace", font_size=font_size, color=color),
        ).arrange()
        self.ok = ok
        self.group = VGroup(
            self.stdin,
            self.code,
        ).arrange()
        self.wheel = (
            SVGMobject("img/gear.svg")
            .scale(0.3)
            .set_fill(GRAY)
            .set_stroke_width(0)
            .set_background_stroke_width(0)
            .set_sheen_direction((0, 0, 0))
            .set_sheen_factor(0)
        )
        self.add(self.group)
        self.add_updater(ProgramInvocation.arrange)

    def arrange(self):
        self.group.arrange(center=False)

    def show_output(self):
        self.group.add(self.stdout)
        self.arrange()
        return FadeIn(self.stdout)

    def show_verdict(self):
        if self.ok:
            verdict = Text("✓", color=GREEN, font_size=80)
        else:
            verdict = Text("×", color=RED, font_size=80)
        self.group.add(verdict)
        self.arrange()
        return FadeIn(self.group[-1], scale=3)

    def finish(self, lag_ratio=0.5):
        return AnimationGroup(
            self.show_output(), self.show_verdict(), lag_ratio=lag_ratio
        )

    def step(self):
        self.wheels += 1
        target_angle = -math.radians(90)
        self.group.add(self.wheel.copy())
        cur = self.group[-1]
        cur.save_state()
        cur.rotate(target_angle)
        self.arrange()

        old_obj = self.wheel.copy().next_to(cur, LEFT)
        old_pos = old_obj.get_center()
        target_pos = cur.get_center()

        def update(self, alpha):
            obj = self.group[-1]
            obj.restore()
            obj.move_to(alpha * target_pos + (1 - alpha) * old_pos).set_fill(
                opacity=alpha
            ).rotate(alpha * target_angle)

        return UpdateFromAlphaFunc(
            self,
            update,
            rate_func=rate_functions.ease_in_out_quad,
            suspend_mobject_updating=True,
        )

    def dumb_down(self):
        new_code = ProgramInvocation._make_code("...").move_to(self.code)
        return self.code.animate.become(new_code)


program_alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~ \n"


def nth_python_program(n):
    C = len(program_alphabet)
    l = 1
    while C**l <= n:
        n -= C**l
        l += 1

    # n-th Python program of length l, so, type n in C-ary
    out = []
    for i in range(l):
        out.append(program_alphabet[n % C])
        n //= C
    return "".join(reversed(out))


def program_to_number(code):
    def cmp(i):
        prog = nth_python_program(i)
        if len(prog) < len(code):
            return -1
        if len(prog) > len(code):
            return 1
        for p, c in zip(prog, code):
            if p == c:
                continue
            if program_alphabet.index(p) < program_alphabet.index(c):
                return -1
            else:
                return 1
        return 0

    n = 1
    while cmp(n) < 0:
        n *= 2
    l = n // 2
    r = n
    while l <= r:
        c = (l + r) // 2
        res = cmp(c)
        if res == 0:
            return c
        if res < 0:
            l = c + 1
        else:
            r = c - 1


def programs_around(code, before=0, after=0):
    num = program_to_number(code)
    return [nth_python_program(i) for i in range(num - before, num + after + 1)]


class ProgramInvocationList(VGroup):
    def __init__(self, stdin, expected_stdout, top_pos, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().arrange(DOWN, center=False)
        self.expected_stdout = expected_stdout
        self.top_pos = top_pos
        self.stdin = stdin
        self.arrange()
        self.add_updater(ProgramInvocationList.arrange)
        self.dots = ProgramInvocation("...", self.stdin, "", False)

    def arrange(self):
        for prev, program in zip(self, self[1:]):
            program.align_to(prev, LEFT)
            prev = program

    def add_program(self, program):
        self.add(program)
        if len(self) == 1:
            program.align_to(self.top_pos, UP)
            program.align_to(self.top_pos, LEFT)
        else:
            program.next_to(self[-2], DOWN)
        self.arrange()
        return FadeIn(self[-1])

    def add_dots(self, reps=1):
        return [self.add_program(self.dots.copy()) for _ in range(reps)]

    def add_programs_around(self, code, code_stdout, before=0, after=0):
        anims = []
        num = program_to_number(code)
        pre = []
        post = []
        for i in range(num - before, num + after + 1):
            if i == num:
                stdout = code_stdout
                ok = stdout == self.expected_stdout
            else:
                stdout = "SyntaxError"
                ok = False
            anims.append(
                self.add_program(
                    ProgramInvocation(nth_python_program(i), self.stdin, stdout, ok)
                )
            )
            if i < num:
                pre.append(self[-1])
            elif i > num:
                post.append(self[-1])
            else:
                important_program = self[-1]
        return anims, (pre, important_program, post)
