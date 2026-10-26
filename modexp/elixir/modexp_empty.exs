#!/usr/bin/env elixir

# Exponentiation modulaire rapide: calcule (base^exponent) % modulus en O(log exponent)

defmodule ModExp do
  def mod_exp(_base, _exponent, _modulus) do
    # TODO: Utilise l'algorithme d'exponentiation rapide (binary exponentiation)
    # exponent doit être positif ou nul
    raise "Not implemented"
  end
end

defmodule Main do
  @limit 1_000_000_000_000_000_000

  def die(msg) do
    IO.puts(:stderr, "error: #{msg}")
    IO.puts(:stderr, "usage: modexp <base> <exponent> <modulus>")
    System.halt(1)
  end

  def parse_int(s) do
    case Integer.parse(s) do
      {n, ""} ->
        if abs(n) > @limit do
          die("number out of range")
        else
          n
        end
      _ ->
        die("invalid number")
    end
  end

  def main(argv) do
    if length(argv) != 3 do
      die("wrong number of arguments")
    end

    [base_s, exponent_s, modulus_s] = argv
    base = parse_int(base_s)
    exponent = parse_int(exponent_s)
    modulus = parse_int(modulus_s)

    if exponent < 0 do
      die("exponent must be non-negative")
    end

    if modulus == 0 do
      die("modulus must be non-zero")
    end

    result = ModExp.mod_exp(base, exponent, modulus)
    IO.puts(result)
  end
end

Main.main(System.argv())
