DIRS = {
    'up': (0, -1),
    'down': (0, 1),
    'left': (-1, 0),
    'right': (1, 0),
}


class Glyph:
    @property
    def score(self):
        return sum(x + self.width * y for x, y in self.solids)

    @property
    def width(self):
        return max(x for x, y in self.solids)

    @property
    def height(self):
        return max(y for x, y in self.solids)

    @property
    def center(self):
        return (self.width + 1) / 2, (self.height + 1) / 2

    @property
    def solids(self):
        try:
            return self._solids
        except AttributeError:
            return set()

    @property
    def openings(self):
        return {(x + i, y + j) for i, j in DIRS.values() for x, y in self.solids} - self.solids

    @solids.setter
    def solids(self, new_solids_list):
        x_offset, y_offset = 1 - min(x for x, y in new_solids_list), 1 - min(y for x, y in new_solids_list)
        self._solids = {(x + x_offset, y + y_offset) for x, y in new_solids_list}

    @property
    def rotated_90(self):
        return Glyph({self._rotate_point_90(p) for p in self.solids})

    def _convert_point_for_rotation(self, point):
        x, y = point
        i, j = self.center
        return x - i, y - j

    def _revert_point_to_default_space(self, point, total_rotation=90):
        x, y = point

        # When reverting back to default space from a rotation, the center might not be updated yet. Therefore, this
        # helps to compensate for that by rotating the center if appropriate.
        if total_rotation in (-360, -180, 0, 180, 360):
            i, j = self.center
        elif total_rotation in (-270, -90, 90, 270):
            j, i = self.center

        return int(x + i), int(y + j)

    def _rotate_point_90(self, point):
        x, y = self._convert_point_for_rotation(point)
        return self._revert_point_to_default_space((-y, x))

    def __init__(self, solids={(1, 1)}):
        self.solids = solids

    def __repr__(self):
        string = ''
        for j in range(self.height + 2):
            string += '\n'
            for i in range(self.width + 2):
                string += '[]' if (i, j) in self.solids else '__'
        string += f'\nScore: {self.score}'
        return string