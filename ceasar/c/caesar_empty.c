/* Chiffrement de César + déchiffrement par force brute. */

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define NB_SHIFTS 26

static const char *USAGE =
    "usage:\n"
    "  caesar encrypt <shift> <text>\n"
    "  caesar decrypt <text>\n";

/* Décale chaque lettre ASCII (a-z, A-Z) de `shift` positions.
 * `out` est déjà alloué (strlen(in) + 1 octets, rempli de zéros). */
void caesar_encrypt(const char *in, char *out, long long shift)
{
    (void)in;
    (void *)out;
    (void)shift;
    return;
}

/* Force brute : remplit les 26 candidats, out[k] étant le texte déchiffré
 * en supposant un décalage de k.
 * Chaque out[k] est déjà alloué (strlen(in) + 1 octets, rempli de zéros). */
void caesar_decrypt(const char *in, char *out[NB_SHIFTS])
{
    (void)in;
    (void *)out;
    return;
}

static void die(const char *msg, const char *arg)
{
    fprintf(stderr, "error: %s", msg);
    if (arg)
        fprintf(stderr, " '%s'", arg);
    fprintf(stderr, "\n%s", USAGE);
    exit(1);
}

static long long parse_shift(const char *s)
{
    const char *p = (*s == '-') ? s + 1 : s;

    if (*p == '\0')
        die("invalid shift", s);
    for (; *p; p++)
        if (*p < '0' || *p > '9')
            die("invalid shift", s);

    errno = 0;
    long long shift = strtoll(s, NULL, 10);
    if (errno == ERANGE)
        die("shift out of range", s);
    return shift;
}

static char *alloc_like(const char *s)
{
    char *buf = calloc(strlen(s) + 1, 1);
    if (!buf)
    {
        perror("calloc");
        exit(1);
    }
    return buf;
}

int main(int argc, char **argv)
{
    if (argc < 2)
        die("missing command", NULL);
    const char *cmd = argv[1];

    if (strcmp(cmd, "encrypt") == 0)
    {
        if (argc != 4)
            die("wrong number of arguments", NULL);
        long long shift = parse_shift(argv[2]);
        const char *text = argv[3];
        char *out = alloc_like(text);
        caesar_encrypt(text, out, shift);
        printf("%s\n", out);
        free(out);
    }
    else if (strcmp(cmd, "decrypt") == 0)
    {
        if (argc != 3)
            die("wrong number of arguments", NULL);
        const char *text = argv[2];
        char *out[NB_SHIFTS];
        for (int k = 0; k < NB_SHIFTS; k++)
            out[k] = alloc_like(text);
        caesar_decrypt(text, out);
        for (int k = 0; k < NB_SHIFTS; k++)
        {
            printf("%d: %s\n", k, out[k]);
            free(out[k]);
        }
    }
    else
    {
        die("unknown command", cmd);
    }
    return 0;
}
