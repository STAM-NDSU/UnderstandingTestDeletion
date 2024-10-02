import os
from enum import Enum
import inflection
from datetime import datetime
from deltest.config.branch import Branch
from deltest.config.remote_base_url import RemoteBaseUrl

# Root directory for deltest
ROOT_DIR = "./"
# Name of the project
PROJECT = os.getenv("PROJECT", "gson")
# Url to local repository project
REPO_PATH = f"./inputs/projects/{PROJECT}"
# Branch of the repository to be analyzed
TARGET_BRANCH = Branch[inflection.underscore(PROJECT)].value
# Url to remote repository
COMMIT_BASE_URL = RemoteBaseUrl[inflection.underscore(PROJECT)].value
# Should the artifacts be exported
HANDLE_EXPORT = True
# Directory where aritfacts files are stored
ARTIFACTS_DIR = "./artifacts"
# Directory where generated files of projects is stored
RESULTS_DIR = "./results"
# Specific directory where generated csv file is stored for a project
OUTPUT_DIR = f"{RESULTS_DIR}/{PROJECT}"
# Filename of generated csv file
STEP = os.getenv("STEP", "step1")
OUTPUT_FILENAME = PROJECT + "-" + STEP + ".csv"

# We have used Refactoring Minor(https://github.com/tsantalis/RefactoringMiner) to filter out refactored tests and generate a json file
# Configure path to generated json file.
REFACTOR_FILE = f"./inputs/RefactoringMiner/artifacts/{PROJECT}.json"

# Valid java file extensions
JAVA_FILE_EXT = [".java"]

# File headers for generated csv files during different steps
CSV_HEADERS = [
    "Datetime",
    "Hash",
    "Parent",
    "Author",
    "Commit Msg",
    "Filepath",
    "Filename",
    "Removed Test Case",
]

# Date format
DATE_FORMAT = "%m/%d/%Y"

# Datetime formart; Used in generated csv files of each steps
DATETIME_FORMAT = "%m/%d/%Y %H:%M:%S"

# Commit Datetime Range considered to the study
start_date, end_date = "01/01/2001", "01/01/2023"
COMMIT_START_DATETIME = datetime.strptime(start_date, DATE_FORMAT)
COMMIT_END_DATETIME = datetime.strptime(end_date, DATE_FORMAT)
