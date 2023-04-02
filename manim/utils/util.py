import math
import hashlib

from manim import *

from .utilgeneral import *

DRAFT = False


class BasePolylogo(Scene):
    def construct_logo(self):
        self.authors = Tex(
            r"\textbf{Richard Hladík, Filip Hlásek, Václav Rozhoň, Václav Volhejn}",
            color=text_color,
            font_size=40,
        ).shift(3 * DOWN + 0 * LEFT)

        self.channel_name = Tex("p", "o", "lylog", color=text_color)
        self.channel_name[1].fade(1)
        self.channel_name.scale(4).shift(1 * UP)
        # self.channel_name_without_o = Tex(r"p\hskip 5.28pt lylog", color=text_color)
        # self.channel_name_without_o.scale(4).shift(1 * UP)

        self.logo_solarized = (
            SVGMobject("img/logo-solarized.svg")
            .scale(0.56)
            .move_to(2 * LEFT + 0.98 * UP + 0.49 * RIGHT)
        )

    def write_logo(self, **kwargs):
        self.play(
            Write(self.authors),
            Write(self.channel_name),
            FadeIn(self.logo_solarized),
            **kwargs,
        )

    def destroy_logo(self, **kwargs):
        # self.add(self.channel_name_without_o)
        self.remove(self.channel_name[1])
        self.play(*[FadeOut(o) for o in self.mobjects], **kwargs)


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
        FadeIn(line1),
    ]

    rec = SurroundingRectangle(num2_tex[0][-1], buff=0.1, color=RED)
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
                    rec.animate.move_to(num2_tex[0][-i - 1].get_center()),
                    FadeIn(nums_intermediate_tex[i]),
                )
            )
            rec.move_to(num2_tex[0][-i - 1].get_center()),
    anims1.append(FadeOut(rec))
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


def allow_breaks(s):
    return "\hskip 0pt{}".join(s)


