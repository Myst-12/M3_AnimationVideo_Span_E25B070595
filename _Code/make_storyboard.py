"""
Builds Storyboard.pdf (6-scene storyboard) with a thumbnail from the
rendered video for every scene.

    python make_storyboard.py <rendered_video.mp4> <output.pdf>
"""
import io
import sys

import av
from fpdf import FPDF

from span_basis_dimension import STUDENT_NAME, STUDENT_ID

FONT = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"
FONT_B = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

OBJECTIVE = ("By the end of this video, the viewer will be able to explain what the span of a set of "
             "vectors is, when a set of vectors forms a basis, and why the dimension of a space is the "
             "number of vectors in any basis — both geometrically and algebraically.")

SCENES = [
    ("1. Hook / Context", "0:00 – 0:35", 20,
     "Spark curiosity: can two arrows reach every point of a plane?",
     "Title card (name, ID). Grid with v₁ = (1,2) and v₂ = (3,1). Three yellow target points are "
     "reached tip-to-tail: (4,3) = v₁ + v₂, (−1,−3) = −1.6v₁ + 0.2v₂, (−4,2) = 2v₁ − 2v₂. "
     "A third vector v₃ appears: \"do we even need it?\""),
    ("2. Concept Introduction", "0:35 – 1:20", 78,
     "State the learning goal and define all notation before using it.",
     "Yellow goal box, then a table of five definitions revealed one row at a time: linear combination, "
     "span, linear independence, basis, dimension."),
    ("3. Visual Intuition", "1:20 – 2:35", 103,
     "Build geometric understanding before any algebra.",
     "One vector: c·v₁ sweeps out a line (dim 1). Two non-parallel vectors: a point c₁v₁ + c₂v₂ wanders "
     "everywhere with live coefficients, then the slanted grid grows outward and tiles the screen, "
     "dots mark integer combinations and the whole plane shades in (dim 2). Parallel vector u = −1.5v₁ stays on the "
     "line (dependent). 3D: a, b span a plane; c = a + b lies in it; d out of the plane gives all of ℝ³ (dim 3)."),
    ("4. Worked Example", "2:35 – 3:55", 203,
     "Show step by step why and how the maths works.",
     "Is {(1,2), (3,1), (4,3)} a basis of ℝ²? Step 1: v₁ + v₂ = (4,3) = v₃ → dependent, drop v₃. "
     "Step 2: c₁v₁ + c₂v₂ = 0 → c₁ = −3c₂, −5c₂ = 0 → c₁ = c₂ = 0 (det = −5, non-zero) → independent. "
     "Step 3: slanted grid shows they span ℝ² → basis, dim 2. Step 4: b = (5,5) → c₂ = 1, c₁ = 2, checked."),
    ("5. Interpretation", "3:55 – 4:32", 266,
     "Connect the algebra back to the picture.",
     "b = 2v₁ + 1v₂ means b has coordinates (2,1) on the slanted grid: a basis is a coordinate system "
     "and dimension = number of coordinates. With v₃ kept, b = 2v₁ + v₂ = v₁ + v₃ → two recipes, "
     "so coordinates are not unique. This is why a basis must be independent."),
    ("6. Summary & Credits", "4:32 – 5:00", 284,
     "Reinforce the three takeaways; cite sources and credit the music.",
     "Three takeaway cards (span / basis / dimension). Closing frame: name, ID, tools (Manim CE), "
     "references (Strang; 3Blue1Brown) and music credit."),
]
CHAPTER_TITLES = ["Can Two Arrows Reach Everything?", "The Five Key Words", "Seeing It Happen",
                  "Let's Solve One Together", "So What Does It Mean?", "The Big Picture"]


def grab_frames(video, times):
    out, todo = {}, sorted(times)
    with av.open(video) as c:
        for f in c.decode(c.streams.video[0]):
            if todo and f.time >= todo[0]:
                buf = io.BytesIO()
                f.to_image().resize((480, 270)).save(buf, format="PNG")
                out[todo.pop(0)] = buf
            if not todo:
                break
    return out


def main(video, pdf_path):
    frames = grab_frames(video, [s[2] for s in SCENES])
    pdf = FPDF(orientation="L", format="A4")
    pdf.add_font("U", "", FONT)
    pdf.add_font("U", "B", FONT_B)
    pdf.set_auto_page_break(False)

    # page 1: overview
    pdf.add_page()
    pdf.set_font("U", "B", 24)
    pdf.cell(0, 14, "Storyboard — Span, Basis & Dimension", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("U", "", 12)
    pdf.cell(0, 8, f"Linear Algebra & Calculus (M3) · Animation Video · {STUDENT_NAME} · {STUDENT_ID}",
             new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_font("U", "B", 14)
    pdf.cell(0, 8, "Learning objective", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("U", "", 12)
    pdf.multi_cell(0, 7, OBJECTIVE)
    pdf.ln(4)
    pdf.set_font("U", "B", 14)
    pdf.cell(0, 8, "Production plan", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("U", "", 12)
    pdf.multi_cell(0, 7,
        "• Tool: Manim Community Edition (Python), one scene file, 1920×1080, 30 fps, 5:00 long.\n"
        "• Colour code (kept constant): v₁ blue, v₂ orange, redundant vector v₃ / u pink, target b green, "
        "key results yellow.\n"
        "• Running example used everywhere: v₁ = (1, 2), v₂ = (3, 1), v₃ = (4, 3) = v₁ + v₂, b = (5, 5) = 2v₁ + v₂.\n"
        "• Voice-over is timed to the scenes; every scene begins at a fixed second via self.until(t).\n"
        "• Look: dark navy background with vignette, rounded info cards, animated chapter titles, "
        "and a chapter progress bar along the bottom.\n"
        "• Music: \"Thinking Music\" by Kevin MacLeod (incompetech.com), CC BY 4.0, looped to 5:00 and "
        "mixed quietly (about −31 dB) under the voice; credited on the end screen.\n"
        "• Maths verification: every combination recomputed by hand; det[[1,3],[2,1]] = −5 (non-zero); "
        "2(1,2) + (3,1) = (5,5); (1,2) + (4,3) = (5,5); (−1,1,2.5) is not of the form (2s, 2t, s+t).")

    # scene pages: 2 scenes per page
    for i, (name, time, t, purpose, plan) in enumerate(SCENES):
        if i % 2 == 0:
            pdf.add_page()
        y0 = 15 + (i % 2) * 95
        pdf.set_draw_color(180, 180, 180)
        pdf.rect(10, y0, 277, 88)
        if t in frames:
            pdf.image(frames[t], x=14, y=y0 + 4, w=142, h=80)
        x = 162
        pdf.set_xy(x, y0 + 5)
        pdf.set_font("U", "B", 16)
        pdf.cell(120, 8, name)
        pdf.set_xy(x, y0 + 13)
        pdf.set_font("U", "", 11)
        pdf.set_text_color(90, 90, 90)
        pdf.cell(120, 6, f"{time}   ·   on-screen chapter: “{CHAPTER_TITLES[i]}”")
        pdf.set_text_color(0, 0, 0)
        pdf.set_xy(x, y0 + 21)
        pdf.set_font("U", "B", 11)
        pdf.multi_cell(120, 5.5, "Purpose: " + purpose)
        pdf.set_x(x)
        pdf.set_font("U", "", 10.5)
        pdf.multi_cell(120, 5.2, "Visual, narration & maths: " + plan)

    pdf.output(pdf_path)
    print("saved", pdf_path)


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
