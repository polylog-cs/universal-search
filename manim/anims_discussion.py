from utils.utilgeneral import *
from utils.util import *
from manim import *
from utils.utilcliparts import *


vasek_head = Square(side_length = 3.5, fill_opacity = 1, fill_color = BLACK, color = BLACK).to_corner(DR, buff = 0)

class Discussion1(Scene):
    def construct(self):
        default()
        self.add(vasek_head)
        # So this was Levin’s universal search and I expect that many of you are now a bit confused, shocked, or even disgusted. None of these are the purpose of this video, so let me finish with a bunch of thoughts on how to understand the universal search and what is the lesson you should take away. 

        # First of all, what I don’t want you to take away, is that asymptotic complexity is a broken concept. Let’s say we want to analyze some algorithm like selectsort. There are a bunch of approaches you could take. First, you could code the algorithm and empirically measure its complexity. 

        # TODO ukazat tam selectsort?         
        # def selectsort(array):
        #     for i in range(len(array)):
        #         mn = i
        #         for j in range(i + 1, len(array)):
        #             if array[j] < array[mn]:
        #                 mn = j
        #         array[i], array[mn] = array[mn], array[i]
        


        empirical_img = ImageMobject("img/select.png").scale_to_fit_width(3).to_corner(UL)

        # Or you could count how many steps the algorithm needs to solve any input of size n, but compute this number exactly, with all constants and lower order terms. 
        # Or you can compute the asymptotic complexity. Or you can just check whether it's a polynomial time algorithm or not. 
        
        exact_tex = Tex("$n^2 + n + 1$").next_to(empirical_img, RIGHT)
        asymptotic_tex = Tex("$O(n^2)$").next_to(exact_tex, RIGHT)
        poly_tex = Tex("polynomial?").next_to(asymptotic_tex, RIGHT)
        tick = clipart_yes_no_maybe("yes", 0.5).next_to(poly_tex, DOWN)

        self.play(
            Succession(
                FadeIn(empirical_img),
                FadeIn(exact_tex),
                FadeIn(asymptotic_tex),
                FadeIn(Group(poly_tex, tick)),
            )
        )
        self.wait()



        # You can see how these options get increasingly abstract and as they are getting more abstract, they are also getting easier to work with. In one extreme, analyzing an algorithm empirically is pretty hard and even impossible to do for nontrivial values of n, because there are too many inputs to check. On the other hand, understanding whether an algorithm runs in polynomial time is often really easy. 

        arrow1 = Arrow(
            start = empirical_img.get_center(),
            end = poly_tex.get_center(),
            buff = 0
        ).next_to(Group(empirical_img, poly_tex, tick), DOWN)
        # TODO pridat duhu

        self.play(
            Create(arrow1)
        )
        self.wait()

        self.play(
            Circumscribe(Group(empirical_img, Dot().move_to(empirical_img.get_bottom() + DOWN)), color = RED),
        )
        self.wait()
        
        self.play(
            Circumscribe(Group(exact_tex, Dot().move_to(exact_tex.get_bottom() + DOWN)), color = RED),
        )
        self.wait()

        self.play(
            Circumscribe(Group(poly_tex, Dot().move_to(poly_tex.get_bottom() + DOWN)), color = RED),
        )
        self.wait()



        # But as the concepts are getting more abstract, they get less informative. In competitive programming for example, it is quite typical that there is an easy quadratic solution to a problem and the hard part is getting it to O(n) or O(nlog(n)). So there we definitely need to distinguish between different polynomial-time algorithms. 

        arrow2 = Arrow(
            start = poly_tex.get_center(),
            end = empirical_img.get_center(),
            buff = 0
        ).next_to(Group(empirical_img, poly_tex, tick), UP)

        self.play(
            FadeIn(arrow2)
        )
        self.wait()

        comp1_tex = Tex("Easy: $O(n^2)$")
        comp2_tex = Tex("Hard: $O(n \log n)$")

        comp_group = Group(
            comp1_tex,
            comp2_tex,
        ).arrange(DOWN).move_to(2*LEFT + 2*DOWN)

        self.play(
            FadeIn(comp1_tex)
        )
        self.wait()
        self.play(
            FadeIn(comp2_tex)
        )
        self.wait()

        self.play(
            Circumscribe(Group(poly_tex, Dot().move_to(poly_tex.get_bottom() + DOWN)), color = RED),
        )
        self.wait()


        # The asymptotic complexity often lies in the sweet spot. It is usually both quite easy to compute, and also quite informative. This makes it the right level of abstraction for many situations, like in understanding data structures or in competitive programming. 
        
        rec = SurroundingRectangle(
            Group(asymptotic_tex, Dot().move_to(asymptotic_tex.get_bottom() + DOWN), Dot().move_to(asymptotic_tex.get_top() + UP)), 
            color = RED
        )

        self.play(
            Create(rec)
        )
        self.wait()

        self.play(
            Uncreate(rec),
            FadeOut(Group(comp1_tex, comp2_tex)),
        )
        self.wait()
        
        # Sure, we cannot apply it blindly: it doesn’t capture that some algorithms may have ridiculously large multiplicative constants in their complexity, which is the case for the universal search. 
        # But you know what, in other fields, like physics, we also work with frictionless surfaces that don’t actually exist. All models are wrong, it’s just that some of them happen to be useful. 

