from manim import *
from utils.util import *
from utils.utilcliparts import *
from utils.utilgeneral import *

prop1_str = r"1) We don't know its time complexity!"
prop2_str = r"2) It's insanely slow. "


class Intro(Scene):
    def construct(self):
        default()
        # This is a continuation of our previous video, you should watch that one first.
        # As many of you guessed by the date when we published our previous video, it was not completely honest. The fact that the video suggested that we solved one of the biggest open problems of computer science may also have been a clue.

        # But you know what? Apart from the video being heavily misleading, what we said there was actually true. Remember, we said that we have a concrete asymptotically optimal algorithm for factoring composite numbers.

        # our_algo_img = make_our_algo()
        # self.play(
        #     FadeIn(our_algo_img),
        # )
        # self.wait()

        # badge_img = make_badge_img()

        # badge_img.generate_target()
        # badge_img.target.scale(0.85).align_to(our_algo_img, DR).shift(2.5 * DOWN)

        # our_algo = Group(our_algo_img, badge_img)

        # self.play(FadeIn(badge_img))
        # self.wait()

        # self.play(MoveToTarget(badge_img))
        # self.wait()

        # our_group = Group(our_algo_img, badge_img)
        # self.play(our_group.animate.scale_to_fit_height(3).move_to(2 * UP))

        our_group = badge_image().scale(1.3)
        self.play(FadeIn(our_group))
        self.wait()
        self.play(
            our_group.animate.scale(0.7)
            .scale_to_fit_height(3)
            .set_stroke(BLACK, 1.5)
            .move_to(2 * UP)
        )

        # statement_tex = Tex(r"Asymptotically optimal algorithm for factoring ").shift(
        #     3 * UP
        # )
        downarrow_tex = (
            Tex(r"$\Downarrow ?$").scale(2).next_to(our_group, DOWN, buff=0.5)
        )
        prices_img = [
            ImageMobject("img/turing.png").scale_to_fit_height(2.5),
            ImageMobject("img/fields.jpg").scale_to_fit_height(2.5),
            ImageMobject("img/abacus.png").scale_to_fit_height(2.5),
        ]
        prices_group = (
            Group(*prices_img)
            .arrange(RIGHT)
            .next_to(downarrow_tex, DOWN)
            .shift(0.1 * DOWN)
        )
        self.play(FadeIn(downarrow_tex))
        self.wait()
        self.play(Succession(*[FadeIn(price) for price in prices_group]))
        self.wait()

        # Before showing you our algorithm, let’s see how it can even be possible that we know such an algorithm and yet do not have Turing awards for finding out what the complexity of factoring is.
        # Well, the only possibility is that although we know the asymptotically optimal algorithm, we unfortunately don’t know what its time complexity is!
        our_group.generate_target()
        our_group.target.to_edge(LEFT)
        statement2_tex = (
            Tex(prop1_str).next_to(our_group.target, RIGHT, buff=0.5).shift(0.5 * UP)
        )

        self.play(
            MoveToTarget(our_group),
            FadeOut(downarrow_tex),
            FadeOut(prices_group),
        )
        self.play(FadeIn(statement2_tex))
        self.wait()

        # But even if we don’t know the complexity of our algorithm, why not just run it on real instances? If we can solve the factoring problem really fast, it means we can break a huge part of today's cryptography and that sounds interesting even without the math proof that the algorithm works.

        mult_group = horrible_multiplication().scale(0.5).to_edge(DOWN)
        # TODO misto tohohle tam hodit screenshot z předchozího videa

        self.play(FadeIn(mult_group))
        self.wait()
        self.play(FadeOut(mult_group))
        self.wait()

        # The only possible conclusion: Our algorithm is insanely slow [sound effect] in practice.

        statement3_tex = (
            Tex(prop2_str)
            .next_to(statement2_tex, DOWN, buff=0.5)
            .align_to(statement2_tex, LEFT)
        )
        self.play(FadeIn(statement3_tex))
        self.wait()

        # self.play(
        #     Group(statement2_tex, statement3_tex).animate.to_edge(UP),
        # )
        line = Line(start=10 * LEFT, end=20 * RIGHT, color=GRAY).next_to(
            our_group, DOWN
        )
        self.play(FadeIn(line))
        self.wait()

        # This is totally possible according to the definition of asymptotic optimality.
        # In computer science, we are doing asymptotic statements all the time, like when we say that select sort has time complexity O(n^2), this big O simply hides some constant in front of the function, plus some lower order terms. [objeví se opravdová komplexita select sortu a u toho “actual complexity”]

        complexities = Group(
            CollapsibleAsymptotics(["", "n^2", "/2 + n/2"]),
            CollapsibleAsymptotics(["3", "n^2", " + 3n + 10"]),
            CollapsibleAsymptotics(["10", "n^2", "{} + 42"]),
            CollapsibleAsymptotics([r"1\,000\,000\,", "n^2", ""]),
        )
        eq_texs = []
        for i in range(len(complexities)):
            eq_texs.append(Tex(r"$=$"))

        table = (
            Group(
                *[o for l in zip(complexities, eq_texs, complexities.copy()) for o in l]
            )
            .arrange_in_grid(cols=3)
            .move_to(1.7 * DOWN)
        )

        for i in range(len(complexities)):
            table[3 * i + 2].generate_target()
            table[3 * i + 2].move_to(table[3 * i].get_center())
            table[3 * i + 2].target.shift(
                table[3 * i + 1].get_center()
                + 1.3 * RIGHT
                - table[3 * i + 2].target.immovable.get_center()
            )

        self.play(AnimationGroup(*map(FadeIn, complexities[0:3]), lag_ratio=1.5))
        self.wait()

        self.play(
            FadeIn(table[1]),
            FadeIn(table[3 + 1]),
            FadeIn(table[6 + 1]),
            MoveToTarget(table[2]),
            MoveToTarget(table[3 + 2]),
            MoveToTarget(table[6 + 2]),
        )
        self.wait()

        self.play(
            AnimationGroup(
                table[2].collapse(),
                table[3 + 2].collapse(),
                table[6 + 2].collapse(),
                lag_ratio=1.5,
            ),
        )
        self.wait()

        self.play(FadeIn(table[3 * 3]))
        self.wait()
        table[11].target.next_to(table[10], RIGHT)
        self.play(FadeIn(table[10]), MoveToTarget(table[11]))
        self.wait()
        self.play(
            table[11].collapse(
                table[11]
                .tex[1]
                .copy()
                .align_to(table[8].new_tex[1], RIGHT)
                .get_center()
            )
        )
        self.wait()

        self.play(
            *[
                FadeOut(o)
                for o in self.mobjects
                if o.get_center()[1] < line.get_center()[1]
            ]
        )

        self.wait(3)

        # select_tex = (
        #     Tex("{{Asymptotic time complexity of select sort }}{{$= O(n^2)$. }}")
        #     .next_to(statement3_tex, DOWN, buff=1)
        #     .to_edge(LEFT)
        # )
        # select_tex2 = (
        #     Tex("{{Actual time complexity: }}{{$= n^2/2 + 3n + 10$. }}")
        #     .next_to(select_tex, DOWN, buff=0.5)
        #     .align_to(select_tex, LEFT)
        # )
        # select_tex2[1].next_to(select_tex[1], DOWN, buff=0.5).align_to(
        #     select_tex[1], LEFT
        # )

        # self.play(FadeIn(select_tex))
        # self.wait()

        # self.play(FadeIn(select_tex2))
        # self.wait()

        # # So all of these functions are O(n^2). [asi bych tam dal i n nebo něco takového protože později implicitně používáme že O není theta]

        # self.play(
        #     FadeOut(
        #         Group(
        #             select_tex[0],
        #             select_tex[1][0],
        #             select_tex[1][-1],
        #             select_tex2[0],
        #             select_tex2[1][0],
        #         )
        #     )
        # )
        # self.wait()

        # complexities = (
        #     Group(
        #         Tex(r"$n^2/2 + 3n + 10$"),
        #         Tex(r"$10n^2 + 42$"),
        #         Tex(r"$n/2$"),
        #         Tex(r"$100000000000n^2$"),
        #     )
        #     .arrange(DOWN)
        #     .move_to(3 * LEFT + 2 * DOWN)
        # )
        # brace = Brace(complexities, RIGHT, buff=1)
        # n2_tex = Tex(r"$O(n^2)$").next_to(brace, RIGHT, buff=1)

        # self.play(
        #     ReplacementTransform(select_tex[1][1:-1], n2_tex),
        #     ReplacementTransform(select_tex2[1][1:], complexities[0]),
        #     FadeIn(brace),
        # )

        # for i in range(1, len(complexities)):
        #     self.play(
        #         FadeIn(complexities[i]),
        #     )
        # self.wait()

        # # In particular, one million times n^2 is also O(n^2), although such an algorithm would be extremely slow in practice. So asymptotic complexity may sometimes be deceptive. It is an empirical fact that this does not usually happen, but you will soon see that our case is, well, very exceptional.

        # self.play(Circumscribe(complexities[-1], color=RED))
        # self.wait()

        # The constant factors in our algorithm are so tragically huge that it struggles to factor even 4 = 2x2. [ukázat, jak to pouštíme v terminálu pro čtyřku]

        # With these two points in mind, let’s now look at what our algorithm actually does.
        # [1) We don’t know the time complexity of the algorithm
        # 2) The algorithm is extremely slow]