def horrible_multiplication():
    authors_tex = Tex(
        "\\hsize=20cm{} [Boudot, Gaudry, Guillevic, Heninger, Thomé, Zimmermann 2020], RSA Factoring Challenge"
    )
    authors_tex.scale(0.4).to_corner(DR)

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
    def __init__(self, tex, font_size=DEFAULT_FONT_SIZE, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tex = MathTex(*[t if t else "{}" for t in tex], font_size=font_size)
        self.font_size = font_size
        self.immovable = self.tex[1]
        self.add(self.tex)

    def collapse(self, target=None):
        fake_tex = Group(
            MathTex("\mathcal{O}(", font_size=self.font_size),
            MathTex(self.immovable.get_tex_string(), font_size=self.font_size),
            MathTex(")", font_size=self.font_size),
        )
        if target is None:
            target = self.immovable.get_center()
        fake_tex[0].next_to(self.tex, LEFT, buff=SMALL_BUFF)
        fake_tex[1].shift(target - fake_tex[1].get_center())
        fake_tex[2].next_to(self.tex, RIGHT, buff=SMALL_BUFF)

        self.new_tex = MathTex(
            "\mathcal{O}(",
            self.immovable.get_tex_string(),
            ")",
            font_size=self.font_size,
        )
        self.new_tex.shift(target - self.new_tex[1].get_center())
        self.new_tex[1].save_state()
        self.new_tex[1].move_to(self.tex[1])
        return Succession(
            AnimationGroup(
                *(FadeIn(self.new_tex[i], target_position=fake_tex[i]) for i in (0, 2)),
                *(
                    FadeOut(
                        self.tex[i],
                        target_position=target,
                        scale=(0, 1, 0) if i != 1 else (1, 1, 0),
                    )
                    for i in (0, 1, 2)
                ),
                self.new_tex[1].animate.restore(),
            ),
        )


class ProgramInvocation(VMobject):
    def make_code(text):
        return Code(
            code=text,
            language="Python",
            tab_width=4,
            style="solarized-light",
            font="monospace",
            insert_line_no=False,
            font_size=24,
            margin=0.15,
            line_spacing=0.4,
        )

    def __init__(
        self,
        code,
        stdin,
        stdout,
        ok,
        show_stdin=True,
        auto_arrange=True,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.wheels = 0
        self.text = code
        self.code = ProgramInvocation.make_code(code)
        self.arrow = MathTex(r"\Rightarrow")
        self.stdin = VGroup(
            Text(stdin, font="monospace", font_size=24), self.arrow.copy()
        ).arrange()
        if not show_stdin:
            self.stdin.foo = self.stdin.copy()
            self.stdin.fade(1)
        self.stdout = stdout
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
        self.wheel = Square()
        self.add(self.group)
        if auto_arrange:
            self.add_updater(ProgramInvocation.arrange)
        self.finished = False

    def arrange(self):
        self.group.arrange(center=False)

    def show_output(self, scale_result=1):
        color = RED if "Error" in self.stdout else TEXT_COLOR
        self.stdout_obj = (
            VGroup(
                self.arrow.copy(),
                Text(self.stdout, font="monospace", font_size=24, color=color),
            )
            .arrange()
            .scale(scale_result)
        )
        self.stdout_obj.next_to(self.group)
        self.group.add(self.stdout_obj)
        return FadeIn(self.stdout_obj)

    def show_verdict(self, scale_result=1):
        if self.ok:
            verdict = Text("✓", color=GREEN, font_size=80, font="monospace")
        else:
            verdict = Text("×", color=RED, font_size=80)
        verdict.scale(scale_result).next_to(self.group)
        self.group.add(verdict)
        return FadeIn(self.group[-1], scale=3)

    def finish(self, lag_ratio=0.5, scale_result=None):
        self.finished = True
        scale_result = scale_result or 1
        anims = [self.show_output(scale_result), self.show_verdict(scale_result)]
        if lag_ratio is None:
            return anims
        return AnimationGroup(*anims, lag_ratio=lag_ratio)

    def make_rotating_updater(obj, target_pos, old_pos, target_angle=-90 * DEGREES):
        def updater(_, alpha):
            obj.restore()
            obj.move_to(alpha * target_pos + (1 - alpha) * old_pos).set_fill(
                opacity=alpha
            ).rotate(alpha * target_angle)

        return updater

    def step(self, finish=False, fade=True, scale_result=None):
        if finish:
            return self.finish(lag_ratio=None, scale_result=scale_result)
        self.wheels += 1
        cur = self.wheel.copy().next_to(self.group)
        self.group.add(cur)
        cur.save_state()
        if fade:
            cur.fade(1)

        if self.wheels > 1:
            old_pos = self.group[-2].get_center()
        else:
            old_pos = self.wheel.copy().next_to(cur, LEFT).get_center()
        target_pos = cur.get_center()
        last = self.group[-1]
        updater = ProgramInvocation.make_rotating_updater(last, target_pos, old_pos)

        return UpdateFromAlphaFunc(
            self,
            updater,
            rate_func=rate_functions.ease_in_out_quad,
            suspend_mobject_updating=True,
            run_time=0.5,
        )

    def dumb_down(self, animate=True):
        new_code = (
            ProgramInvocation.make_code("[code]")
            .move_to(self.code)
            .align_to(self.code, LEFT)
        )
        if animate:
            return self.code.animate.become(new_code)
        else:
            return self.code.become(new_code)


program_alphabet = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ \n!\"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"


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


def rotating_wheel():
    waiting_big = Circle(color=BASE0, stroke_width=8, radius=0.2)
    waiting_small = Arc(color=BASE02, stroke_width=8, radius=0.2).shift(
        waiting_big.get_center()
    )
    waiting = VGroup(waiting_big, waiting_small)
    always_rotate(waiting, rate=-120 * DEGREES)
    return waiting


class SpecialAnimGroup(AnimationGroup):
    # To be able to tell it apart by isinstance
    pass


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
        self.dummy = ProgramInvocation(
            "[code]", self.stdin, "foo", False, auto_arrange=False
        )
        self.ptr = 0
        self.arrow = (
            Arrow(start=RIGHT, end=LEFT)
            .move_to(self.top_pos)
            .shift(0.3 * DOWN)
            .set_x(6)
        )
        self.now_adding = False

    def arrange(self):
        for prev, program in zip(self, self[1:]):
            program.align_to(prev, LEFT)
            prev = program

    def add_program(self, program, fade=True, special_group=False):
        if len(self) == 0:
            program.align_to(self.top_pos, UP)
            program.align_to(self.top_pos, LEFT)
        else:
            program.next_to(self[-1], DOWN).align_to(self[-1], LEFT)
        self.add(program)
        program.save_state()
        program.stdin.save_state()
        program.code.save_state()
        if fade:
            program.stdin.fade(1)
            program.code.fade(1)
        if special_group:
            group_class = SpecialAnimGroup
            run_time = 0.5
        else:
            group_class = AnimationGroup
            run_time = 1
        return group_class(
            program.stdin.animate(run_time=run_time).restore(),
            program.code.animate(run_time=run_time).restore(),
        )

    def add_dots(self, reps=1):
        return [self.add_program(self.dots.copy(), fade=False) for _ in range(reps)]

    def add_dummy(self, reps=1, fade=True):
        return [
            self.add_program(self.dummy.copy(), fade=fade, special_group=True)
            for _ in range(reps)
        ]

    def add_programs_around(
        self, code, code_stdout, before=0, after=0, fade=True, show_stdin=True
    ):
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
                    ProgramInvocation(
                        nth_python_program(i),
                        self.stdin,
                        stdout,
                        ok,
                        show_stdin=show_stdin,
                    ),
                    fade=fade,
                )
            )
            if i < num:
                pre.append(self[-1])
            elif i > num:
                post.append(self[-1])
            else:
                important_program = self[-1]
        return anims, (pre, important_program, post)

    def point_arrow_at(self, i):
        target = self.arrow.copy().next_to(self[i], RIGHT).set_x(6)
        return self.arrow.animate.move_to(target)

    def step(self, finish=False, scale_result=None, say_sound=False, move_arrow=True):
        anims = []
        oldlen = len(self)

        def mkret(anims):
            if say_sound:
                return anims, sound
            else:
                return anims

        sound = False
        if oldlen == 0:
            return mkret(self.add_dummy())
        if self.now_adding:
            anims_dummy = self.add_dummy()
            if move_arrow:
                anims.append(self.point_arrow_at(oldlen))
            anims.append(*anims_dummy)
            oldlen += 1
            self.now_adding = False
        else:
            sound = True
            step = self[self.ptr].step(finish, scale_result=scale_result)
            if move_arrow:
                anims.append(self.point_arrow_at(self.ptr))
            if type(step) != list:
                step = [step]
            anims += step
            if self.ptr == 0:
                self.now_adding = True
                return mkret(anims)

        while True:
            self.ptr = (self.ptr - 1 + oldlen) % oldlen
            if not self[self.ptr].finished:
                break
        return mkret(anims)

    def return_for_jagging(self, ignore=None):
        cogs = []
        for i, p in enumerate(self):
            if i == ignore or p.wheels <= 2:
                continue
            hsh = hashlib.md5(str(i).encode()).digest()
            hsh = hsh[0] + (hsh[1] << 8) + (hsh[2] << 16)
            if hsh % 2 != 0:
                continue
            num = hsh % (p.wheels - 1) + 1
            cogs += list(p.group[-num:])
        return cogs


