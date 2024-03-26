import random

def main():
    # Taking input for prime number n and primitive root g
    n = int(input("Enter a prime number (n): "))
    g = int(input("Enter a primitive root of n (g): "))

    # A's side
    a = random.randint(1, n - 1)  # Random private number selected by A
    print("A selected (a):", a)
    ga = mod_pow(g, a, n)  # A's public value
    print("A published (ga):", ga)

    # B's side
    b = random.randint(1, n - 1)  # Random private number selected by B
    print("B selected (b):", b)
    gb = mod_pow(g, b, n)  # B's public value
    print("B published (gb):", gb)

    # C's side
    c = random.randint(1, n - 1)  # Random private number selected by C for A
    d = random.randint(1, n - 1)  # Random private number selected by C for B
    print("C selected private number for A (c):", c)
    print("C selected private number for B (d):", d)
    gea = mod_pow(g, c, n)  # C's public value for A
    geb = mod_pow(g, d, n)  # C's public value for B
    print("C published value for A (gc):", gea)
    print("C published value for B (gd):", geb)

    # Computing secret key
    sa = mod_pow(geb, a, n)  # A's computed secret key
    sb = mod_pow(gea, b, n)  # B's computed secret key
    sea = mod_pow(gea, a, n)  # C's computed secret key for A
    seb = mod_pow(geb, b, n)  # C's computed secret key for B
    print("A computed (S1):", sa)
    print("B computed (S2):", sb)
    print("C computed key for A (S1):", sea)
    print("C computed key for B (S2):", seb)

# Method to compute (base^exponent) % modulus efficiently
def mod_pow(base, exponent, modulus):
    result = 1
    base %= modulus
    while exponent > 0:
        if exponent & 1:
            result = (result * base) % modulus
        exponent >>= 1
        base = (base * base) % modulus
    return result

if __name__ == "__main__":
    main()