class Polylogo(BasePolylogo):
    def construct(self):
        default()
        self.construct_logo()
        Group(self.channel_name, self.logo_solarized).shift(2 * LEFT + 0.5 * UP)
        self.authors.scale(0.5).next_to(self.channel_name, DOWN)

        self.write_logo()
        self.wait()

        levin_img = ImageMobject("img/levin.jpg").scale_to_fit_width(3).to_corner(DR)
        quote_txt = (
            Group(
                Tex(r"\textit{``Only math nerds would call $2^{500}$ finite.''}"),
                Tex("Attributed to Leonid Levin").scale(0.7),
            )
            .arrange_in_grid(cols=1, cell_alignment=RIGHT)
            .next_to(levin_img, LEFT)
            .align_to(levin_img, DOWN)
        )

        self.play(FadeIn(levin_img), FadeIn(quote_txt))

        self.wait()
        self.destroy_logo()


class MonkeyTyping(Scene):
    def construct(self):
        default()
        # Explaining Levin’s search
        # Have you heard this joke that if you give a monkey a typewriter, after sufficiently many trials it writes the complete works of Shakespeare? But you know what? With enough time the monkey also writes all kinds of valid Python programs ([in the remaining cases, it writes Perl program). Now even though I don’t know whether there is an efficient algorithm for factoring composite numbers, if there is one, the monkey also writes its Python implementation, given enough time. And this will be the main idea behind our algorithm.
        # [naobrazku je simpanz ne monkey]

        # [Tady by to chtělo nějaké vtipné programy, nebo možná opice co píše hlavičku programu a tvrdí že vyřeší factoring nebo tak něco

        # undef $/;open(_,$0);/ \dx([\dA-F]*)/while(<_>);@&=split(//,$1);@/=@&;
        # $".=chr(hex(join("",splice(@&,0,2))))while(@&); eval$”;

        # http://www.foo.be/docs/tpj/issues/vol3_2/tpj0302-0012.html
        # ]

        def perl_program(randomize=True):
            str = r"""undef $/;open(_,$0);/ \dx([\dA-F]*)/while(<_>);@&=split(//,$1);@/=@&;
$".=chr(hex(join("",splice(@&,0,2))))while(@&); eval$”;
($C,$_,@\)=(($a=$/[1]*4)*5+1, q| |x(0x20).q|\||.chr(32)x(0x10).q$*$.
chr(0x20)x(0x10).(pack("CC",124,10)), sub{s/.\|(\s*?)(\S)./\|$1 $2/},
sub{s/\|(\s*?).(\S)/ \|$1$2 /}, sub{$2.$1.$3},sub{$tt=(3*$tt+7)%$C},
sub{$1.$3.$2}); while ($_) {sselect $/, undef, $/, $C/1E3;(sysread(STDIN,
$k, 1),s/(.)(\*)(.)/(&{$\[(ord($k)-44&2)+2]})/e) if (select($a=chr(1),$/,$/,0));
print 0x75736520504F5349583B2024743D6E657720504F5349583A3A5465726D696F73
3B24742D3E676574617474722828303D3E2A5F3D5C2423292F32293B2024742D3E
365746C666C61672824742D3E6765746C666C6167267E284543484F7C4543484F4
7C4943414E4F4E29293B2024742D3E7365746363285654494D452C31293B24742D
E7365746174747228302C544353414E4F57293B24643D224352415348215C6E223B0A;
  ($p?(/.{70}\|$/):(/^\|/))||(&{$\[3]}<$/[0])?($p=!$p):&{$\[$p]}||die("$d");
  (&{$\[3]}<$/[1])&&(s/ \|$/\|/);(/\|.*\*.*\|$/)||die("$d");}
(by David Powell, Obfuscated Perl Contest) """
            if not randomize:
                return str.split("\n")
            return [
                "".join(random.sample(line, len(line))) for line in str.splitlines()
            ]

        def random_text(num_of_lines, line_length=30):
            from string import ascii_lowercase, ascii_uppercase, digits

            choices = ascii_lowercase + ascii_uppercase + digits + "              /.,"

            ret = []
            for _ in range(num_of_lines):
                ret.append("".join(random.choices(choices, k=line_length)))
            return ret

        texts = [
            random_text(5),
            random_text(4),
            random_text(6),
            random_text(5),
            r"""SONNET 1:
From fairest creatures we desire increase,
That thereby beauty’s rose might never die,
But as the riper should by time decease,
His tender heir might bear his memory;
But thou, contracted to thine own bright eyes,
Feed’st thy light’s flame with self-substantial fuel,
Making a famine where abundance lies,
Thyself thy foe, to thy sweet self too cruel.
Thou that art now the world’s fresh ornament
And only herald to the gaudy spring,
Within thine own bud buriest thy content,
And, tender churl, mak’st waste in niggarding.
Pity the world, or else this glutton be,
To eat world’s bananas, by the grave and thee.
            """.strip().split(
                "\n"
            ),
            random_text(5),
            random_text(4),
            random_text(6),
            """
for i in range(42):
    print(
        f"{i+1} bananas is better",
        "than {i} bananas."
    )
            """.strip().split(
                "\n"
            ),
            random_text(10, 50),
            perl_program(False),
            random_text(10, 50),
            random_text(5),
            random_text(4),
            """
# Absolutely amazing factoring algorithm

import antigravity
import delorean
import this
import time

def factor(n):

    # Buy us some time:
    time.sleep(-10**n)

    arp = "X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"

    # TODO: refactor
    def is_true(var):
        if var == True:
            return True
        else:
            return False

    for self in this.s:
""".split(
                "\n"
            ),
        ]

        chimp_img = (
            ImageMobject("img/chimp.jpg", z_index=100)
            .scale_to_fit_width(6)
            .to_corner(UR, buff=0.2)
        )
        self.play(FadeIn(chimp_img))
        self.wait()

        paragraphs = (
            VGroup(
                *(
                    Paragraph(
                        *lines,
                        z_index=0,
                        font="monospace",
                        line_spacing=1.2,
                        font_size=0.7 * DEFAULT_FONT_SIZE,
                    ).scale(0.5)
                    for lines in texts
                )
            )
            .arrange_in_grid(cols=1, cell_alignment=LEFT, buff=1)
            .align_to(Dot().to_edge(DOWN), UP)
            .align_to(Dot().to_edge(LEFT), LEFT)
        )

        for par in paragraphs:
            for line in par:
                for char in line:
                    char.set_color(BACKGROUND_COLOR)

        def updater(obj, alpha):
            total = sum(sum(len(line) for line in par) for par in paragraphs)
            end = int(alpha * total)

            def do_updating():
                remains = end
                for par in paragraphs:
                    for line in par:
                        for char in line:
                            remains -= 1
                            char.set_color(GRAY)
                            if remains <= 0:
                                return line
                return char

            last = do_updating()
            current_pos = last.get_bottom()[1]
            want_pos = -config["frame_y_radius"] + 0.1
            paragraphs.shift((want_pos - current_pos) * UP)

        self.wait(2)

        self.add_sound("audio/typewriter/typewriter_long.mp3", time_offset=0)

        self.add(paragraphs)
        self.play(
            UpdateFromAlphaFunc(
                paragraphs, updater, rate_func=linear, run_time=8 if DRAFT else 40
            )
        )
        self.wait(3)


