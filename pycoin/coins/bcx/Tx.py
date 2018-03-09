
from .SolutionChecker import BCXSolutionChecker
from .Solver import BCXSolver

from pycoin.tx.Tx import Tx as BaseTx

class Tx(BaseTx):
    Solver = BCXSolver
    SolutionChecker = BCXSolutionChecker
    ALLOW_SEGWIT = True
