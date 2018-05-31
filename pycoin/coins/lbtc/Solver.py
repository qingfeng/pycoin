from ..hardfork.Solver import HardforkSolver
from ...tx.script.flags import SIGHASH_FORKID, SIGHASH_ALL

from .SolutionChecker import LBTCSolutionChecker

class LBTCSolver(HardforkSolver):
    SolutionChecker = LBTCSolutionChecker

    def solve(self, *args, **kwargs):
        if kwargs.get("hash_type") is None:
            kwargs["hash_type"] = SIGHASH_ALL
        return super(HardforkSolver, self).solve(*args, **kwargs)
