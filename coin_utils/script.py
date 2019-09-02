from coin_utils.varint import decode_varint, encode_varint 
from coin_utils.opcodes import OP_CODE_FUNCTIONS, OP_CODE_NAMES

class Script:

    def __init__(self, cmds=[]):
        self.cmds = cmds
    
    def __add__(self, other):
        return Script(self.cmds + other.cmds)

    def evaluate(self, z):
        cmds = self.cmds[:]
        stack = []
        altstack = []
        i = 0
        while len(cmds) > 0:
            cmd = cmds.pop(0)
            print(i, len(cmds))
            i += 1
            if type(cmd) == int:
                operation = OP_CODE_FUNCTIONS[cmd]
                if cmd in (99, 100):
                    if not operation(stack, cmds):
                        print('bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
                elif cmd in (107, 108):
                    if not operation(stack, altstack):
                        print('bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
                elif cmd in (172, 173, 174, 175):
                    if not operation(stack, z):
                        print('bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
                else:
                    if not operation(stack):
                        print('bad op: {}'.format(OP_CODE_NAMES[cmd]))
                        return False
            else:
                stack.append(cmd)
        if len(stack) == 0:
            return False
        if stack.pop() == b'':
            return False
        return True

    def serialize(self):
        result = self.raw_serialize()
        total  = len(result)
        return encode_varint(total) + result    

    def raw_serialize(self):
        result = b''
        for cmd in self.cmds:
            if type(cmd) == int:
                result += cmd.to_bytes(1, 'little')
            else:
                length = len(cmd)
                if length < 75:
                    result += length.to_bytes(1, 'little')
                elif length > 75 and length < 0x100:
                    result += (76).to_bytes(1, 'little')
                    result += length.to_bytes(1, 'little')
                elif length >= 0x100 and length <= 520:
                    result += (77).to_bytes(1, 'little')
                    result += length.to_bytes(2, 'little')
                else:
                    raise ValueError('command too long')
                result += cmd                
        return result

    @classmethod
    def parse(cls, s):
        length = decode_varint(s)
        cmds = []
        count = 0
        while count < length:
            current = s.read(1)
            count  += 1
            current_byte = current[0]
            if current_byte >= 1 and current_byte <= 75:
                n = current_byte
                cmds.append(s.read(n))
                count += n
            elif current_byte == 76:
                data_len = int.from_bytes(s.read(1), 'little')
                cmds.append(s.read(data_len))
                count += data_len + 1
            elif current_byte == 77:
                data_len = int.from_bytes(s.read(2), 'little')
                cmds.append(s.read(data_len))
                count += data_len + 2
            else:
                op_code = current_byte
                cmds.append(op_code)
        if count != length:
            raise SyntaxError("parsing script failed")
        return cls(cmds)

