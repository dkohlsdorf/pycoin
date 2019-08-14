

TWO_BYTE_MARKER   = 0xfd # 253
FOUR_BYTE_MARKER  = 0xfe # 254
EIGHT_BYTE_MARKER = 0xff # 255


def decode_varint(stream):
    i = stream.read(1)[0]
    if i == TWO_BYTE_MARKER:
        return int.from_bytes(stream.read(2), 'little')
    elif i == FOUR_BYTE_MARKER:
        return int.from_bytes(stream.read(4), 'little')
    elif i == EIGHT_BYTE_MARKER:
        return int.from_bytes(stream.read(8), 'little')
    else:
        return i


def encode_varint(i):
    if i < 0xfd:
        return bytes(i)
    elif i < 0x10000:
        return b'\xfd' + i.to_bytes(2, 'little')
    elif i < 0x100000000:
        return b'\xfe' + i.to_bytes(4, 'little')
    elif i < 0x10000000000000000:
        return b'\xff' + i.to_bytes(8, 'little')
    else:
        raise ValueError('integer too large: {}'.format(i))