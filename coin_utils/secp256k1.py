from coin_utils.elliptic_curves import *
from coin_utils.fields import *
from coin_utils.signatures import * 


# Parameters of the finite field and the elliptic curve
SECP256_PRIME = 2 ** 256 - 2 ** 32 - 977
SECP256_A = 0
SECP256_B = 7
SECP256_N = 0xfffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364141


class S256Field(FieldElement):

    def __init__(self, num, prime=None):
        super().__init__(num = num, prime=SECP256_PRIME)

    def __repr__(self):
        return '{:x}'.format(self.num).zfill(64)


class S256Point(Point):

    def __init__(self, x, y, a = None, b = None):
        a, b = S256Field(SECP256_A), S256Field(SECP256_B)
        if type(x) == int:
            x, y = S256Field(x), S256Field(y)
        super().__init__(x,y,a,b)        
        
    def __rmul__(self, coefficient):        
        return super().__rmul__(coefficient % SECP256_N) # cycle early        

    def __repr__(self):
        if self.x is None:
            return 'S256Point(infinity)'
        else:
            return 'S256Point({}, {})'.format(self.x, self.y)

    def verify(self, signature_hash, signature):
        # self represents public key
        s_inverted = pow(signature.s, SECP256_N - 2, SECP256_N)
        u = signature_hash * s_inverted % SECP256_N
        v = signature.r * s_inverted % SECP256_N
        total = u * SECP256_G + v * self
        return total.x.num == signature.r


SECP256_G = S256Point(
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
) 