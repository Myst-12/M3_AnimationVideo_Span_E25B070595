"""
style.py — the "look" of the video, kept in one place.

Everything here is a small helper that returns a Manim object:
    text(...)      a piece of text in the video's font
    box(...)       a rounded card behind something
    vector(...)    an arrow on a coordinate plane
    label(...)     a vector's name, placed beside its arrow
    target(...)    a ring that shows "this is the point we want to reach"
"""
import numpy as np
from manim import *

# ---------------------------------------------------------------- colours --
BG = "#0E1422"         # background (dark navy)
CARD = "#161E31"       # fill colour of every box / card
EDGE = "#2C3A57"       # outline colour of every box / card
YELLOW = "#FFD166"     # highlights and key results
BLUE = "#4FC3F7"       # v1 is always blue
ORANGE = "#FFB74D"     # v2 is always orange
PINK = "#F06292"       # the redundant vector (v3 / u) is always pink
GREEN = "#81C784"      # the target b, and "correct ✓"
GREY = "#9AA7BD"       # small, less important text

FONT = "Avenir Next"

# Colour the vector names automatically wherever they appear in text.
VECTOR_COLOURS = {"v₁": BLUE, "v₂": ORANGE, "v₃": PINK}

# Drawing layers: a bigger number is drawn on top.
LAYER_BACKGROUND = -10
LAYER_GRID = 1
LAYER_DOTS = 2
LAYER_ARROWS = 4
LAYER_LABELS = 5
LAYER_BOXES = 10      # captions, titles, equation boxes – always on top


def text(words, size=30, color=WHITE, bold=False, colour_vectors=True):
    """Text in the video's font. v₁, v₂, v₃ are coloured automatically."""
    return Text(words, font=FONT, font_size=size, color=color,
                weight=BOLD if bold else NORMAL,
                t2c=VECTOR_COLOURS if colour_vectors else {})


def box(content, outline=EDGE, accent=None, padding=0.28):
    """A rounded card behind `content`. `accent` adds a coloured bar on the left."""
    bar_space = 0.2 if accent else 0
    card = RoundedRectangle(corner_radius=0.16,
                            width=content.width + 2 * padding + bar_space,
                            height=content.height + 2 * padding,
                            fill_color=CARD, fill_opacity=0.97,
                            stroke_color=outline, stroke_width=1.6)
    card.move_to(content).shift(LEFT * bar_space / 2)
    group = VGroup(card)
    if accent:
        bar = RoundedRectangle(corner_radius=0.035, width=0.07, height=card.height - 0.34,
                               fill_color=accent, fill_opacity=1, stroke_width=0)
        bar.move_to(card.get_left() + RIGHT * 0.2)
        group.add(bar)
    group.add(content)
    return group


def vector(plane, start, end, color, width=6):
    """An arrow on `plane` from point `start` to point `end` (plane coordinates)."""
    start = np.array(start, dtype=float)
    end = np.array(end, dtype=float)
    if np.linalg.norm(end - start) < 0.05:          # a zero-length arrow would crash
        end = start + np.array([0.05, 0])
    arrow = Arrow(plane.c2p(*start), plane.c2p(*end), buff=0, color=color,
                  stroke_width=width, max_tip_length_to_length_ratio=0.2,
                  max_stroke_width_to_length_ratio=8)
    return arrow.set_z_index(LAYER_ARROWS)


def label(arrow, name, color, side=1, size=30, distance=0.42):
    """Put `name` next to the arrow's tip, off to one side, so it never covers the arrow.
    side = +1 puts it on the left of the arrow's direction, -1 on the right."""
    direction = arrow.get_end() - arrow.get_start()
    direction = direction / np.linalg.norm(direction)
    sideways = np.array([-direction[1], direction[0], 0])     # direction turned 90°
    lab = text(name, size, color, bold=True, colour_vectors=False)
    lab.set_stroke(BG, width=10, background=True)              # dark outline = readable on grid
    lab.move_to(arrow.get_end() - 0.4 * direction + side * distance * sideways)
    return lab.set_z_index(LAYER_LABELS)


def target(point, color=YELLOW):
    """A ring with a dot in the middle — the arrow tip points right into it."""
    ring = Circle(radius=0.17, color=color, stroke_width=3).move_to(point)
    dot = Dot(point, radius=0.045, color=color)
    return VGroup(ring, dot).set_z_index(LAYER_DOTS)


def grid_plane(x_range, y_range, width, height, opacity=0.35):
    """The blue graph-paper background used for every 2-D picture."""
    return NumberPlane(
        x_range=x_range, y_range=y_range, x_length=width, y_length=height,
        background_line_style={"stroke_color": "#2B5E8C", "stroke_opacity": opacity,
                               "stroke_width": 1},
        axis_config={"stroke_color": "#8796AE", "stroke_width": 2},
    )


def line_inside(point, direction, xmin, xmax, ymin, ymax):
    """The straight line  point + t·direction,  cut down to the part inside a rectangle.
    Simple method: walk along the line in small steps and keep the points that are inside.
    Returns the first and last inside point, or None if the line misses the rectangle."""
    point = np.array(point, dtype=float)
    direction = np.array(direction, dtype=float)
    inside = []
    for t in np.linspace(-40, 40, 8001):
        x, y = point[:2] + t * direction[:2]
        if xmin <= x <= xmax and ymin <= y <= ymax:
            inside.append((x, y))
    if len(inside) < 2:
        return None
    return inside[0], inside[-1]


# ------------------------------------------------ tiny icons for the summary --
def small_arrow(start, end, color):
    return Arrow([*start, 0], [*end, 0], buff=0, color=color, stroke_width=4, tip_length=0.13,
                 max_tip_length_to_length_ratio=0.4, max_stroke_width_to_length_ratio=20)


def icon_span():
    """A short arrow lying on its (faded) line."""
    return VGroup(Line([-0.45, -0.38, 0], [0.55, 0.46, 0], color=BLUE, stroke_width=7, stroke_opacity=0.35),
                  small_arrow((0, 0), (0.33, 0.28), BLUE))


def icon_basis():
    """Two arrows and the slanted grid they make."""
    a, b = np.array([0.22, 0.42, 0]), np.array([0.5, 0.15, 0])
    lines = VGroup(*[Line(k * a, k * a + 2 * b, stroke_width=1, color=YELLOW, stroke_opacity=0.5) for k in range(3)],
                   *[Line(k * b, k * b + 2 * a, stroke_width=1, color=YELLOW, stroke_opacity=0.5) for k in range(3)])
    return VGroup(lines, small_arrow((0, 0), a[:2], BLUE), small_arrow((0, 0), b[:2], ORANGE))


def icon_dimension():
    """A line (1-D), a square (2-D) and a cube (3-D)."""
    line = Line(ORIGIN, [0.35, 0, 0], color=BLUE, stroke_width=4)
    square = Square(0.35, color=ORANGE, stroke_width=3, fill_opacity=0.2)
    front = Square(0.32, color=GREEN, stroke_width=3)
    back = front.copy().shift([0.13, 0.11, 0])
    cube = VGroup(back, front, *[Line(front.get_corner(c), back.get_corner(c), color=GREEN, stroke_width=3)
                                 for c in (UL, UR, DL, DR)])
    shapes = VGroup(line, square, cube).arrange(RIGHT, buff=0.22, aligned_edge=DOWN)
    numbers = VGroup(*[Text(n, font=FONT, font_size=16, color=GREY).next_to(s, DOWN, buff=0.08)
                       for n, s in zip("123", shapes)])
    numbers.align_to(numbers[0], DOWN)
    return VGroup(shapes, numbers)
