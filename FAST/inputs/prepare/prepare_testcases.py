"""
This file compiles all testcases present in the parent commits of test deletion commit(TDC) in a single text file

For each parent commit, it first navigates to the project repository directory and then checkout a parent commit.
Then, it compiles all the testclasses present in a single text file for reduction.
"""

import sys

sys.path.append("../")

import os
from testdelbench.utils.utils import is_candidate_test_file, strip_commit_url
import json
from pathlib import Path
import pandas as pd
from functools import reduce
from FAST.config import (
    PROJECTS,
    TESTDELBENCH_PROJECTS_DIR,
    DELETED_TESTS_DIR,
    TESTCASES_DIR,
)

current_state = os.getcwd()

for project in PROJECTS:
    print("Project: ", project)
    REPO_PATH = f"{TESTDELBENCH_PROJECTS_DIR}/{project}"
    deleted_tests_filepath = Path(f"{DELETED_TESTS_DIR}/{project}.csv")
    if not os.path.exists(f"{REPO_PATH}"):
        print(
            "Error: path does not exit -> ",
            REPO_PATH,
        )
        break
    if not os.path.exists(f"{deleted_tests_filepath}"):
        print(
            "Error: path does not exit -> ",
            deleted_tests_filepath,
        )
        break

    deleted_tc_df = pd.read_csv(deleted_tests_filepath)
    stripped_parent_commits = deleted_tc_df["Parent"].map(strip_commit_url)
    commits_list = list(set(stripped_parent_commits))
    print("Commits to scan:", len(commits_list))

    all_commits_data = {}
    # Change directory to be target project repository
    os.chdir(REPO_PATH)
    # We are now inside the project directory
    for commit in commits_list:
        # Checkout to test deletion commit
        cmd = f"git checkout {commit}"
        os.system(cmd)

        print("Git checkout out: ", commit)

        global_testsuite_content = ""
        global_testsuite_history = {}
        line = 1
        for root, dirs, files in os.walk("./", topdown=False):
            for name in files:
                name = name.replace("$", "")
                if is_candidate_test_file(name):
                    if not os.path.exists(f"{os.path.join(root, name)}"):
                        print(
                            "Error: path does not exit -> ",
                            os.path.join(root, name),
                        )
                        break
                    with open(os.path.join(root, name), "r") as f:
                        content = ""
                        try:
                            content = f.read()
                        except Exception as e:
                            content = ""

                        if not content:
                            continue

                        content = (
                            content.replace("\n", "")
                            .replace("\t", "")
                            .replace("\r", "")
                        )
                        if global_testsuite_content:
                            global_testsuite_content = (
                                global_testsuite_content + "\n" + content
                            )
                        else:
                            global_testsuite_content = content
                        global_testsuite_history[os.path.join(root, name)] = line
                        line += 1

        print("File path")
        project_dir = f"{TESTCASES_DIR}/{project}"
        if not os.path.exists(project_dir):
            os.makedirs(project_dir)
        
        testsuite_path = f"{project_dir}/{project}-{commit}-ts.txt"
        testsuite_history_path = f"{project_dir}/{project}-{commit}-tsh.json"
        print(testsuite_history_path)

        f = open(testsuite_path, "w")
        f.write(global_testsuite_content)
        f = open(testsuite_history_path, "w")
        f.write(json.dumps(global_testsuite_history, indent=4))
    print("=========================")

    # Change back to original state;
    os.chdir(current_state)
    # We are now back to root repository
sys.stdout.close()