class Discussion2(Scene):
    def construct(self):
        default()
        self.add(vasek_head)

        # Going back to the universal search, knowing a bunch of weird examples is often extremely useful if you are a researcher in the area, because it helps you to build intuition and quickly disprove some hypotheses. 
        
        #TODO


        
        width = 6
        explanation_scale = 0.5


        weier_img = ImageMobject("img/weierstrass.png").scale_to_fit_width(width)
        weiertitle_tex = Tex("Weierstrass function").next_to(weier_img, DOWN)
        weierexplanation_tex = Tex("Continuous everywhere, yet differentiable nowhere. ").scale(explanation_scale).next_to(weiertitle_tex, DOWN)

        cantor_img = ImageMobject("img/cantor.png").scale_to_fit_width(width).align_to(weier_img, DOWN)
        cantortitle_tex = Tex("Cantor function").next_to(cantor_img, DOWN)
        cantorexplanation_tex = Tex("Zero derivative almost everywhere, yet goes continuously from 0 to 1. ").scale(explanation_scale).next_to(cantortitle_tex, DOWN)

        # TODO mozna hilbert misto osgood        
        # osgood_img = ImageMobject("img/osgood.png").scale_to_fit_width(width).align_to(weier_img, DOWN)
        # osgoodtitle_tex = Tex("Osgood curve").next_to(osgood_img, DOWN)
        # osgoodexplanation_tex = Tex("A non-self-intersecting curve with positive area. ").scale(explanation_scale).next_to(osgoodtitle_tex, DOWN)

        anims = [
            [AnimationGroup(
                FadeIn(img),
                FadeIn(title),
                FadeIn(explanation)
            ), AnimationGroup(
                FadeOut(img),
                FadeOut(title),
                FadeOut(explanation)
            )] for img, title, explanation in [[weier_img, weiertitle_tex, weierexplanation_tex], [cantor_img, cantortitle_tex, cantorexplanation_tex]]
        ]        

        self.play(
            anims[0][0],
        )
        self.wait()

        self.play(
            anims[0][1],
            anims[1][0],
        )
        self.wait()

        self.play(
            anims[1][1],
        )
        self.wait()

        from hilbertcurve.hilbertcurve import HilbertCurve

        def create_curve(iter):
            if(iter >= 10):
                return Square(color = RED, fill_opacity = 1, fill_color = RED).scale_to_fit_width(3)
                #TODO pak dropnout, aby se i plný čtverec nakreslil Hilbertovsky
            distances = list(range(4**iter))
            points = HilbertCurve(iter, 2).points_from_distances(distances)
            points = [[p[0], p[1], 0] for p in points]
            print(points)
            curve = Polygon(*points, color = RED).scale_to_fit_width(3 * (1 - 2**(-iter)))
            bounding_square = Square(color = GRAY).scale_to_fit_width(3).move_to(curve.get_center())
            return Group(bounding_square, curve)
        
        curves = Group(
            create_curve(1),
            create_curve(2),
            create_curve(3),
            Tex(r"$\dots$"),
            create_curve(10)
        ).arrange(RIGHT).to_corner(UL)
        curves[2:].next_to(curves[0], DOWN).align_to(curves[0], LEFT)

        hilberttitle_tex = Tex("Hilbert curve").next_to(curves[4], DOWN)
        hilbertexplanation_tex = Tex("A continuous curve with positive area. ").scale(explanation_scale).next_to(hilberttitle_tex, DOWN)
        
        self.play(
            Succession(
                FadeIn(curves[0]),
                FadeIn(curves[1]),
                FadeIn(curves[2]),
                FadeIn(curves[3]),
                FadeIn(curves[4]),
                FadeIn(hilberttitle_tex),
                FadeIn(hilbertexplanation_tex),
            )
        )
        self.wait()


        # 
        # So if you ever took calculus, you may know this creature, and that one, or even that one. 
        # [
        # https://en.wikipedia.org/wiki/Weierstrass_function Weierstrass’ function: continuous everywhere & differentiable nowhere
        # https://en.wikipedia.org/wiki/Cantor_function Cantor’s stairway to hell: Continuous everywhere and zero derivative almost everywhere & still goes from 0 to 1
        # https://en.wikipedia.org/wiki/Conway_base_13_function Conway’s base 13 function
        # ]

        # All of them are really weird and yet useful to have in the back of your mind. The same goes for the universal search - I explain one situation where it makes a useful counterexample in the video description. 

