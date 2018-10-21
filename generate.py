# This script generates all glyphs up to a known point.
from glyph import Glyph


def homogenize(g):
    a, b, c, d = g, g.rotated_90, g.rotated_90.rotated_90, g.rotated_90.rotated_90.rotated_90
    selection = [a, b, c, d]
    if not a.width == b.width == c.width == d.width:
        if a.width < b.width:
            selection.remove(a)
            selection.remove(c)
        else:
            selection.remove(b)
            selection.remove(d)
    representative = min(selection, key=lambda glyph: glyph.score)
    return representative, frozenset(a.solids), frozenset(b.solids), frozenset(c.solids), frozenset(d.solids)


if __name__ == "__main__":
    starter_glyph = Glyph()
    unique_glyphs, all_glyphs, latest_generation = {starter_glyph}, {frozenset(starter_glyph.solids): starter_glyph}, {starter_glyph}
    for i in range(3):
        print(f'Generation: {i}')
        new_glyphs = set()
        while latest_generation:
            parent = latest_generation.pop()
            for o in parent.openings:
                new_solids = parent.solids | {o}
                new_g = Glyph(new_solids)
                if not frozenset(new_solids) in all_glyphs.keys():
                    result = homogenize(new_g)
                    representative, all_glyph_forms = result[0], result[1:]
                    unique_glyphs |= {representative}
                    for frozen_solid in all_glyph_forms:
                        all_glyphs[frozen_solid] = representative
                    new_glyphs |= {new_g}

        print("New glyphs generated:", *new_glyphs, sep="\n", end="\n\n")
        latest_generation |= new_glyphs