def make_checking_code():
    code = ProgramInvocation.make_code(
        """
if a * b == num:

✓
else:

×
""".strip()
    )
    for i, col in (2, GREEN), (-1, RED):
        code.code[i].set_color(col).scale(2.5).shift(0.9 * RIGHT + 0.15 * UP)
    return code


FACTORING_EXAMPLE_PROGRAM = """
for a in range(2, num):
    b = num // a
    if a * b == num:
        return a, b
""".strip()


def make_factoring_example_program():
    return ProgramInvocation.make_code(FACTORING_EXAMPLE_PROGRAM)


def you_image():
    return SVGMobject("img/you.svg").set_stroke(BLACK, 3)


def badge_image():
    return (
        SVGMobject("img/badge_drawing.svg").scale_to_fit_height(5).set_stroke(BLACK, 3)
    )


def arrive_from(obj, dir, buff=0.5):
    pos = obj.get_center()
    obj.align_to(Point().to_edge(dir, buff=0), -dir).shift(buff * dir)
    return obj.animate.move_to(pos)


def step_sound(randomize=True):
    if randomize:
        return random_pop_file()
    else:
        return "audio/pop/pop_0.wav"


def add_sounds_for_anims(scene, anim_group, run_time, sound_fn):
    for anim, start, end in anim_group.anims_with_timings:
        time = (start + end) / 2
        alpha = time / anim_group.max_end_time
        l, r = 0, 1
        for _ in range(20):
            inv = (l + r) / 2
            if anim_group.rate_func(inv) > alpha:
                r = inv
            else:
                l = inv
        time = inv * run_time
        sound = sound_fn(anim, time)
        if sound is not None:
            scene.add_sound(sound, time_offset=time)
