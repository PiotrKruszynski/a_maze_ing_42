"""Wczytywanie pliku konfiguracyjnego A-Maze-ing."""


class ConfigError(Exception):
    """Blad w pliku konfiguracyjnym."""


def read_pairs(path: str) -> dict[str, str]:
    """Czyta plik KEY=VALUE i zwraca slownik kluczy."""
    try:
        with open(path, "r", encoding="utf-8") as handle:
            lines = handle.readlines()
    except OSError as err:
        raise ConfigError(f"nie moge otworzyc {path}: {err.strerror}")

    pairs: dict[str, str] = {}
    for number, line in enumerate(lines, start=1):
        text = line.strip()
        if not text or text.startswith("#"):
            continue
        if "=" not in text:
            raise ConfigError(f"linia {number}: oczekiwano KEY=VALUE")
        name, _, value = text.partition("=")
        key = name.strip().upper()
        if not key:
            raise ConfigError(f"linia {number}: pusta nazwa klucza")
        if key in pairs:
            raise ConfigError(f"linia {number}: {key} juz byl wczesniej")
        pairs[key] = value.strip()
    return pairs