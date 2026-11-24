"""Reading of config file of A-Maze-ing."""

from dataclasses import dataclass

MANDATORY_KEYS = (
    "WIDTH",
    "HEIGHT",
    "ENTRY",
    "EXIT",
    "OUTPUT_FILE",
    "PERFECT",
)
OPTIONAL_KEYS = ("SEED",)

MIN_SIDE = 2
MAX_SIDE = 1000

TRUE_WORDS = {"true", "1", "yes"}
FALSE_WORDS = {"false", "0", "no"}


class ConfigError(Exception):
    """Error in config file"""


@dataclass(frozen=True)
class Config:
    """Parameter for Config"""

    width: int
    height: int
    entry: tuple[int, int]
    exit: tuple[int, int]
    output_file: str
    perfect: bool
    seed: int | None


def read_pairs(path: str) -> dict[str, str]:
    """Read KEY=VALUE and return dict of keys"""
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


def check_keys(pairs: dict[str, str]) -> None:
    """Check mandatory keys and look for optional"""
    missing = [key for key in MANDATORY_KEYS if key not in pairs]
    if missing:
        raise ConfigError(f"brak kluczy: {', '.join(missing)}")
    known = set(MANDATORY_KEYS) | set(OPTIONAL_KEYS)
    unknown = sorted(set(pairs) - known)
    if unknown:
        raise ConfigError(f"nieznane klucze: {', '.join(unknown)}")


def as_int(pairs: dict[str, str], key: str) -> int:
    """change to int"""
    raw = pairs[key]
    try:
        return int(raw)
    except ValueError:
        raise ConfigError(f"{key}={raw!r} to nie liczba calkowita") from None


def as_coords(pairs: dict[str, str], key: str) -> tuple[int, int]:
    """Change from x,y to pair of int"""
    raw = pairs[key]
    parts = raw.split(",")
    if len(parts) != 2:
        raise ConfigError(f"{key}={raw!r} ma miec format x,y")
    try:
        return (int(parts[0]), int(parts[1]))
    except ValueError:
        raise ConfigError(f"{key}={raw!r} to nie dwie liczby") from None


def as_bool(pairs: dict[str, str], key: str) -> bool:
    """change key value to bool"""
    raw = pairs[key]
    word = raw.lower()
    if word in TRUE_WORDS:
        return True
    if word in FALSE_WORDS:
        return False
    raise ConfigError(f"{key}={raw!r} ma byc True albo False")


def validate(config: Config) -> None:
    """Check if making of maze is possibol"""
    for name, size in (("WIDTH", config.width), ("HEIGHT", config.height)):
        if not MIN_SIDE <= size <= MAX_SIDE:
            raise ConfigError(
                f"{name}={size} poza zakresem {MIN_SIDE}..{MAX_SIDE}"
            )
    check_inside("ENTRY", config.entry, config)
    check_inside("EXIT", config.exit, config)
    if config.entry == config.exit:
        raise ConfigError("ENTRY i EXIT wskazuja te sama komorke")
    if not config.output_file:
        raise ConfigError("OUTPUT_FILE nie moze byc pusty")


def check_inside(
    name: str, point: tuple[int, int], config: Config
) -> None:
    """Check if point is in maze"""
    x, y = point
    if not 0 <= x < config.width or not 0 <= y < config.height:
        raise ConfigError(
            f"{name}={x},{y} is out of maze"
            f"{config.width}x{config.height}"
        )


def load_config(path: str) -> Config:
    """Check config and return validate one"""
    pairs = read_pairs(path)
    check_keys(pairs)
    config = Config(
        width=as_int(pairs, "WIDTH"),
        height=as_int(pairs, "HEIGHT"),
        entry=as_coords(pairs, "ENTRY"),
        exit=as_coords(pairs, "EXIT"),
        output_file=pairs["OUTPUT_FILE"],
        perfect=as_bool(pairs, "PERFECT"),
        seed=as_int(pairs, "SEED") if "SEED" in pairs else None,
    )
    validate(config)
    return config
