from ...tx.script import errno
from ...tx.script import ScriptError
from ...tx.script.flags import SIGHASH_FORKID

from ...serialize.bitcoin_streamer import (
    stream_bc_string
)
from ..hardfork.SolutionChecker import HardforkSolutionChecker

class UBTCSolutionChecker(HardforkSolutionChecker):
    signature_type_segwit = False
    def append_signature(self, f):
        stream_bc_string(f, b'ub')
