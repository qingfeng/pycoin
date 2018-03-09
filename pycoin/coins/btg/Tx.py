
from .SolutionChecker import BTGSolutionChecker
from .Solver import BTGSolver

from pycoin.tx.Tx import Tx as BaseTx


class Tx(BaseTx):
    Solver = BTGSolver
    SolutionChecker = BTGSolutionChecker
    ALLOW_SEGWIT = False
