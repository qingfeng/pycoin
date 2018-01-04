from ..bitcoin.Solver import BitcoinSolver
from ...tx.script.flags import SIGHASH_FORKID, SIGHASH_ALL

from .SolutionChecker import BCDSolutionChecker

class BCDSolver(BitcoinSolver):
    SolutionChecker = BCDSolutionChecker

