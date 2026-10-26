#!/usr/bin/env node
// Chiffrement de César + déchiffrement par force brute.
"use strict";

const USAGE = `usage:
  caesar encrypt <shift> <text>
  caesar decrypt <text>`;

/** Décale chaque lettre ASCII (a-z, A-Z) de `shift` positions. */
function encrypt(text, shift) {
  // TODO
  throw new Error("TODO: encrypt");
}

/**
 * Force brute : renvoie les 26 candidats, l'élément k étant le texte
 * déchiffré en supposant un décalage de k.
 */
function decrypt(text) {
  // TODO
  throw new Error("TODO: decrypt");
}

function die(msg) {
  process.stderr.write(`error: ${msg}\n${USAGE}\n`);
  process.exit(1);
}

function parseShift(s) {
  if (!/^-?[0-9]+$/.test(s)) die(`invalid shift '${s}'`);
  const shift = Number(s);
  if (!Number.isSafeInteger(shift)) die(`shift out of range '${s}'`);
  return shift;
}

function main(argv) {
  if (argv.length === 0) die("missing command");
  const [cmd, ...args] = argv;

  if (cmd === "encrypt") {
    if (args.length !== 2) die("wrong number of arguments");
    process.stdout.write(encrypt(args[1], parseShift(args[0])) + "\n");
  } else if (cmd === "decrypt") {
    if (args.length !== 1) die("wrong number of arguments");
    const lines = decrypt(args[0]).map(
      (candidate, k) => `${k}: ${candidate}\n`,
    );
    process.stdout.write(lines.join(""));
  } else {
    die(`unknown command '${cmd}'`);
  }
}

main(process.argv.slice(2));
