# Span, Basis & Dimension — M3 Animation Video

**Course:** Linear Algebra & Calculus (M3) · Internal Assessment, Project Option 1
**Student:** Kushal Mittal · E25B070595

**Learning objective:** By the end of this video, the viewer will be able to explain what the span of a set of vectors is, when a set of vectors forms a basis, and why the dimension of a space is the number of vectors in any basis, both geometrically and algebraically.

## Repository contents
| File | What it is |
|---|---|
| `_Video.mp4` | Final video: 1920×1080, 16:9, 5:07, with voice-over and background music |
| `_Code/span_basis_dimension.py` | The whole video: one Manim scene with one method per chapter |
| `_Code/style.py` | Colours, fonts and small helpers (text, boxes, arrows, labels) |
| `_Code/add_music.py` | Loops the music to 5:00, fades it, and mixes it under the video (quiet, about −31 dB) |
| `_Code/make_storyboard.py` | Builds the storyboard PDF with thumbnails from the video |
| `_Code/assets/` | Background vignette image and the music track (`thinking_music.mp3`) |
| `Storyboard.pdf` | 6-scene storyboard (Hook → Concept → Intuition → Worked example → Interpretation → Summary) |

## Rebuild the video
```bash
pip install manim          # macOS also needs: brew install cairo pkg-config
cd _Code
manim -r 1920,1080 --fps 30 span_basis_dimension.py SpanBasisDimension
```
The output appears in `_Code/media/videos/span_basis_dimension/1080p30/`. No LaTeX is needed because all maths is drawn as Unicode text.

Add the music:
```bash
python add_music.py media/videos/span_basis_dimension/1080p30/SpanBasisDimension.mp4 assets/thinking_music.mp3 ../_Video.mp4
```

## Worked example (verified by hand)
- v₁ = (1, 2), v₂ = (3, 1), v₃ = (4, 3)
- v₁ + v₂ = (4, 3) = v₃, so {v₁, v₂, v₃} is dependent
- c₁v₁ + c₂v₂ = 0 gives c₁ = −3c₂ and −5c₂ = 0, so c₁ = c₂ = 0 and {v₁, v₂} is independent (det = −5)
- {v₁, v₂} is therefore a basis of ℝ², and dim ℝ² = 2
- b = (5, 5) = 2v₁ + 1v₂; check: (2, 4) + (3, 1) = (5, 5) ✓

## Credits & AI disclosure
- Animation: [Manim Community Edition](https://www.manim.community/)
- References: G. Strang, *Introduction to Linear Algebra*, Ch. 3; 3Blue1Brown, *Essence of Linear Algebra*, Ch. 2
- Music: "Inspired" by Kevin MacLeod ([incompetech.com](https://incompetech.com)), licensed under [Creative Commons: By Attribution 4.0](https://creativecommons.org/licenses/by/4.0/). (Earlier drafts used "Thinking Music" by Kevin MacLeod, CC BY 4.0, which is still named on the end screen.)
- **AI disclosure:** I used AI (Claude by Anthropic) to help create the visuals and animations, to write the animation code, and for parts of the narration script. All mathematics was checked by hand, and the voice-over is my own.
