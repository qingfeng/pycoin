from pycoin.tx.Tx import Tx as BaseTx

from ...serialize.bitcoin_streamer import (
    parse_struct, parse_bc_int, parse_bc_string,
    stream_struct, stream_bc_string
)
from .SolutionChecker import BCDSolutionChecker
from .Solver import BCDSolver

class Tx(BaseTx):
    Solver = BCDSolver
    SolutionChecker = BCDSolutionChecker
    ALLOW_SEGWIT = False

    def __init__(self, version, txs_in, txs_out, lock_time=0, unspents=None, pre_block_hash=None):
        super(Tx, self).__init__(version, txs_in, txs_out, lock_time=0, unspents=None)
        self.pre_block_hash = pre_block_hash

    def replace(self, **kwargs):
        new_tx = super(Tx, self).replace(**kwargs)
        new_tx.pre_block_hash = kwargs.get(
            'pre_block_hash', self.pre_block_hash)
        return new_tx

    def stream(self, f, blank_solutions=False, include_unspents=False, include_witness_data=True):
        """Stream a Bitcoin transaction Tx to the file-like object f."""
        include_witnesses = include_witness_data and self.has_witness_data()
        stream_struct("L", f, self.version)
        if self.version == 12:
            # BCD fork
            assert self.pre_block_hash
            stream_struct("#", f, self.pre_block_hash)
        if include_witnesses:
            f.write(b'\0\1')
        stream_struct("I", f, len(self.txs_in))
        for t in self.txs_in:
            t.stream(f, blank_solutions=blank_solutions)
        stream_struct("I", f, len(self.txs_out))
        for t in self.txs_out:
            t.stream(f)
        if include_witnesses:
            for tx_in in self.txs_in:
                witness = tx_in.witness
                stream_struct("I", f, len(witness))
                for w in witness:
                    stream_bc_string(f, w)
        stream_struct("L", f, self.lock_time)
        if include_unspents and not self.missing_unspents():
            self.stream_unspents(f)

    @classmethod
    def parse(cls, f, allow_segwit=None):
        """Parse a Bitcoin transaction Tx from the file-like object f."""
        if allow_segwit is None:
            allow_segwit = cls.ALLOW_SEGWIT
        txs_in = []
        txs_out = []
        version, = parse_struct("L", f)
        if version == 12:
            pre_block_hash, = parse_struct("#", f)
        else:
            pre_block_hash = None

        v1 = ord(f.read(1))
        is_segwit = allow_segwit and (v1 == 0)
        v2 = None
        if is_segwit:
            flag = f.read(1)
            if flag == b'\0':
                raise ValueError("bad flag in segwit")
            if flag == b'\1':
                v1 = None
            else:
                is_segwit = False
                v2 = ord(flag)
        count = parse_bc_int(f, v=v1)
        txs_in = []
        for i in range(count):
            txs_in.append(cls.TxIn.parse(f))
        count = parse_bc_int(f, v=v2)
        txs_out = []
        for i in range(count):
            txs_out.append(cls.TxOut.parse(f))

        if is_segwit:
            for tx_in in txs_in:
                stack = []
                count = parse_bc_int(f)
                for i in range(count):
                    stack.append(parse_bc_string(f))
                tx_in.witness = stack
        lock_time, = parse_struct("L", f)
        return cls(version, txs_in, txs_out, lock_time, pre_block_hash=pre_block_hash)