# Smaller values for faster preview
NUM_DOTS = 5
NUM_AROUND = 5
if not DRAFT:
    NUM_DOTS = 30
    NUM_AROUND = 15
STDIN = "4"
STDOUT = r"2,2"
INFINITE_PROGRAM = """
while True:
    print("Are we there yet?")
""".strip()


class ProgramsWithoutStepping(MovingCameraScene):
    def construct(self):
        default()
        # Instead of hiring monkeys, We are going to iterate over all strings in their lexicographical order, try to interpret each one of them as a program in Python, run it for the input number, and then check if by chance the program factored that number into prime factors.

        p = ProgramInvocationList(STDIN, STDOUT, 6.5 * LEFT + 3 * UP)
        self.play(
            AnimationGroup(
                *p.add_programs_around("a", "SyntaxError", 0, 10, show_stdin=False)[0],
                lag_ratio=0.1,
            )
        )
        for q in p:
            q.stdin.foo.move_to(q.stdin)
        self.wait(1)
        self.play(AnimationGroup(*(FadeIn(q.stdin.foo) for q in p), lag_ratio=0.2))
        self.play(AnimationGroup(*(q.finish() for q in p[:3]), lag_ratio=0.8))
        self.play(AnimationGroup(*(q.finish() for q in p[3:]), lag_ratio=0.2))
        p.add_dots(NUM_DOTS),
        _, (pre, banana, post) = p.add_programs_around(
            'print("banana")', "banana", NUM_AROUND, NUM_AROUND, fade=False
        )
        self.add(p)  # To display the newly added programs

        self.play(
            self.camera.frame.animate.align_to(banana.get_bottom() + 0.1 * DOWN, DOWN),
            run_time=3,
        )
        self.play(
            AnimationGroup(*(q.finish() for q in pre[-NUM_AROUND:]), lag_ratio=0.2)
        )

        self.play(banana.show_output())
        checker = make_checking_code().move_to(self.camera.frame).shift(4.5 * RIGHT)
        self.play(FadeIn(checker, target_position=banana.get_right(), scale=0))
        self.wait(2)
        self.play(FadeOut(checker))
        self.play(banana.show_verdict())
        for q in post:
            q.finish()

        # That’s the main idea. There are just a few small problems with this approach: the most important one is that at some point we encounter algorithms with infinite loops that do not terminate, like this one:

        p.add_dots(NUM_DOTS)
        _, (pre, infinite, post) = p.add_programs_around(
            INFINITE_PROGRAM, "", NUM_AROUND, 0, fade=False
        )
        self.add(p)
        for q in pre:
            q.finish()
        self.play(
            self.camera.frame.animate.align_to(
                infinite.get_bottom() + 0.1 * DOWN, DOWN
            ),
            run_time=3,
        )
        self.wait(2)
        self.play(infinite.show_output())
        self.wait(2)

        waiting = rotating_wheel().next_to(infinite.group, RIGHT)

        infinite.add(waiting)
        self.play(FadeIn(waiting))

        self.wait(5, frozen_frame=False)
        self.play(
            FadeOut(p[:-1]),
            infinite.animate.align_to(self.camera.frame.get_top() + 0.1 * DOWN, UP),
        )
        self.play(FadeOut(waiting), FadeOut(infinite.stdout_obj))
        self.play(
            infinite.dumb_down(),
            self.camera.frame.animate.align_to(infinite.stdin.get_top() + 0.5 * UP, UP),
        )
        infinite.arrange()

        # The naive sequential simulation would get stuck at these algorithms forever [kolečko se na jednom algoritmu furt točí], so we’ll be a bit smarter and do something similar to the diagonalization trick you may know from mathematics.
        self.wait(2)


