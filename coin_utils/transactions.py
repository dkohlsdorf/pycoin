import requests

from io import BytesIO

from coin_utils.utils  import hash256
from coin_utils.varint import decode_varint, encode_varint
from coin_utils.script import Script


class TxFetcher:
    cache = {}

    @classmethod
    def get_url(cls, testnet=False):
        if testnet:
            return 'http://testnet.programmingbitcoin.com'
        else:
            return 'http://mainnet.programmingbitcoin.com'

    @classmethod
    def fetch(cls, tx_id, testnet=False, fresh=False):
        if fresh or (tx_id not in cls.cache):
            url = '{}/tx/{}.hex'.format(cls.get_url(testnet), tx_id)
            response = requests.get(url)
            try:
                raw = bytes.fromhex(response.text.strip())
            except ValueError:
                raise ValueError('unexpected response: {}'.format(response.text))
            if raw[4] == 0:
                raw = raw[:4] + raw[6:]
                tx = Tx.parse(BytesIO(raw), testnet = testnet)
                tx.locktime = int.from_bytes(raw[-4:], 'little')
            else:
                tx = Tx.parse(BytesIO(raw), testnet = testnet)
            if tx.id() != tx_id:
                raise ValueError('not the same id: {} vs {}'.format(tx.id(), tx_id))
            cls.cache[tx_id] = tx
        cls.cache[tx_id].testnet = testnet
        return cls.cache[tx_id]


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
    
    def fee(self, testnet=False):        
        amount_in  = sum([i.amount(testnet) for i in self.ins])
        amount_out = sum([o.amount for o in self.outs]) 
        return amount_in - amount_out

    def id(self):
        self.hash().hex()

    def hash(self):
        hash256(self.serialize())[::-1]

    def serialize(self):
        result  = self.version.to_bytes(4, 'little')
        result += encode_varint(len(self.ins))
        for tx in self.ins:
            result += tx.serialize()
        result += encode_varint(len(self.outs))
        for tx in self.outs:
            result += tx.serialize()
        result += self.locktime.to_bytes(4, 'little')
        return result 

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
        locktime = int.from_bytes(stream.read(4), 'little')
        return cls(version, inputs, outputs, locktime, testnet=testnet)


class TxIn:        

    def __init__(self, prev_tx, prev_idx, script_sig=None, sequence=0xffffffff):
        self.prev_tx  = prev_tx
        self.prev_idx = prev_idx
        if script_sig is None:
            self.script = Script()
        else:
            self.script = script_sig
        self.sequence = sequence

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

    def serialize(self):
        result  = self.prev_tx[::-1]
        result += self.prev_idx.to_bytes(4, 'little')
        result += self.script.serialize()
        result += self.sequence.to_bytes(4, 'little')
        return result

    def fetch_tx(self, testnet=False):
        return TxFetcher.fetch(self.prev_tx.hex(), testnet=testnet)

    def amount(self, testnet=False):
        tx = self.fetch_tx(testnet=testnet)
        return tx.tx_outs[self.prev_idx].amount

    def script_pubkey(self, testnet=False):
        tx = self.fetch_tx(testnet=testnet)
        return tx.tx_outs[self.prev_idx].script_pubkey


class TxOut:

    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey

    def __repr__(self):
        return '{}:{}'.format(self.amount, self.script_pubkey)

    def serialize(self):
        result  = self.amount.to_bytes(8, 'little')
        result += self.script_pubkey.serialize()
        return result 

    @classmethod
    def parse(cls, s):
        amount = int.from_bytes(s.read(8), 'little')
        script = Script.parse(s)
        return cls(amount, script)