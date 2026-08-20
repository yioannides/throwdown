import json
from pathlib import Path
from random import choice

from gi.repository import Gio

_TRICKS_PATH = Path(__file__).parent / "tricks.json"

with _TRICKS_PATH.open(encoding="utf-8") as _file:
    _tricks = json.load(_file)

stance = _tricks["stance"]
direction = _tricks["direction"]
spin = _tricks["spin"]
highpop = _tricks["highpop"]
midpop = _tricks["midpop"]
lowpop = _tricks["lowpop"]
pressure = _tricks["pressure"]
grind = _tricks["grind"]
flat = _tricks["flat"]
_aliases = _tricks["aliases"]

def _combo_pools():

    settings = Gio.Settings.new("io.github.yioannides.Throwdown")

    if settings.get_boolean("enable-360-spins"):
        spin = _tricks["spin"]
    else:
        spin = _tricks["spin"][:1]

    easy = [
        [stance, midpop],
        [stance, highpop],
        [stance, "to", grind],
        [stance, direction, spin],
        [stance, direction, highpop],
        [stance, highpop, "Late", direction, spin],
    ]

    medium = [
        [stance, lowpop],
        [stance, pressure],
        [stance, direction, midpop],
        [stance, direction, pressure],
        [stance, highpop, "to", flat],
        [grind, "to", direction, spin],
        [stance, direction, spin, highpop],
        [stance, direction, spin, "to", flat],
        [stance, direction, spin, "to", grind],
        [stance, direction, highpop, "to", grind],
        [stance, midpop, "Late", direction, spin],
    ]

    hard = [
        [grind, "to", highpop],
        [stance, direction, lowpop],
        [stance, direction, midpop],
        [stance, direction, spin, highpop],
        [stance, direction, spin, pressure],
        [stance, direction, spin, "to", grind],
        [stance, direction, lowpop, "to", grind],
        [stance, direction, midpop, "to", grind],
        [stance, lowpop, "Late", direction, spin],
        [stance, pressure, "Late", direction, spin],
        [stance, direction, spin, highpop, "to", grind],
        [stance, direction, midpop, "to", flat, "to", midpop],
        [stance, direction, lowpop, "to", flat, "to", highpop],
        [stance, direction, highpop, "to", flat, "to", highpop],
        [stance, direction, midpop, "to", grind, "to", highpop],
        [stance, direction, spin, midpop, "to", flat, "to", midpop],
        [stance, direction, spin, midpop, "to", flat, "to", highpop],
        [stance, direction, midpop, "to", flat, "to", direction, spin],
        [stance, direction, spin, highpop, "to", grind, "to", highpop],
        [stance, direction, highpop, "to", flat, "to", direction, spin],
        [stance, direction, midpop, "to", grind, "to", direction, spin],
        [stance, direction, highpop, "to", flat, "to", direction, highpop],
        [stance, direction, spin, midpop, "to", flat, "to", direction, midpop],
        [stance, direction, spin, midpop, "to", flat, "to", direction, highpop],
    ]

    return {
        "easy": easy,
        "medium": medium,
        "hard": hard,
    }

def _resolve_combo(combo):
    resolved = []
    for item in combo:
        if item is highpop:
            resolved.append(choice(highpop[:2]))
        elif isinstance(item, list):
            resolved.append(choice(item))
        else:
            resolved.append(item)

    if any("Manual" in item for item in resolved):
        for i, item in enumerate(combo):
            if item is highpop:
                resolved[i] = choice(highpop)

    return resolved

def _format(trick_list):
    output = " ".join(str(x) for x in trick_list).strip()
    if output.startswith("to"):
        output = "Ollie " + output

    return output

def _apply_aliases(combo):
    for original in sorted(_aliases, key=len, reverse=True):
        combo = combo.replace(original, _aliases[original])
    combo = combo.replace("Modern Ghetto Bird 360", "Backside Hardflip 360")

    return combo

def generate_trick(difficulty="random"):
    pools = _combo_pools()

    if difficulty == "random":
        difficulty = choice(list(pools))

    combo = choice(pools[difficulty])
    combo = _resolve_combo(combo)
    combo = _format(combo)
    combo = _apply_aliases(combo)

    return combo.replace(" to ", "\n↓\n")
