class Signature:

    def __init__(self, r, s):
        self.r = r
        self.s = s 

    def __repr__(self):
        return 'Signature({:x}{:x})'.format(self.r, self.s)
    
    def der(self):
        rbin = der_num(self.r)
        result = bytes([2, len(rbin)]) + rbin
        sbin = der_num(self.s)
        result += bytes([2, len(sbin)]) + sbin
        return bytes([0x3, len(result)]) + result


def der_num(num):
    num = num.to_bytes(32, byteorder='big')
    num = num.lstrip(b'\x00')
    if num[0] & 0x80:
        num = b'\x00' + num
    return num

