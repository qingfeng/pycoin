from ..bitcoin.Solver import BitcoinSolver
from ...tx.script.flags import SIGHASH_FORKID, SIGHASH_ALL

from .SolutionChecker import HardforkSolutionChecker


class HardforkSolver(BitcoinSolver):
    SolutionChecker = HardforkSolutionChecker

    def solve(self, *args, **kwargs):
        if kwargs.get("hash_type") is None:
            kwargs["hash_type"] = SIGHASH_ALL
        kwargs["hash_type"] |= SIGHASH_FORKID | (self.SolutionChecker.fork_id << 8)
        return super(HardforkSolver, self).solve(*args, **kwargs)
