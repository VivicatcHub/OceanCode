#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define LIMIT 1000000000000000000LL  /* 10^18 */

/* Exponentiation modulaire rapide: calcule (base^exponent) % modulus en O(log exponent). */

long long mod_exp(long long base, long long exponent, long long modulus) {
    /* Utilise l'algorithme d'exponentiation rapide (binary exponentiation).
       exponent doit être positif ou nul. */
    /* TODO */
    return -1;  /* placeholder */
}

void die(const char *msg) {
    fprintf(stderr, "error: %s\n", msg);
    fprintf(stderr, "usage: modexp <base> <exponent> <modulus>\n");
    exit(1);
}

long long parse_int(const char *s) {
    char *end;

    if (*s == '\0' || (s[0] == '-' && s[1] == '\0')) {
        die("invalid number");
    }

    long long n = strtoll(s, &end, 10);
    if (*end != '\0') {
        die("invalid number");
    }
    if (n > LIMIT || n < -LIMIT) {
        die("number out of range");
    }
    return n;
}

int main(int argc, char *argv[]) {
    if (argc != 4) {
        die("wrong number of arguments");
    }

    long long base = parse_int(argv[1]);
    long long exponent = parse_int(argv[2]);
    long long modulus = parse_int(argv[3]);

    if (exponent < 0) {
        die("exponent must be non-negative");
    }
    if (modulus == 0) {
        die("modulus must be non-zero");
    }

    long long result = mod_exp(base, exponent, modulus);
    printf("%lld\n", result);

    return 0;
}
