from ..hardfork.Solver import HardforkSolver
from ...tx.script.flags import SIGHASH_FORKID

from .SolutionChecker import HardforkSolutionChecker


class BTGSolver(HardforkSolver):
    SolutionChecker = HardforkSolutionChecker
