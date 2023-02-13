import itertools

from manim.constants import DEGREES, PI
from manim.utils.color import *

from manim.mobject.types.vectorized_mobject import VGroup
from manim import override_animate
import numpy as np
from utils.cubie import Cubie
from utils.cube_utils import parse_move

DEFAULT_CUBE_COLORS = ["#ffffff", "#b71234", "#009b48", "#ffd500", "#ff5800", "#0046ad"]





class RubiksCube(VGroup):
    # Each coordinate starts at 0 and goes to (Dimensions - 1)

    # Colors are in the order Up, Right, Front, Down, Left, Back
    def __init__(self, dim=3, colors=None, cubie_size=1.0, rotate_nicely=True):
        if not (dim >= 2):
            raise Exception("Dimension must be >= 2")

        super(RubiksCube, self).__init__()

        if colors is None:
            colors = DEFAULT_CUBE_COLORS

        self.dimensions = dim
        self.colors = colors
        self.cubie_size = cubie_size
        self.cubies = np.ndarray((dim, dim, dim), dtype=Cubie)
        self.generate_cubies()

        # Center around the origin
        self.shift(-self.cubie_size * (self.dim - 1) / 2)

        # Rotate so that under the default camera, F is really the front etc.
        self.rotate(axis=np.array([0, 0, 1]), angle=PI / 2)
        self.rotate(axis=np.array([1, 0, 0]), angle=-PI / 2)

        if rotate_nicely:
            self.rotate(-20 * DEGREES, axis=np.array([0, 1, 0]))
            self.rotate(20 * DEGREES, axis=np.array([1, 0, 0]))
            

    def generate_cubies(self):
        for x in range(self.dimensions):
            for y in range(self.dimensions):
                for z in range(self.dimensions):
                    cubie = Cubie(
                        x, y, z, self.dimensions, self.colors, self.cubie_size
                    )
                    cubie.shift(np.array((x, y, z), dtype=float) * self.cubie_size)
                    self.add(cubie)
                    self.cubies[x, y, z] = cubie

    def set_state(self, positions):
        colors = {
            "U": self.colors[0],
            "R": self.colors[1],
            "F": self.colors[2],
            "D": self.colors[3],
            "L": self.colors[4],
            "B": self.colors[5],
        }
        positions = list(positions)
        # TODO: Try/except in case a color was not given
        # try:
        for cubie in np.rot90(self.get_face("U", False), 2).flatten():
            cubie.get_face("U").set_fill(colors[positions.pop(0)], 1)

        for cubie in np.rot90(np.flip(self.get_face("R", False), (0, 1)), -1).flatten():
            cubie.get_face("R").set_fill(colors[positions.pop(0)], 1)

        for cubie in np.rot90(np.flip(self.get_face("F", False), 0)).flatten():
            cubie.get_face("F").set_fill(colors[positions.pop(0)], 1)

        for cubie in np.rot90(np.flip(self.get_face("D", False), 0), 2).flatten():
            cubie.get_face("D").set_fill(colors[positions.pop(0)], 1)

        for cubie in np.rot90(np.flip(self.get_face("L", False), 0)).flatten():
            cubie.get_face("L").set_fill(colors[positions.pop(0)], 1)

        for cubie in np.rot90(np.flip(self.get_face("B", False), (0, 1)), -1).flatten():
            cubie.get_face("B").set_fill(colors[positions.pop(0)], 1)
        # except:
        #     return

    def solve_by_kociemba(self, state):
        return sv.solve(state).replace("3", "'").replace("1", "").split()

    def get_face_slice(self, face):
        """
        Return a NumPy slice object specifying which part of the array corresponds
        to which face. NumPy sli indexing a ndarray,
        e.g. a[:, 2] == a[np.s_[:, 2]]
        """
        face_slices = {
            "F": np.s_[0, :, :],
            "B": np.s_[self.dimensions - 1, :, :],
            "U": np.s_[:, :, self.dimensions - 1],
            "D": np.s_[:, :, 0],
            "L": np.s_[:, self.dimensions - 1, :],
            "R": np.s_[:, 0, :],
        }

        if face in face_slices:
            return face_slices[face]
        else:
            raise ValueError("Invalid face identifier " + face)

    def get_face(self, face, flatten=True):
        face = self.cubies[self.get_face_slice(face)]

        if flatten:
            return face.flatten()
        else:
            return face

    def do_move(self, move):
        face, n_turns = parse_move(move)

        # Actually do the spatial rotation
        axis = self.get_face(face, flatten=False)[1, 1].get_center() - self.get_center()

        VGroup(*self.get_face(face)).rotate(
            -(PI / 2) * n_turns,
            axis,
        )

        self.update_indices_after_move(move)

        # For chaining
        return self

    def update_indices_after_move(self, move):
        face, n_turns = parse_move(move)

        # We need to make sure that moves that are supposed to be clockwise really are
        n_turns_indices = n_turns if (face in {"L", "F", "D"}) else -n_turns

        # Get to a non-negative value
        n_turns_indices = (n_turns_indices + 4) % 4

        face_slice = self.get_face_slice(face)
        face_cubies = self.cubies[face_slice]

        # Change the indices of the cubies to what we expect after the move
        face_cubies = np.rot90(face_cubies, k=n_turns_indices)

        self.cubies[face_slice] = face_cubies

    @override_animate(do_move)
    def _do_move_animation(self, move, anim_args=None):
        if anim_args is None:
            anim_args = {}
        anim = CubeMove(self, move, **anim_args)
        return anim

    def hash(self) -> int:
        """
        Returns a deterministic int representation of the cube's configuration (state).
        """
        h = 0
        for i, j, k in itertools.product(range(3), range(3), range(3)):
            h = hash((self.cubies[i][j][k].hash_id, h))
        
        return h
    
    def set_stroke_width(self, stroke_width: float):
        for cubie in self.cubies.reshape(-1):
            for face in cubie.submobjects:
                face.stroke_width = stroke_width
        
        return self


import numpy as np
from manim.animation.animation import Animation
from manim.constants import PI
from manim.mobject.types.vectorized_mobject import VGroup

from utils.cube import RubiksCube


class CubeMove(Animation):
    def __init__(self, mobject: RubiksCube, move, target_position=None, **kwargs):
        # This only makes sense when called on a RubiksCube
        assert isinstance(mobject, RubiksCube)

        self.target_position = target_position if target_position is not None else mobject.get_center()
        face, n_turns = parse_move(move)

        # Compute the axis of rotation by taking the vector from the cube's center
        # to the middle cubie of the rotated face
        # TODO: this might accumulate numerical errors, but it seems ok for tens of moves
        self.axis = (
            mobject.get_face(face, flatten=False)[1, 1].get_center()
            - mobject.get_center()
        )

        self.move = move        
        self.face = face
        self.n_turns = n_turns

        super().__init__(mobject, **kwargs)

    def create_starting_mobject(self):
        starting_mobject = self.mobject.copy()
        return starting_mobject

    def interpolate_mobject(self, alpha):
        self.mobject.become(self.starting_mobject)

        self.mobject.move_to(
            self.rate_func(alpha) * self.target_position
            + (1 - self.rate_func(alpha)) * self.starting_mobject.get_center()
        )

        VGroup(*self.mobject.get_face(self.face)).rotate(
            -self.rate_func(alpha) * (PI / 2) * self.n_turns,
            self.axis,
        )

    def finish(self):
        super().finish()
        self.mobject.update_indices_after_move(self.move)