# kdyz se generuje kod tak bud zadny zvuk nebo jiny zvuk (da se udelat v postprocessingu)
class ProgramsWithStepping(MovingCameraScene):
    def construct(self):
        default()
        # We will maintain a list of simulated algorithms. At the beginning, this list will be empty and we will proceed in steps. In the k-th iterationstep, we first add the k-th lexicographically smallest algorithm to this list and then simulate one step of each algorithm in the list. After we are done with all the algorithms in our list, we go to the next iteration, add the next algorithm, then simulate one step of each algorithm in the list, and so on.

        p = ProgramInvocationList(STDIN, STDOUT, 6.5 * LEFT)
        p.add_dummy(fade=False)
        self.add(p)
        self.camera.frame.align_to(p[0].stdin.get_top() + 0.5 * UP, UP)
        self.wait(1)
        self.play(FadeIn(p.arrow))
        for i in range(15):
            anims, sound = p.step(say_sound=True)
            self.play(AnimationGroup(*anims, lag_ratio=0.3))
            if sound:
                self.add_sound(step_sound(), time_offset=-0.25)
        # self.wait(5)

        # Of course, whenever some simulation of an algorithm finishes, either because the program returned some answer, or, more likely, it simply crashed, we check whether the output of the algorithm is, by chance, two numbers whose product is our input number.
        prog = p[p.ptr]
        arrow, stdout, tick = p.step(True)
        prog.group[-1].save_state().fade(1)
        checker = (
            make_checking_code()
            .move_to(self.camera.frame)
            .shift(1.5 * RIGHT + 1.5 * UP)
        )
        self.play(arrow, stdout)
        self.play(FadeIn(checker))
        self.wait(2)
        self.play(FadeOut(checker))
        prog.group[-1].restore()
        self.add_sound("audio/polylog_failure.wav", time_offset=0.5)
        self.play(tick)
        self.wait(2)

        for i in range(11):
            anims, sound = p.step(say_sound=True)
            self.play(AnimationGroup(*anims, lag_ratio=0.2))
            if sound:
                self.add_sound(step_sound(), time_offset=-0.25)

        prog = p[p.ptr]
        prog.stdout = STDOUT
        prog.ok = True
        arrow, stdout, tick = p.step(True)
        prog.group[-1].save_state().fade(1)
        self.play(arrow, stdout)
        checker.shift(2 * DOWN + 1 * RIGHT)
        self.play(FadeIn(checker))
        self.wait(2)
        # self.play(FadeOut(checker))
        prog.group[-1].restore()
        self.add_sound("audio/polylog_success.wav", time_offset=0.5)
        self.play(tick)
        self.wait(2)

        output = prog.stdout_obj[1]
        tick = prog.group[-1]
        prog.group.remove(tick)
        prog.stdout_obj.remove(output)
        win_group = (
            VGroup(Text(r"4 = 2 × 2").move_to(output.get_center()), tick.copy())
            .arrange(RIGHT)
            .move_to(self.camera.frame)
            .scale_to_fit_width(self.camera.frame.width)
            .scale(0.2)
            .shift(2 * LEFT)
        )
        self.play(
            FadeOut(p),
            FadeOut(p.arrow),
            output.animate.become(win_group[0]),
            tick.animate.become(win_group[1]),
        )
        self.wait()

        self.play(
            Circumscribe(checker, color=HIGHLIGHT),
            run_time=2,
        )

        # In the unlikely case the finished program actually returned a correct solution, we print it to the output and terminate the whole search procedure. Fortunately, this final checking can be done very quickly and this is by the way the only place where we actually use that our problem is factoring and not something else.
        # [zase pseudokód s if a*b == n → ✓, ten se pak zvětší a trojúhelník zmizí a highlightne se řádka “print(a, b); return”]
        # [A NEBO: tick vedle algoritmu co se zvetsi na celou obrazovku]

        self.wait(5)


