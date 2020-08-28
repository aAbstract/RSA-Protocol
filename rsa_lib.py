import random
import numpy as np


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


def get_mod_inv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('[ERROR]: MODULAR INVERSE IS NOT EXIST!')
    else:
        return x % m


def gen_keypair(p, q):
    n = p * q
    phi = (p-1) * (q-1)
    e = random.randrange(1, phi)
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)
    d = get_mod_inv(e, phi)
    return (e, n), (d, n)


def encrypt(pk, plaintext):
    key, n = pk
    cipher = [pow(ord(char), key) % n for char in plaintext]
    return cipher


def decrypt(pk, ciphertext):
    key, n = pk
    plain = [chr(pow(char, key) % n) for char in ciphertext]
    return ''.join(plain)


def get_rand_mills_prime(seed):
    mu = np.float128(1.3063778838630806904686144926026057129167845851567136443680537599664340537668)
    p = np.floor(np.power(mu, np.power(3, seed)))
    return int(p)