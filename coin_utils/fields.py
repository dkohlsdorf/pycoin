

class FieldElement:
    '''
    Implements elements in a finite field

    A finite set is:
      1: Closed: If a and b are in the set, a + b and a ⋅ b are in the set.   
      2: Additive Identity: 0 exists and has the property a + 0 = a.
      3: Multiplicative Identity: 1 exists and has the property a ⋅ 1 = a. 
      4: Additive Inverse: If a is in the set, –a is in the set,
         which is defined as the value that makes a + (– a ) = 0.
      5: Multiplicative Inverse: If a is in the set and is not 0,
         a^–1 is in the set, 
         which is defined as the value that makes a * a ^ –1 = 1.

    Song, Jimmy. Programming Bitcoin (p. 2). O'Reilly Media. Kindle Edition. 
    '''

    def __init__(self, num, prime):
        assert(num < prime or num >= 0)
        self.num = num
        self.prime = prime

    def __repr__(self):
        return 'FieldElement_{}({})'.format(self.prime, self.num)

    def __eq__(self, other):
        if other is None:
            return False        
        return self.num == other.num and self.prime == other.prime
    
    def __ne__(self, other):
        if other is None:
            return True
        return self.num != other.num or self.prime != other.prime

    def __add__(self, other):
        assert self.prime == other.prime
        num = (self.num + other.num) % self.prime
        return self.__class__(num, self.prime)

    def __sub__(self, other):
        assert self.prime == other.prime
        num = (self.num - other.num) % self.prime
        return self.__class__(num, self.prime)

    def __mul__(self, other):
        assert self.prime == other.prime
        num = (self.num * other.num) % self.prime
        return self.__class__(num, self.prime)

    def __pow__(self, exponent):
        n = exponent % (self.prime - 1)
        num = pow(self.num, n, self.prime)
        return self.__class__(num, self.prime)

    def __truediv__(self, other):
        assert self.prime == other.prime
        num = (self.num * pow(other.num, self.prime - 2, self.prime)) % self.prime
        return self.__class__(num, self.prime)

    def __rmul__(self, coefficient):
        num = (self.num * coefficient) % self.prime
        return self.__class__(num=num, prime=self.prime)
