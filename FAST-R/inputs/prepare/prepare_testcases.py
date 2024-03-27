"""
Compiles all testcases present in the parent commits of test deletion commit in a single test history file
"""

import sys

sys.path.append("../../")

import os
import importlib
from testdelbench.utils.utils import is_candidate_test_file, strip_commit_url
from testdelbench.config import REPO_PATH
import json
from pathlib import Path
import pandas as pd
from functools import reduce

config = importlib("FAST-R/config")


OUTPUT_DIR = "./testcases"
DELETED_TESTS_DIR = "./deleted-tests"
current_state = os.getcwd()

for project in config.PROJECTS:
    print("Project: ", project)
    print(REPO_PATH)
    validated_tests_file_path = Path(f"{DELETED_TESTS_DIR}/{project}.csv")
    if not os.path.exists(f"{REPO_PATH}"):
        print(
            "Error: path does not exit -> ",
            REPO_PATH,
        )
        break
    if not os.path.exists(f"{validated_tests_file_path}"):
        print(
            "Error: path does not exit -> ",
            validated_tests_file_path,
        )
        break

    df = pd.read_csv(validated_tests_file_path)
    deleted_tc_df = df[df["Final Results"] == "yes"]
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
                print(name, dirs, root)
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

        print(all_commits_data)
        print("File path")
        print(OUTPUT_DIR + "/" + project + "-" + commit + "-ts.txt")
        f = open(
            OUTPUT_DIR + "/" + project + "-" + commit + "-ts.txt",
            "w",
        )
        f.write(global_testsuite_content)
        f = open(
            OUTPUT_DIR + "/" + project + "-" + commit + "-tsh.json",
            "w",
        )
        f.write(json.dumps(global_testsuite_history, indent=4))
    print("=========================")

    # Change back to original state;
    os.chdir(current_state)
    # We are now back to root repository
sys.stdout.close()
