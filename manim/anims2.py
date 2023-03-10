from utils.utilgeneral import *
from utils.util import *
from manim import *
from utils.utilcliparts import *


class Intro(Scene):
    def construct(self):
        default()
        # This is a continuation of our previous video, you should watch that one first.
        # As many of you guessed by the date when we published our previous video, it was not completely honest. The fact that the video suggested that we solved one of the biggest open problems of computer science may also have been a clue.

        # But you know what? Apart from the video being heavily misleading, what we said there was actually true. Remember, we said that we have a concrete asymptotically optimal algorithm for factoring composite numbers.
        statement_tex = Tex(
            r"Asymptotically optimal algorithm for factoring "
        ).shift(3 * UP)
        downarrow_tex = (
            Tex(r"$\Downarrow ?$").scale(2).next_to(statement_tex, DOWN, buff=1)
        )
        prices_img = [
            ImageMobject("img/turing.jpg").scale_to_fit_height(3),
            ImageMobject("img/fields.jpg").scale_to_fit_height(3),
            ImageMobject("img/abacus.png").scale_to_fit_height(3),
        ]
        prices_group = Group(*prices_img).arrange(RIGHT).next_to(downarrow_tex, DOWN).shift(1*DOWN)


        self.play(FadeIn(statement_tex))
        self.wait()
        self.play(FadeIn(downarrow_tex))
        self.wait()
        self.play(Succession(
            *[FadeIn(price) for price in prices_group]
            ))
        self.wait()
        # TODO vtip s mísou?

        # Before showing you our algorithm, let’s see how it can even be possible that we know such an algorithm and yet do not have Turing awards for finding out what the complexity of factoring is.
        # Well, the only possibility is that although we know the asymptotically optimal algorithm, we unfortunately don’t know what its time complexity is!
        statement2_tex = Tex(r"1) We don't know its time complexity!").next_to(
            statement_tex, DOWN, buff=1
        )

        self.play(
            FadeOut(downarrow_tex),
            FadeOut(prices_group),
        )
        self.play(FadeIn(statement2_tex))
        self.wait()

        # But even if we don’t know the complexity of our algorithm, why not just run it on real instances? If we can solve the factoring problem really fast, it means we can break a huge part of today's cryptography and that sounds interesting even without the math proof that the algorithm works.

        mult_group = horrible_multiplication().scale(0.5).to_edge(DOWN)
        #TODO misto tohohle tam hodit screenshot z předchozího videa

        self.play(FadeIn(mult_group))
        self.wait()
        self.play(FadeOut(mult_group))
        self.wait()
        

        # The only possible conclusion: Our algorithm is insanely slow [sound effect] in practice.

        statement3_tex = (
            Tex(r"2) The algorithm is insanely slow. ")
            .next_to(statement2_tex, DOWN, buff=0.5)
            .align_to(statement2_tex, LEFT)
        )
        self.play(FadeIn(statement3_tex))
        self.wait()

        self.play(
            FadeOut(statement_tex),
            Group(statement2_tex, statement3_tex).animate.to_edge(UP),
            )
        line = Line(start = 10*LEFT, end = 10*RIGHT, color = GRAY).next_to(statement3_tex, DOWN)
        self.play(FadeIn(line))
        self.wait()

        # This is totally possible according to the definition of asymptotic optimality.
        # In computer science, we are doing asymptotic statements all the time, like when we say that select sort has time complexity O(n^2), this big O simply hides some constant in front of the function, plus some lower order terms. [objeví se opravdová komplexita select sortu a u toho “actual complexity”]

        complexities = (
            Group(
                Tex(r"{{$n^2$}}{{$/2$}}{{$ + 3n $}}{{$ + 10$}}"),
                Tex(r"{{$10$}}{{$n^2$}}{{$ + 42$}}"),
                Tex(r"{{$10$}}{{$n^2 $}}{{$ + 42$}}"),
                Tex(r"{{$100000000000$}}{{$n^2$}}"),
            )
            .arrange(DOWN)
            .move_to(3 * LEFT + 2 * DOWN)
        )
        
        for i, obj in zip([0, 1, 1, 1], complexities):
            obj.generate_target()
            obj.target = Tex(r"$O(n^2)$")
            obj.target.shift(
                obj[i][0].get_center()
                - obj.target[0][2].get_center()
            )

        self.play(
            Succession(
                FadeIn(complexities[0]), Wait(),
                FadeIn(complexities[1]), Wait(),
                FadeIn(complexities[2]), Wait(),
            )
        )
        self.wait()

        self.play(
            Succession(
                FadeIn(complexities[0].target), Wait(),
                FadeIn(complexities[1].target), Wait(),
                FadeIn(complexities[2].target), Wait(),
            )
        )
        self.wait()

        
        

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

        logo_solarized = (
            ImageMobject("img/logo-solarized.png")
            .scale(0.032)
            .move_to(2 * LEFT + 1 * UP + 0.5 * RIGHT)
        )
        Group(channel_name, logo_solarized).shift(2 * LEFT + 0.5 * UP)
        authors.scale(0.5).next_to(channel_name, DOWN)

        self.play(
            Write(authors),
            Write(channel_name),
            FadeIn(logo_solarized),
        )
        self.wait()

        levin_img = ImageMobject("img/levin.jpg").scale_to_fit_width(3).to_corner(DR)
        quote_txt = (
            Group(
                Tex(r"\textit{``Only math nerds would call $2^{500}$ finite. ''}"),
                Tex("Attributed to Leonid Levin").scale(0.7),
            )
            .arrange_in_grid(cols=1, cell_alignment=RIGHT)
            .next_to(levin_img, LEFT)
            .align_to(levin_img, DOWN)
        )

        self.play(FadeIn(levin_img), FadeIn(quote_txt))

        self.wait()
        self.play(*[FadeOut(o) for o in self.mobjects])
        self.wait()


