from coin_utils.elliptic_curves import *
from coin_utils.fields import *

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
