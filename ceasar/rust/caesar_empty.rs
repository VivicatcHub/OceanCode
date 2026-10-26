// Chiffrement de César + déchiffrement par force brute.

use std::env;
use std::process;

const USAGE: &str = "usage:
  caesar encrypt <shift> <text>
  caesar decrypt <text>";

/// Décale chaque lettre ASCII (a-z, A-Z) de `shift` positions.
#[allow(unused_variables)]
fn encrypt(text: &str, shift: i64) -> String {
    todo!("encrypt")
}

/// Force brute : renvoie les 26 candidats, l'élément k étant le texte
/// déchiffré en supposant un décalage de k.
#[allow(unused_variables)]
fn decrypt(text: &str) -> Vec<String> {
    todo!("decrypt")
}

fn die(msg: &str) -> ! {
    eprintln!("error: {msg}");
    eprintln!("{USAGE}");
    process::exit(1)
}

fn parse_shift(s: &str) -> i64 {
    let digits = s.strip_prefix('-').unwrap_or(s);
    if digits.is_empty() || !digits.bytes().all(|b| b.is_ascii_digit()) {
        die(&format!("invalid shift '{s}'"));
    }
    s.parse()
        .unwrap_or_else(|_| die(&format!("shift out of range '{s}'")))
}

fn main() {
    let args: Vec<String> = env::args().skip(1).collect();
    let args: Vec<&str> = args.iter().map(String::as_str).collect();

    match args.as_slice() {
        ["encrypt", shift, text] => println!("{}", encrypt(text, parse_shift(shift))),
        ["decrypt", text] => {
            for (k, candidate) in decrypt(text).iter().enumerate() {
                println!("{k}: {candidate}");
            }
        }
        [] => die("missing command"),
        ["encrypt" | "decrypt", ..] => die("wrong number of arguments"),
        [cmd, ..] => die(&format!("unknown command '{cmd}'")),
    }
}