class Part1(Scene):
    def construct(self):
        default()
        # Explaining Levin’s search
        # Have you heard this joke that if you give a monkey a typewriter, after sufficiently many trials it writes the complete works of Shakespeare? But you know what? With enough time the monkey also writes all kinds of valid Python programs ([in the remaining cases, it writes Perl program). Now even though I don’t know whether there is an efficient algorithm for factoring composite numbers, if there is one, the monkey also writes its Python implementation, given enough time. And this will be the main idea behind our algorithm.
        # [naobrazku je simpanz ne monkey]

        # [Tady by to chtělo nějaké vtipné programy, nebo možná opice co píše hlavičku programu a tvrdí že vyřeší factoring nebo tak něco

        # undef $/;open(_,$0);/ \dx([\dA-F]*)/while(<_>);@&=split(//,$1);@/=@&;
        # $".=chr(hex(join("",splice(@&,0,2))))while(@&); eval$”;
        # TODO simpanzi nejsou opice

        # http://www.foo.be/docs/tpj/issues/vol3_2/tpj0302-0012.html
        # ]

        chimp_img = ImageMobject("img/chimp.jpg").scale_to_fit_width(6)
        self.add(chimp_img)

        for i in range(20):
            self.add_sound(random_typewriter_file())
            self.wait(0.3)

        return        

        # Instead of hiring monkeys, We are going to iterate over all strings in their lexicographical order, try to interpret each one of them as a program in Python, run it for the input number, and then check if by chance the program factored that number into prime factors.

        # [animace se stackem programů, postupně točíme kolečka a z algortimů vždy vypadne nějaká chybová hláška nebo nějaký output]

        # That’s the main idea. There are just a few small problems with this approach: the most important one is that at some point we encounter algorithms with infinite loops that do not terminate, like this one:

        # while True:
        # 	print(“Are we there yet?”)

        infinite_tex = Tex(r"{{while True: }}{{print(“Are we there yet?”)}}")

        # The naive sequential simulation would get stuck at these algorithms forever [kolečko se na jednom algoritmu furt točí], so we’ll be a bit smarter and do something similar to the diagonalization trick you may know from mathematics.

        # We will maintain a list of candidate algorithms. At the beginning, this list will be empty and we will proceed in steps. In the k-th iterationstep, we first add the k-th lexicographically smallest algorithm to this list and then, we simulate one step of each algorithm. After we are done with all the algorithms in our list, we go to the next iteration, add the next algorithm, simulate one step of each algorithm in the list, and so on.

        # Of course, whenever some simulation of an algorithm finishes, either because the program returned some answer, or, more likely, it simply crashed, we check whether the output of the algorithm is, by chance, two numbers whose product is our input number.

        # In the unlikely case the finished program actually returned a correct solution, we print it to the output and terminate the whole search procedure. Fortunately, this final checking can be done very quickly and this is by the way the only place where we use that our problem is factoring and not something else.

        # And that’s basically the whole algorithm. In the actual code we shared with you, we simulated Brainfuck programs instead of Python programs because it was suggested to us by a higher authority [konverzace s ChatGPT], but in this explanation, let’s stick with Python.

        gpt_img = ImageMobject("img/chatgpt.jpg").scale_to_fit_height(8)

        # This algorithm was discovered by Leonid Levin in the early 1970’s and now it is known as the universal search, so I will use this name from now on.  [Levin s thug life glasses?] I hope that now you can intuitively see how it can happen that we have no idea what the time complexity of the universal search is and also why it is so slow that it struggles to factor the number 4. [Zopakovat ty dva body]

        levin_img = ImageMobject("img/levin.jpg").scale_to_fit_width(3)
        levin_tex = Tex("Leonid Levin")
        levin_group = Group(levin_img, levin_tex).to_corner(DR)

        # But the only thing I promised was that universal search is asymptotically optimal. In other words, I promised that whenever there is some factoring algorithm with time complexity f(n), then the universal search has time complexity O(f(n)), in other words, it is slower at most by a constant factor.

        # For simplicity, I explained a version of the universal search that has a weaker property: whenever there is a factoring algorithm with time complexity f(n), our universal search has time complexity O(f(n)^2 + f(n)*n^2). I will now explain this complexity and then I will tell you how to improve the algorithm to achieve the promised O(f(n)).

        # So, let us fix some valid factoring algorithm that needs f(n) time to factor numbers of size n. To have a concrete example in mind, you can think of the naive algorithm that simply tries to divide the input number by 2,3,4 and so on, until it succeeds.

        # The most important observation is that our universal search will at some point start simulating this algorithm. For example, this code has roughly 1000 letters, so if we are using the ASCII encoding with 128 different letters, it will take only roughly 128^1000 iterations of universal search until we start simulating this algorithm. This number, that I will call L from now on, is ridiculously huge, but what’s absolutely essential is that it is constant and clearly does not depend on the length of the input number we want to factor. [možná input číslo a nad tím svorka n]

        # Ok, so what happens after the Lth iteration at which we start simulating our algorithm on the input? Well, since our algorithm finishes after f(n) steps on inputs with n digits, [needs f(n) steps] and in one iteration we simulate just one step of every algorithm in our growing list, it will take f(n) additional iterations before the simulation of this factoring algorithm finishes. When it finishes, it factors the numbers correctly, and the universal search terminates. [Možná točící se gears, píše checking, tři tečky pak řekne correct!] Of course, maybe it terminates even earlier because of some other factoring algorithm that has already finished.

        # So what is the total number of steps we need to make? Well, look at this triangle diagram that shows how many steps were simulated. In the worst case, the number of steps of the universal search is proportional to the number of dots in this picture. Since it took f(n) steps before we finished simulating our algorithm, we started the simulation of another f(n) algorithms in the meantime. So, the area of this triangle is roughly ½ * (L+f(n))^2. Remember, L is just a constant, so this is simply O(f(n)^2) steps.

        # But we also need to account for the time we spent by checking whether the outputs of the finished algorithms are correct. Remember, to make this check, we need to multiply two long numbers and that takes up to n^2 steps if we do it with the basic multiplication algorithm, so we also need to add the term f(n) * n^2 to the final asymptotic complexity.

        # So this is the analysis of the version of universal search I explained. But how do we improve this complexity to O(f(n)) as I promised? Well, we can do that by tweaking the algorithm a bit: instead of simulating exactly one step of every algorithm in each iteration, we allocate different numbers of steps for different algorithms that will grow as an exponential series. So we run one step in the newest algorithm, then 2 steps in the one before that, then 4 steps and so on. The complexity of such improved universal search becomes O(f(n) + n^2). We still need this additional quadratic term because we simply have to check whether the output is correct by multiplying two long numbers.

        # However, we can get rid of the quadratic term by using a faster algorithm for multiplication. Multiplication algorithms is a complex and fascinating topic, but long story short, in the classical models of computing, there is a way to multiply two long numbers in linear time. If we use that linear time algorithm, n^2 is replaced by n, which is at most f(n), so we finally get the complexity O(f(n)). Nice!
        # [<3000BC unknown  Standard n^2
        # 1962 Karatsuba divide&conquer n^1.58
        # 1963 Toom divide&conquer n^1+o(1)
        # 1966 Schönhage&Strassen FFT n polylog(n)
        # 1979 Schönhage FFT + tricks n (word RAM)
        # 2019 Harvey&van Der Hoeven dark magic nlog(n) (bit operations)
        # ]

        mult_algs_texts = [
            ["When", "Who", "Technique", "Complexity"],
            ["$<$3000BC", "unknown", "straightforward", r"$O(n^2)$"],
            ["1962", "Karatsuba", "divide \& conquer", r"$O(n^{1.58})$"],
            ["1963", "Toom", "divide \& conquer", r"$O(n^{1.01})$"],
            ["1966", "Schönhage \& Strassen", "FFT", r"$n \cdot \text{polylog}(n)$"],
            ["1979", "Schönhage", "FFT + tricks", r"$O(n)$ {\tiny (word RAM)}"],
            [
                "2019",
                "Harvey \& van Der Hoeven",
                "dark magic",
                r"$O(n\text{log}(n))$ {\tiny (bit operations)}",
            ],
        ]

        mult_algs_group = (
            Group(*[Tex(str).scale(0.5) for line in mult_algs_texts for str in line])
            .arrange_in_grid(cols=4)
            .to_corner(DR)
        )

        self.play(FadeIn(mult_algs_group))
        self.wait()

        self.play(
            Circumscribe(mult_algs_group[4 * 5 : 4 * 6], color=RED),
        )
        self.wait()

        # I hope you can see that the universal search is a pretty general algorithm. For example, let’s say we want to solve another classical problem: sorting. Then we can simply change a few lines of code in the universal search: we now check whether the output of a simulated algorithm is the same set of numbers as those we received on input, but in the sorted order. [assume uniqueness]  And now we have an asymptotically optimal algorithm for sorting! Of course, as in the case of factoring, though asymptotically optimal, this sorting algorithm is entirely useless.
