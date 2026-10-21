#!/usr/bin/env python3
"""A-Maze-ing — generator labiryntow."""

from amaze.config import ConfigError, read_pairs

import sys


def main(argv: list[str]) -> int:
    """Zwraca kod wyjscia: 0 gdy OK, 1 gdy blad uzycia."""
    try:
        pairs = read_pairs(argv[1])
    except ConfigError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1
    print(pairs)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))