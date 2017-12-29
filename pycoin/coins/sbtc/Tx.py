
from .SolutionChecker import SBTCSolutionChecker
from .Solver import SBTCSolver

from pycoin.tx.Tx import Tx as BaseTx

class Tx(BaseTx):
    Solver = SBTCSolver
    SolutionChecker = SBTCSolutionChecker
