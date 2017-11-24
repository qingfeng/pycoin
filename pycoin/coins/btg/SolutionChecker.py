from ...tx.script import errno
from ...tx.script import ScriptError
from ...tx.script.flags import SIGHASH_FORKID

from ..hardfork.SolutionChecker import HardforkSolutionChecker

class BTGSolutionChecker(HardforkSolutionChecker):
    fork_id = 79
