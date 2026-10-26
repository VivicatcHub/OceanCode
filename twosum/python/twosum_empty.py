#!/usr/bin/env python3
"""Two Sum : trouver deux indices i < j tels que nums[i] + nums[j] == target."""

import re
import sys

USAGE = "usage: twosum <target>   (nombres lus sur stdin)"
LIMIT = 10**18


def two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    """Renvoie (i, j) avec i < j et nums[i] + nums[j] == target, ou None.

    S'il y a plusieurs solutions : le plus petit j, puis le plus petit i.
    Doit être en O(n).
    """
    # TODO
    raise NotImplementedError("two_sum")


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
    if len(argv) != 1:
        die("wrong number of arguments")
    target = parse_int(argv[0])
    nums = [parse_int(tok) for tok in sys.stdin.read().split()]

    res = two_sum(nums, target)
    print("none" if res is None else f"{res[0]} {res[1]}")


if __name__ == "__main__":
    main(sys.argv[1:])
