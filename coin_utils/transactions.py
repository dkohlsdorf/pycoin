from coin_utils.utils import hash256
from coin_utils.varint import decode_varint

class Tx:

    def __init__(self, version, ins, outs, locktime, testnet=False):
        self.version = version
        self.ins = ins
        self.outs = outs
        self.locktime = locktime
        self.testnet = testnet
        
    def __repr__(self):
        tx_ins = ''
        for tx in self.ins:
            tx_ins += tx.__repr__() + "\n"
        tx_outs = ''
        for tx in self.outs:
            tx_outs += tx.__repr__() + "\n"
        return 'tx: {}\nversion:{}\ntx_ins:\n{}tx_outs:\n{}locktime: {}'.format(
            self.id(),
            self.version,
            tx_ins,
            tx_outs,
            self.locktime
        )
    
    def id(self):
        self.hash().hex()

    def hash(self):
        hash256(self.serialize())[::-1]

    @classmethod
    def parse(cls, stream, testnet=False):
        version = int.from_bytes(stream.read(4), 'little')
        n_inputs = decode_varint(stream)
        inputs = []
        for _ in range(n_inputs):
            inputs.append(TxIn.parse(stream))
        n_outputs = decode_varint(stream)
        outputs = []
        for _ in range(n_outputs):
            outputs.append(TxOut.parse(stream))
        locktime = int.from_bytes(s.read(4), 'little')
        return cls(version, inputs, outputs, locktime, testnet=testnet)


class TxIn:        

    def __init__(self, prev_tx, prev_idx, script=None, sequence=0xffffffff):
        self.prev_tx  = prev_tx
        self.prev_idx = prev_idx
        if script is None:
            self.script = Script()
        else:
            self.script = script

    @classmethod
    def parse(cls, s):
        prev_tx  = s.read(32)[::-1]
        prev_idx = int.from_bytes(s.read(4), 'little')
        script   = Script.parse(s)
        sequence = int.from_bytes(s.read(4), 'little')
        return cls(prev_tx, prev_idx, script, sequence)

    def __repr__(self):
        return '{}:{}'.format(
            self.prev_tx.hex(),
            self.prev_idx
        )


class TxOut:

    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    def __repr__(self):
        return '{}:{}'.format(self.amount, self.script_pubkey)

    @classmethod
    def parse(cls, s):
        amount = int.from_bytes(s.read(8), 'little')
        script = Script.parse(s)
        return cls(amount, script)