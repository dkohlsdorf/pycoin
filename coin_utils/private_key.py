from coin_utils.signatures import *
from coin_utils.secp256k1 import SECP256_G, SECP256_N
from random import randint

class PrivateKey:

    def __init__(self, secret):
        self.secret = secret
        self.point = secret * SECP256_G

    def hex(self):
        return '{:x}'.format(self.secret).zfill(64)

    def sign(self, z):
        k = randint(0, SECP256_N)
        r = (k * SECP256_G).x.num
        k_inv = pow(k, SECP256_N - 2, SECP256_N)
        s = (z + r * self.secret) * k_inv % SECP256_N
        if s < SECP256_N / 2:
            s = SECP256_N - s
        return Signature(r, s)