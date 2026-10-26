#!/usr/bin/env python3
"""Tester commun pour les 5 implémentations de Two Sum.

Spécification testée :
  twosum <target>       (les nombres sont lus sur stdin, séparés par des blancs :
                         espaces, tabulations, retours à la ligne)

  -> "i j\\n"   : indices (base 0, i < j) de deux éléments distincts tels que
                 nums[i] + nums[j] == target
  -> "none\\n"  : s'il n'existe aucune paire

  - S'il y a plusieurs solutions : celle avec le plus petit j, puis le plus petit i.
    (c'est exactement ce que donne l'algo "une passe + table de hachage" en ne
    gardant que la PREMIÈRE occurrence de chaque valeur)
  - Un même élément ne peut pas être utilisé deux fois.
  - target et les nombres : entiers décimaux "-?[0-9]+", dans [-10^18, 10^18].
  - Doit être en O(n) : il y a des entrées de 200 000 nombres.
  - Erreur (mauvais nombre d'args, target ou nombre invalide / hors bornes)
    -> message sur stderr, rien sur stdout, code de sortie 1.

Usage :
  python3 tester.py                 # teste les 5 langages
  python3 tester.py go zig          # seulement certains
  python3 tester.py -v python       # affiche le détail des échecs
"""

import os
import random
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BINARIES = {
    "python": ROOT / "bin" / "twosum-python",
    "lisp": ROOT / "bin" / "twosum-lisp",
    "zig": ROOT / "bin" / "twosum-zig",
    "ocaml": ROOT / "bin" / "twosum-ocaml",
    "go": ROOT / "bin" / "twosum-go",
}
TIMEOUT = 10
ENV = {**os.environ, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}
LIMIT = 10**18

GREEN, RED, YELLOW, BOLD, DIM, RESET = (
    ("\033[32m", "\033[31m", "\033[33m", "\033[1m", "\033[2m", "\033[0m")
    if sys.stdout.isatty()
    else ("",) * 6
)


# --------------------------------------------------------------------------- #
# Implémentation de référence
# --------------------------------------------------------------------------- #


def ref_two_sum(nums: list[int], target: int) -> tuple[int, int] | None:
    seen: dict[int, int] = {}
    for j, x in enumerate(nums):
        if target - x in seen:
            return seen[target - x], j
        seen.setdefault(x, j)
    return None


def ref_output(nums: list[int], target: int) -> str:
    res = ref_two_sum(nums, target)
    return "none\n" if res is None else f"{res[0]} {res[1]}\n"


# --------------------------------------------------------------------------- #
# Cas de test
# --------------------------------------------------------------------------- #


@dataclass
class Case:
    name: str
    args: list[str]
    stdin: str
    stdout: str | None  # None = cas d'erreur : stdout doit être vide
    code: int = 0


def ok(name, target, nums, expected=None, sep=" "):
    exp = ref_output(nums, target) if expected is None else expected + "\n"
    return Case(name, [str(target)], sep.join(map(str, nums)) + "\n", exp)


def raw(name, target, stdin, expected):
    return Case(name, [target], stdin, expected + "\n")


def err(name, args, stdin="1 2 3\n"):
    return Case(name, list(args), stdin, None, code=1)