class Discussion3(Scene):
    def construct(self):
        default()
        self.add(vasek_head)

        # A very different way to understand the universal search is via historical lens. The 1960’s and 70’s were really interesting times, it was back then when researchers were trying to discover the right approach to develop a theory behind algorithms. 
        
        cards_data = [
            [61, "early 1960's", "Edmonds", "polynomial time"],
            [65, "1965", "Hartmanis-Stearns", "Time hierarchy theorem"],
            [67, "1967", "Blum", "Blum's speedup theorem"],
            [71, "1971", "Cook, independently Levin", "Satisfiability is NP complete"],
            [72, "1972", "Karp", "21 NP complete problems"],
            [73, "1973", "Levin", "Universal search"],
        ]

        timeline = Arrow(
            start = 6*LEFT,
            end = 6*RIGHT,
            color = GREY,
        ).shift(3*UP)

        self.play(
            FadeIn(timeline)
        )

        def create_card(card_data):
            
            card = Group(
                Line(start = 0.2*UP, end = 0.2*DOWN, buff = 0, color = GREY),
                Tex(card_data[1]),
                Tex(card_data[2]).scale(0.5),
                Tex(card_data[3]).scale(0.5),
            ).arrange(DOWN)
            card[0].shift(0.5*UP)

            card.shift(
                0.9 * (card_data[0] - 68) * RIGHT + timeline.get_center()[1]*UP
                - card[0].get_center()
            )

            return card
        
        card_objs = [create_card(card_data) for card_data in cards_data]
            
        self.play(
            Succession(
                *[FadeIn(card) for card in card_objs]
            )
        )
        self.wait()

        # If you look at the theorems that people proved around that time, some of them are now considered to be absolutely important foundational results, like the Cook-Levin theorem that kickstarted the whole P vs NP question and was discovered independently by Steve Cook and our good friend Leonid Levin. 

        self.play(
            Circumscribe(card_objs[3][1:], color = RED)
        )
        self.wait()

        img_width = 2.5
        cook_img = ImageMobject("img/cook.jpg").scale_to_fit_width(img_width)
        cook_tex = Tex("Steve Cook").next_to(cook_img)
        levin_img = ImageMobject("img/levin.jpg").scale_to_fit_width(img_width)
        levin_tex = Tex("Leonid Levin").next_to(levin_img)

        imgs = Group(cook_img, levin_img, cook_tex, levin_tex).arrange_in_grid(cols = 2).next_to(card_objs[3], DOWN)

        self.play(
            FadeIn(imgs[0], imgs[2])
        )
        self.play(
            FadeIn(imgs[1], imgs[3])
        )
        self.wait()

        self.play(
            FadeOut(imgs)
        )
        self.wait()

        # But there are other theorems from this time period that people were excited about around that time but now they look a bit obscure. 
        
        rec1 = SurroundingRectangle(card_objs[2][1:], color = RED)
        rec2 = SurroundingRectangle(card_objs[5][1:], color = RED)
        
        self.play(FadeIn(rec1), FadeIn(rec2))
        self.wait()
        
        self.play(FadeOut(rec1), FadeOut(rec2))
        self.wait()
        

        # Since nobody knew what the right approach was, people were asking these extremely fundamental questions like: does there even exist an asymptotically optimal algorithm for every problem, or can we have a sequence of faster and faster algorithms, but no fastest one? The universal search says that often the answer is yes, but then again the so-called Blum’s speedup theorem says that not always. 

        question1_tex = Tex("Does every problem has asymptotically optimal algorithm? ").next_to(card_objs[0], DOWN).to_edge(LEFT)
        question2_tex = Tex(r"Or can we have e.g. a problem solved by algorithms with complexities $O\left( 2^{n} \right), O\left( 2^{0.1n} \right), O\left( 2^{0.01n} \right), \dots$").next_to(question1_tex, DOWN).to_edge(LEFT)
        question3_tex = Tex(r"but with no fastest algorithm? ").next_to(question2_tex, DOWN).to_edge(LEFT)
       
        self.play(
            FadeIn(question1_tex),
        )
        self.wait()
        self.play(
            FadeIn(question2_tex),
            FadeIn(question3_tex),
        )
        self.wait()

        recc1 = SurroundingRectangle(question1_tex, color = RED)
        recc2 = SurroundingRectangle(Group(question2_tex, question3_tex), color = RED)
        rec1, rec2 = rec2, rec1

        self.play(
            FadeIn(rec1), FadeIn(recc1)
        )
        self.wait()
        
        self.play(
            FadeOut(rec1), FadeOut(recc1),
            FadeIn(rec2), FadeIn(recc2)
        )
        self.wait()
        
        self.play(
            FadeOut(rec2), FadeOut(recc2),
        )
        self.wait()

        self.play(
            FadeOut(Group(question1_tex, question2_tex, question3_tex)),
        )
        self.wait()

        # As remarked by Manuel Blum himself, these results turned out to be a bit too abstract and perhaps not that useful. That is in contrast with the P vs NP approach which really gives you a handle on the kinds of problems people are interested in. 

        blum_img = ImageMobject("img/blum.jpg").scale_to_fit_width(img_width)
        blum_name = Tex("Manuel Blum").next_to(blum_img, DOWN)
        blum_stuff = Group(blum_img, blum_name).to_corner(DL)
        blum_quote_tex = Text("[These results were] very abstract and not very useful … It didn’t do what Steve Cook’s P vs NP does, [that gives you] a real handle on the kinds of problems people are really interested in computing. ").scale(0.5).next_to(blum_img, RIGHT)

        self.play(FadeIn(blum_stuff))
        self.play(AddTextLetterByLetter(blum_quote_tex), run_time = 10)
        self.wait()

        # [Manuel Blum: “[These results were] very abstract and not very useful. … It didn’t do what Steve Cook’s P vs NP does, [It’s P vs NP that gives you] a real handle on the kinds of problems people are really interested in computing. “ zjevit citát postupně] 

        # So I think that the universal search is a good example of the sad truth that even though we think of mathematical theorems as being timeless, because if they are correct, they stay correct in the future, they may simply come out of fashion and become forgotten for all kinds of reasons. If you happen to know some other examples of this phenomenon, share them with us in the comments section!

        # In any case, I hope you enjoyed this video about universal search - an explicit asymptotically optimal algorithm for many problems. The content of this video was extremely subtle, so let us know if you are confused about something and whether you appreciate this theoretical content more or less than our usual explainers. See you next time!

        self.play(
            *[FadeOut(o) for o in self.mobjects]
        )

        uni_tex = Tex(r"{{Universal search \\}}{{an explicit asymptotically optimal algorithm for many problems}}")
        #Group(uni_tex[0], uni_tex[1]).arrange(DOWN).to_edge(DOWN)
        uni_tex[0].scale(2).shift(0.4*UP)
        uni_tex[1].scale(0.9)
        uni_tex.to_edge(UP).shift(1*DOWN)   

        self.play(
            Succession(
            Create(uni_tex),
            #Create(uni_tex[1])            
            )
        )
        self.wait(5)

        # TODO zopakovat pěknout trojúhelníkovou animaci?