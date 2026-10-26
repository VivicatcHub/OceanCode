#!/usr/bin/env python3
"""Chiffrement de César + déchiffrement par force brute."""

import re
import sys

USAGE = """usage:
  caesar encrypt <shift> <text>
  caesar decrypt <shift> <text>
  caesar bruteforce <text>"""


def encrypt(text: str, shift: int) -> str:
    """Décale chaque lettre ASCII (a-z, A-Z) de `shift` positions."""
    # TODO
    raise NotImplementedError("encrypt")


def decrypt(text: str, shift: int) -> str:
    """Inverse de encrypt."""
    # TODO
    raise NotImplementedError("decrypt")


def bruteforce(text: str) -> list[str]:
    """Renvoie les 26 candidats : l'élément k vaut decrypt(text, k)."""
    # TODO
    raise NotImplementedError("bruteforce")


def die(msg: str) -> None:
    print(f"error: {msg}", file=sys.stderr)
    print(USAGE, file=sys.stderr)
    sys.exit(1)


def parse_shift(s: str) -> int:
    if not re.fullmatch(r"-?[0-9]+", s):
        die(f"invalid shift '{s}'")
    return int(s)


def main(argv: list[str]) -> None:
    if not argv:
        die("missing command")
    cmd, args = argv[0], argv[1:]

    if cmd in ("encrypt", "decrypt"):
        if len(args) != 2:
            die("wrong number of arguments")
        shift = parse_shift(args[0])
        f = encrypt if cmd == "encrypt" else decrypt
        print(f(args[1], shift))
    elif cmd == "bruteforce":
        if len(args) != 1:
            die("wrong number of arguments")
        for k, candidate in enumerate(bruteforce(args[0])):
            print(f"{k}: {candidate}")
    else:
        die(f"unknown command '{cmd}'")


if __name__ == "__main__":
    main(sys.argv[1:])
