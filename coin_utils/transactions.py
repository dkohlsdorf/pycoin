from coin_utils.utils import hash256


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
    def parse(cls, stream):
        version = int.from_bytes(stream.read(4), 'little')


class TxIn:        

    def __init__(self, prev_tx, prev_idx, script=None, sequence=0xffffffff):
        self.prev_tx  = prev_tx
        self.prev_idx = prev_idx
        if script is None:
            self.script = Script()
        else:
            self.script = script

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

        