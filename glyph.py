from typing import Tuple, Set, Iterable, Dict, Optional

DIRS: Dict[str, Tuple[int, int]] = {
    'up': (0, -1),
    'down': (0, 1),
    'left': (-1, 0),
    'right': (1, 0),
}


class Glyph:
    @property
    def class_(self) -> int:
        return len(self.solids)

    @property
    def score(self) -> int:
        return sum(x + self.width * y for x, y in self.solids)

    @property
    def width(self) -> int:
        return max(x for x, y in self.solids)

    @property
    def height(self) -> int:
        return max(y for x, y in self.solids)

    @property
    def center(self) -> Tuple[float, float]:
        return (self.width + 1) / 2, (self.height + 1) / 2

    @property
    def solids(self) -> Set[Tuple[int, int]]:
        try:
            return self._solids
        except AttributeError:
            return set()

    @property
    def openings(self) -> Set[Tuple[int, int]]:
        return {(x + i, y + j) for i, j in DIRS.values() for x, y in self.solids} - self.solids

    @property
    def children(self) -> Set['Glyph']:
        return {Glyph(self.solids | {o}) for o in self.openings}

    @solids.setter
    def solids(self, new_solids_list: Iterable[Tuple[int, int]]) -> None:
        x_offset, y_offset = 1 - min(x for x, y in new_solids_list), 1 - min(y for x, y in new_solids_list)
        self._solids: Set[Tuple[int, int]] = {(x + x_offset, y + y_offset) for x, y in new_solids_list}

    @property
    def rotated_90(self) -> 'Glyph':
        return Glyph({self._rotate_point_90(p) for p in self.solids})

    def _convert_point_for_rotation(self, point: Tuple[int, int]) -> Tuple[float, float]:
        x, y = point
        i, j = self.center
        return x - i, y - j

    def _revert_point_to_default_space(self, point: Tuple[int, int], total_rotation: int = 90) -> Tuple[int, int]:
        x, y = point

        # When reverting back to default space from a rotation, the center might not be updated yet. Therefore, this
        # helps to compensate for that by rotating the center if appropriate.
        if total_rotation in (-360, -180, 0, 180, 360):
            i, j = self.center
        elif total_rotation in (-270, -90, 90, 270):
            j, i = self.center

        return int(x + i), int(y + j)

    def _rotate_point_90(self, point: Tuple[int, int]) -> Tuple[int, int]:
        x, y = self._convert_point_for_rotation(point)
        return self._revert_point_to_default_space((-y, x))

    def __init__(self, solids: Optional[Set[Tuple[int, int]]] = None):
        self.solids = solids if solids else {(1, 1)}

    def __repr__(self) -> str:
        string = ''
        for j in range(self.height + 2):
            string += '\n'
            for i in range(self.width + 2):
                string += chr(1) if (i, j) in self.solids else chr(183)
            string += '\t\t\t'
            for i in range(self.width + 2):
                string += chr(1) if (i, j) in self.solids else chr(215) if (i, j) in self.openings else chr(183)
        string += f'\nScore: {self.score}'
        return string