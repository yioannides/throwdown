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
        [stance, direction, spin, highpop],
        [stance, highpop, "Late", direction, spin],
    ]

    medium = [
        [stance, lowpop],
        [stance, pressure],
        [stance, highpop, "to", flat],
        [stance, highpop, "to", grind],
        [grind, "to", direction, spin],
        [stance, direction, spin, midpop],
        [stance, direction, spin, highpop],
        [stance, direction, spin, pressure],
        [stance, direction, spin, "to", flat],
        [stance, direction, spin, "to", grind],
        [stance, midpop, "Late", direction, spin],
        [stance, "to", grind, "to", direction, spin],
        [stance, direction, spin, highpop, "to", grind],
    ]

    hard = [
        [stance, midpop, "to", flat],
        [stance, lowpop, "to", flat],
        [stance, midpop, "to", grind],
        [stance, lowpop, "to", grind],
        [stance, pressure, "to", flat],
        [stance, direction, spin, lowpop],
        [stance, direction, spin, midpop],
        [stance, direction, spin, highpop],
        [stance, direction, spin, pressure],
        [stance, "to", grind, "to", highpop],
        [stance, direction, spin, "to", grind],
        [stance, lowpop, "Late", direction, spin],
        [stance, lowpop, "to", grind, "to", midpop],
        [stance, lowpop, "to", grind, "to", midpop],
        [stance, pressure, "Late", direction, spin],
        [stance, midpop, "to", grind, "to", highpop],
        [stance, lowpop, "to", grind, "to", highpop],
        [stance, direction, spin, lowpop, "to", grind],
        [stance, direction, spin, midpop, "to", grind],
        [stance, direction, spin, highpop, "to", grind],
    ]

    pro = [
        [stance, direction, spin, midpop, "to", flat, "to", midpop],
        [stance, direction, spin, lowpop, "to", flat, "to", midpop],
        [stance, direction, spin, lowpop, "to", flat, "to", highpop],
        [stance, direction, spin, midpop, "to", flat, "to", highpop],
        [stance, direction, spin, highpop, "to", flat, "to", highpop],
        [stance, direction, spin, midpop, "to", grind, "to", highpop],
        [stance, direction, spin, highpop, "to", grind, "to", highpop],
        [stance, direction, spin, midpop, "to", flat, "to", direction, spin],
        [stance, direction, spin, highpop, "to", flat, "to", direction, spin],
        [stance, direction, spin, midpop, "to", grind, "to", direction, spin],
        [stance, direction, spin, midpop, "to", flat, "to", direction, midpop],
        [stance, direction, spin, midpop, "to", flat, "to", direction, spin, highpop],
        [stance, direction, spin, lowpop, "to", grind, "to", direction, spin, midpop],
        [stance, direction, spin, midpop, "to", grind, "to", direction, spin, highpop],
        [stance, direction, spin, highpop, "to", flat, "to", direction, spin, highpop],
        [stance, direction, spin, highpop, "to", grind, "to", direction, spin, highpop],
    ]

    return {
        "easy": easy,
        "medium": medium,
        "hard": hard,
        "pro": pro,
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

    if not any("Casper" in str(item) or "Primo" in str(item) for item in resolved):
        for i, item in enumerate(combo):
            if item is highpop:
                resolved[i] = choice(highpop)

    if "Pop Shove-it" in resolved[-1]:
        if grind in combo:
            resolved[-1] = resolved[-1].replace("Pop ", "")

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
