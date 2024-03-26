"""
This file is modified version of original experimentBudget.py of FAST-R.
It is used to run all FAST-R algorithms in all commits of target project in given Budget scenario(loose or strict)
"""

import math
import os
import pickle
import sys
import fastr
import metric
from pathlib import Path
from utils import strip_commit_url
import json
from config import REPEATS, RESULTS_DIR, TESTCASES_DIR
from utils.helpers import (
    get_whole_file_test_deletion_parent_commits,
    get_no_of_deleted_testfiles_in_test_deletion_commit_parent,
)

# Pre-computed budget for loose setting
import json

# Budget File contains pre-computed budget for loose setting
from config import BUDGET_FILE
all_projects_loose_budget = json.load(open(f"{BUDGET_FILE}"))

# Check if algorithm should run 
# NOTE: It is handy to run single algortihm during debugging
def run_algorithm(enforce_algorithm, enforced_algo, algo):
    if not enforce_algorithm:
        return True
    else:
        return enforced_algo == algo


def main(prog, setting, enforce_algorithm=False, enforced_algorithm="FAST-all"):
    commits_list = get_whole_file_test_deletion_parent_commits(prog)

    # Strict Scenario
    if setting == "strict":
        for commit in commits_list:
            commit = strip_commit_url(commit)
            directory = "{}/strict/{}/{}/".format(RESULTS_DIR, prog, commit)
            if not os.path.exists(directory):
                os.makedirs(directory)
            if not os.path.exists(directory + "selections/"):
                os.makedirs(directory + "selections/")
            if not os.path.exists(directory + "measures/"):
                os.makedirs(directory + "measures/")

            # FAST-R parameters
            k, n, r, b = 5, 10, 1, 10
            dim = 10

            # FAST-f sample size
            def all_(x):
                return x

            def sqrt_(x):
                return int(math.sqrt(x)) + 1

            def log_(x):
                return int(math.log(x, 2)) + 1

            def one_(x):
                return 1

            inputFile = "{}/{}/{}-{}-ts.txt".format(
                TESTCASES_DIR, prog, prog, commit
            )
            outpath = "{}/strict/{}/{}/".format(RESULTS_DIR, prog, commit)
            sPath = outpath + "selections/"
            tPath = outpath + "measures/"

            numOfTCS = sum(
                (1 for _ in open(inputFile))
            )  # Total no. of testclass in particular commit history
            no_of_deleted_testfiles = (
                get_no_of_deleted_testfiles_in_test_deletion_commit_parent(prog, commit)
            )
            no_of_preserved_testfiles = numOfTCS - no_of_deleted_testfiles
            print("Total test files: ", numOfTCS)
            print("No. of deleted test files: ", no_of_deleted_testfiles)
            print("No. of preserved test files: ", no_of_preserved_testfiles)

            # Final budget[no. of testcases remaining] in percentage
            # Repetition => [step size i.e increases from 1%-30% in FAST-R]
            repetitions = int(no_of_preserved_testfiles / numOfTCS * 100)
            print("Computed Repetitions: ", repetitions)

            # for reduction in range(1, repetitions+1):
            # Current budget for each step[step size increases from 1%-30%]
            # B = int(numOfTCS * reduction / 100)

            # Budget(actual number of tests preserved) is fixed in loose scenario
            # B = int(numOfTCS * repetitions / 100) # Commenting this because no. of actual tests deleted is not equal to percentage B
            B = no_of_preserved_testfiles

            # reduction (percentage of test preserved)
            reduction = repetitions

            if run_algorithm(enforce_algorithm, enforced_algorithm, "FAST++"):
                for run in range(REPEATS):
                    sOut = "{}/{}-{}-{}.pickle".format(
                        sPath, "FAST++", reduction, run + 1
                    )
                    tOut = "{}/{}-{}-{}.pickle".format(
                        tPath, "FAST++", reduction, run + 1
                    )
                    # Skip if file exists
                    if os.path.exists(sOut) and os.path.exists(tOut):
                        continue
                    pTime, rTime, sel = fastr.fastPlusPlus(inputFile, dim=dim, B=B)
                    pickle.dump(sel, open(sOut, "wb"))
                    pickle.dump((pTime, rTime), open(tOut, "wb"))
                    print("FAST++", reduction, pTime, rTime, run)

            if run_algorithm(enforce_algorithm, enforced_algorithm, "FAST-CS"):
                for run in range(REPEATS):
                    sOut = "{}/{}-{}-{}.pickle".format(
                        sPath, "FAST-CS", reduction, run + 1
                    )
                    tOut = "{}/{}-{}-{}.pickle".format(
                        tPath, "FAST-CS", reduction, run + 1
                    )
                    # Skip if file exists
                    if os.path.exists(sOut) and os.path.exists(tOut):
                        continue
                    pTime, rTime, sel = fastr.fastCS(inputFile, dim=dim, B=B)
                    pickle.dump(sel, open(sOut, "wb"))
                    pickle.dump((pTime, rTime), open(tOut, "wb"))
                    print("FAST-CS", reduction, pTime, rTime, run)

            if run_algorithm(enforce_algorithm, enforced_algorithm, "FAST-pw"):
                for run in range(REPEATS):
                    sOut = "{}/{}-{}-{}.pickle".format(
                        sPath, "FAST-pw", reduction, run + 1
                    )
                    tOut = "{}/{}-{}-{}.pickle".format(
                        tPath, "FAST-pw", reduction, run + 1
                    )
                    if os.path.exists(sOut) and os.path.exists(tOut):
                        continue
                    pTime, rTime, sel = fastr.fast_pw(
                        inputFile, r, b, bbox=True, k=k, memory=True, B=B
                    )
                    pickle.dump(sel, open(sOut, "wb"))
                    pickle.dump((pTime, rTime), open(tOut, "wb"))
                    print("FAST-pw", reduction, pTime, rTime, run)

            if run_algorithm(enforce_algorithm, enforced_algorithm, "FAST-all"):
                for run in range(REPEATS):
                    sOut = "{}/{}-{}-{}.pickle".format(
                        sPath, "FAST-all", reduction, run + 1
                    )
                    tOut = "{}/{}-{}-{}.pickle".format(
                        tPath, "FAST-all", reduction, run + 1
                    )
                    # Skip if file exists
                    if os.path.exists(sOut) and os.path.exists(tOut):
                        continue
                    pTime, rTime, sel = fastr.fast_(
                        inputFile, all_, r=r, b=b, bbox=True, k=k, memory=True, B=B
                    )
                    pickle.dump(sel, open(sOut, "wb"))
                    pickle.dump((pTime, rTime), open(tOut, "wb"))
                    print("FAST-all", reduction, pTime, rTime, run)

    # Loose Scenario
    if setting == "loose":
        # Budget for loose scenario
        MIN_PERCENTAGE_OF_TEST_PRESERVED = all_projects_loose_budget[prog]["Min Budget"]

        for commit in commits_list:
            commit = strip_commit_url(commit)
            directory = "{}/loose/{}/{}/".format(RESULTS_DIR, prog, commit)
            if not os.path.exists(directory):
                os.makedirs(directory)
            if not os.path.exists(directory + "selections/"):
                os.makedirs(directory + "selections/")
            if not os.path.exists(directory + "measures/"):
                os.makedirs(directory + "measures/")

            # FAST-R parameters
            k, n, r, b = 5, 10, 1, 10
            dim = 10

            # FAST-f sample size
            def all_(x):
                return x

            def sqrt_(x):
                return int(math.sqrt(x)) + 1

            def log_(x):
                return int(math.log(x, 2)) + 1

            def one_(x):
                return 1

            inputFile = "{}/{}/{}-{}-ts.txt".format(
                TESTCASES_DIR, prog, prog, commit
            )
            outpath = "{}/loose/{}/{}/".format(RESULTS_DIR, prog, commit)
            sPath = outpath + "selections/"
            tPath = outpath + "measures/"

            numOfTCS = sum(
                (1 for _ in open(inputFile))
            )  # Total no. of testclass in particular commit history
            no_of_deleted_testfiles = (
                get_no_of_deleted_testfiles_in_test_deletion_commit_parent(prog, commit)
            )
            no_of_preserved_testfiles = numOfTCS - no_of_deleted_testfiles
            print("Total test files: ", numOfTCS)
            print("No. of deleted test files: ", no_of_deleted_testfiles)
            print("No. of preserved test files: ", no_of_preserved_testfiles)

            # Final budget[no. of testcases remaining] in percentage; # STRICT SCENARIO
            repetitions = int(no_of_preserved_testfiles / numOfTCS * 100)
            print("Computed Repetitions: ", repetitions)

            # Budget(actual number of tests preserved) is fixed in loose scenario
            B = int(numOfTCS * MIN_PERCENTAGE_OF_TEST_PRESERVED / 100)
            # reduction (percentage of test preserved)
            reduction = MIN_PERCENTAGE_OF_TEST_PRESERVED

            if run_algorithm(enforce_algorithm, enforced_algorithm, "FAST++"):
                for run in range(REPEATS):
                    sOut = "{}/{}-{}-{}.pickle".format(
                        sPath, "FAST++", reduction, run + 1
                    )
                    tOut = "{}/{}-{}-{}.pickle".format(
                        tPath, "FAST++", reduction, run + 1
                    )
                    # Skip if file exists
                    if os.path.exists(sOut) and os.path.exists(tOut):
                        continue
                    pTime, rTime, sel = fastr.fastPlusPlus(inputFile, dim=dim, B=B)
                    pickle.dump(sel, open(sOut, "wb"))
                    pickle.dump((pTime, rTime), open(tOut, "wb"))
                    print("FAST++", reduction, pTime, rTime)

            if run_algorithm(enforce_algorithm, enforced_algorithm, "FAST-CS"):
                for run in range(REPEATS):
                    sOut = "{}/{}-{}-{}.pickle".format(
                        sPath, "FAST-CS", reduction, run + 1
                    )
                    tOut = "{}/{}-{}-{}.pickle".format(
                        tPath, "FAST-CS", reduction, run + 1
                    )
                    # Skip if file exists
                    if os.path.exists(sOut) and os.path.exists(tOut):
                        continue
                    pTime, rTime, sel = fastr.fastCS(inputFile, dim=dim, B=B)
                    pickle.dump(sel, open(sOut, "wb"))
                    pickle.dump((pTime, rTime), open(tOut, "wb"))
                    print("FAST-CS", reduction, pTime, rTime)

            if run_algorithm(enforce_algorithm, enforced_algorithm, "FAST-pw"):
                for run in range(REPEATS):
                    sOut = "{}/{}-{}-{}.pickle".format(
                        sPath, "FAST-pw", reduction, run + 1
                    )
                    tOut = "{}/{}-{}-{}.pickle".format(
                        tPath, "FAST-pw", reduction, run + 1
                    )
                    # Skip if file exists
                    if os.path.exists(sOut) and os.path.exists(tOut):
                        continue
                    pTime, rTime, sel = fastr.fast_pw(
                        inputFile, r, b, bbox=True, k=k, memory=True, B=B
                    )
                    pickle.dump(sel, open(sOut, "wb"))
                    pickle.dump((pTime, rTime), open(tOut, "wb"))
                    print("FAST-pw", reduction, pTime, rTime)

            if run_algorithm(enforce_algorithm, enforced_algorithm, "FAST-all"):
                for run in range(REPEATS):
                    sOut = "{}/{}-{}-{}.pickle".format(
                        sPath, "FAST-all", reduction, run + 1
                    )
                    tOut = "{}/{}-{}-{}.pickle".format(
                        tPath, "FAST-all", reduction, run + 1
                    )
                    # Skip if file exists
                    if os.path.exists(sOut) and os.path.exists(tOut):
                        continue
                    pTime, rTime, sel = fastr.fast_(
                        inputFile, all_, r=r, b=b, bbox=True, k=k, memory=True, B=B
                    )
                    pickle.dump(sel, open(sOut, "wb"))
                    pickle.dump((pTime, rTime), open(tOut, "wb"))
                    print("FAST-all", reduction, pTime, rTime)
