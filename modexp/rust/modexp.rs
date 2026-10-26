// Exponentiation modulaire rapide: calcule (base^exponent) % modulus en O(log exponent)

const LIMIT: i64 = 1_000_000_000_000_000_000; // 10^18

fn p_modulo(a: i128, b: i128) -> i128 {
    return (a % b + b) % b;
}

fn mod_exp(base: i64, exponent: i64, modulus: i64) -> i64 {
    let mut result: i128 = 1;
    let mut b: i128 = base as i128;
    let mut e: i128 = exponent as i128;

    while e > 0 {
        if (e & 1) > 0 {
            result = p_modulo(result, modulus as i128);
            result = p_modulo(result * b, modulus as i128);
        }
        e = e >> 1;
        b = p_modulo(b, modulus as i128);
        b = p_modulo(b * b, modulus as i128);
    }
    result as i64
}

fn die(msg: &str) -> ! {
    eprintln!("error: {}", msg);
    eprintln!("usage: modexp <base> <exponent> <modulus>");
    std::process::exit(1);
}

fn parse_int(s: &str) -> i64 {
    match s.parse::<i64>() {
        Ok(n) => {
            if n.abs() > LIMIT {
                die("number out of range");
            }
            n
        }
        Err(_) => die("invalid number"),
    }
}

fn main() {
    let args: Vec<String> = std::env::args().collect();

    if args.len() != 4 {
        die("wrong number of arguments");
    }

    let base = parse_int(&args[1]);
    let exponent = parse_int(&args[2]);
    let modulus = parse_int(&args[3]);

    if exponent < 0 {
        die("exponent must be non-negative");
    }
    if modulus == 0 {
        die("modulus must be non-zero");
    }

    let result = mod_exp(base, exponent, modulus);
    println!("{}", result);
}
