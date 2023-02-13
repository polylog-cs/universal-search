import copy
import itertools
import random
import math
from manim import *
from utils.util import *
from queue import PriorityQueue
import matplotlib.colors as mcolors

PRAGUE = 0
ROME = 1
# TODO uzsi sipky
# https://docs.manim.community/en/stable/reference/manim.mobject.geometry.tips.ArrowTip.html
highlight_color = DARK_BROWN #"#b58900"
red_stroke_width = DEFAULT_STROKE_WIDTH  * 1.75



BASE03 = "#002b36"
BASE02 = "#073642"
BASE01 = "#586e75"

# content tones

BASE00 = "#657b83"
BASE0 = "#839496"
BASE1 = "#93a1a1"

# background tones (light theme)

BASE2 = "#eee8d5"
BASE3 = "#fdf6e3"

# accent tones

YELLOW = "#d0b700"
YELLOW2 = "#b58900" # The original Solarized yellow
ORANGE = "#c1670c"
ORANGE2 = "#cb4b16" # The original Solarized orange - too close to red
RED = "#dc322f"
MAGENTA = "#d33682"
VIOLET = "#6c71c4"
BLUE = "#268bd2"
CYAN = "#2aa198"
GREEN = "#859900"

# Alias
GRAY = BASE00
GREY = BASE00



def color_from_potential(weight, pot_dif):
    weight = 0.5
    if pot_dif > 0:
        pot_dif_cropped = min(pot_dif, weight)
        return mcolors.to_hex(  
                (pot_dif_cropped / weight ) * np.array(mcolors.to_rgb(RED)) 
                + ( 1.0 - pot_dif_cropped / weight) * np.array(mcolors.to_rgb(GRAY)) 
            )
    else:
        pot_dif_cropped = min(-pot_dif, weight)
        return mcolors.to_hex( ( pot_dif_cropped / weight)  * np.array(mcolors.to_rgb(GREEN)) + ( 1.0 - pot_dif_cropped / weight) * np.array(mcolors.to_rgb(GRAY)) )

def edge_potential_updater(mob, edge, graph):
    u = edge[0]
    v = edge[1]
    mob.set_value(
        graph.edge_weights_vals[edge].get_value()
        + graph.vertex_potentials[edge[1]].get_value()
        - graph.vertex_potentials[edge[0]].get_value()
    )
    weight = graph.edge_weights_vals[edge].get_value()
    pot_dif = graph.vertex_potentials[v].get_value() - graph.vertex_potentials[u].get_value()
    mob.set_color(color_from_potential(weight, pot_dif))


