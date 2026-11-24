"""
Span, Basis & Dimension — M3 Animation Video   (Kushal Mittal · E25B070595)

How to render (1920×1080, 30 fps):
    manim -r 1920,1080 --fps 30 span_basis_dimension.py SpanBasisDimension

How the file is organised
-------------------------
The whole video is ONE Manim scene. `construct()` calls six methods, one per
chapter of the storyboard. Each chapter starts at a fixed second; the helper
`self.until(t)` simply waits until the video clock reaches t, so the video
always lines up with the narration script.

Colours, text and arrow helpers live in style.py.
The maths is written as plain Unicode text (₁ ₂ ℝ ⇒ …), so LaTeX is not needed.
"""
import numpy as np
from manim import *

from style import *

STUDENT_NAME = "Kushal Mittal"
STUDENT_ID = "E25B070595"

config.background_color = BG

# ----------------------------------------------------------- the vectors --
V1 = np.array([1, 2])
V2 = np.array([3, 1])
V3 = np.array([4, 3])      # = V1 + V2   (the redundant one)
B = np.array([5, 5])       # = 2·V1 + 1·V2

# ------------------------------------------- chapters: start, end, title --
CHAPTERS = [
    (0, 35, "01", "Can Two Arrows Reach Everything?"),
    (35, 80, "02", "The Five Key Words"),
    (80, 155, "03", "Seeing It Happen"),
    (155, 235, "04", "Let's Solve One Together"),
    (235, 272, "05", "So What Does It Mean?"),
    (272, 300, "06", "The Big Picture"),
]


