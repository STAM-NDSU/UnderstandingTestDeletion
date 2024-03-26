import sys

sys.path.append("../")

from core import analyzer_main
from config import PROJECTS

"""
This file analyzes the [all available - 1 to repetitions ~ 50/commit]reduced test suite and computes the success ratio for all Fast-R algorithms 
comparing with developer reduced test sutie in loose scenario.
"""

for index, prog in enumerate(PROJECTS):
    analyzer_main(prog, "strict")
