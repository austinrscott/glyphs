# This script generates all glyphs up to a known point.

class Glyph:
	def __init__(self, glyph_string):
		solids = []
		for i,row in enumerate(glyph_string):
			for j,character in enumerate(row):
				if character == '#':
					new_solid = (i, j)
					solids += new_solid
		available_nodes = []
		for i,j in solids:
			for x,y in ((i+1,j), (i-1,j), (i,j+1), (i,j-1)):
				if (x, y) not in solids:
					available_nodes += (x, y)