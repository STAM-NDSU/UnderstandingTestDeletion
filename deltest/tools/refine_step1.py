"""
This utility file help to refine the result output file from the step 1 for 
projects commons-lang, joda-time and cts.
The refined output file is then used as input file for next step i.e step 2
"""

import sys

sys.path.append("../")

import os.path
from pathlib import Path
import pandas as pd
from deltest.config import RESULTS_DIR
from deltest.utils.utils import (
    parse_commit_hash_by_project,
    get_change_id_from_commit_msg,
)

# For commons-lang and joda-time filter out manually identified outliers commits from candidate test deletion commits
# which have abnormal test deletions (near or more than thousands of tests
# For cts, we identify a pattern in which there are many redundant commits which have different commit hash
# but similar change history. We filter them out commits that explictly mention "merged from" or "Change-Id"  in the commit msg
# We identify commits of these nature as false candidate test deletion commits through manual inspection

OUTLIER_COMMITS = {
    "commons-lang": [
        "4f3b6e55f86c8b59ea9b3991ca055c3905eb05a1",
    ],
    "joda-time": ["72b22654962284bac59c2777131b42a2d1f53228"],
}

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usuage: python tools/refine_step1.py <project>")
        sys.exit(1)

    script, project = sys.argv

    if project not in ["commons-lang", "joda-time", "cts"]:
        print("Good News!!! You can proceed to step 2.")
        exit(1)

    input_file_path = Path(f"{RESULTS_DIR}/{project}/hydrated_{project}-step1.csv")
    output_file_path = Path(
        f"{RESULTS_DIR}/{project}/hydrated_{project}-step1_refined.csv"
    )

    if not os.path.exists(f"{input_file_path}"):
        print(f"File does not exist: {input_file_path}")
        exit(1)

    df = pd.read_csv(f"{input_file_path}")
    print("Start Size:", df.shape)
    df = df.iloc[:, 0:11]

    if project != "cts":
        to_ignore_commits = list(
            map(
                lambda each: parse_commit_hash_by_project(
                    project,
                    each,
                ),
                OUTLIER_COMMITS[project],
            )
        )
        print(to_ignore_commits)
        df = df[~df["Hash"].isin(to_ignore_commits)]

    else:
        # Check for duplicated change id
        print("Step: 1")
        unique_changeid = []
        unique_changeid_hash = []
        to_be_dropped_commit_hash = []
        for index, row in df.iterrows():
            if "Change-Id: " in row["Commit Msg"]:
                change_id = get_change_id_from_commit_msg(row["Commit Msg"])
                # print(change_id)
                if change_id in unique_changeid:
                    if row["Hash"] in unique_changeid_hash:
                        pass
                    else:
                        if row["Hash"] not in to_be_dropped_commit_hash:
                            to_be_dropped_commit_hash.append(row["Hash"])
                else:
                    unique_changeid.append(change_id)

                    if row["Hash"] not in unique_changeid_hash:
                        unique_changeid_hash.append(row["Hash"])

        print("Commits to be dropped: ", len(to_be_dropped_commit_hash))

        for hash in to_be_dropped_commit_hash:
            to_be_dropped_index = df[(df["Hash"] == hash)].index
            df.drop(to_be_dropped_index, inplace=True)

        print("Step 1 Size:", df.shape)

        # Check for merged from
        print("Step: 2")
        to_be_dropped_commit_hash = []
        for index, row in df.iterrows():
            if "merged from:" in row["Commit Msg"]:
                if row["Hash"] not in to_be_dropped_commit_hash:
                    to_be_dropped_commit_hash.append(row["Hash"])

        print("Commits to be dropped: ", len(to_be_dropped_commit_hash))

        for hash in to_be_dropped_commit_hash:
            to_be_dropped_index = df[(df["Hash"] == hash)].index
            df.drop(to_be_dropped_index, inplace=True)

        print("Step 2 Size:", df.shape)

    # Finally export the refined dataframe
    print("Final Size:", df.shape)
    df.to_csv(f"{output_file_path}", index=False)
    print(f"Generated {output_file_path}")


for project in ["commons-lang", "joda-time", "cts"]:
    input_file_path = Path(f"{RESULTS_DIR}/{project}/hydrated_{project}-step1.csv")
    output_file_path = Path(
        f"{RESULTS_DIR}/{project}/hydrated_{project}-step1_refined.csv"
    )

    if not os.path.exists(f"{input_file_path}"):
        print(f"File does not exist: {input_file_path}")
        exit(1)

    df = pd.read_csv(f"{input_file_path}")
    print("Start Size:", df.shape)
    df = df.iloc[:, 0:11]

    if project != "cts":
        to_ignore_commits = list(
            map(
                lambda each: parse_commit_hash_by_project(
                    project,
                    each,
                ),
                OUTLIER_COMMITS[project],
            )
        )
        print(to_ignore_commits)
        df = df[~df["Hash"].isin(to_ignore_commits)]

    else:
        # Check for duplicated change id
        print("Step: 1")
        unique_changeid = []
        unique_changeid_hash = []
        to_be_dropped_commit_hash = []
        for index, row in df.iterrows():
            if "Change-Id: " in row["Commit Msg"]:
                change_id = get_change_id_from_commit_msg(row["Commit Msg"])
                # print(change_id)
                if change_id in unique_changeid:
                    if row["Hash"] in unique_changeid_hash:
                        pass
                    else:
                        if row["Hash"] not in to_be_dropped_commit_hash:
                            to_be_dropped_commit_hash.append(row["Hash"])
                else:
                    unique_changeid.append(change_id)

                    if row["Hash"] not in unique_changeid_hash:
                        unique_changeid_hash.append(row["Hash"])

        print("Commits to be dropped: ", len(to_be_dropped_commit_hash))

        for hash in to_be_dropped_commit_hash:
            to_be_dropped_index = df[(df["Hash"] == hash)].index
            df.drop(to_be_dropped_index, inplace=True)

        print("Step 1 Size:", df.shape)

        # Check for merged from
        print("Step: 2")
        to_be_dropped_commit_hash = []
        for index, row in df.iterrows():
            if "merged from:" in row["Commit Msg"]:
                if row["Hash"] not in to_be_dropped_commit_hash:
                    to_be_dropped_commit_hash.append(row["Hash"])

        print("Commits to be dropped: ", len(to_be_dropped_commit_hash))

        for hash in to_be_dropped_commit_hash:
            to_be_dropped_index = df[(df["Hash"] == hash)].index
            df.drop(to_be_dropped_index, inplace=True)

        print("Step 2 Size:", df.shape)

    # Finally export the refined dataframe
    print("Final Size:", df.shape)
    df.to_csv(f"{output_file_path}", index=False)
    print(f"Generated {output_file_path}")
