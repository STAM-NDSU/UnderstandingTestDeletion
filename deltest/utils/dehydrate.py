""" 
This utility file prettifies csv files generated for all the steps of deltest 
for all the projects. Thus, prevents congestion of data during manual inspection for easier reading.

This utility file removes redundant commit information such as messgae,
datetime etc for individual cadidate deleted tests in the csv files to allow 
and faster inspection.
"""

import sys

sys.path.append("../")

import os.path
from pathlib import Path
import pandas as pd

from deltest.config import RESULTS_DIR

PROJECT_ARTIFACTS = [
    {
        "project": "pmd",
        "filename": [
            "hydrated_pmd-step1",
            "hydrated_pmd-step2",
            "hydrated_pmd-step3",
        ],
    },
    {
        "project": "commons-math",
        "filename": [
            "hydrated_commons-math-step1",
            "hydrated_commons-math-step2",
            "hydrated_commons-math-step3",
        ],
    },
    {
        "project": "commons-lang",
        "filename": [
            "hydrated_commons-lang-step1",
            "hydrated_commons-lang-step1_refined",
            "hydrated_commons-lang-step2",
            "hydrated_commons-lang-step3",
        ],
    },
    {
        "project": "joda-time",
        "filename": [
            "hydrated_joda-time-step1",
            "hydrated_joda-time-step1_refined",
            "hydrated_joda-time-step2",
            "hydrated_joda-time-step3",
        ],
    },
    {
        "project": "gson",
        "filename": [
            "hydrated_gson-step1",
            "hydrated_gson-step2",
            "hydrated_gson-step3",
        ],
    },
    {
        "project": "jfreechart",
        "filename": [
            "hydrated_jfreechart-step1",
            "hydrated_jfreechart-step2",
            "hydrated_jfreechart-step3",
        ],
    },
    {
        "project": "cts",
        "filename": [
            "hydrated_cts-step1",
            "hydrated_cts-step1_refined",
            "hydrated_cts-step2",
            "hydrated_cts-step3",
        ],
    },
]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usuage: python tools/dehydrate.py <project>")
        sys.exit(1)

    script, project = sys.argv

    # Get the project artifacts info
    project_info = list(
        filter(lambda each: each["project"] == project, PROJECT_ARTIFACTS)
    )[0]

    if not project_info:
        print("Please specify the project correctly. ")
        print("And, please ensure all preceding steps are perfomed in correct order.")

    for file in project_info["filename"]:
        file_path = Path(f"{RESULTS_DIR}/{project}/{file}.csv")

        if not os.path.exists(f"{file_path}"):
            print(f"{file_path} does not exist")
            continue

        with open(file_path, "r") as a:
            df = pd.read_csv(f"{file_path}")
            prev = {
                "Datetime": None,
                "Hash": None,
                "Parent": None,
                "Author": None,
                "Commit Msg": None,
                "Filepath": None,
                "Filename": None,
                "Removed Test Case": None,
            }

            for index, row in df.iterrows():
                if index == 0:
                    prev = {
                        "Datetime": row["Datetime"],
                        "Commit Msg": row["Commit Msg"],
                        "Hash": row["Hash"],
                        "Parent": row["Parent"],
                        "Author": row["Author"],
                        "Filepath": row["Filepath"],
                        "Filename": row["Filename"],
                        "Removed Test Case": row["Removed Test Case"],
                    }

                else:
                    if row["Hash"] == prev["Hash"]:
                        row["Hash"] = ""
                        row["Parent"] = ""
                        row["Author"] = ""
                        row["Commit Msg"] = ""
                        row["Datetime"] = ""

                        if row["Filepath"] == prev["Filepath"]:
                            row["Filepath"] = ""
                            row["Filename"] = ""
                        else:
                            prev["Filepath"] = row["Filepath"]
                            prev["Filename"] = row["Filename"]

                    else:
                        prev["Hash"] = row["Hash"]
                        prev["Parent"] = row["Parent"]
                        prev["Datetime"] = row["Datetime"]
                        prev["Commit Msg"] = prev["Commit Msg"]
                        prev["Filepath"] = row["Filepath"]
                        prev["Filename"] = row["Filename"]

            filename = file.replace("hydrated_", "")
            df.to_csv(f"{RESULTS_DIR}/{project}/{filename}.csv", index=False)
            print(f"Generated {RESULTS_DIR}/{project}/{filename}.csv")
