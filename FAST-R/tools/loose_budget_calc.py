"""
Computes budget for all the projects in loose scenario including 
correnposing commit meta data
"""

import sys

sys.path.append("../")

from utils.utils import strip_commit_url
import json
import numpy as np

from config import TESTCASES_DIR, PROJECTS
from utils.helpers import (
    get_deleted_testcases_with_whole_file_df,
    get_whole_file_test_deletion_parent_commits,
    get_deleted_testfiles_in_test_deletion_commit_parent,
    get_no_of_deleted_testfiles_in_test_deletion_commit_parent,
)

# File path to store budget calculations for loose setting
from config import BUDGET_FILE

LOOSE_BUDGET = {}


if __name__ == "__main__":
    for index, prog in enumerate(PROJECTS):
        commits_list = get_whole_file_test_deletion_parent_commits(prog)

        # Strict Scenario
        MIN_PERCENTAGE_OF_TEST_PRESERVED = 100
        MIN_PERCENTAGE_OF_TEST_PRESERVED_F = 100.00
        ALL_BUDGETS = []
        ALL_BUDGETS_F = []

        for commit in commits_list:
            commit = strip_commit_url(commit)
            # IGNORE 100% TEST DELETION CASE OF COMMONS-MATH FROM STUDY
            if (
                prog == "commons-math"
                and commit == "e389289e779612c5930d7c292bbbc94027695ae5"
            ):
                continue

            inputFile = "{}/{}/{}-{}-ts.txt".format(TESTCASES_DIR, prog, prog, commit)

            numOfTCS = sum(
                (1 for _ in open(inputFile))
            )  # Total no. of testclass in particular commit history
            no_of_deleted_testfiles = (
                get_no_of_deleted_testfiles_in_test_deletion_commit_parent(prog, commit)
            )
            no_of_preserved_testfiles = numOfTCS - no_of_deleted_testfiles

            # Final budget in percentage[no. of testcases remaining]
            repetitions = int(no_of_preserved_testfiles / numOfTCS * 100)

            # Precise Final budget in percentage [no. of testcases remaining]
            repetitionsF = float(no_of_preserved_testfiles / numOfTCS * 100)

            if repetitions <= MIN_PERCENTAGE_OF_TEST_PRESERVED:
                MIN_PERCENTAGE_OF_TEST_PRESERVED = repetitions
                MIN_PERCENTAGE_OF_TEST_PRESERVED_F = repetitionsF
                min_data = {
                    "numOfTCS": numOfTCS,
                    "no_of_deleted_testfiles": no_of_deleted_testfiles,
                    "hash": commit,
                }
            ALL_BUDGETS.append(repetitions)
            ALL_BUDGETS_F.append(repetitionsF)

        # Loose Scenario
        if MIN_PERCENTAGE_OF_TEST_PRESERVED <= 100:
            LOOSE_BUDGET[prog] = {
                "Min Budget": MIN_PERCENTAGE_OF_TEST_PRESERVED,
                "Min Budget F": MIN_PERCENTAGE_OF_TEST_PRESERVED_F,
                "Min data": min_data,
                "Max Budget": int(np.max(ALL_BUDGETS)),
                "Max Budget F": float(np.max(ALL_BUDGETS_F)),
                "Average Budget": int(np.mean(ALL_BUDGETS)),
                "Average Budget F": float(np.mean(ALL_BUDGETS_F)),
            }
            print(min_data)

        print("================================================================")

    f = open(f"{BUDGET_FILE}", "w")
    f.write(json.dumps(LOOSE_BUDGET, indent=2))
