#!/usr/bin/env python3
"""Tester commun pour les 5 implémentations du chiffre de César.

Spécification testée :
  caesar encrypt <shift> <text>   -> texte chiffré + "\\n"
  caesar decrypt <text>           -> force brute : 26 lignes "k: <candidat>", k = 0..25,
                                     où <candidat> = text déchiffré avec un décalage k
                                     (c.-à-d. encrypt(text, -k))

  - Seules les lettres ASCII a-z / A-Z sont décalées, la casse est conservée.
  - Tout le reste (chiffres, ponctuation, espaces, accents, emoji, \\n...) est inchangé.
  - shift est un entier signé quelconque (64 bits) : négatif, >= 26, énorme...
  - Erreur d'usage (commande inconnue, mauvais nombre d'args, shift invalide)
    -> message sur stderr, rien sur stdout, code de sortie 1.

Usage :
  python3 tester.py                 # teste les 5 langages
  python3 tester.py c rust          # seulement certains
  python3 tester.py -v python       # affiche le détail des échecs
"""

import os
import random
import string
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BINARIES = {
    "python": ROOT / "bin" / "caesar-python",
    "c": ROOT / "bin" / "caesar-c",
    "rust": ROOT / "bin" / "caesar-rust",
    "haskell": ROOT / "bin" / "caesar-haskell",
    "js": ROOT / "bin" / "caesar-js",
}
TIMEOUT = 10
ENV = {**os.environ, "LANG": "C.UTF-8", "LC_ALL": "C.UTF-8"}

GREEN, RED, YELLOW, BOLD, DIM, RESET = (
    ("\033[32m", "\033[31m", "\033[33m", "\033[1m", "\033[2m", "\033[0m")
    if sys.stdout.isatty()
    else ("",) * 6
)


# --------------------------------------------------------------------------- #
# Implémentation de référence
# --------------------------------------------------------------------------- #


def ref_encrypt(text: str, shift: int) -> str:
    out = []
    for c in text:
        if "a" <= c <= "z":
            out.append(chr((ord(c) - ord("a") + shift) % 26 + ord("a")))
        elif "A" <= c <= "Z":
            out.append(chr((ord(c) - ord("A") + shift) % 26 + ord("A")))
        else:
            out.append(c)
    return "".join(out)


def ref_decrypt(text: str) -> str:
    return "".join(f"{k}: {ref_encrypt(text, -k)}\n" for k in range(26))


# --------------------------------------------------------------------------- #
# Cas de test
# --------------------------------------------------------------------------- #


@dataclass
class Case:
    name: str
    args: list[str]
    stdout: str | None  # None = cas d'erreur : stdout doit être vide
    code: int = 0


def enc(name, shift, text, expected=None):
    exp = ref_encrypt(text, shift) if expected is None else expected
    return Case(name, ["encrypt", str(shift), text], exp + "\n")


def dec(name, text):
    return Case(name, ["decrypt", text], ref_decrypt(text))


def err(name, *args):
    return Case(name, list(args), None, code=1)


