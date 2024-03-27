import sys
import os

sys.path.append("../")

# Set project and step from cmd into env variables
if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usuage: python tools/testdel.py <project> <step>")
        sys.exit(1)

    script, project, step = sys.argv
    os.environ["PROJECT"] = project
    os.environ["STEP"] = step


from testdelbench.utils.helpers import export_to_csv
from testdelbench.analyzer.analyzer import get_removed_test_functions_details
from testdelbench.utils.utils import *
from testdelbench.config import (
    PROJECT,
    REPO_PATH,
    TARGET_BRANCH,
    OUTPUT_DIR,
    OUTPUT_FILENAME,
    STEP,
    CSV_HEADERS,
    HANDLE_EXPORT,
    REFACTOR_FILE,
)
import json
import traceback
from pathlib import Path
import pandas as pd


repo_path = REPO_PATH
target_branch = TARGET_BRANCH
if not repo_path or not target_branch:
    print("Please configure project details correctly.")
else:
    print(f"Repository Path: {repo_path}")
    try:
        # Get candidate test deletion commits
        if STEP == "step1":
            results = get_removed_test_functions_details(
                repo_path, target_branch, step=1, previous_step_df=None
            )

            if HANDLE_EXPORT == True:
                headers = CSV_HEADERS
                export_to_csv(
                    headers=CSV_HEADERS,
                    records=results,
                    dir=OUTPUT_DIR,
                    filename="hydrated_" + OUTPUT_FILENAME,
                )
        # Get candidate deleted tests and refine candidate test deletion commits
        elif STEP == "step2":
            print("Start step 2-------")
            file_path = Path(f"{OUTPUT_DIR}/hydrated_{PROJECT}-step1.csv")
            refined_file_path = Path(
                f"{OUTPUT_DIR}/hydrated_{PROJECT}-step1_refined.csv"
            )

            # Check if step 1 file is refined for the project [Use refined file if available]
            if not os.path.exists(file_path):
                print("Files from step 1 do not exist.")
                print("Please perfrom step 1 before perfoming to step 2.")
                exit(1)

            # Use refined step 1 file for commons-lang, joda-time and cts
            if project in ["commons-lang", "joda-time", "cts"]:
                if not os.path.exists(refined_file_path):
                    print(
                        f"Refined file from step 1 does not exits for project {project}"
                    )
                    print(f"Please execute: python tools/refine_step1.py {project}")
                    exit(1)
                else:
                    file_path = refined_file_path

            with open(file_path, "r") as a:
                step1_hydrated_df = pd.read_csv(f"{file_path}")
                print(
                    "Total rows in step1 csv file: " + str(step1_hydrated_df.shape[0])
                )

                step2_df = get_removed_test_functions_details(
                    repo_path,
                    target_branch,
                    step=2,
                    previous_step_df=step1_hydrated_df,
                )

                if HANDLE_EXPORT == True:
                    step2_df.to_csv(
                        f"{OUTPUT_DIR}/hydrated_{PROJECT}-step2.csv",
                        index=False,
                    )
                    print(
                        f"Successfully generated {OUTPUT_DIR}/hydrated_{PROJECT}-step2.csv"
                    )
                print("------- END step 2")

        # Filter our refactored test cases [suggested by RefMiner]
        elif STEP == "step3":
            print("Start step 3-------")
            refactoring_file = open(REFACTOR_FILE)
            refactorings_data = json.load(refactoring_file)["commits"]

            file_path = Path(f"{OUTPUT_DIR}/hydrated_{PROJECT}-step2.csv")
            with open(file_path, "r") as a:
                df = pd.read_csv(f"{file_path}")
                new_df = pd.DataFrame()

                for index, row in df.iterrows():
                    is_refactor = False
                    testcase_filename = row["Filename"]
                    testcase_hash = strip_commit_url(row["Hash"])
                    testcase_name = str(row["Removed Test Case"])
                    # TO FIX: gson issue "string as left operand, not float in 'in each["codeElement"]'"
                    testcase_filepath = row["Filepath"]

                    # refactors_commit_data = list(filter(lambda each: each["sha1"] == commit.hash, repo_refactors))[0]
                    refactors_commit_data = next(
                        (
                            each
                            for each in refactorings_data
                            if each["sha1"] == testcase_hash
                        ),
                        None,
                    )

                    refactors_commit = (
                        refactors_commit_data["refactorings"]
                        if not refactors_commit_data is None
                        else []
                    )

                    # Check if testcase is refactored [e.g Rename Method - method is refactored]
                    for refactor in refactors_commit:
                        for each in refactor["leftSideLocations"]:
                            if (
                                each["codeElement"]
                                and (testcase_name in each["codeElement"])
                                and (testcase_filepath == each["filePath"])
                            ):
                                is_refactor = True
                                break

                    # Check if test class is renamed [e.g Rename Class- all methods are refactored]
                    if not is_refactor:
                        for refactor in refactors_commit:
                            if refactor["type"] == "Rename Class":
                                for each in refactor["leftSideLocations"]:
                                    if each["codeElement"] and (
                                        testcase_filepath == each["filePath"]
                                    ):
                                        is_refactor = True
                                        break

                    # Append only testcases not refactored
                    if not is_refactor:
                        new_df = pd.concat(
                            [new_df, pd.DataFrame([row])], ignore_index=True
                        )

                        # Deprecated: Used before pandas v2.0
                        # new_df.loc[len(new_df)] = row
                        # new_df = new_df.append(row, ignore_index=True)

                if HANDLE_EXPORT == True:
                    new_df.to_csv(
                        f"{OUTPUT_DIR}/hydrated_{OUTPUT_FILENAME}",
                        index=False,
                    )
                    print(
                        f"Successfully generated {OUTPUT_DIR}/hydrated_{OUTPUT_FILENAME}"
                    )

            refactoring_file.close()
            print("------- End step 3")

    except Exception as e:
        print(f"Error occurred: {type(e).__name__}")
        # print(e)
        traceback.print_exc()