class SpanBasisDimension(ThreeDScene):     # ThreeDScene because chapter 3 has a 3-D part

    # ===================================================== small helpers ===
    def until(self, t):
        """Wait until the video clock reaches t seconds."""
        if t > self.renderer.time:
            self.wait(t - self.renderer.time)

    def clear_screen(self, run_time=0.8):
        """Fade out everything except the background and the progress bar."""
        to_remove = [m for m in self.mobjects if m not in self.always_on_screen]
        if to_remove:
            self.play(*[FadeOut(m) for m in to_remove], run_time=run_time)
        self.remove(*to_remove)

    def chapter_tag(self, number, title):
        """The small rounded tag in the top-left corner, e.g. '03  Seeing It Happen'."""
        words = VGroup(text(number, 21, YELLOW, bold=True), text(title, 21, colour_vectors=False))
        words.arrange(RIGHT, buff=0.22)
        pill = RoundedRectangle(corner_radius=0.24, width=words.width + 0.55, height=0.5,
                                fill_color=CARD, fill_opacity=0.97, stroke_color=EDGE, stroke_width=1.6)
        tag = VGroup(pill, words.move_to(pill)).to_corner(UL, buff=0.3)
        return tag.set_z_index(LAYER_BOXES)

    def chapter_intro(self, index):
        """Big chapter title in the middle of the screen, which then shrinks into the corner tag."""
        _, _, number, title = CHAPTERS[index]
        small = text(f"CHAPTER {number}", 26, YELLOW, bold=True)
        big = text(title, 58, bold=True, colour_vectors=False)
        if big.width > 11.5:
            big.scale_to_fit_width(11.5)
        VGroup(small, big).arrange(DOWN, buff=0.3)
        underline = Line(big.get_corner(DL), big.get_corner(DR), color=YELLOW, stroke_width=4).shift(DOWN * 0.3)

        self.play(FadeIn(small, shift=UP * 0.2), FadeIn(big, shift=UP * 0.3), run_time=0.6)
        self.play(Create(underline), run_time=0.45)
        self.wait(0.55)
        tag = self.chapter_tag(number, title)
        self.play(FadeOut(VGroup(small, big, underline), shift=UP * 0.4, scale=0.8),
                  FadeIn(tag, shift=DOWN * 0.15), run_time=0.7)
        return tag

    def caption(self, words, color=WHITE, accent=YELLOW):
        """A caption box along the bottom of the screen."""
        return box(text(words, 26, color), accent=accent, padding=0.22) \
            .to_edge(DOWN, buff=0.42).set_z_index(LAYER_BOXES)

    def switch_caption(self, new):
        """Swap the current bottom caption for a new one."""
        if self.current_caption is None:
            self.play(FadeIn(new, shift=UP * 0.15), run_time=0.6)
        else:
            self.play(FadeOut(self.current_caption, shift=DOWN * 0.15), FadeIn(new, shift=UP * 0.15), run_time=0.6)
        self.current_caption = new

    def draw_combination(self, plane, c1, a, color_a, c2, b, color_b, run_time=1.0):
        """Draw c1·a and then c2·b tip-to-tail, so the second arrow ends at c1·a + c2·b."""
        first = vector(plane, (0, 0), c1 * a, color_a, 5)
        second = vector(plane, c1 * a, c1 * a + c2 * b, color_b, 5)
        self.play(GrowArrow(first), run_time=run_time)
        self.play(GrowArrow(second), run_time=run_time)
        return VGroup(first, second)

    def make_progress_bar(self):
        """Thin bar along the bottom edge, one segment per chapter, that fills up as the video plays."""
        tracks, fills = VGroup(), VGroup()
        x = -6.95
        for start, end, _, _ in CHAPTERS:
            width = 13.55 * (end - start) / 300
            track = Rectangle(width=width, height=0.05, stroke_width=0, fill_color=WHITE, fill_opacity=0.13)
            track.move_to([x + width / 2, -3.87, 0])
            tracks.add(track)
            fills.add(Rectangle(width=0.001, height=0.05, stroke_width=0, fill_opacity=0))
            x += width + 0.07
        bar = VGroup(tracks, fills).set_z_index(LAYER_BOXES)
        self.video_time = 0

        def fill_up(bar, dt):             # runs once per frame; dt = time since last frame
            self.video_time += dt
            for (start, end, _, _), track, fill in zip(CHAPTERS, tracks, fills):
                fraction = np.clip((self.video_time - start) / (end - start), 0, 1)
                new_fill = Rectangle(width=max(track.width * fraction, 0.001), height=0.05, stroke_width=0,
                                     fill_color=YELLOW, fill_opacity=0.9 if fraction > 0 else 0)
                fill.become(new_fill.align_to(track, LEFT).set_y(track.get_y()).set_z_index(LAYER_BOXES))

        bar.add_updater(fill_up)
        return bar

    # ========================================================= the video ===
    def construct(self):
        # background darkening at the edges (a picture) + the progress bar stay for the whole video
        vignette = ImageMobject("assets/vignette.png").set_width(config.frame_width + 0.02)
        vignette.set_z_index(LAYER_BACKGROUND)
        progress = self.make_progress_bar()
        self.add_fixed_in_frame_mobjects(vignette, progress)   # so they don't move in the 3-D part
        self.add(vignette, progress)
        self.always_on_screen = [vignette, progress]
        self.current_caption = None

        self.title_screen()          # 0:00 – 0:08
        self.chapter1_hook()         # 0:08 – 0:35
        self.chapter2_key_words()    # 0:35 – 1:20
        self.chapter3_seeing_it()    # 1:20 – 2:35
        self.chapter4_example()      # 2:35 – 3:55
        self.chapter5_meaning()      # 3:55 – 4:32
        self.chapter6_summary()      # 4:32 – 5:00

    # ------------------------------------------------- 0:00 title screen ---
    def title_screen(self):
        tag = text("LINEAR ALGEBRA  ·  M3", 20, YELLOW, bold=True)
        tag = VGroup(RoundedRectangle(corner_radius=0.2, width=tag.width + 0.5, height=0.42,
                                      stroke_color=YELLOW, stroke_width=1.5), tag)
        title = text("Span, Basis\n& Dimension", 74, bold=True)
        subtitle = text("How a few arrows build an entire space", 30, GREY)
        name = text(f"{STUDENT_NAME}   ·   {STUDENT_ID}", 28, BLUE)
        left_side = VGroup(tag, title, subtitle, name).arrange(DOWN, aligned_edge=LEFT, buff=0.38)
        name.shift(DOWN * 0.25)
        left_side.to_edge(LEFT, buff=0.8).shift(UP * 0.1)

        # right side: a small picture of v1, v2 and the points they reach
        plane = grid_plane((-1, 5, 1), (-1, 5, 1), 4.8, 4.8, opacity=0.4).move_to(RIGHT * 3.75 + DOWN * 0.1)
        v1, v2 = vector(plane, (0, 0), V1, BLUE), vector(plane, (0, 0), V2, ORANGE)
        cell = Polygon(*[plane.c2p(*p) for p in ((0, 0), V1, V1 + V2, V2)], stroke_width=0,
                       fill_color=YELLOW, fill_opacity=0.15).set_z_index(LAYER_GRID)
        dots = VGroup()
        for i in range(-3, 4):
            for j in range(-3, 4):
                x, y = i * V1 + j * V2
                if -1 <= x <= 5 and -1 <= y <= 5:
                    dots.add(Dot(plane.c2p(x, y), radius=0.04, color=WHITE).set_z_index(LAYER_DOTS))

        self.play(FadeIn(tag, shift=DOWN * 0.2), Create(plane), run_time=0.8)
        self.play(Write(title), GrowArrow(v1), GrowArrow(v2), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.2), FadeIn(cell),
                  LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.05), run_time=1.2)
        self.play(FadeIn(name, shift=UP * 0.2), run_time=0.6)
        self.until(7.2)
        self.clear_screen()

    # ------------------------------------------------------ 1. the hook ---
    def chapter1_hook(self):
        self.until(8)
        self.chapter_intro(0)
        plane = grid_plane((-9, 9, 1), (-6, 6, 1), 14.4, 9.6).shift(DOWN * 0.6)
        self.play(Create(plane), run_time=1.2)

        v1 = vector(plane, (0, 0), V1, BLUE)
        v2 = vector(plane, (0, 0), V2, ORANGE)
        self.play(GrowArrow(v1), FadeIn(label(v1, "v₁", BLUE, side=1)), run_time=0.9)
        self.play(GrowArrow(v2), FadeIn(label(v2, "v₂", ORANGE, side=-1)), run_time=0.9)

        # the question sits top-right, on the same row as the chapter tag, so it never covers an arrow
        question = box(text("Stretch, flip, add v₁ and v₂ — can we reach ANY point?", 23),
                       accent=YELLOW, padding=0.18).to_corner(UR, buff=0.3).set_z_index(LAYER_BOXES)
        self.play(FadeIn(question, shift=DOWN * 0.2), run_time=0.7)
        self.until(19)

        # three example points, each reached by a different mix of v1 and v2
        examples = [((4, 3), 1, 1, "(4, 3)", "1·v₁ + 1·v₂", 23.5),
                    ((-1, -3), -1.6, 0.2, "(−1, −3)", "−1.6·v₁ + 0.2·v₂", 27.5),
                    ((-4, 2), 2, -2, "(−4, 2)", "2·v₁ − 2·v₂", 31)]
        for point, c1, c2, point_text, recipe, end_time in examples:
            ring = target(plane.c2p(*point))
            self.play(FadeIn(ring, scale=1.6), run_time=0.4)
            path = self.draw_combination(plane, c1, V1, BLUE, c2, V2, ORANGE, run_time=0.8)
            equation = VGroup(text(point_text, 36, YELLOW, bold=True), text("=", 36, bold=True),
                              text(recipe, 36, bold=True)).arrange(RIGHT, buff=0.25)
            # equation box on the right-hand side, below all the arrows
            eq_box = box(equation, outline=YELLOW, accent=YELLOW, padding=0.3)
            eq_box.to_edge(RIGHT, buff=0.35).set_y(-1.95).set_z_index(LAYER_BOXES)
            self.play(Flash(ring[1], color=YELLOW, flash_radius=0.3), FadeIn(eq_box, shift=UP * 0.2), run_time=0.7)
            self.until(end_time)
            self.play(FadeOut(path), FadeOut(eq_box), FadeOut(ring), run_time=0.4)

        v3 = vector(plane, (0, 0), V3, PINK)
        question2 = box(text("Now add a third vector v₃ … do we even need it?", 23),
                        accent=PINK, padding=0.18).to_corner(UR, buff=0.3).set_z_index(LAYER_BOXES)
        self.play(GrowArrow(v3), FadeIn(label(v3, "v₃ ?", PINK, side=-1)),
                  FadeOut(question), FadeIn(question2), run_time=1)
        self.until(34.2)
        self.clear_screen()

    # --------------------------------------------------- 2. key words -----
    def chapter2_key_words(self):
        self.until(35)
        self.chapter_intro(1)

        goal_badge = text("GOAL", 20, BG, bold=True)
        goal_badge = VGroup(RoundedRectangle(corner_radius=0.12, width=goal_badge.width + 0.3, height=0.38,
                                             fill_color=YELLOW, fill_opacity=1, stroke_width=0), goal_badge)
        goal_words = text("By the end you'll be able to explain span, basis and dimension —\n"
                          "both as pictures and as equations.", 25)
        goal = box(VGroup(goal_badge, goal_words).arrange(RIGHT, buff=0.35), outline=YELLOW, padding=0.24)
        goal.move_to(UP * 2.5)

        # one big table: the word on the left, its meaning on the right
        table = RoundedRectangle(corner_radius=0.2, width=13.4, height=5.3, fill_color=CARD, fill_opacity=0.97,
                                 stroke_color=EDGE, stroke_width=1.6).move_to(DOWN * 0.7)
        self.play(FadeIn(goal, shift=DOWN * 0.2), FadeIn(table), run_time=0.8)
        self.until(48)

        rows = [
            ("Linear combination", "c₁v₁ + c₂v₂ + c₃v₃ + …      (the c's are any real numbers)", 56),
            ("Span", "the set of ALL linear combinations\n= every point you can reach", 63),
            ("Linearly independent", "no vector is a combination of the others:\n"
                                     "c₁v₁ + c₂v₂ + … = 0  only when every c = 0", 70),
            ("Basis", "a linearly independent set that spans the whole space", 75),
            ("Dimension", "the number of vectors in a basis\n(line 1 · plane 2 · space 3)", 79.2),
        ]
        y = table.get_top()[1] - 0.4
        for i, (word, meaning, end_time) in enumerate(rows):
            word_text = text(word, 27, BLUE, bold=True)
            meaning_text = text(meaning, 24)
            if meaning_text.width > 8.4:
                meaning_text.scale_to_fit_width(8.4)
            height = max(word_text.height, meaning_text.height)
            word_text.move_to([-6.25, y - height / 2, 0], aligned_edge=LEFT)
            meaning_text.move_to([-2.0, y - height / 2, 0], aligned_edge=LEFT)
            row = VGroup(word_text, meaning_text)
            if i < len(rows) - 1:          # thin divider line under every row except the last
                divider = Line([-6.4, y - height - 0.22, 0], [6.4, y - height - 0.22, 0],
                               color=EDGE, stroke_width=1.5)
                row.add(divider)
            self.play(FadeIn(row, shift=RIGHT * 0.2), run_time=0.7)
            self.until(end_time)
            y -= height + 0.44
        self.clear_screen()

    # -------------------------------------------------- 3. seeing it ------
    def chapter3_seeing_it(self):
        self.until(80)
        self.chapter_intro(2)
        plane = grid_plane((-9, 9, 1), (-5.5, 5.5, 1), 14.4, 8.8).shift(UP * 0.5)
        self.play(Create(plane), run_time=1.0)
        # Everything is drawn inside this rectangle, so nothing runs under the caption or the corner tag.
        XMIN, XMAX, YMIN, YMAX = -6.9, 6.9, -2.5, 3.2

        # ---- (a) ONE vector: all its multiples c·v1 make a line ----
        c = ValueTracker(1.0)
        moving = always_redraw(lambda: vector(plane, (0, 0), c.get_value() * V1, BLUE))
        moving_label = always_redraw(lambda: label(moving, f"{c.get_value():+.1f} · v₁", BLUE,
                                                   size=26, distance=0.75))
        self.add(moving, moving_label)
        span_line = Line(plane.c2p(*(-1.7 * V1)), plane.c2p(*(2.0 * V1)), color=BLUE,
                         stroke_width=10, stroke_opacity=0.4).set_z_index(LAYER_GRID)
        self.switch_caption(self.caption("One vector:   Span{v₁} = a line through the origin   →   dimension 1"))
        self.play(c.animate.set_value(2.0), run_time=1.4)
        self.play(c.animate.set_value(-1.7), Create(span_line), run_time=3.2)
        self.play(c.animate.set_value(1.0), run_time=1.3)
        self.until(96)

        # ---- (b) TWO vectors: mixing them reaches every point of the plane ----
        self.remove(moving, moving_label)
        v1 = vector(plane, (0, 0), V1, BLUE)
        v1_label = label(v1, "v₁", BLUE, side=1)
        v2 = vector(plane, (0, 0), V2, ORANGE)
        v2_label = label(v2, "v₂", ORANGE, side=-1)
        self.add(v1, v1_label)
        self.play(GrowArrow(v2), FadeIn(v2_label), run_time=0.8)
        self.switch_caption(self.caption("Two vectors:   mix them as  c₁v₁ + c₂v₂  and the tip can go anywhere"))

        # A point that wanders around: at every moment it is  c1·v1 + c2·v2  for some numbers c1, c2.
        s = ValueTracker(0)
        c1 = lambda: 1.0 * np.sin(s.get_value())
        c2 = lambda: 1.2 * np.sin(1.6 * s.get_value() + 0.6)
        part1 = always_redraw(lambda: vector(plane, (0, 0), c1() * V1, BLUE, 5))
        part2 = always_redraw(lambda: vector(plane, c1() * V1, c1() * V1 + c2() * V2, ORANGE, 5))
        tip = always_redraw(lambda: Dot(plane.c2p(*(c1() * V1 + c2() * V2)), radius=0.08, color=YELLOW)
                            .set_z_index(LAYER_LABELS))
        trail = TracedPath(tip.get_center, stroke_color=YELLOW, stroke_width=3, dissipating_time=2.0)
        readout = always_redraw(lambda: box(text(f"{c1():+.1f}·v₁  {c2():+.1f}·v₂", 26, bold=True), padding=0.18)
                                .to_corner(UR, buff=0.3).set_z_index(LAYER_BOXES))
        self.add(trail, part1, part2, tip, readout)
        self.play(s.animate.set_value(2.5 * PI), run_time=6, rate_func=linear)
        self.play(FadeOut(VGroup(part1, part2, tip, trail, readout)), run_time=0.4)
        self.remove(part1, part2, tip, trail, readout)

        # The slanted grid: lines along v1 (through every k·v2) and along v2 (through every k·v1).
        # They grow outwards from the origin until they tile the whole screen.
        rings = []
        for k in range(0, 8):
            ring = VGroup()
            for sign in ([1] if k == 0 else [1, -1]):
                for start, direction in ((sign * k * V2, V1), (sign * k * V1, V2)):
                    p = plane.c2p(*start)
                    d = plane.c2p(*direction) - plane.c2p(0, 0)
                    ends = line_inside(p, d, XMIN, XMAX, YMIN, YMAX)
                    if ends:
                        ring.add(Line([*ends[0], 0], [*ends[1], 0], color=YELLOW, stroke_width=2,
                                      stroke_opacity=0.45).set_z_index(LAYER_GRID))
            rings.append(ring)
        self.play(LaggedStart(*[Create(r) for r in rings], lag_ratio=0.3), run_time=3)

        # where the grid lines cross = whole-number combinations
        dots = VGroup()
        for i in range(-7, 8):
            for j in range(-7, 8):
                x, y, _ = plane.c2p(*(i * V1 + j * V2))
                if XMIN < x < XMAX and YMIN < y < YMAX:
                    dots.add(Dot([x, y, 0], radius=0.05, color=WHITE).set_z_index(LAYER_DOTS))
        self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dots], lag_ratio=0.02), run_time=1.5)
        shade = Rectangle(width=XMAX - XMIN, height=YMAX - YMIN, stroke_width=0, fill_color=BLUE,
                          fill_opacity=0.12).move_to([0, (YMAX + YMIN) / 2, 0]).set_z_index(LAYER_GRID)
        self.play(FadeIn(shade), run_time=0.8)
        self.switch_caption(self.caption(
            "Two non-parallel vectors:   Span{v₁, v₂} = the whole plane ℝ²   →   dimension 2"))
        self.until(114)

        # ---- (c) a PARALLEL vector adds nothing ----
        self.play(FadeOut(VGroup(*rings, dots, shade, v2, v2_label)), run_time=0.8)
        u = vector(plane, (0, 0), -1.5 * V1, PINK)
        self.play(GrowArrow(u), FadeIn(label(u, "u = −1.5·v₁", PINK, side=-1, size=26, distance=0.9)), run_time=1)
        self.switch_caption(self.caption(
            "Parallel vectors:   Span{v₁, u} is STILL just the line   →   u is redundant", accent=PINK))
        self.play(Indicate(span_line, color=PINK), run_time=1.2)
        self.until(129)
        self.clear_screen()
        self.current_caption = None

        # ---- (d) the same idea in 3-D ----
        self.set_camera_orientation(phi=65 * DEGREES, theta=-75 * DEGREES, zoom=0.95)
        axes = ThreeDAxes(x_range=(-3, 3, 1), y_range=(-3, 3, 1), z_range=(-2, 3, 1),
                          x_length=6, y_length=6, z_length=5)
        a, b = np.array([2, 0, 1]), np.array([0, 2, 1])
        tag = self.chapter_tag("03", "Seeing It Happen — now in 3-D space ℝ³")

        def name_3d(letter, color, position):
            """A letter that always faces the camera."""
            t = text(letter, 34, color, bold=True).move_to(axes.c2p(*position))
            t.set_stroke(BG, width=10, background=True)
            self.add_fixed_orientation_mobjects(t)
            return t

        def caption_3d(words, color=WHITE, accent=YELLOW):
            """Captions must be 'fixed in frame' so they don't rotate with the camera."""
            cap = self.caption(words, color, accent)
            self.add_fixed_in_frame_mobjects(cap)
            self.remove(cap)
            self.switch_caption(cap)

        self.add_fixed_in_frame_mobjects(tag)
        self.remove(tag)
        self.play(Create(axes), FadeIn(tag), run_time=1.2)

        arrow_a = Arrow3D(axes.c2p(0, 0, 0), axes.c2p(*a), color=BLUE)
        arrow_b = Arrow3D(axes.c2p(0, 0, 0), axes.c2p(*b), color=ORANGE)
        # the plane = all combinations s·a + t·b
        plane_ab = Surface(lambda s_, t_: axes.c2p(*(s_ * a + t_ * b)), u_range=(-1.3, 1.3),
                           v_range=(-1.3, 1.3), resolution=(8, 8), fill_color=BLUE, fill_opacity=0.3,
                           checkerboard_colors=[BLUE, BLUE], stroke_width=0.3, stroke_color=BLUE)
        self.play(Create(arrow_a), Create(arrow_b), FadeIn(name_3d("a", BLUE, a * 1.15)),
                  FadeIn(name_3d("b", ORANGE, b * 1.15)), run_time=1.2)
        caption_3d("Span{a, b} = a flat plane inside ℝ³   →   dimension 2")
        self.play(FadeIn(plane_ab), run_time=1.5)
        self.until(138)

        arrow_c = Arrow3D(axes.c2p(0, 0, 0), axes.c2p(*(a + b)), color=PINK)
        name_c = name_3d("c", PINK, (a + b) * 1.12)
        self.play(Create(arrow_c), FadeIn(name_c), run_time=1.2)
        caption_3d("c = a + b lies IN the plane   →   adds nothing new", PINK, PINK)
        self.until(145)

        d = np.array([-1, 1, 2.5])              # not of the form (2s, 2t, s+t), so not in the plane
        arrow_d = Arrow3D(axes.c2p(0, 0, 0), axes.c2p(*d), color=GREEN)
        self.play(FadeOut(arrow_c), FadeOut(name_c), Create(arrow_d), FadeIn(name_3d("d", GREEN, d * 1.12)),
                  run_time=1.2)
        caption_3d("d points OUT of the plane   →   Span{a, b, d} = all of ℝ³   →   dimension 3", GREEN, GREEN)
        self.begin_ambient_camera_rotation(rate=0.22)
        self.until(154)
        self.stop_ambient_camera_rotation()
        self.clear_screen(0.6)
        self.current_caption = None
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, zoom=1)   # back to normal 2-D view

    # -------------------------------------------- 4. worked example ------
    def chapter4_example(self):
        self.until(155)
        self.tag = self.chapter_intro(3)

        # layout: working on the left card, picture on the right card
        self.left_card = RoundedRectangle(corner_radius=0.2, width=6.75, height=6.55, fill_color=CARD,
                                          fill_opacity=0.97, stroke_color=EDGE, stroke_width=1.6).move_to([-3.45, -0.3, 0])
        right_card = self.left_card.copy().stretch_to_fit_width(6.6).move_to([3.55, -0.3, 0])
        plane = grid_plane((-1, 6, 1), (-1, 6, 1), 5.6, 5.6, opacity=0.5).move_to(right_card).shift(UP * 0.05)
        numbers = VGroup()
        for i in range(1, 6):
            numbers.add(text(str(i), 18, GREY).next_to(plane.c2p(i, 0), DOWN, buff=0.08))
            numbers.add(text(str(i), 18, GREY).next_to(plane.c2p(0, i), LEFT, buff=0.08))
        self.plane = plane
        self.play(FadeIn(self.left_card), FadeIn(right_card), run_time=0.6)
        self.play(Create(plane), FadeIn(numbers), run_time=0.9)

        question = text("Is { v₁, v₂, v₃ } a basis of ℝ² ?", 30, bold=True)
        given = text("v₁ = (1, 2)     v₂ = (3, 1)     v₃ = (4, 3)", 26)
        header = VGroup(question, given).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        header.move_to(self.left_card.get_corner(UL) + np.array([0.35, -0.32, 0]), aligned_edge=UL)
        rule = Line(LEFT, RIGHT, color=EDGE, stroke_width=1.5).set_width(6.05)
        rule.next_to(given, DOWN, buff=0.22).align_to(given, LEFT)

        self.v1 = vector(plane, (0, 0), V1, BLUE)
        self.v2 = vector(plane, (0, 0), V2, ORANGE)
        self.v3 = vector(plane, (0, 0), V3, PINK)
        self.v3_label = label(self.v3, "v₃", PINK, side=-1, size=26, distance=0.34)
        self.play(Write(question), run_time=1.0)
        self.play(FadeIn(given), Create(rule), GrowArrow(self.v1), GrowArrow(self.v2), GrowArrow(self.v3),
                  FadeIn(label(self.v1, "v₁", BLUE, side=1, size=26, distance=0.34)),
                  FadeIn(label(self.v2, "v₂", ORANGE, side=-1, size=26, distance=0.34)),
                  FadeIn(self.v3_label), run_time=1.4)
        self.until(165)

        def show_lines(lines, times):
            """Show the lines of one step one at a time under the header.
            Each line is (words, colour, bold). After line i we wait until times[i] (None = no wait)."""
            step = VGroup(*[text(words, 25, colour, bold) for words, colour, bold in lines])
            step.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
            if step.width > 6.0:
                step.scale_to_fit_width(6.0)
            step.next_to(rule, DOWN, buff=0.3).align_to(rule, LEFT)
            for line, t in zip(step, times):
                self.play(FadeIn(line, shift=RIGHT * 0.15), run_time=0.6)
                if t:
                    self.until(t)
            return step

        # STEP 1 — v3 is just v1 + v2
        step1 = show_lines([("STEP 1  ·  Look for a redundant vector", YELLOW, True),
                            ("v₁ + v₂ = (1+3, 2+1) = (4, 3) = v₃", WHITE, False)], [None, 170])
        moved_v2 = vector(plane, V1, V1 + V2, ORANGE, 5)        # v2 drawn from the tip of v1
        self.play(GrowArrow(moved_v2), run_time=1)
        self.play(Indicate(self.v3, color=PINK, scale_factor=1.1), Flash(plane.c2p(*V3), color=PINK), run_time=1)
        more = VGroup(text("v₃ is a combination of v₁ and v₂", 25),
                      text("⇒ { v₁, v₂, v₃ } is DEPENDENT ✗  (drop v₃)", 25, PINK, bold=True))
        more.arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(step1, DOWN, buff=0.2, aligned_edge=LEFT)
        if more.width > 6.0:
            more.scale_to_fit_width(6.0).align_to(step1, LEFT)
        self.play(FadeIn(more[0]), run_time=0.6)
        self.until(176)
        self.play(FadeIn(more[1]), run_time=0.6)
        self.until(179.4)
        self.play(FadeOut(step1), FadeOut(more), FadeOut(moved_v2),
                  self.v3.animate.set_opacity(0.25), self.v3_label.animate.set_opacity(0.25), run_time=0.6)

        # STEP 2 — v1 and v2 are independent
        step2 = show_lines([("STEP 2  ·  Is { v₁, v₂ } independent?", YELLOW, True),
                            ("Solve   c₁(1, 2) + c₂(3, 1) = (0, 0)", WHITE, False),
                            ("   c₁ + 3c₂ = 0          (i)", WHITE, False),
                            ("  2c₁ +   c₂ = 0          (ii)", WHITE, False),
                            ("(i)  ⇒  c₁ = −3c₂", WHITE, False),
                            ("(ii) ⇒  −6c₂ + c₂ = −5c₂ = 0", WHITE, False),
                            ("⇒  c₂ = 0,  c₁ = 0     INDEPENDENT ✓", GREEN, True),
                            ("(check: det = 1·1 − 3·2 = −5 ≠ 0)", GREY, False)],
                           [183, 187, 189.5, 193, 197.5, 201, 204.4, None])
        self.play(FadeOut(step2), run_time=0.6)

        # STEP 3 — they span the plane: draw the slanted grid made of v1 and v2
        self.slanted_grid = VGroup()
        for k in range(-8, 9):
            for start, direction in ((k * V2, V1), (k * V1, V2)):
                ends = line_inside(start, direction, -1, 6, -1, 6)       # keep it inside the small plane
                if ends:
                    self.slanted_grid.add(Line(plane.c2p(*ends[0]), plane.c2p(*ends[1]), stroke_width=1.5,
                                               color=YELLOW, stroke_opacity=0.35).set_z_index(LAYER_GRID))
        step3 = show_lines([("STEP 3  ·  Do v₁, v₂ span ℝ² ?", YELLOW, True),
                            ("Two non-parallel vectors in a plane", WHITE, False),
                            ("⇒ their combinations reach every point", WHITE, False),
                            ("Basis = { v₁, v₂ }     dim ℝ² = 2", GREEN, True)], [None] * 4)
        self.play(Create(self.slanted_grid), run_time=2.5)
        self.until(219.4)
        self.play(FadeOut(step3), run_time=0.6)

        # STEP 4 — write b = (5, 5) using v1 and v2
        self.b_ring = target(plane.c2p(*B), GREEN)
        b_name = text("b = (5, 5)", 24, GREEN, bold=True).next_to(self.b_ring, UP, buff=0.08).shift(LEFT * 0.35)
        b_name.set_stroke(BG, width=10, background=True)
        self.play(FadeIn(self.b_ring, scale=1.6), FadeIn(b_name), run_time=0.6)
        step4 = show_lines([("STEP 4  ·  Write b = (5, 5) using v₁, v₂", YELLOW, True),
                            ("c₁ + 3c₂ = 5     2c₁ + c₂ = 5", WHITE, False),
                            ("(i) ⇒ c₁ = 5 − 3c₂  ⇒  10 − 6c₂ + c₂ = 5", WHITE, False),
                            ("⇒  c₂ = 1,   c₁ = 2", GREEN, True)], [None, 225, 229, None])
        self.draw_combination(plane, 2, V1, BLUE, 1, V2, ORANGE, run_time=0.9)
        check = box(text("Check: 2(1, 2) + 1(3, 1) = (5, 5) ✓", 25, GREEN, bold=True), outline=GREEN, padding=0.16)
        check.next_to(step4, DOWN, buff=0.25, aligned_edge=LEFT)
        self.play(FadeIn(check), Flash(self.b_ring[1], color=GREEN), run_time=0.8)
        self.until(235)
        self.left_side_text = VGroup(header, rule, step4, check)

    # --------------------------------------------- 5. what it means ------
    def chapter5_meaning(self):
        plane = self.plane
        # this chapter continues on the same picture, so only the corner tag and the left text change
        new_tag = self.chapter_tag("05", CHAPTERS[4][3])
        self.play(FadeOut(self.left_side_text), FadeOut(self.tag, shift=UP * 0.2),
                  FadeIn(new_tag, shift=DOWN * 0.2), run_time=0.8)

        def stack(items):
            """Stack items top-to-bottom inside the left card (each scaled to fit its width)."""
            for item in items:
                if item.width > 6.0:
                    item.scale_to_fit_width(6.0)
            items.arrange(DOWN, aligned_edge=LEFT, buff=0.38)
            items.move_to(self.left_card.get_corner(UL) + np.array([0.35, -0.4, 0]), aligned_edge=UL)
            return items

        # b's coordinates in the new basis
        meaning = stack(VGroup(
            text("b = 2·v₁ + 1·v₂", 44, bold=True),
            text("Coordinates of b in the basis { v₁, v₂ }:", 27),
            box(text("(2, 1)", 38, YELLOW, bold=True), outline=YELLOW, padding=0.16),
            text("A basis is a coordinate system —\neach grid step is one copy of v₁ or v₂.", 27),
            box(text("Dimension = how many\ncoordinates you need", 27, GREEN, bold=True), outline=GREEN, padding=0.2),
        ))
        self.play(FadeIn(meaning[0], shift=RIGHT * 0.2), run_time=0.7)
        self.until(240)
        self.play(FadeIn(meaning[1]), FadeIn(meaning[2], scale=0.9),
                  self.slanted_grid.animate.set_stroke(opacity=0.75), run_time=0.8)
        self.until(244)
        self.play(FadeIn(meaning[3]), run_time=0.8)
        self.until(248)
        self.play(FadeIn(meaning[4], shift=UP * 0.15), run_time=0.8)
        self.until(252)

        # why independence matters: with v3 kept, b has two different recipes
        self.play(FadeOut(meaning), self.v3.animate.set_opacity(1), self.v3_label.animate.set_opacity(1),
                  run_time=0.8)
        why = stack(VGroup(
            text("Why must a basis be independent?", 32, YELLOW, bold=True),
            text("Keep v₃ as well, and the same point b\nhas two recipes:", 27),
            text("b = 2v₁ + v₂        b = v₁ + v₃", 34, bold=True),
            box(text("Two recipes ⇒ coordinates\nare NOT unique ✗", 27, PINK, bold=True), outline=PINK, padding=0.2),
            box(text("A basis gives exactly ONE\nrecipe per point ✓", 27, GREEN, bold=True), outline=GREEN, padding=0.2),
        ))
        self.play(FadeIn(why[0]), run_time=0.7)
        self.until(257)
        self.play(FadeIn(why[1]), FadeIn(why[2]), run_time=0.7)
        second_recipe = self.draw_combination(plane, 1, V1, BLUE, 1, V3, PINK, run_time=0.9)
        self.until(264)
        self.play(FadeIn(why[3], shift=UP * 0.15), run_time=0.7)
        self.until(268)
        self.play(FadeIn(why[4], shift=UP * 0.15), FadeOut(second_recipe), run_time=0.7)
        self.until(271.2)
        self.clear_screen()

    # ----------------------------------------- 6. summary + end screen ---
    def chapter6_summary(self):
        self.until(272)
        self.chapter_intro(5)
        takeaways = [
            ("Span", "Everything you can reach\nwith linear combinations.", icon_span(), BLUE),
            ("Basis", "Spans with NO redundancy —\nevery vector gets exactly\none set of coordinates.", icon_basis(), ORANGE),
            ("Dimension", "The number of basis vectors:\nline 1 · plane 2 · space 3", icon_dimension(), GREEN),
        ]
        cards = VGroup()
        for number, (word, meaning, picture, colour) in enumerate(takeaways, start=1):
            card = RoundedRectangle(corner_radius=0.2, width=4.2, height=4.6, fill_color=CARD,
                                    fill_opacity=0.97, stroke_color=EDGE, stroke_width=1.6)
            top_stripe = Line(card.get_corner(UL) + RIGHT * 0.2, card.get_corner(UR) + LEFT * 0.2,
                              color=colour, stroke_width=5).shift(DOWN * 0.02)
            circle = Circle(radius=0.34, color=colour, stroke_width=2.5, fill_color=colour, fill_opacity=0.15)
            circle.add(text(str(number), 28, colour, bold=True).move_to(circle))
            picture.scale_to_fit_height(1.1)
            if picture.width > 2.2:
                picture.scale_to_fit_width(2.2)
            meaning_text = text(meaning, 24)
            if meaning_text.width > 3.6:
                meaning_text.scale_to_fit_width(3.6)
            inside = VGroup(circle, picture, text(word, 40, colour, bold=True), meaning_text)
            inside.arrange(DOWN, buff=0.32).move_to(card)
            cards.add(VGroup(card, top_stripe, inside))
        cards.arrange(RIGHT, buff=0.4).move_to(DOWN * 0.25)
        for card, end_time in zip(cards, (276, 281, 286.5)):
            self.play(FadeIn(card, shift=UP * 0.3, scale=0.95), run_time=0.8)
            self.until(end_time)
        self.clear_screen(0.6)

        # end screen with credits
        background = grid_plane((-9, 9, 1), (-5, 5, 1), 14.4, 8, opacity=0.18)
        credits = VGroup(
            text("Animated in Python with Manim Community Edition", 22, GREY),
            text("References:  G. Strang, Introduction to Linear Algebra (Ch. 3)  ·  "
                 "3Blue1Brown, Essence of Linear Algebra (Ch. 2)", 20, GREY),
            text("Music:  “Thinking Music” by Kevin MacLeod (incompetech.com)  ·  "
                 "Licensed under Creative Commons: By Attribution 4.0", 20, GREY),
        ).arrange(DOWN, buff=0.22)
        if credits.width > 11.6:
            credits.scale_to_fit_width(11.6)
        end_card = box(VGroup(text("Thanks for watching!", 56, bold=True),
                              text(f"{STUDENT_NAME}   ·   {STUDENT_ID}", 28, BLUE),
                              Line(LEFT * 3, RIGHT * 3, color=YELLOW, stroke_width=3),
                              credits).arrange(DOWN, buff=0.35), padding=0.5).move_to(UP * 0.1)
        self.play(FadeIn(background), run_time=0.6)
        self.play(FadeIn(end_card, shift=UP * 0.25), run_time=0.9)
        self.until(300)
