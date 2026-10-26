// Chiffrement de César + déchiffrement par force brute.

use std::env;
use std::process;

const USAGE: &str = "usage:
  caesar encrypt <shift> <text>
  caesar decrypt <text>";

/// Décale chaque lettre ASCII (a-z, A-Z) de `shift` positions.
fn encrypt(text: &str, shift: i64) -> String {
    let mut result = String::from("");
    let shift = shift.rem_euclid(26);

    for c in text.chars() {
        if 'a' as i64 <= c as i64 && c as i64 <= 'z' as i64 {
            let v = ((c as i64 - 'a' as i64) + shift as i64) % 26;
            let value: i64;
            if v < 0 {
                value = v + 26 + 'a' as i64;
            } else {
                value = v + 'a' as i64;
            }
            result.push_str(value as u8 as char);
        } else if 'A' as i64 <= c as i64 && c as i64 <= 'Z' as i64 {
            let v = ((c as i64 - 'A' as i64) + shift as i64) % 26;
            let value: i64;
            if v < 0 {
                value = v + 26 + 'A' as i64;
            } else {
                value = v + 'A' as i64;
            }
            result.push_str(value as u8 as char);
        } else {
            result.push(c);
        }
    }
    return result;
}

/// Force brute : renvoie les 26 candidats, l'élément k étant le texte
/// déchiffré en supposant un décalage de k.
fn decrypt(text: &str) -> Vec<String> {
    let mut vec = Vec::new();
    for i in 0..26 {
        vec.push(encrypt(text, -i));
    }
    return vec;
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