class CustomGraph(Graph):
    edge_weights_vals = {} # edge -> ValueTracker
    edge_weights_objs = {} # edge -> Decimal
    vertex_names = {} # vertex -> Tex
    vertex_potentials = {} # vertex -> ValueTracker
    vertex_height_lines = {} # vertex -> Line
    directed = True
    
    def make_directed(self, directed):
        self.directed = directed

    def get_adjacency_list(self):
        adj = dict([(v, []) for v in self.vertices])
        for v1, v2 in self.edges:
            adj[v1].append(v2)
            if not self.directed:
                adj[v2].append(v1)

        return adj

    def neighbors(self, vertex):
        return self.get_adjacency_list()[vertex]


    def create_name(self, vertex, name, offset, scale = 0.5):
        self.vertex_names[vertex] = Tex(name, color=GRAY, font_size = DEFAULT_FONT_SIZE).scale(scale).move_to(self.vertices[vertex].get_center()).shift(offset)
        self.vertex_names[vertex].add_updater(
            lambda mob, dt: mob.move_to(self.vertices[vertex].get_center()).shift(offset)
        )

    def show_names(self, vertices):
        # shows selected vertex names
        anims = []
        for v in vertices:
            anims.append(FadeIn(self.vertex_names[v]))
        return AnimationGroup(*anims)

    def hide_names(self, vertices):
        # hides selected vertex names
        anims = []
        for v in vertices:
            anims.append(FadeOut(self.vertex_names[v]))
        return AnimationGroup(*anims)


    def create_edge_length(self, edge, weight, offset = 0*RIGHT):
        number = DecimalNumber(
            weight, 
            num_decimal_places=1,
            color = GRAY
        ).scale(0.3)
        self.edge_weights_objs[edge] = number
        self.edge_weights_vals[edge] = ValueTracker(weight)
        number.move_to(self.edges[edge].get_center()).shift(offset)
        number.add_updater(
            lambda mob, dt: mob.move_to(self.edges[edge].get_center()).shift(offset)
        )

    def show_edge_lengths(self, edges):
        anims = []
        for e in edges:
            anims.append(
                FadeIn(self.edge_weights_objs[e])
            )
        return AnimationGroup(*anims)

    def hide_edge_lengths(self, edges):
        anims = []
        for e in edges:
            anims.append(FadeOut(self.edge_weights_objs[e]))
        return AnimationGroup(*anims)

    def change_edge_length(self, edge, change, new_color):
        return AnimationGroup(
            self.edges[edge].animate().set_color(new_color),
            self.edge_weights_objs[edge].animate().increment_value(change),
        )

    # for 2D scenes
    def disable_heights(self):
        for v in self.vertices:
            self.vertices[v].add_updater(
                lambda mob, dt, v=v: mob.move_to(
                    [
                        mob.get_center()[0],
                        mob.get_center()[1],
                        0
                    ]
                )
            )

    def disable_colors(self):
        for e in self.edges:
            self.edges[e].add_updater(
                lambda mob, dt: mob.set_color(GRAY)
            )


    def setup_potentials(self, potentials = {}, rate = 1):
        # updater: edge_length = original_edge_length + potential(v) - potential(u)
        # ideally (but maybe hard), add also updater on the color, so that when it decreases/increases it gets a shade of green/red based on how fast it increases/decreases
        for v in self.vertices:
            self.vertex_potentials[v] = ValueTracker(0)
            if v in potentials:
                self.vertex_potentials[v] = ValueTracker(potentials[v])

            self.vertices[v].add_updater(
                lambda mob, dt, v=v: mob.move_to(
                    [
                        mob.get_center()[0],
                        mob.get_center()[1],
                        self.vertex_potentials[v].get_value() * rate
                    ]
                )
            )
        for v in self.vertices:
            self.vertex_height_lines[v] = Line(#DashedLine(
                start = self.vertices[v].get_center(),
                end = np.array([self.vertices[v].get_center()[0], self.vertices[v].get_center()[1], 0]) + 0.001*DOWN,
                color = GRAY,
                stroke_width = 5
            ).add_updater(
                lambda mob, dt, v=v: mob.put_start_and_end_on(
                    self.vertices[v].get_center(),
                    np.array([self.vertices[v].get_center()[0], self.vertices[v].get_center()[1], 0]) + 0.001*DOWN
                )
            )

        for edge in self.edges:
            

            def edge_arrow_potential_updater(mob, edge):
                u = edge[0]
                v = edge[1]
                weight = self.edge_weights_vals[edge].get_value()
                pot_dif = self.vertex_potentials[v].get_value() - self.vertex_potentials[u].get_value()
                mob.set_color(color_from_potential(weight, pot_dif))


            self.edge_weights_objs[edge].add_updater(
                lambda mob, dt, edge = edge: edge_potential_updater(mob, edge, self)
            )
            self.edges[edge].add_updater(
                lambda mob, dt, edge = edge: edge_arrow_potential_updater(mob, edge)
            )

	

    def gen_zero_potentials(self):
        pots = {}
        for v in self.vertices:
            pots[v] = 0
        return pots

    def gen_air_potentials(self, source):
        pots = {}
        for v in self.vertices:
            pots[v] = np.linalg.norm(self.vertices[v].get_center() - self.vertices[source].get_center())
        return pots


    def set_new_potentials(self, potentials):
        for v, pot in potentials.items():
            self.vertex_potentials[v].set_value(pot)

    def anim_new_potentials(self, new_potentials):
        anims = []
        for v, pot in new_potentials.items():
            anims.append(self.vertex_potentials[v].animate.set_value(pot))
        return AnimationGroup(*anims)

    def add_directed_edge(self, u, v, offset = 0, weight = 1, offset_weight = 0):
        def compute_positions(u, v, offset):
            dir = (self.vertices[v].get_center() - self.vertices[u].get_center() ) / np.linalg.norm(self.vertices[v].get_center() - self.vertices[u].get_center())
            start = self.vertices[u].get_center() + offset
            end = self.vertices[v].get_center() + offset
            u_radius = self.vertices[u].width/2.0
            v_radius = self.vertices[v].width/2.0
            if np.linalg.norm(offset) < u_radius:
                start += dir * np.sqrt(u_radius ** 2 - np.linalg.norm(offset) ** 2)
            if np.linalg.norm(offset) < v_radius:
                end -= dir * np.sqrt(v_radius ** 2 - np.linalg.norm(offset) ** 2)
                
            return (start, end)
            
        start_pos, end_pos = compute_positions(u, v, offset)

        edge = Arrow(
            start = start_pos,
            end = end_pos,
            buff = 0,
            stroke_width=1,
            tip_length = 0.13,
            color = GRAY,
        )

        self.edges[(u,v)] = edge

        def edge_updater(mob, u, v, offset):
            start_pos, end_pos = compute_positions(u, v, offset)
            mob.put_start_and_end_on(start_pos, end_pos)

        edge.add_updater(lambda mob, dt, u=u, v=v, offset=offset: edge_updater(mob, u, v, offset))
        edge.put_start_and_end_on(start_pos, end_pos)

        self.create_edge_length((u,v), weight, offset_weight)

        return AnimationGroup(Create(edge))

    def run_dijkstra(self, start_node, end_node, speed, thumbnail = False):
        # initialize potentials and weights to default values to be sure
        for edge in self.edges:
            if not edge in self.edge_weights_vals:
                self.edge_weights_vals[edge] = ValueTracker(1)


        for vert in self.vertices:
            if not vert in self.vertex_potentials:
                self.vertex_potentials[vert] = ValueTracker(0)

        # run A*
        all_anims = []

        G = self.get_adjacency_list()
        q = PriorityQueue()
        q.put((0, start_node, -1))
        
        distances = {}
        predecessors = {}

        mover_anims = []
        node_anims = []
        red_nodes = []
        while not q.empty():
            (dist, node, predecessor) = q.get()
            if not node in distances:
                distances[node] = dist
                predecessors[node] = predecessor

                node_anims.append((dist, node))
                

                for neighbor in G[node]:
                    if not neighbor in distances:
                        edge = (node, neighbor)
                        
                        new_dist = dist + self.edge_weights_vals[edge].get_value() + self.vertex_potentials[neighbor].get_value() - self.vertex_potentials[node].get_value()
                        q.put((new_dist, neighbor, node))

                        mover_anims.append(
                            (
                                self.vertices[node].get_center(), 
                                self.vertices[neighbor].get_center(), 
                                dist, 
                                dist + self.edge_weights_vals[edge].get_value() + self.vertex_potentials[neighbor].get_value() - self.vertex_potentials[node].get_value(),
                                node,
                                neighbor
                            )
                        )

        shortest_path_nodes = [end_node]
        shortest_path_edges = [[], []]

        node = end_node
        while node != start_node:
            pred = predecessors[node]
            shortest_path_nodes.append(pred)
            shortest_path_edges[0].append((pred, node))
            shortest_path_edges[1].append((node, pred))
            node = pred

        for anim in node_anims:
            (dist, node) = anim
            if dist <= distances[end_node]:
                red_nodes.append(node)
                all_anims.append(
                    Succession(
                        Wait(dist * speed),
                        self.vertices[node].animate.set_color(highlight_color)
                    )
                )

        all_lines = {}
        for anim in mover_anims:
            (start_pos, end_pos, start_time, end_time, node, neighbor) = anim
            #finish_time = min(finish_time, distances[end_node])
            if start_time >= distances[end_node]:
                continue
            if end_time >= distances[end_node]:
                ratio = (distances[end_node] - start_time) *1.0 / (end_time - start_time)
                end_time = start_time + ratio * (end_time - start_time)
                end_pos = ratio * end_pos + (1-ratio) * start_pos

            param = red_stroke_width if thumbnail == False else 2*DEFAULT_STROKE_WIDTH
            line = Line(
                    start = start_pos,
                    end = end_pos,
                    buff = 0,
                    color = highlight_color,
                    z_index = 1000,
                    stroke_width = param
                )
            all_anims.append(
                Succession(
                    Wait(start_time * speed),
                    AnimationGroup(
                        Create(line, rate_func = linear), 
                        run_time = ( end_time - start_time ) * speed,
                    )
                )
            )
            #print(node, neighbor, start_time, end_time)
            all_lines[(node, neighbor)] = line
        
        # all_anims.append(Flash(self.vertices[PRAGUE], color = RED))
        # all_anims.append(Succession(Wait(distances[ROME] * speed), Flash(self.vertices[ROME], color = RED)))
        

        return (
            AnimationGroup(*all_anims),
            all_lines,
            shortest_path_nodes,
            shortest_path_edges[0] + shortest_path_edges[1],
            distances,
            red_nodes
        )
        

