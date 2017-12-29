from ..hardfork.Solver import HardforkSolver
from ...tx.script.flags import SIGHASH_FORKID, SIGHASH_ALL

from .SolutionChecker import SBTCSolutionChecker

class SBTCSolver(HardforkSolver):
    SolutionChecker = SBTCSolutionChecker

    def solve(self, *args, **kwargs):
        if kwargs.get("hash_type") is None:
            kwargs["hash_type"] = SIGHASH_ALL
        kwargs["hash_type"] |= SIGHASH_FORKID
        return super(HardforkSolver, self).solve(*args, **kwargs)
