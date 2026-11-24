import random

NORTH = 1
EAST = 2
SOUTH = 4
WEST = 8

# FULL = 15 = 0b1111
FULL = NORTH | EAST | SOUTH | WEST

# (dx, dy, ściana_bieżącej_komórki, ściana_sąsiada)
MOVES: dict[int, tuple[int, int, int, int]] = {
    NORTH: (0, -1, NORTH, SOUTH), # bo idzie w dół
    EAST: (1, 0, EAST, WEST),
    SOUTH: (0, 1, SOUTH, NORTH),
    WEST: (-1, 0, WEST, EAST),
}


class MazeGenerator:

    def __init__(
        self,
        width: int,
        height: int,
        *,
        entry: tuple[int, int] = (0, 0),
        exit: tuple[int, int] | None = None,
        perfect: bool = False,
        seed: int | None = None,
    ) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit if exit is not None else (width - 1, height - 1)
        self.perfect = perfect
        self.seed = seed
        self.rng = random.Random(seed) # własne źródło losowości
        self.grid: list[list[int]] = [
            [FULL] * width for _ in range(height)
        ] # dostęp do komórki przez self.grid[y][x]

    def generate(self) -> None:
        """dyrygent całości"""
        raise NotImplementedError

    def solve(self) -> str:
        raise NotImplementedError

    def pattern_cells(self) -> set[tuple[int, int]]:
        """zwraca zbiór współrzędnych (x, y), które mają zostać zamurowane i tworzą wzór „42“."""
        raise NotImplementedError

    def _carve(self, x: int, y: int, direction: int) -> None:
        """otwiera jedną ścianę. Czyta MOVES[direction], kasuje bit u siebie i przeciwny u sąsiada."""
        raise NotImplementedError

