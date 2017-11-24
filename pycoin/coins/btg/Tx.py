
from .SolutionChecker import HardforkSolutionChecker
from .Solver import HardforkSolver

from pycoin.tx.Tx import Tx as BaseTx


class Tx(BaseTx):
    Solver = HardforkSolver
    SolutionChecker = HardforkSolutionChecker
