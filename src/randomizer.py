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
flipside = _tricks["flipside"]
highpop = _tricks["highpop"]
midpop = _tricks["midpop"]
lowpop = _tricks["lowpop"]
pressure = _tricks["pressure"]
grind = _tricks["grind"]
flat = _tricks["flat"]
_aliases = _tricks["aliases"]

def _preferences():
    settings = Gio.Settings.new("io.github.yioannides.Throwdown")

    return {
        "spin": (
            _tricks["spin"]
            if settings.get_boolean("enable-360-spins")
            else _tricks["spin"][:1]
        )
    }

def _combo_pools(preferences):

    spin = preferences["spin"]

    easy = [
        [stance, midpop],
        [stance, highpop],
        [stance, "to", grind],
        [stance, direction, spin],
        [stance, direction, spin, highpop],
        [stance, highpop, "late", direction, spin],
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
        [stance, midpop, "late", direction, spin],
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
        [stance, lowpop, "late", direction, spin],
        [stance, lowpop, "to", grind, "to", midpop],
        [stance, midpop, "to", grind, "to", midpop],
        [stance, pressure, "late", direction, spin],
        [stance, midpop, "to", grind, "to", highpop],
        [stance, lowpop, "to", grind, "to", highpop],
        [stance, pressure, "to", grind, "to", highpop],
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
        [stance, direction, spin, pressure, "to", flat, "to", direction, spin],
        [stance, direction, spin, midpop, "to", flat, "to", direction, spin, midpop],
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

def _resolve_combo(combo, preferences):
    resolved = []
    # init: convert items to tricks
    for item in combo:
        if item is highpop:
            resolved.append(choice(highpop[:2]))
        elif isinstance(item, list):
            resolved.append(choice(item))
        else:
            resolved.append(item)
    # 01: if shuvits -> no flipped flat tricks / no body varial with late flips
    if not any("casper" in str(item) or "primo" in str(item) for item in resolved):
        pool = highpop
        if "late" in combo:
            pool = pool[:-1]
        for i, item in enumerate(combo):
            if item is highpop:
                resolved[i] = choice(pool)
    # 02: if spin -> no flipped flat tricks
    if preferences["spin"] in combo:
        for i, item in enumerate(combo):
            if item is flat:
                resolved[i] = choice(flat[:2])
    # 03: direction for shuvits
    for i, item in enumerate(resolved):
        if "pop shove-it" in item:
         resolved[i] = choice(flipside) + " " + item

    return resolved

def _format(trick_list):
    output = " ".join(str(x) for x in trick_list).strip()
    if output.startswith("to"):
        output = "Ollie " + output

    return output

def _apply_aliases(combo, resolved):
    for original in sorted(_aliases, key=len, reverse=True):
        combo = combo.replace(original, _aliases[original])
    # 04: no pop for shuv outs
    if "pop shove-it" in resolved[-1]:
        if any(item in grind for item in resolved):
            combo = combo.replace(resolved[-1], resolved[-1].replace("pop ", ""))

    return combo

def _capitalize(combo):
    items = combo.split(" to ")
    capitalization = "\n↓\n".join(str(x).title() for x in items)
    capitalization = capitalization.replace("Fs", "FS").replace("fs", "FS") \
                                    .replace("Bs", "BS").replace("bs", "BS")
    return capitalization

def generate_trick(difficulty="random"):
    preferences = _preferences()
    pools = _combo_pools(preferences)

    if difficulty == "random":
        difficulty = choice(list(pools))

    selection = choice(pools[difficulty])
    resolved = _resolve_combo(selection, preferences)
    formatted = _format(resolved)
    aliased = _apply_aliases(formatted, resolved)
    output = _capitalize(aliased)

    return output
