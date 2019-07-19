# This script generates all glyphs up to a known point.
from glyph import Glyph
import pyyaml

def homogenize(g):
    a, b, c, d = g, g.rotated_90, g.rotated_90.rotated_90, g.rotated_90.rotated_90.rotated_90
    a_h = a.flip_horizontal
    b_h, c_h, d_h = a_h.rotated_90, a_h.rotated_90.rotated_90, a_h.rotated_90.rotated_90.rotated_90
    a_w = a.flip_vertical
    b_w, c_w, d_w = a_w.rotated_90, a_w.rotated_90.rotated_90, a_w.rotated_90.rotated_90.rotated_90
    selection = {a, b, c, d, a_h, b_h, c_h, d_h, a_w, b_w, c_w, d_w}
    if not (a.width == b.width == c.width == d.width):
        if a.width < b.width:
            map(selection.remove, (a, c, a_h, c_h, a_w, c_w))
        else:
            map(selection.remove, (b, d, b_h, d_h, b_w, d_w))
    representative = min(selection, key=lambda glyph: glyph.score)
    selection.remove(representative)
    return representative, selection


if __name__ == "__main__":
    memo = {}
    generations = 0
    this_generation = {Glyph()}
    for i in range(generations + 1):
        print(f"Gen {i} ", end="-" * 80 + "\n")
        next_generation = {}
        for glyph in this_generation:
            rep, selection = homogenize(glyph)
            m = {
                'representative': rep,
                'all_forms': selection | {rep}
            }
            for form in selection | {rep}:
                memo[form] = m
                next_generation |= form.children