def build_cases() -> dict[str, list[Case]]:
    rng = random.Random(42)

    # Sanity check de la référence
    assert ref_output([2, 7, 11, 15], 9) == "0 1\n"
    assert ref_output([5, 1, 5, 5], 10) == "0 2\n"

    normal = [
        ok("exemple classique", 9, [2, 7, 11, 15], "0 1"),
        ok("solution au milieu", 6, [3, 2, 4], "1 2"),
        ok("doublon", 6, [3, 3], "0 1"),
        ok("négatifs", -8, [-1, -2, -3, -4, -5], "2 4"),
        ok("négatif + positif", 0, [-3, 4, 3, 90], "0 2"),
        ok("zéros", 0, [0, 4, 3, 0], "0 3"),
        ok("solution à la fin", 19, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "8 9"),
        ok("deux éléments", 3, [1, 2], "0 1"),
    ]

    choice = [
        ok("plusieurs solutions : plus petit j", 5, [1, 2, 3, 4], "1 2"),
        ok("plusieurs solutions : plus petit i", 10, [5, 1, 5, 5], "0 2"),
        ok("que des 1", 2, [1, 1, 1, 1], "0 1"),
        ok("première occurrence gardée", 8, [4, 0, 4, 4], "0 2"),
        ok("j minimal avant i minimal", 7, [3, 1, 6, 4], "1 2"),
        ok("pas l'élément avec lui-même", 6, [3, 1, 3], "0 2"),
    ]

    none = [
        ok("aucune solution", 100, [1, 2, 3, 4], "none"),
        ok("un seul élément", 6, [3], "none"),
        raw("stdin vide", "5", "", "none"),
        raw("stdin que des blancs", "0", "  \n\t \n", "none"),
        ok("pas deux fois le même", 10, [5, 1, 2], "none"),
    ]

    fmt = [
        ok("séparés par newlines", 9, [2, 7, 11, 15], "0 1", sep="\n"),
        raw("tabs et espaces multiples", "9", "\t2   \t 7\n\n11 15", "0 1"),
        raw("sans newline final", "9", "2 7 11 15", "0 1"),
        raw("blancs au début", "9", "\n\n   2 7", "0 1"),
        raw("CRLF", "9", "2\r\n7\r\n", "0 1"),
        raw("zéros en tête", "10", "007 003", "0 1"),
        raw("-0", "0", "-0 0", "0 1"),
        raw("target -0", "-0", "5 -5", "0 1"),
        raw("target zéros en tête", "0009", "4 5", "0 1"),
    ]

    big = [
        ok("bornes ±10^18", 0, [LIMIT, -LIMIT], "0 1"),
        ok("target = 10^18", LIMIT, [LIMIT, 0], "0 1"),
        ok("target = -10^18", -LIMIT, [0, -LIMIT], "0 1"),
        ok("complément hors bornes", LIMIT, [-LIMIT, 5, 3], "none"),
        ok("grandes valeurs", LIMIT - 1, [5, LIMIT, -1], "1 2"),
    ]

    perf = []
    n = 200_000
    nums = rng.sample(range(-(10**12), 10**12), n)
    perf.append(ok("200k, solution à la fin", nums[-1] + nums[-2], nums))
    nums = list(range(0, 2 * n, 2))  # que des pairs
    perf.append(ok("200k, aucune solution", 1, nums, "none"))
    nums = [7] * n
    perf.append(ok("200k doublons", 14, nums, "0 1"))
    nums = [7] * n
    perf.append(ok("200k doublons, aucune solution", 15, nums, "none"))

    randomized = []
    for i in range(20):
        size = rng.randint(0, 40)
        nums = [rng.randint(-20, 20) for _ in range(size)]
        target = rng.randint(-30, 30)
        randomized.append(ok(f"aléatoire petit #{i}", target, nums))
    for i in range(5):
        nums = [rng.randint(-LIMIT, LIMIT) for _ in range(1000)]
        a, b = sorted(rng.sample(range(1000), 2))
        nums[a] = rng.randint(-LIMIT // 2, LIMIT // 2)
        nums[b] = rng.randint(-LIMIT // 2, LIMIT // 2)
        target = nums[a] + nums[b]
        randomized.append(ok(f"aléatoire grand #{i}", target, nums))

    errors = [
        err("aucun argument", []),
        err("trop d'arguments", ["9", "2"]),
        err("target non numérique", ["abc"]),
        err("target vide", [""]),
        err("target décimal", ["3.5"]),
        err("target '+3'", ["+3"]),
        err("target '-'", ["-"]),
        err("target '--3'", ["--3"]),
        err("target avec espace", [" 3"]),
        err("target 1e3", ["1e3"]),
        err("target hexadécimal", ["0x10"]),
        err("target chiffre arabe '٣'", ["٣"]),
        err("target > 10^18", [str(LIMIT + 1)]),
        err("target < -10^18", [str(-LIMIT - 1)]),
        err("target énorme", ["99999999999999999999999999"]),
        err("nombre non numérique", ["3"], "1 2 x 4\n"),
        err("nombre décimal", ["3"], "1 2.0 4\n"),
        err("nombre '+4'", ["5"], "1 +4\n"),
        err("nombre '-'", ["5"], "1 - 4\n"),
        err("nombre hexadécimal", ["5"], "0x1 4\n"),
        err("nombre séparé par virgules", ["5"], "1,4\n"),
        err("nombre > 10^18", ["5"], f"1 {LIMIT + 1}\n"),
        err("nombre < -10^18", ["5"], f"1 {-LIMIT - 1}\n"),
        err("nombre énorme", ["5"], "1 99999999999999999999999999\n"),
        err("nombre invalide après la solution", ["3"], "1 2 zzz\n"),
    ]

    return {
        "Cas normaux": normal,
        "Choix de la solution": choice,
        "Pas de solution": none,
        "Format d'entrée": fmt,
        "Grandes valeurs": big,
        "Performance (O(n))": perf,
        "Aléatoires": randomized,
        "Erreurs": errors,
    }


# --------------------------------------------------------------------------- #
# Exécution
# --------------------------------------------------------------------------- #


def short(s: str, n: int = 200) -> str:
    s = repr(s)
    return s if len(s) <= n else s[:n] + f"... ({len(s)} chars)"


def run_case(binary: Path, case: Case) -> str | None:
    """Renvoie None si OK, sinon un message d'erreur."""
    try:
        proc = subprocess.run(
            [str(binary), *case.args],
            input=case.stdin.encode(),
            capture_output=True,
            timeout=TIMEOUT,
            env=ENV,
        )
    except subprocess.TimeoutExpired:
        return f"timeout (> {TIMEOUT}s)"
    except OSError as e:
        return f"impossible de lancer: {e}"

    out = proc.stdout.decode("utf-8", errors="replace")
    errout = proc.stderr.decode("utf-8", errors="replace").strip()
    stderr_hint = (
        f"\n      stderr  : {short(errout.splitlines()[-1])}" if errout else ""
    )

    if proc.returncode != case.code:
        return f"code de sortie {proc.returncode}, attendu {case.code}{stderr_hint}"
    if case.code != 0:
        return f"stdout devrait être vide, obtenu {short(out)}" if out else None
    if out != case.stdout:
        return (
            f"attendu : {short(case.stdout)}\n      obtenu  : {short(out)}"
            + stderr_hint
        )
    return None


def test_language(
    lang: str, groups: dict[str, list[Case]], verbose: bool
) -> tuple[int, int]:
    binary = BINARIES[lang]
    total = sum(len(cases) for cases in groups.values())
    print(f"\n{BOLD}=== {lang} ==={RESET} {DIM}({binary.relative_to(ROOT)}){RESET}")

    if not binary.exists():
        print(f"  {YELLOW}binaire absent — lance `make`{RESET}")
        return 0, total

    passed = 0
    for group, cases in groups.items():
        good = 0
        failures = []
        for case in cases:
            msg = run_case(binary, case)
            if msg is None:
                good += 1
            else:
                failures.append((case, msg))
        passed += good
        color = GREEN if good == len(cases) else RED
        print(f"  {color}{good:>2}/{len(cases):<2}{RESET} {group}")
        shown = failures if verbose else failures[:3]
        for case, msg in shown:
            print(f"     {RED}✗{RESET} {case.name}")
            if verbose:
                print(
                    f"      {DIM}args    : {short(' '.join(map(repr, case.args)), 120)}{RESET}"
                )
                print(f"      {DIM}stdin   : {short(case.stdin, 120)}{RESET}")
                print(f"      {msg}")
        if len(shown) < len(failures):
            print(f"     {DIM}... et {len(failures) - len(shown)} autre(s){RESET}")
    return passed, total


def main() -> int:
    args = sys.argv[1:]
    verbose = "-v" in args
    langs = [a for a in args if a != "-v"] or list(BINARIES)
    unknown = [lang for lang in langs if lang not in BINARIES]
    if unknown:
        print(
            f"langage(s) inconnu(s): {', '.join(unknown)} "
            f"(choix: {', '.join(BINARIES)})",
            file=sys.stderr,
        )
        return 2

    groups = build_cases()
    results = {lang: test_language(lang, groups, verbose) for lang in langs}

    print(f"\n{BOLD}=== Résumé ==={RESET}")
    for lang, (passed, total) in results.items():
        color = GREEN if passed == total else RED
        print(f"  {lang:<8} {color}{passed:>3}/{total}{RESET}")
    if not verbose and any(p != t for p, t in results.values()):
        print(f"{DIM}(relance avec -v pour voir le détail des échecs){RESET}")
    return 0 if all(p == t for p, t in results.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
