#!/usr/bin/env python3
"""Tester commun pour les 5 implémentations d'exponentiation modulaire rapide.

Spécification testée :
  modexp <base> <exponent> <modulus>    -> (base^exponent) % modulus

  - Doit utiliser l'algorithme d'exponentiation rapide (O(log exponent)).
  - exponent doit être positif ou nul.
  - modulus doit être non-zéro.
  - base, exponent, modulus : entiers décimaux "-?[0-9]+", dans [-10^18, 10^18].
  - Erreur (mauvais nombre d'args, nombre invalide / hors bornes, exponent négatif, modulus zéro)
    -> message sur stderr, rien sur stdout, code de sortie 1.

Usage :
  python3 tester.py                 # teste les 5 langages
  python3 tester.py python rust     # seulement certains
  python3 tester.py -v c            # affiche le détail des échecs
"""

import os
import random
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BINARIES = {
    "python": ROOT / "bin" / "modexp-python",
    "c": ROOT / "bin" / "modexp-c",
    "elixir": ROOT / "bin" / "modexp-elixir",
    "rust": ROOT / "bin" / "modexp-rust",
    "ruby": ROOT / "bin" / "modexp-ruby",
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


def ref_mod_exp(base: int, exponent: int, modulus: int) -> int:
    """Utilise pow(base, exponent, modulus) de Python qui implémente l'algo rapide."""
    return pow(base, exponent, modulus)


# --------------------------------------------------------------------------- #
# Cas de test
# --------------------------------------------------------------------------- #


@dataclass
class Case:
    name: str
    args: list[str]
    stdout: str | None  # None = cas d'erreur : stdout doit être vide
    code: int = 0


def ok(name, base, exponent, modulus, expected=None):
    exp = ref_mod_exp(base, exponent, modulus) if expected is None else expected
    return Case(name, [str(base), str(exponent), str(modulus)], f"{exp}\n")


def err(name, *args):
    return Case(name, list(args), None, code=1)


def build_cases() -> dict[str, list[Case]]:
    rng = random.Random(42)

    # Sanity check de la référence
    assert ref_mod_exp(2, 10, 1000) == 24
    assert ref_mod_exp(3, 5, 7) == 5

    normal = [
        ok("2^10 % 1000", 2, 10, 1000, 24),
        ok("3^5 % 7", 3, 5, 7, 5),
        ok("7^6 % 13", 7, 6, 13, 12),
        ok("123^456 % 789", 123, 456, 789),
        ok("exponent = 0", 5, 0, 7, 1),
        ok("exponent = 1", 5, 1, 7, 5),
        ok("base = 0", 0, 5, 7, 0),
        ok("base = 1", 1, 100, 7, 1),
        ok("base = modulus", 7, 3, 7, 0),
        ok("base > modulus", 15, 2, 7, 1),
        ok("base négatif", -2, 5, 7, 3),
        ok("base = -1", -1, 100, 7, 1),
        ok("base = -1, exp impair", -1, 5, 7, 6),
        ok("modulus = 1", 5, 10, 1, 0),
        ok("modulus = 2", 3, 7, 2, 1),
    ]

    shifts = [
        ok("exponent énorme", 2, 1_000_000_000_000, 1_000_000_007),
        ok("base énorme", LIMIT, 2, LIMIT - 1),
        ok("modulus énorme", 123, 456, LIMIT),
        ok("tous énormes", LIMIT - 1, 999, LIMIT - 2),
        ok("négatif énorme", -LIMIT, 3, LIMIT),
        ok("2^53 % 1000000007", 2, 9_007_199_254_740_992, 1_000_000_007),
    ]

    crypto = [
        # Quelques tests inspirés de cryptographie (RSA-like)
        ok("petit RSA-like", 7, 13, 143),  # 7^13 % (11*13)
        ok("exponentiation rapide vs lente", 2, 30, 1_000_000_007),
        ok("fermat petit théorème", 2, 1_000_000_006, 1_000_000_007, 1),
    ]

    special = [
        ok("base 0, exp 0, mod 5", 0, 0, 5, 1),
        ok("base négatif petit", -3, 4, 5, 1),
        ok("base négatif, exp 0", -5, 0, 7, 1),
        ok("base = -(modulus)", -7, 2, 7, 0),
        ok("base = -(modulus-1)", -6, 3, 7, 1),
    ]

    randomized = []
    for i in range(10):
        base = rng.randint(-1000, 1000)
        exponent = rng.randint(0, 500)
        modulus = rng.randint(1, 10000)
        randomized.append(ok(f"aléatoire #{i}", base, exponent, modulus))

    errors = [
        err("aucun argument"),
        err("un argument", "2"),
        err("deux arguments", "2", "10"),
        err("quatre arguments", "2", "10", "1000", "extra"),
        err("base non numérique", "abc", "10", "7"),
        err("exponent non numérique", "2", "abc", "7"),
        err("modulus non numérique", "2", "10", "abc"),
        err("base décimal", "2.5", "10", "7"),
        err("exponent décimal", "2", "10.5", "7"),
        err("modulus décimal", "2", "10", "7.5"),
        err("exponent négatif", "2", "-10", "7"),
        err("modulus = 0", "2", "10", "0"),
        err("base > limite", str(LIMIT + 1), "2", "7"),
        err("base < -limite", str(-LIMIT - 1), "2", "7"),
        err("exponent > limite", "2", str(LIMIT + 1), "7"),
        err("modulus > limite", "2", "10", str(LIMIT + 1)),
    ]

    return {
        "Cas normaux": normal,
        "Cas limite (grands nombres)": shifts,
        "Cryptographie": crypto,
        "Cas spéciaux": special,
        "Aléatoires": randomized,
        "Erreurs": errors,
    }


# --------------------------------------------------------------------------- #
# Exécution
# --------------------------------------------------------------------------- #


def short(s: str, n: int = 200) -> str:
    s = repr(s)
    return s if len(s) <= n else s[:n] + f"... ({len(s)} chars)"


def first_diff(expected: str, got: str) -> str:
    exp_lines, got_lines = expected.splitlines(True), got.splitlines(True)
    for i, (e, g) in enumerate(zip(exp_lines, got_lines)):
        if e != g:
            return f"ligne {i + 1}:\n      attendu : {short(e)}\n      obtenu  : {short(g)}"
    return (
        f"nombre de lignes: attendu {len(exp_lines)}, obtenu {len(got_lines)}\n"
        f"      attendu : {short(expected)}\n      obtenu  : {short(got)}"
    )


def run_case(binary: Path, case: Case) -> str | None:
    """Renvoie None si OK, sinon un message d'erreur."""
    try:
        proc = subprocess.run(
            [str(binary), *case.args], capture_output=True, timeout=TIMEOUT, env=ENV
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
        return first_diff(case.stdout, out) + stderr_hint
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
        ok = 0
        failures = []
        for case in cases:
            msg = run_case(binary, case)
            if msg is None:
                ok += 1
            else:
                failures.append((case, msg))
        passed += ok
        color = GREEN if ok == len(cases) else RED
        print(f"  {color}{ok:>2}/{len(cases):<2}{RESET} {group}")
        shown = failures if verbose else failures[:3]
        for case, msg in shown:
            print(f"     {RED}✗{RESET} {case.name}")
            if verbose:
                print(
                    f"      {DIM}args    : {short(' '.join(map(repr, case.args)), 120)}{RESET}"
                )
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