class ExplanationBeginning(Scene):
    def construct(self):
        default()

        title_tex = Tex("Universal search", font_size=3 * DEFAULT_FONT_SIZE).to_edge(UP)
        self.play(FadeIn(title_tex))
        self.wait()

        levin_img = ImageMobject("img/levin.jpg").scale_to_fit_width(3)
        name_txt = Tex("Leonid Levin").scale(1).next_to(levin_img, DOWN)
        levin_group = (
            Group(levin_img, name_txt).arrange(DOWN).to_edge(RIGHT).shift(0.3 * DOWN)
        )

        self.play(FadeIn(levin_group))
        self.wait()

        prop1_tex = Tex(prop1_str)
        prop2_tex = Tex(prop2_str)
        props = (
            Group(prop1_tex, prop2_tex)
            .arrange_in_grid(
                cols=1,
                cell_alignment=LEFT,
            )
            .to_edge(LEFT)
        )

        self.play(FadeIn(props))
        self.wait()
        self.play(FadeOut(props), FadeOut(levin_group))
        self.wait()

        shft = 1 * DOWN
        your_algo_img = you_image().scale_to_fit_height(3.5)
        fn = Tex(r"$f(n)$")
        your_algo = Group(your_algo_img, fn).arrange(DOWN).move_to(3 * LEFT).shift(shft)
        self.play(arrive_from(your_algo, LEFT))
        self.wait()

        our_algo_img = badge_image().scale_to_fit_height(3.5)
        fn2 = Tex(r"{{$\mathcal{O}\big( f(n$}}{{)}}{{$ \big)$}}")
        our_algo = (
            Group(our_algo_img, fn2)
            .arrange(DOWN)
            .move_to(3 * RIGHT)
            .align_to(your_algo, DOWN)
        )
        self.play(arrive_from(our_algo, RIGHT))

        fn2_new = Tex(r"{{$\mathcal{O}\big( f(n$}}{{$)^2$}}{{$ \big)$}}").move_to(
            fn2.get_center()
        )
        fn2.save_state()
        self.play(Transform(fn2, fn2_new))
        self.wait()
        self.play(fn2.animate.restore())
        self.wait()

        self.wait(3)


class BazillionScroll(MovingCameraScene):
    def construct(self):
        default()
        # So, let’s say that you give me some algorithm that needs f(n) time to factor numbers of size n. To have a concrete example in mind, we can think of the naive algorithm that simply tries to divide the input number by 2,3,4 and so on, until it succeeds.

        # The most important observation is that our universal search will at some point start simulating this algorithm. For example, we begin to simulate this code in iteration roughly 10^140. I will call this number L from now on. L is ridiculously huge, but what’s absolutely essential is that it is a constant which does not depend on the length of the input number we want to factor.
        p = ProgramInvocationList(STDIN, STDOUT, 6.5 * LEFT)
        p.arrow.fade(1)

        p.add_programs_around("a", "", 0, NUM_AROUND, fade=False)
        self.camera.frame.align_to(p.get_top() + 0.1 * UP, UP)
        p.add_dots(NUM_DOTS)
        _, (_, bazillion, _) = p.add_programs_around(
            FACTORING_EXAMPLE_PROGRAM, "", NUM_AROUND, 0, fade=False
        )

        g = VGroup()
        for q in p:
            if q.text == "...":
                continue
            num = program_to_number(q.text) + 1
            tex = Tex(
                "\\hsize=7cm{}\\rightskip=0pt plus 1fill{} " + allow_breaks(str(num))
            )
            if num > 1e10:
                tex.scale_to_fit_width(6)
            g.add(tex.next_to(q).align_to(self.camera.frame, RIGHT).shift(0.5 * LEFT))
        self.play(FadeIn(p), FadeIn(g))
        self.play(
            self.camera.frame.animate.align_to(
                bazillion.get_bottom() + 0.1 * DOWN, DOWN
            ),
            run_time=3,
        )

        self.wait(1)


