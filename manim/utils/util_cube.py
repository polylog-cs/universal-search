import glob
import random

from manim import *
from utils.cube import *

class RubikScene(ThreeDScene):
    def __init__(self, *args, **kwargs):
        super(RubikScene, self).__init__(*args, **kwargs)
        self.camera.set_focal_distance(20000.0)
        self.camera.should_apply_shading = False
        self.bfs_counter = 0
        self.cube_sounds = []

    def play_bfs_sound(self, time_offset=0, animation_run_time=None):
        if animation_run_time is not None:
            assert (
                time_offset == 0
            ), "Nelze nastavit jak time_offset tak animation_length"
            time_offset = max(
                0, min(animation_run_time - 0.2, animation_run_time * 0.5)
            )

        self.add_sound(f"audio/bfs/bfs_{self.bfs_counter:03d}", time_offset=time_offset)
        self.bfs_counter += 1
    
    def play_cube_sound(self, time_offset=0, animation_run_time=None):
        if animation_run_time is not None:
            assert (
                time_offset == 0
            ), "Nelze nastavit jak time_offset tak animation_length"
            time_offset = max(
                0, min(animation_run_time - 0.2, animation_run_time * 0.5)
            )

        if not self.cube_sounds:
            self.cube_sounds = glob.glob("audio/cube/r*.wav")
            random.shuffle(self.cube_sounds)

        self.add_sound(self.cube_sounds.pop(), time_offset=time_offset)


def bfs(adj, start):
    res_vertices = [[start]]
    res_edges = [[]]
    seen = set([start])

    while True:
        cur_vertices = []
        cur_edges = []

        for v1 in res_vertices[-1]:
            for v2 in adj[v1]:
                cur_edges.append((v1, v2))

                if v2 not in seen:
                    cur_vertices.append(v2)
                    seen.add(v2)

        if cur_vertices:
            res_vertices.append(cur_vertices)
            res_edges.append(cur_edges)
        else:
            res_edges.append(cur_edges)
            break

    return res_vertices, res_edges


# https://ruwix.com/blog/feliks-zemdegs-rubiks-world-record-2016-4-73/
# TODO check (with our program?) this is indeed the best solution

def scramble(cube, MOVES):
    for move in MOVES:
        cube.do_move(move)

def invert_move(move):
    face, n_turns = parse_move(move)
    # Note these are already inverted
    endings = {
        1: "'",
        2: "2",
        3: "",
    }
    return face + endings[(n_turns + 4) % 4]


scramble1 = [
    "U2",
    "F",
    "L2",
    "U2",
    "R2",
    "F",
]
#     "L2",
#     "F2",
#     "L'",
#     "D'",
# ]
unscramble1 = [invert_move(move) for move in scramble1[::-1]]

scramble2 = [
    "L'",
    "D'",
    "B2",
    "R",
    "D2",
    "R'",
    # "B'",
    # "U'",
    # "L'",
    # "B'",
]
unscramble2 = [invert_move(move) for move in scramble2[::-1]]



FELIKS_ACTUAL_SOLUTION_MOVES_RAW = [
    "U'",
    "R",
    "F",
    "R'",
    "U'",
    "D",
    "L'",
    "U2",
    "L2",
    "U'",
    "L'",
    "U",
    "R'",
    "U",
    "R",
    "R'",
    "U",
    "R",
    "U",
    "R'",
    "U'",
    "R",
    "F",
    "R",
    "U'",
    "R'",
    "U'",
    "R",
    "U",
    "R'",
    "F'",
    "R",
    "U'",
    "R",
    "U",
    "R",
    "U",
    "R",
    "U'",
    "R'",
    "U'",
    "R2",
    "U",
]


def apply_feliks_turn(move):
    # Apply the INVERSE of x' y'. These are rotations of the whole cube,
    # so they essentially transform the moves performed
    replacements = {
        "U": "B",
        "D": "F",
        "L": "D",
        "R": "U",
        "F": "L",
        "B": "R",
    }
    return replacements[move[0]] + move[1:]


FELIKS_ACTUAL_SOLUTION_MOVES = [
    apply_feliks_turn(move) for move in FELIKS_ACTUAL_SOLUTION_MOVES_RAW
]

POSSIBLE_MOVES = [
    "U",
    "U'",
    "U2",
    "D",
    "D'",
    "D2",
    "L",
    "L'",
    "L2",
    "R",
    "R'",
    "R2",
    "F",
    "F'",
    "F2",
    "B",
    "B'",
    "B2",
]
POSSIBLE_MOVES = [
    "U",
    "D",
    "L",
    "R",
    "F",
    "B",
    "U2",
    "D2",
    "L2",
    "R2",
    "F2",
    "B2",
    "U'",
    "D'",
    "L'",
    "R'",
    "F'",
    "B'",
]




class BFSCircleAnimations:
    def __init__(
        self,
        center,
        iterations,
        label_angle=0.25 * PI,
        base_radius=0.9,
        radius_step=0.4,
    ):
        self.center = center
        self.iterations = iterations
        self.base_radius = base_radius
        self.radius_step = radius_step

        self.circle = Circle(color=RED, radius=base_radius).move_to(center)
        self.label = MathTex(r"1", color=RED)
        self.label.add_updater(
            lambda x: x.move_to(
                Point()
                .move_to(self.circle.get_right() + RIGHT * 0.4)
                .rotate(angle=label_angle, about_point=self.circle.get_center()),
            )
        )

        self.step = -1
        self.circles = [self.circle]

    def __next__(self):
        self.step += 1

        if self.step == 0:
            return (GrowFromCenter(self.circle), FadeIn(self.label))
        elif self.step < self.iterations:
            c2 = self.circle.copy()
            self.circles.append(c2)

            # This is needed so that the label follows properly during the animation
            # (we can't be moving `c2`, it has to be `circle`)
            self.circle, c2 = c2, self.circle

            label2 = MathTex(str(self.step + 1), color=RED)

            c3 = Circle(
                color=RED, radius=self.base_radius + self.step * self.radius_step
            ).move_to(self.center)

            return (
                self.circle.animate.become(c3),
                c2.animate.set_color(GRAY),
                self.label.animate.become(label2),
            )
        else:
            # tex.clear_updaters()
            raise StopIteration

    def __iter__(self):
        return self


def generate_path_animations(center, angle, base_radius, radius_step, n_steps):
    spread = 0.3

    def get_radius(i):
        return base_radius + i * radius_step

    points = [Dot(color=RED).shift(center)]
    animations = [[Create(points[0])]]

    for i in range(n_steps):
        if i < n_steps - 1:
            cur_spread = np.arcsin(spread / get_radius(i))
            cur_angle = np.random.uniform(angle - cur_spread, angle + cur_spread)
        else:
            # Keep the last one centered to match the other side
            cur_angle = angle

        point = (
            Dot(color=RED)
            .shift(RIGHT * get_radius(i))
            .rotate_about_origin(cur_angle)
            .shift(center)
        )
        points.append(point)
        animations.append([Create(point)])

    for i in range(1, n_steps + 1):
        animations[i].append(
            Create(Line(points[i - 1].get_center(), points[i].get_center(), color=RED))
        )

    return points, animations
