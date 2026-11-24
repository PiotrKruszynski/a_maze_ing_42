#!/usr/bin/env python3
"""A-Maze-ing — generator labiryntow."""

import sys

from amaze.config import Config, ConfigError, load_config


def debug_print(config: Config) -> None:
    """Tymczasowy podglad configu - leci, gdy ruszy generator."""
    print(f"rozmiar : {config.width}x{config.height}")
    print(f"entry   : {config.entry}")
    print(f"exit    : {config.exit}")
    print(f"perfect : {config.perfect}")
    print(f"seed    : {config.seed}")
    print(f"output  : {config.output_file}")


def main(argv: list[str]) -> int:
    """Zwraca kod wyjscia: 0 gdy OK, 1 gdy blad uzycia."""
    if len(argv) != 2:
        print("usage: python3 a_maze_ing.py config.txt", file=sys.stderr)
        return 1
    try:
        config = load_config(argv[1])
    except ConfigError as err:
        print(f"Error: {err}", file=sys.stderr)
        return 1
    debug_print(config)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))