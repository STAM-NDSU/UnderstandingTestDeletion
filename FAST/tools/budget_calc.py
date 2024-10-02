"""
USAGE: python3 tools/loose_budget_calc.py
"""

"""
Computes budget for all the projects in loose scenario including 
correnposing commit meta data
"""

import sys

sys.path.append("../")

from FAST.utils.utils import strip_commit_url
import json
import numpy as np

from FAST.config import TESTCASES_DIR, PROJECTS, BUDGET_FILEPATH
from FAST.utils.helpers import (
    get_whole_file_redundant_test_deletion_parent_commits,
    get_no_of_deleted_redundant_testfiles_in_test_deletion_commit_parent,
)


LOOSE_BUDGET = {}


if __name__ == "__main__":
    for index, prog in enumerate(PROJECTS):
        commits_list = get_whole_file_redundant_test_deletion_parent_commits(prog)

        # First of all, we compute buget for each parent commit of test deletion commit. Such a budget is used in the strict scenario.
        # Then, we take all the budgets and compute budget for loose scenario
        MIN_PERCENTAGE_OF_TEST_PRESERVED = 100
        MIN_PERCENTAGE_OF_TEST_PRESERVED_F = 100.00 # Floating point representation of the budget
        ALL_BUDGETS = []
        ALL_BUDGETS_F = [] # Holds floating point representation of the budget for maximum precision

        for commit in commits_list:
            commit = strip_commit_url(commit)

            inputFile = "{}/{}/{}-{}-ts.txt".format(TESTCASES_DIR, prog, prog, commit)

            numOfTCS = sum(
                (1 for _ in open(inputFile))
            )  # Total no. of testclass in particular commit history

            no_of_deleted_redundant_testfiles = (
                get_no_of_deleted_redundant_testfiles_in_test_deletion_commit_parent(
                    prog, commit
                )
            )
            
            no_of_preserved_testfiles = numOfTCS - no_of_deleted_redundant_testfiles

            # INFO: `repetitions` means budget for TSR
            
            # Final budget in percentage[no. of testcases remaining]
            repetitions = int(no_of_preserved_testfiles / numOfTCS * 100)

            # Precise Final budget in percentage [no. of testcases remaining]
            repetitionsF = float(no_of_preserved_testfiles / numOfTCS * 100)

            if repetitionsF <= MIN_PERCENTAGE_OF_TEST_PRESERVED_F:
                MIN_PERCENTAGE_OF_TEST_PRESERVED = repetitions
                MIN_PERCENTAGE_OF_TEST_PRESERVED_F = repetitionsF
                min_data = {
                    "numOfTCS": numOfTCS,
                    "no_of_deleted_redundant_testfiles": no_of_deleted_redundant_testfiles,
                    "hash": commit,
                }
            ALL_BUDGETS.append(repetitions)
            ALL_BUDGETS_F.append(repetitionsF)

        # Compute budget for loose scenario
        if MIN_PERCENTAGE_OF_TEST_PRESERVED < 100:
            LOOSE_BUDGET[prog] = {
                "Min Budget": MIN_PERCENTAGE_OF_TEST_PRESERVED,
                "Min Budget F": MIN_PERCENTAGE_OF_TEST_PRESERVED_F,
                "Min data": min_data,
                "Max Budget": int(np.max(ALL_BUDGETS)),
                "Max Budget F": float(np.max(ALL_BUDGETS_F)),
                "Average Budget": int(np.mean(ALL_BUDGETS)),
                "Average Budget F": float(np.mean(ALL_BUDGETS_F)),
            }
            print("Computed loose budget for " + prog)

        print("================================================================")

    # BUDGET_FILEPATH indicates file path to store budget calculations for loose setting
    f = open(f"{BUDGET_FILEPATH}", "w")
    f.write(json.dumps(LOOSE_BUDGET, indent=2))
