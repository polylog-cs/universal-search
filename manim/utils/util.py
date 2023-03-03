from manim import *

def multiplication_animation(num1, num2, obj1, obj2):
    #TODO dá se získat text v obj1?
    # create objects

    nums_intermediate = []
    tmp = num2
    while(tmp > 0):
        digit = tmp % 10
        tmp //= 10
        nums_intermediate.append(digit * num1)
    num = num1*num2


    num1_tex, num2_tex, num_tex = [Tex(str(n)) for n in [num1, num2, num]]
    nums_intermediate_tex = [Tex(str(n)) for n in nums_intermediate]
    num2_tex = Tex(r"$\times$" + str(num2))

    line1 = Line(start = num2_tex.get_left(), end = num2_tex.get_right(), color = GRAY)
    line2 = line1.copy() 
    
    objects = Group(
        num1_tex,
        num2_tex,
        line1,
        *nums_intermediate_tex,
        line2,
        num_tex,
    ).arrange_in_grid(cols = 1, cell_alignment = RIGHT)

    for i in range(1, len(nums_intermediate_tex)):
        nums_intermediate_tex[i].align_to(nums_intermediate_tex[i-1][0][-2], RIGHT)

    # print(line2.get_center())

    objects.remove(line2)
    objects.add(Line(
        start = nums_intermediate_tex[-1].get_left()[0]*RIGHT
            + line2.get_center()[1]*UP, 
        end = nums_intermediate_tex[0].get_right()[0]*RIGHT
            + line2.get_center()[1]*UP,
        color = GRAY))
    
    # print(line2.get_center())




    # animations

    anims1 = Succession(
        ReplacementTransform(obj1, num1_tex),
        ReplacementTransform(obj2, num2_tex),
        FadeIn(objects),
    )

    anims2 = AnimationGroup(
        FadeOut(objects),
    )

    return objects, [anims1, anims2]



def division_animation(num, obj):
    num_tex = Tex(num).scale(2).to_edge(LEFT)
    div_sign = Tex(r"/").scale(2).next_to(num_tex, RIGHT)
    eq_sign = Tex(r"=").scale(2).next_to(num_tex, RIGHT).shift(4*RIGHT)

    objects = Group(
        num_tex
    )

    # animations
    anims1 = Succession(
        ReplacementTransform(obj, num_tex),
        FadeIn(Group(div_sign, eq_sign)),
    )

    anims2 = AnimationGroup(
        FadeOut(num_tex)
    )

    return objects, [anims1, anims2]

def horrible_multiplication():
    n = 2140324650240744961264423072839333563008614715144755017797754920881418023447140136643345519095804679610992851872470914587687396261921557363047454770520805119056493106687691590019759405693457452230589325976697471681738069364894699871578494975937497937
    a = 64135289477071580278790190170577389084825014742943447208116859632024532344630238623598752668347708737661925585694639798853367
    b = 33372027594978156556226010605355114227940760344767554666784520987023841729210037080257448673296881877565718986258036932062711
    return (n, a, b)
