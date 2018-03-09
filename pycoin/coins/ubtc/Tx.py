
from .SolutionChecker import UBTCSolutionChecker
from .Solver import UBTCSolver

from pycoin.tx.Tx import Tx as BaseTx

class Tx(BaseTx):
    Solver = UBTCSolver
    SolutionChecker = UBTCSolutionChecker
    ALLOW_SEGWIT = False
