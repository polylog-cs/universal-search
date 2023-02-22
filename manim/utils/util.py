from manim import *

def multiplication_animation(num1, num2):
    
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
    line2 = Line(
        start = nums_intermediate_tex[-1].get_left(), 
        end = np.array([
            nums_intermediate_tex[-1].get_left()[0], 
            nums_intermediate_tex[0].get_right()[1],
            0]), 
        color = GRAY)
    
    objects = Group(
        num1_tex,
        num2_tex,
        line1,
        *nums_intermediate_tex,
        line2,
        num_tex,
    ).arrange(DOWN)

    # animations

    anims1 = AnimationGroup(
        FadeIn(objects),
    )

    anims2 = AnimationGroup(
        FadeOut(objects),
    )

    return objects, [anims1, anims2]

