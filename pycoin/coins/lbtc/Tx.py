
from .SolutionChecker import LBTCSolutionChecker
from .Solver import LBTCSolver

from pycoin.tx.Tx import Tx as BaseTx

class Tx(BaseTx):
    Solver = LBTCSolver
    SolutionChecker = LBTCSolutionChecker
    ALLOW_SEGWIT = False
