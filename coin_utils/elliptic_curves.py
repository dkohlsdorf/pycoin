from coin_utils.fields import * 

class Point:
    '''
    A point (x, y) defined on the elliptic
    curve y^2 = x^3 + a * x + b. This works
    for all finite sets. 
    '''
    
    def __init__(self, x, y, a, b):        
        self.x = x
        self.y = y
        self.a = a
        self.b = b

    def __eq__(self, other):
        same_curve = self.a == other.a and self.b == other.b
        same_point = self.x == other.x and self.y == other.y 
        return same_curve and same_point

    def __ne__(self, other):
        same_curve = self.a != other.a or self.b != other.b
        same_point = self.x != other.x or self.y != other.y  
        return same_curve or same_point

    def is_inf(self):
        return self.x == None and self.y == None

    def __rmul__(self, coefficient):
        coef    = coefficient
        current = self
        result  = self.__class__(None, None, self.a, self.b)
        while coef:
            if coef & 1:
                result += current
            current += current
            coef >>= 1
        return result
                
    def __add__(self, other):
        assert self.a == other.a and self.b == other.b
        if self.is_inf():
            return other
        if other.is_inf():
            return self
        if self.x != other.x:
            s   = (other.y - self.y) / (other.x - self.x)
            x3  = (s ** 2)  - self.x - other.x
            y3  = s * (self.x - x3) - self.y    
            return self.__class__(x3, y3, self.a, self.b)
        if self == other and self.y == 0 * self.x:
            return self.__class_(None, None, self.a, self.b)
        if self == other:
            self.x ** 2 
            s  = (3 * self.x ** 2 + self.a) / (2 * self.y)
            x3 = (s ** 2) - 2 * self.x
            y3 = s * (self.x - x3) - self.y
            return self.__class__(x3, y3, self.a, self.b)

    def __repr__(self):
        if self.x is None:
            return 'Point(infinity)'
        elif isinstance(self.x, FieldElement):
            return 'Point({},{})_{}_{} FieldElement({})'.format(
                self.x.num, self.y.num, self.a.num, self.b.num, self.x.prime)
        else:
            return 'Point({},{})_{}_{}'.format(self.x, self.y, self.a, self.b)