class TimeComplexityAnalysis(MovingCameraScene):
    def construct(self):
        default()

        self.next_section(skip_animations=False)
        your_algo = you_image().scale_to_fit_height(2.5).shift(2 * LEFT)
        self.play(arrive_from(your_algo, LEFT))
        code = make_factoring_example_program()
        code.next_to(your_algo)
        self.play(FadeIn(code, target_position=your_algo, scale=0))
        self.wait(2)
        pos = 3 * RIGHT + 2.5 * DOWN
        self.play(Group(code, your_algo).animate.move_to(self.camera.frame).shift(pos))
        self.wait()
        orig_width = self.camera.frame.width

        def your_updater(grp):
            zoom = self.camera.frame.width / orig_width
            code.restore()
            your_algo.restore()
            grp.scale(zoom).move_to(self.camera.frame).shift(zoom * pos)
            your_algo.set_stroke(BLACK, 3 * zoom)

        your_grp = Group(code, your_algo)
        code.save_state()
        your_algo.save_state()
        your_grp.add_updater(your_updater)
        self.add(your_grp)
        # self.remove(code, your_algo)

        # self.play(FadeOut(code, your_algo))
        p = ProgramInvocationList(STDIN, STDOUT, 6.5 * LEFT + 3.7 * UP)
        p.arrow.fade(1)
        L = 5
        time = 10
        ZOOM = 4
        run_time1 = 2
        run_time2 = 2
        if not DRAFT:
            L = 20
            time = 40
            ZOOM = 8
            run_time1 = 10
            run_time2 = 10
        total = L + time - 1
        steps_till_appearance = (L + 1) * L // 2
        steps_till_finished = (total + 1) * (total) // 2 + total - L
        anims = [
            anim
            for _ in range(steps_till_appearance)
            for anim in p.step(move_arrow=False)
        ]
        zoomed_out = self.camera.frame.copy().scale(
            ZOOM, about_point=self.camera.frame.get_corner(UP + LEFT)
        )
        zoomed_out.shift(LEFT * zoomed_out.width * 0.1 + UP * zoomed_out.height * 0.1)
        anim_group = AnimationGroup(
            *anims, lag_ratio=0.5, rate_func=rate_functions.ease_in_out_quad
        )

        add_sounds_for_anims(
            self,
            anim_group,
            run_time1,
            lambda anim: "audio/pop/pop_0.wav"
            if isinstance(anim, UpdateFromAlphaFunc)
            else None,
        )
        self.play(
            anim_group,
            self.camera.frame.animate.become(zoomed_out),
            run_time=run_time1,
        )
        our_prog = p[L - 1]

        # Group(code, your_algo).scale(ZOOM).move_to(self.camera.frame).shift(ZOOM * pos)
        # your_algo.set_stroke(BLACK, 3 * ZOOM)

        self.add(
            code, your_algo
        )  # I hope the fact it is not there for a while can be solved in postprocessing
        # self.play(FadeIn(your_algo))

        your_algo_arrow = Arrow(
            our_prog.get_left() + 0.8 * ZOOM * LEFT,
            our_prog.get_left() + 0.2 * ZOOM * LEFT,
        )
        your_algo_small = (
            your_algo.copy()
            .set_stroke(BLACK, 1 * ZOOM)
            .scale(0.2)
            .next_to(your_algo_arrow, LEFT)
        )
        self.play(
            FadeIn(your_algo_arrow),
            ReplacementTransform(your_algo.copy(), your_algo_small),
        )
        your_grp.remove_updater(your_updater)

        def mkbrace(
            obj,
            text,
            dir,
            buff=0.15 * ZOOM,
            label_buff=0.15 * ZOOM,
            font_size=48 * ZOOM,
            stroke_width=2 * ZOOM,
            sharpness=4 / ZOOM,
            **kwargs
        ):
            brace = Brace(
                obj, dir, buff, stroke_width=stroke_width, sharpness=sharpness, **kwargs
            )
            text = MathTex(text, font_size=font_size)
            brace.put_at_tip(text, buff=label_buff)
            return VGroup(brace, text).set_color(kwargs["color"])

        color_l = RED
        color_fn = BLUE

        l_label = mkbrace(p, "L", LEFT, color=color_l)

        num = program_to_number(FACTORING_EXAMPLE_PROGRAM) + 1
        iter_number = (
            Tex(
                "$L$",
                r"$\,=\,$",
            )
            .scale(ZOOM)
            .next_to(code, UP)
            .shift(ZOOM * (1.5 * UP + 2 * LEFT))
        )
        number = (
            Tex("\\hsize=7cm{}\\rightskip=0pt plus 1fill{}" + allow_breaks(str(num)))
            .scale(0.4 * ZOOM)
            .next_to(iter_number, buff=0.1 * ZOOM)
        )
        iter_number[0][0].set_color(RED)

        self.play(FadeIn(number))
        self.wait()

        self.play(FadeIn(iter_number))
        self.wait()

        self.play(
            FadeOut(iter_number[1], number),
            FadeOut(code),
            FadeOut(your_algo),
            FadeIn(l_label[0]),
            ReplacementTransform(iter_number[0], l_label[1]),
        )
        self.wait()

        anims = [
            anim
            for _ in range(steps_till_appearance, steps_till_finished)
            for anim in p.step(move_arrow=False)
        ]
        anim_last = p.step()
        dist = our_prog.group[3].get_center() - our_prog.group[2].get_center()
        first_wheel = our_prog.group[2]
        last_wheel = our_prog.group[-1]

        fn_label_horiz = mkbrace(
            Group(Point(first_wheel.get_bottom()), Point(last_wheel.get_bottom())),
            "f(n)",
            DOWN,
            buff=0,
            z_index=100,
            color=color_fn,
        )
        fn_tex = fn_label_horiz[1]
        fn_tex.set_z_index(100)
        behind = BackgroundRectangle(
            fn_tex, z_index=99, buff=SMALL_BUFF * ZOOM, corner_radius=0.2 * ZOOM
        )

        self.play(FadeIn(fn_label_horiz), FadeIn(behind))
        anim_group = AnimationGroup(
            *anims, lag_ratio=0.5, rate_func=rate_functions.ease_in_out_quart
        )
        add_sounds_for_anims(
            self,
            anim_group,
            run_time2,
            lambda anim: "audio/pop/pop_0.wav"
            if isinstance(anim, UpdateFromAlphaFunc)
            else None,
        )
        self.play(
            anim_group,
            run_time=run_time2,
        )
        self.play(*anim_last)
        self.add_sound(step_sound(), time_offset=-0.5)
        p.ptr += 1
        our_prog.stdout = STDOUT
        our_prog.ok = True
        self.add_sound("audio/polylog_success.wav", time_offset=0.5)
        self.play(*p.step(finish=True, scale_result=3))

        output = our_prog.stdout_obj[1]
        tick = our_prog.group[-1]
        our_prog.group.remove(tick)
        our_prog.stdout_obj.remove(output)
        win_group = (
            VGroup(output.copy(), tick.copy())
            .move_to(self.camera.frame)
            .scale_to_fit_width(self.camera.frame.width)
            .scale(0.2)
        )
        self.play(
            FadeOut(our_prog.stdout_obj),
            output.animate.become(win_group[0]),
            tick.animate.become(win_group[1]),
        )
        our_prog.stdout_obj.fade(1)
        self.play(FadeOut(output), FadeOut(tick))
        triangle = Polygon(
            p[0].group[2].get_center(),
            p[-1].group[2].get_center(),
            p[0].group[-1].get_center() + dist,
            color=GREEN,
            stroke_width=4 * ZOOM,
        )
        self.play(FadeIn(triangle))
        self.wait(3)
        jag = p.return_for_jagging(L - 1)
        self.play(*map(FadeOut, jag))
        self.wait(2)
        self.play(*map(FadeIn, jag))
        self.wait(2)
        # arrow_down = arrow.copy()
        # arrow_down.generate_target()
        # arrow_down.target.rotate(
        #    -90 * DEGREES).move_to(our_prog.group[2]).align_to(our_prog.group[2].get_center(), UP)
        # self.play(MoveToTarget(arrow_down))
        fn_label_horiz_copy = fn_label_horiz.copy()

        vg = VGroup(p[L:])
        fn_label = mkbrace(vg, "f(n)", LEFT, color=color_fn)
        self.play(fn_label_horiz_copy.animate.become(fn_label))
        self.wait()
        fn_label = fn_label_horiz_copy
        triangle_top = triangle.get_corner(UP + LEFT)
        triangle_bot = triangle.get_corner(DOWN + LEFT)
        alpha = L / (L + time)
        triangle_vmid = (1 - alpha) * triangle_top + alpha * triangle_bot
        l_relabel = mkbrace(
            Group(Line(triangle_top, triangle_vmid)), "L", LEFT, color=color_l
        )
        fn_relabel = mkbrace(
            Group(Line(triangle_vmid, triangle_bot)), "f(n)", LEFT, color=color_fn
        )
        self.play(
            fn_label.animate.become(fn_relabel),
            l_label.animate.become(l_relabel),
            FadeOut(p),
            FadeOut(fn_label_horiz),
            FadeOut(behind),
            FadeOut(your_algo_small),
            FadeOut(your_algo_arrow),
            triangle.animate.set_fill(GREEN, 1),
        )
        self.wait()

        self.remove(p)

        triangle_left = triangle.get_corner(UP + LEFT)
        triangle_right = triangle.get_corner(UP + RIGHT)
        triangle_hmid = (1 - alpha) * triangle_left + alpha * triangle_right
        l_rehor = l_label.copy()
        l_rehor.target = mkbrace(
            Group(Line(triangle_left, triangle_hmid)), "L", UP, color=color_l
        )
        fn_rehor = fn_label.copy()
        fn_rehor.target = mkbrace(
            Group(Line(triangle_hmid, triangle_right)), "f(n)", UP, color=color_fn
        )
        self.wait(2)
        self.play(
            MoveToTarget(fn_rehor),
            MoveToTarget(l_rehor),
        )
        self.wait()

        self.next_section(skip_animations=False)
        area = (
            MathTex(r"{{\text{area} \approx}} \frac12 \cdot ({{L}} + {{f(n)}})^2")
            .scale(ZOOM)
            .move_to(self.camera.frame)
            .shift(ZOOM * (2 * RIGHT + 1 * UP))
        )
        pos2 = area[2].get_center()
        pos4 = area[4].get_center()
        area[2].set_color(color_l).move_to(l_label[1])
        area[4].set_color(color_fn).move_to(fn_label[1])
        self.play(
            *(FadeIn(area[i]) for i in (0, 1, 3, 5)),
            area[2].animate.move_to(pos2),
            area[4].animate.move_to(pos4),
        )
        self.wait()

        area2 = area[1:].copy()
        self.play(area2.animate.shift(ZOOM * 1.5 * DOWN))
        self.wait()
        shift = -area2.get_center()
        for obj in [area, area2, triangle, fn_label, l_label, fn_rehor, l_rehor]:
            obj.shift(shift)
        self.camera.frame.shift(shift)

        a = MathTex(
            r"{{\mathcal{O}\left(}}\frac12 \cdot {{(L + f(n))^2}}{{\right)}}"
        ).scale(ZOOM)
        a.shift(area2[0][0].get_center() - a[1][0].get_center())
        a[2][1].set_color(color_l)
        a[2][3:7].set_color(color_fn)
        self.play(FadeIn(a))
        self.wait()
        self.remove(area2)
        b = MathTex(r"{{\mathcal{O}\left(}}{{(L + f(n))^2}}{{\right)}}").scale(ZOOM)
        b[1][1].set_color(color_l)
        b[1][3:7].set_color(color_fn)
        b.shift(a[2][3].get_center() - b[1][3].get_center())
        b_two = MathTex(r"{{\mathcal{O}\left(}}(L + {{f(n)}}){{^2}}{{\right)}}").scale(
            ZOOM
        )
        b_two[1][1].set_color(color_l)
        b_two[2].set_color(color_fn)
        b_two.shift(a[2][3].get_center() - b_two[2][0].get_center())
        c = MathTex(r"{{\mathcal{O}\left(}}{{f(n)}}{{^2}}{{\right)}}").scale(ZOOM)
        c[1].set_color(color_fn)
        c.shift(a[2][3].get_center() - c[1][0].get_center())
        self.wait()
        self.play(TransformMatchingTex(a, b))
        self.wait()
        self.remove(b)
        self.add(b_two)
        self.wait()
        self.play(TransformMatchingTex(b_two, c))
        self.play(
            *(
                map(
                    FadeOut,
                    (triangle, area, fn_label, l_label, fn_rehor, l_rehor),
                )
            ),
            c.animate.scale(1.5).move_to(self.camera.frame),
        )

        shft = DOWN
        self.camera.frame.center().scale(1 / ZOOM)
        c.center().scale(1 / ZOOM)
        self.camera.frame.shift(-shft)
        c.shift(-shft)

        with_multiplication = MathTex(
            r"{{\mathcal{O}\left(}}{{f(n)}}{{^2}}+{{f(n) \cdot T_\textit{mul}(n)}}{{\right)}}"
        ).scale(2)

        with_multiplication[1].set_color(color_fn)
        with_multiplication[4].set_color(ORANGE2)
        without_multiplication = c.copy().shift(shft)
        self.wait(2)
        checker = make_checking_code().scale(1.5).shift(-shft + 2 * UP)
        self.play(FadeIn(checker), c.animate.shift(shft))
        self.wait()
        self.play(Circumscribe(checker, color=HIGHLIGHT))
        self.wait()
        self.play(TransformMatchingTex(c, with_multiplication))
        self.wait(2)
        self.play(TransformMatchingTex(with_multiplication, without_multiplication))
        self.wait()
        self.play(Circumscribe(without_multiplication[2], color=HIGHLIGHT))
        self.wait()
        self.play(FadeOut(checker), FadeOut(without_multiplication))
        self.wait()

        # Ok, so what happens after the Lth iteration at which we start simulating our algorithm on the input? Well, since our algorithm finishes after f(n) steps on inputs with n digits, [needs f(n) steps] and in one iteration we simulate just one step of every algorithm in our growing list, it will take f(n) additional iterations before the simulation of this factoring algorithm finishes. When it finishes, it factors the numbers correctly, and the universal search terminates. Of course, maybe it terminates even earlier because of some other factoring algorithm that has already finished.

        # So what is the total number of steps we need to make? Well, look at this triangle diagram that shows how many steps were simulated in total. Of course, some of the simulated algorithms may have finished much earlier [ zubatice], but in the worst case, the number of steps of the universal search is proportional to the number of dots in this picture. Since it took f(n) steps before we finished simulating our algorithm, we started the simulation of another f(n) algorithms in the meantime [čára f(n) se orotuje]. So, the area of this triangle is roughly ½ * (L+f(n))^2. Remember, L is just a constant, so this is simply O(f(n)^2) steps.

        # We also need to account for the time we spent by checking whether the outputs of the finished algorithms are correct. Fortunately, if we use the fastest known algorithms for multiplication [*Schonhage 1979] instead of the standard algorithm, the time we spend checking is negligible.
        # [znova se zjeví pseudokód pro checkování, nějaký zvýraznění multiplikace v něm]


