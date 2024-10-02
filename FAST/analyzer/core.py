"""
This core file analyzes the reduced test suite and computes number of developer deleted tests 
detected for all Fast-R algorithms in both loose and strict scenario.

For evaluating FAST-R algorithms, we consider only parent test deletion commits of test deletion commits in which whole test class is removed(TDC-C).
"""

import sys

sys.path.append("../")

import pickle
from FAST.utils.utils import *
import json
import os
from FAST.config import RESULTS_DIR, REPEATS, ARTIFACTS_DIR, BUDGET_FILEPATH
from FAST.utils.helpers import (
    get_redundant_deleted_testcases_with_whole_file_df,
    get_whole_file_redundant_test_deletion_parent_commits,
    get_deleted_redundant_testfiles_in_test_deletion_commit_parent,
    get_redundant_deleted_testcases_by_project_and_removed_filepath,
)
from FAST.analyzer.utils import (
    get_line_no_history_testfiles,
    get_test_filename_by_line_no,
    get_no_of_testfiles_in_commit,
)
from math import fsum

# BUDGET_FILEPATH indicates filepath where precomputed budget calculations for loose setting are stored
budget_data = json.load(open(f"{BUDGET_FILEPATH}"))


def analyzer_main(prog, setting):
    analyzer_data = {}
    # Get parent commits of test deletion commit(TDC) in which whole test class is deleted
    commits_list = get_whole_file_redundant_test_deletion_parent_commits(prog)
    analyzer_data["Total test deletion parent commits:"] = len(commits_list)

    # Get test cases deleted with test class
    deleted_testcases_with_whole_file = (
        get_redundant_deleted_testcases_with_whole_file_df(prog)
    )
    analyzer_data["Total test cases deleted with whole file:"] = len(
        deleted_testcases_with_whole_file
    )

    analyzer_data["details"] = []

    print("Looping each commit START")
    for index, commit in enumerate(commits_list):
        print("Commit :", (index + 1))
        commit = strip_commit_url(commit)

        # handle both strict and loose setting
        setting_dir = "loose" if setting == "loose" else "strict"
        directory = "{}/{}/{}/{}/".format(RESULTS_DIR, setting_dir, prog, commit)

        selection_dir = directory + "selections"
        measurement_dir = directory + "measures"

        # Total no. of testclass in particular parent_commit history
        numOfTCS = get_no_of_testfiles_in_commit(prog, commit)
        print("Total test files: ", numOfTCS)

        deleted_testfiles = (
            get_deleted_redundant_testfiles_in_test_deletion_commit_parent(prog, commit)
        )
        no_of_deleted_testfiles = len(deleted_testfiles)
        print("Total no. of deleted test files: ", no_of_deleted_testfiles)
        print("Deleted Test files")
        print(deleted_testfiles)

        deleted_testfiles_line_no_history = get_line_no_history_testfiles(
            prog, commit, deleted_testfiles
        )
        no_of_preserved_testfiles = numOfTCS - no_of_deleted_testfiles
        print("No. of preserved test files: ", no_of_preserved_testfiles)
        # handle both strict and loose setting
        # Final budget[no. of testcases remaining] in percentage is fixed for loose scenario
        FINAL_BUDGET = (
            budget_data[prog]["Min Budget"]
            if setting == "loose"
            else int(no_of_preserved_testfiles / numOfTCS * 100)
        )

        print("Computed Final Budget: ", FINAL_BUDGET)

        algo_data = {}
        for algo in ["FAST++", "FAST-all", "FAST-CS", "FAST-pw"]:
            # Max Detects from 1 to repetition
            max_detects = 0
            max_detects_line_no = []
            max_detects_test_files = []
            max_failed_detects_test_files = []
            max_repetition = 0
            max_false_detects_line_no = []
            max_false_detects_test_files = []
            max_detects_redundant_deleted_tests = 0

            # Metrics
            total_execution = []
            total_preparation = []
            optimal_execution = 0
            optimal_preparation = 0

            for i in range(1, REPEATS + 1):
                # selection_path = "{}/{}-{}-{}.pickle".format(
                #     selection_dir, algo, FINAL_BUDGET, REPEATS
                # )
                # measurement_path = "{}/{}-{}-{}.pickle".format(
                #     measurement_dir, algo, FINAL_BUDGET, REPEATS
                # )
                selection_path = "{}/{}-{}-{}.pickle".format(
                    selection_dir, algo, FINAL_BUDGET, i
                )
                measurement_path = "{}/{}-{}-{}.pickle".format(
                    measurement_dir, algo, FINAL_BUDGET, i
                )

                if not os.path.exists(selection_path):
                    continue

                # Get metrics: execution and preparation time
                with open(measurement_path, "rb") as pickle_file:
                    metrics_data = pickle.load(pickle_file)
                    # Add total execution and preparation time
                    total_preparation.append(metrics_data[0])
                    total_execution.append(metrics_data[1])

                with open(selection_path, "rb") as pickle_file:
                    reduced_testfiles_line_no = pickle.load(pickle_file)

                # Check if removed testfile from parent commit exists in reduced testsuite
                # Increase no. of detected deleted testfiles if does not exist
                no_of_detected_deleted_testfiles = 0
                detected_deleted_testfiles_line_no = []
                detected_deleted_testfiles = []
                failed_detected_deleted_testfiles = []

                no_of_detected_deleted_obsolete_tests = 0
                no_of_detected_deleted_redundant_tests = 0

                # Detected redundant tests; not present in reduced test suite
                redundant_tests_line_no = []
                redundant_tests = []
                for idx in range(1, numOfTCS + 1):
                    if idx not in reduced_testfiles_line_no:
                        redundant_tests_line_no.append(idx)
                        redundant_tests.append(
                            get_test_filename_by_line_no(prog, commit, idx)
                        )

                for deleted_each_testfiles_line_no in deleted_testfiles_line_no_history:
                    # Check if deleted test file exist in reduced test suite; hit if does not exist, miss if exist
                    if deleted_each_testfiles_line_no not in reduced_testfiles_line_no:
                        no_of_detected_deleted_testfiles += 1
                        detected_deleted_testfiles_line_no.append(
                            deleted_each_testfiles_line_no
                        )
                        filename = get_test_filename_by_line_no(
                            prog, commit, deleted_each_testfiles_line_no
                        )
                        detected_deleted_testfiles.append(filename)

                        # Calculate number of redundant tests detected
                        detected_deleted_redundant_tests_df = get_redundant_deleted_testcases_by_project_and_removed_filepath(
                            prog, commit, filename
                        )
                        no_of_detected_deleted_redundant_tests += len(
                            detected_deleted_redundant_tests_df
                        )
                    else:
                        failed_detected_deleted_testfiles.append(
                            get_test_filename_by_line_no(
                                prog, commit, deleted_each_testfiles_line_no
                            )
                        )

                # Select the Max detection repetition step among 1 to repetitions
                if no_of_detected_deleted_testfiles > max_detects:
                    max_detects = no_of_detected_deleted_testfiles
                    max_detects_line_no = detected_deleted_testfiles_line_no
                    max_detects_test_files = detected_deleted_testfiles
                    max_failed_detects_test_files = failed_detected_deleted_testfiles
                    max_repetition = i
                    max_detects_redundant_deleted_tests = (
                        no_of_detected_deleted_redundant_tests
                    )

                    # False detects is (detected redundant_testfiles - deleted_testfiles)
                    max_false_detects_line_no = list(
                        set(redundant_tests_line_no).difference(
                            set(deleted_testfiles_line_no_history)
                        )
                    )
                    max_false_detects_test_files = [
                        get_test_filename_by_line_no(prog, commit, i)
                        for i in max_false_detects_line_no
                    ]

                    # Get optimal preparation and execution time
                    optimal_execution = metrics_data[0]
                    optimal_preparation = metrics_data[1]

            reduction_info = {
                "Total Detected Deleted Testfiles": max_detects,
                "Total Failed To Detect Deleted Testfiles": (
                    no_of_deleted_testfiles - max_detects
                ),
                "Detected Testfiles Line No": max_detects_line_no,
                "Detected Testfiles": max_detects_test_files,
                "Failed Detected Testfiles": max_failed_detects_test_files,
                "False Detected Testfiles Line No": max_false_detects_line_no,
                "False Detected Testfiles": max_false_detects_test_files,
                "Total Detected Deleted Redundant Tests": max_detects_redundant_deleted_tests,
                "Max_repetition": max_repetition,
                "Total execution time": fsum(total_execution),
                "Total preparation time": fsum(total_preparation),
                "Optimal execution time": optimal_execution,
                "Optimal preparation time": optimal_preparation,
            }
            algo_data[algo] = reduction_info

        analyzer_data["details"].append(
            {
                "Parent": commit,
                "Total Testfiles": numOfTCS,
                "Total Deleted Testfiles": no_of_deleted_testfiles,
                "Deleted Testfiles": deleted_testfiles,
                "Total Preserved Testfiles": no_of_preserved_testfiles,
                "Computed Final Budget": FINAL_BUDGET,
                "Algorithm": algo_data,
            }
        )

        # handle both strict and loose setting
        setting_dir = "loose" if setting == "loose" else "strict"

        dir_path = f"./{ARTIFACTS_DIR}/{setting_dir}"
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
        f = open(f"{dir_path}/{prog}.json", "w")
        f.write(json.dumps(analyzer_data, indent=2))

    print("Looping each commit END")
