#!/usr/bin/env python3
"""Chiffrement de César + déchiffrement par force brute."""

import re
import sys

USAGE = """usage:
  caesar encrypt <shift> <text>
  caesar decrypt <text>"""


def encrypt(text: str, shift: int) -> str:
    """Décale chaque lettre ASCII (a-z, A-Z) de `shift` positions."""
    result: list[str] = []
    for c in text:
        if "a" <= c <= "z":
            value: int = (ord(c) + shift - ord("a")) % 26 + ord("a")
            result.append(chr(value))
        elif "A" <= c <= "Z":
            value: int = (ord(c) + shift - ord("A")) % 26 + ord("A")
            result.append(chr(value))
        else:
            result.append(c)
    return "".join(result)


def decrypt(text: str) -> list[str]:
    """Force brute : renvoie les 26 candidats, l'élément k étant le texte
    déchiffré en supposant un décalage de k."""
    return [encrypt(text, -i) for i in range(26)]


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

    if cmd == "encrypt":
        if len(args) != 2:
            die("wrong number of arguments")
        print(encrypt(args[1], parse_shift(args[0])))
    elif cmd == "decrypt":
        if len(args) != 1:
            die("wrong number of arguments")
        for k, candidate in enumerate(decrypt(args[0])):
            print(f"{k}: {candidate}")
    else:
        die(f"unknown command '{cmd}'")


if __name__ == "__main__":
    main(sys.argv[1:])