def build_cases() -> dict[str, list[Case]]:
    rng = random.Random(42)
    accents = "Ça va très bien, ÉLÈVE ñ ß Œuvre — 日本語 🎉👍🏽"
    boundaries = "@AZ[ `az{"  # caractères juste avant/après A-Z et a-z
    printable = string.ascii_letters + string.digits + string.punctuation + " "
    long_text = "".join(rng.choice(printable) for _ in range(100_000))
    mid_text = "".join(rng.choice(printable + "éàüç") for _ in range(20_000))

    # Sanity check de la référence sur un cas connu : la ligne 3 est le clair.
    assert "3: Hello, World!\n" in ref_decrypt("Khoor, Zruog!")

    normal = [
        enc("encrypt simple", 3, "abc", "def"),
        enc("encrypt phrase", 3, "Hello, World!", "Khoor, Zruog!"),
        enc("wrap minuscules", 1, "xyz", "yza"),
        enc("wrap majuscules", 3, "XYZ", "ABC"),
        enc(
            "ROT13",
            13,
            "Why did the chicken cross the road?",
            "Jul qvq gur puvpxra pebff gur ebnq?",
        ),
        enc("alphabet complet", 7, string.ascii_lowercase + string.ascii_uppercase),
        dec("decrypt simple", "Khoor"),
        dec("decrypt phrase", "Khoor, Zruog!"),
        dec("decrypt pangramme", "Wkh txlfn eurzq ira mxpsv ryhu wkh odcb grj."),
        dec("decrypt ROT13", "Jul qvq gur puvpxra pebff gur ebnq?"),
        dec("decrypt casse mixte", "AbCdEfGhIjKlMnOpQrStUvWxYz"),
    ]

    shifts = [
        enc("shift 0", 0, "Inchangé ?"),
        enc("shift 26", 26, "Tour complet"),
        enc("shift 52", 52, "Deux tours"),
        enc("shift 25", 25, "Presque un tour"),
        enc("shift -1", -1, "abc ABC", "zab ZAB"),
        enc("shift -27", -27, "abc ABC", "zab ZAB"),
        enc("shift -26", -26, "abc ABC", "abc ABC"),
        enc("shift énorme", 1_000_000_000_003, "Hello"),
        enc("shift énorme négatif", -1_000_000_000_003, "Hello"),
        enc("shift 2^53-1", 9_007_199_254_740_991, "Big Shift"),
        Case("shift -0", ["encrypt", "-0", "abc"], "abc\n"),
    ]

    tricky_text = [
        enc("texte vide", 5, "", ""),
        enc("que de la ponctuation", 4, "1234 !?.,;:()[]{}<>/\\|~^#&*"),
        enc("bornes ASCII @[`{", 1, boundaries, "@BA[ `ba{"),
        enc("bornes ASCII shift négatif", -1, boundaries, "@ZY[ `zy{"),
        enc("accents / unicode", 3, accents),
        enc("espaces multiples", 2, "  a   b  ", "  c   d  "),
        enc("newline et tab", 1, "ab\ncd\tef\r\n", "bc\nde\tfg\r\n"),
        enc("texte qui ressemble à une option", 1, "-abc", "-bcd"),
        enc("texte = --help", 1, "--help", "--ifmq"),
        enc("shift négatif + texte en '-'", -1, "-5 apples", "-5 zookdr"),
        enc("texte qui est un nombre", 3, "42", "42"),
        enc("long texte (100k)", 17, long_text),
        dec("decrypt vide", ""),
        dec("decrypt sans lettres", "123 !?"),
        dec("decrypt bornes ASCII", boundaries),
        dec("decrypt accents / unicode", accents),
        dec("decrypt texte en '-'", "-abc"),
        dec("decrypt texte = --help", "--help"),
        dec("decrypt long texte (20k)", mid_text),
    ]

    randomized = []
    for i in range(10):
        plain = "".join(rng.choice(printable) for _ in range(rng.randint(1, 80)))
        shift = rng.randint(-(10**6), 10**6)
        randomized.append(enc(f"aléatoire encrypt #{i}", shift, plain))
        randomized.append(dec(f"aléatoire decrypt #{i}", ref_encrypt(plain, shift)))

    errors = [
        err("aucun argument"),
        err("commande inconnue", "rot13", "abc"),
        err("ancienne commande bruteforce", "bruteforce", "abc"),
        err("commande en majuscules", "ENCRYPT", "3", "abc"),
        err("encrypt sans texte", "encrypt", "3"),
        err("encrypt sans rien", "encrypt"),
        err("encrypt trop d'args", "encrypt", "3", "abc", "def"),
        err("decrypt sans texte", "decrypt"),
        err("decrypt avec un shift", "decrypt", "3", "abc"),
        err("shift non numérique", "encrypt", "abc", "hello"),
        err("shift vide", "encrypt", "", "hello"),
        err("shift décimal", "encrypt", "3.5", "hello"),
        err("shift '12abc'", "encrypt", "12abc", "hello"),
        err("shift '-'", "encrypt", "-", "hello"),
        err("shift '--3'", "encrypt", "--3", "hello"),
        err("shift avec espace", "encrypt", " 3", "hello"),
        err("shift notation 1e3", "encrypt", "1e3", "hello"),
        err("shift hexadécimal", "encrypt", "0x10", "hello"),
        err("shift chiffre arabe '٣'", "encrypt", "٣", "hello"),
    ]

    return {
        "Cas normaux": normal,
        "Shifts limites": shifts,
        "Textes piégeux": tricky_text,
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