class TimeComplexityAfterthoughts(MovingCameraScene):
    def construct(self):
        default()
        p = ProgramInvocationList(STDIN, STDOUT, 13 * LEFT + 7 * UP)
        sc = 2
        self.camera.frame.scale(sc)
        p.arrow.fade(1)
        to_hide = []
        for i in range(5, -1, -1):
            p.add_dummy(fade=False)
            for k in range(1 << i):
                p[-1].step(fade=False)
            num_hide = (1 << i) - (i + 1)
            if num_hide <= 0:
                continue
            for j, cog in enumerate(p[-1].group[-num_hide:]):
                dist = j + 1
                to_hide.append((cog, p[-1].group[-num_hide - 1], dist))
        for cog, *_ in to_hide:
            cog.save_state()
            cog.fade(1)

        og_tex = Tex(
            r"{{Original complexity: }}{{$(L + f(n))^2 $}}{{$=$}}{{$\mathcal{O}(f(n)^2). $}}"
        )
        new_tex = Tex(
            r"{{New complexity: }}{{$2^L \cdot f(n) $}}{{$=$}}{{$\mathcal{O}(f(n)). $}}"
        )
        Group(*og_tex, *new_tex).scale(sc).arrange_in_grid(
            rows=2, buff=MED_SMALL_BUFF * 2, cell_alignment=RIGHT
        ).move_to(1 * DOWN)
        new_tex.shift(0.3 * DOWN)

        self.add(p, og_tex)
        self.wait()

        self.play(
            *(
                UpdateFromAlphaFunc(
                    cog,
                    ProgramInvocation.make_rotating_updater(
                        cog, cog.get_center(), last.get_center(), -90 * dist * DEGREES
                    ),
                    rate_func=rate_functions.smooth,
                    suspend_mobject_updating=True,
                )
                for cog, last, dist in to_hide
            )
        )

        self.wait()
        self.play(
            FadeIn(new_tex[0:2]),
        )
        self.wait()
        bigo_tex = Tex(r"$\mathcal{O}$").scale(10).next_to(new_tex, DOWN, buff=0.7)
        self.play(FadeIn(bigo_tex))
        self.wait()
        self.play(
            FadeIn(new_tex[2]),
            FadeIn(new_tex[3][1:]),
            Transform(bigo_tex, new_tex[3][0]),
        )

        # self.play(*(FadeOut(cog) for cog in to_hide))
        self.wait(5)
