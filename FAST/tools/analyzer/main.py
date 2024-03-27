usuage = """
USAGE: python3 tools/analyzer/main.py <prog> <setting>
"""

import sys

sys.path.append("../")

from FAST.analyzer.core import analyzer_main
from FAST.config import PROJECTS, SETTINGS

"""
This file analyzes the [all available - 1 to repetitions ~ 50/commit]reduced test suite and computes the success ratio for all Fast-R algorithms 
comparing with developer reduced test sutie in loose and strict scenario.
"""

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please provide all the required arguments.")
        print(usuage)
        exit(1)

    script, prog, setting = sys.argv

    if prog not in PROJECTS:
        print(
            "Please provide a valid project name. It should be one of the 7 analyzed projects in the study."
        )
        exit(1)

    if setting not in SETTINGS:
        print(
            "Please provide a valid setting. Setting should be either 'strict' or 'loose'. "
        )
        exit(1)

    for index, prog in enumerate(PROJECTS):
        analyzer_main(prog, setting)
