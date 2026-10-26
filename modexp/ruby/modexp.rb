#!/usr/bin/env ruby

# Exponentiation modulaire rapide: calcule (base^exponent) % modulus en O(log exponent)

LIMIT = 1_000_000_000_000_000_000  # 10^18

def mod_exp(base, exponent, modulus)
  result = 1
  while exponent > 0
    if (exponent & 1) > 0
      result = (result * base) % modulus
    end
    exponent = exponent >> 1
    base = (base * base) % modulus
  end
  result
end

def die(msg)
  STDERR.puts("error: #{msg}")
  STDERR.puts("usage: modexp <base> <exponent> <modulus>")
  exit(1)
end

def parse_int(s)
  if /\A-?\d+\z/.match?(s)
    n = s.to_i
    if n.abs > LIMIT
      die("number out of range")
    end
    n
  else
    die("invalid number")
  end
end

argv = ARGV
if argv.length != 3
  die("wrong number of arguments")
end

base = parse_int(argv[0])
exponent = parse_int(argv[1])
modulus = parse_int(argv[2])

if exponent < 0
  die("exponent must be non-negative")
end

if modulus == 0
  die("modulus must be non-zero")
end

result = mod_exp(base, exponent, modulus)
puts(result)
