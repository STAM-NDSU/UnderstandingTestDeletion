usuage = """
USAGE: python3 tools/analyzer/compile_results.py 
"""

"""
This file compiles results computed across loose and stricts setting for 4 FAST-R algorithms
across all parent commits of test deletion commits
"""

import sys

sys.path.append("../")

import json
from math import fsum
import pandas as pd
import os
from datetime import timedelta
from FAST.config import (
    ARTIFACTS_DIR,
    PROJECTS,
    ALGOS,
    COMPILED_RESULTS_FILEPATH,
    REPEATS,
)
from FAST.utils.helpers import get_whole_file_test_deletion_parent_commits

data = {"strict": {}, "loose": {}}

for index, project in enumerate(PROJECTS):
    loose_file = open(f"{ARTIFACTS_DIR}/loose/{project}.json")
    strict_file = open(f"{ARTIFACTS_DIR}/strict/{project}.json")
    algo_analyzed_strict = json.load(strict_file)
    algo_analyzed_loose = json.load(loose_file)

    # Total parent commits taken into consideration for reduction using FAST-R
    total_parent_commits = len(get_whole_file_test_deletion_parent_commits(project))

    for index, algo in enumerate(ALGOS):

        def parse_results(setting):
            data_to_look = (
                algo_analyzed_strict if setting == "strict" else algo_analyzed_loose
            )

            total_detected = 0
            total_failed_to_detect = 0
            total_detected_deleted_and_redundant_tests = 0
            total_detected_deleted_and_obsolete_tests = 0

            # Takes into account all the 50 iterations for reducing test suite
            total_preparation_time = 0
            total_execution_time = 0
            total_avg_preparation_time = 0
            total_avg_execution_time = 0
            total_preparation_time_arr = []
            total_execution_time_arr = []

            # Takes into account only 1(optimal) iteration for reducing test suite
            total_optimal_preparation_time = 0
            total_optimal_execution_time = 0
            total_avg_optimal_preparation_time = 0
            total_avg_optimal_execution_time = 0
            total_optimal_preparation_time_arr = []
            total_optimal_execution_time_arr = []

            for algo_analyzed_commit in data_to_look["details"]:
                alog_analyzed_commit_each_algo = algo_analyzed_commit["Algorithm"][algo]

                total_detected += alog_analyzed_commit_each_algo[
                    "Total Detected Deleted Testfiles"
                ]
                total_failed_to_detect += alog_analyzed_commit_each_algo[
                    "Total Failed To Detect Deleted Testfiles"
                ]

                # Takes into account all the 50 iterations for reducing test suite
                total_preparation_time_arr.append(
                    round(alog_analyzed_commit_each_algo["Total preparation time"], 3)
                )
                total_execution_time_arr.append(
                    round(alog_analyzed_commit_each_algo["Total execution time"], 3)
                )

                # Takes into account only 1(optimal) iteration for reducing test suite
                total_optimal_preparation_time_arr.append(
                    round(alog_analyzed_commit_each_algo["Optimal preparation time"], 3)
                )
                total_optimal_execution_time_arr.append(
                    round(alog_analyzed_commit_each_algo["Optimal execution time"], 3)
                )

                total_failed_to_detect += alog_analyzed_commit_each_algo[
                    "Total Failed To Detect Deleted Testfiles"
                ]

                # # Total detected deleted obsolete and redundant tests
                total_detected_deleted_and_obsolete_tests += (
                    alog_analyzed_commit_each_algo[
                        "Total Detected Deleted And Obsolete Tests"
                    ]
                )
                total_detected_deleted_and_redundant_tests += (
                    alog_analyzed_commit_each_algo[
                        "Total Detected Deleted And Redundant Tests"
                    ]
                )

            total_preparation_time = fsum(
                total_preparation_time_arr,
            )
            total_execution_time = fsum(
                total_execution_time_arr,
            )
            # Takes into account total repeats i.e default 50 iterations for reducing test suite for all parent commits
            total_avg_preparation_time = total_preparation_time / (
                total_parent_commits * REPEATS
            )
            total_avg_execution_time = total_execution_time / (
                total_parent_commits * REPEATS
            )

            # Takes into account only 1(optimal) iteration for reducing test suite
            total_optimal_preparation_time = fsum(
                total_optimal_preparation_time_arr,
            )
            total_optimal_execution_time = fsum(
                total_optimal_execution_time_arr,
            )
            total_avg_optimal_preparation_time = total_optimal_preparation_time / (
                total_parent_commits
            )
            total_avg_optimal_execution_time = total_optimal_execution_time / (
                total_parent_commits
            )

            if project not in data[setting]:
                data[setting][project] = {}

            data[setting][project][algo] = (
                {
                    "Total Detected Deleted Testfiles": total_detected,
                    "Total Failed To Detect Deleted Testfiles": total_failed_to_detect,
                    "Total Detected Deleted And Obsolete Tests": total_detected_deleted_and_obsolete_tests,
                    "Total Detected Deleted And Redundant Tests": total_detected_deleted_and_redundant_tests,
                    "Total Preparation Time": str(
                        timedelta(seconds=total_preparation_time)
                    ),
                    "Total Execution Time": str(
                        timedelta(seconds=total_execution_time)
                    ),
                    "Total Avg Preparation Time": str(
                        timedelta(seconds=total_avg_preparation_time)
                    ),
                    "Total Avg Execution Time": str(
                        timedelta(seconds=total_avg_execution_time)
                    ),
                    "Total Optimal Preparation Time": str(
                        timedelta(seconds=total_preparation_time)
                    ),
                    "Total Optimal Execution Time": str(
                        timedelta(seconds=total_execution_time)
                    ),
                    "Total Avg Optimal Preparation Time": str(
                        timedelta(seconds=total_avg_optimal_preparation_time)
                    ),
                    "Total Avg Optimal Execution Time": str(
                        timedelta(seconds=total_avg_optimal_execution_time)
                    ),
                    "Total Avg Optimal Preparation Time(U)": str(
                        timedelta(
                            seconds=total_avg_optimal_preparation_time
                        ).microseconds
                    ),
                    "Total Avg Optimal Execution Time(U)": str(
                        timedelta(seconds=total_avg_optimal_execution_time).microseconds
                    ),
                    "Total Avg Optimal Time(U)": str(
                        timedelta(
                            seconds=(
                                total_avg_optimal_preparation_time
                                + total_avg_optimal_execution_time
                            )
                        ).microseconds
                    ),
                },
            )

        # Handle strict scenario
        parse_results("loose")
        # Handle loose scenario
        parse_results("strict")


f = open(f"{COMPILED_RESULTS_FILEPATH}", "w")
f.write(json.dumps(data, indent=2))
print("Sucessfully generated compiled results at " + COMPILED_RESULTS_FILEPATH)
