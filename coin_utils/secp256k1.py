from coin_utils.elliptic_curves import *
from coin_utils.fields import *
from coin_utils.signatures import * 
from coin_utils.utils import * 


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

    def sqrt(self):
        return self ** ((SECP256_PRIME + 1) // 4)


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

    def sec(self, compressed = True):
        if compressed:
            if self.y.num % 2 == 0:
                return b'\x02' \
                    + self.x.num.to_bytes(32, 'big')                
            else:
                return b'\x03' \
                    + self.x.num.to_bytes(32, 'big')
        return b'\x04{}{}' \
            + self.x.num.to_bytes(32, 'big') \
            + self.y.num.to_bytes(32, 'big')
        
    def address(self, compressed=True, testnet=False):
        h160 = hash160(self.sec(compressed))
        if testnet:
            prefix = b'\x6f'
        else:
            prefix = b'x00'
        return encode_base58_checksum(prefix + h160)

    @classmethod
    def parse(self, sec_bin):
        if sec_bin[0] == 4:
            x = int.from_bytes(sec_bin[1:33],  'big')
            y = int.from_bytes(sec_bin[33:65], 'big')
            return S256Point(x=x,y=y)
        is_even = sec_bin[0] == 2
        x = S256Field(int.from_bytes(sec_bin[1:], 'big'))
        alpha = x**3 + S256Field(SECP256_B)
        beta = alpha.sqrt()        
        if beta.num % 2 == 0:
            even_beta = beta
            odd_beta = S256Field(SECP256_PRIME - beta.num)
        else:
            even_beta = S256Field(SECP256_PRIME - beta.num)
            odd_beta = beta
        if is_even:
            return S256Point(x, even_beta)
        else:
            return S256Point(x, odd_beta)


SECP256_G = S256Point(
    0x79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798, 
    0x483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8
) 