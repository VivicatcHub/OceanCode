#!/usr/bin/env python3
"""Exponentiation modulaire rapide: calcule (base^exponent) % modulus en O(log exponent)."""

import re
import sys

USAGE = "usage: modexp <base> <exponent> <modulus>"
LIMIT = 10**18


def mod_exp(base: int, exponent: int, modulus: int) -> int:
    """Calcule (base^exponent) % modulus en O(log exponent).

    Utilise l'algorithme d'exponentiation rapide (binary exponentiation).
    exponent doit être positif ou nul.
    """
    # TODO
    raise NotImplementedError("mod_exp")


def die(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    print(USAGE, file=sys.stderr)
    sys.exit(1)


def parse_int(s: str) -> int:
    if not re.fullmatch(r"-?[0-9]+", s):
        die(f"invalid number '{s}'")
    n = int(s)
    if abs(n) > LIMIT:
        die(f"number out of range '{s}'")
    return n


def main(argv: list[str]) -> None:
    if len(argv) != 3:
        die("wrong number of arguments")
    base = parse_int(argv[0])
    exponent = parse_int(argv[1])
    modulus = parse_int(argv[2])

    if exponent < 0:
        die("exponent must be non-negative")
    if modulus == 0:
        die("modulus must be non-zero")

    result = mod_exp(base, exponent, modulus)
    print(result)


if __name__ == "__main__":
    main(sys.argv[1:])
