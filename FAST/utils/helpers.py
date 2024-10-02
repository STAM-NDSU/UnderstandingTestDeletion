import os
from pathlib import Path
import pandas as pd
from FAST.utils.utils import parse_commit_as_hyperlink_by_project
from FAST.config import REDUNDANT_TESTS_DIR

print_info_for_TSR_called = dict()


def print_info_for_TSR(project, redundant_deleted_tc_with_whole_file_df):
    """Prints Information for Test Suite Reduction"""

    global print_info_for_TSR_called
    if project in print_info_for_TSR_called:
        return

    print(project)
    print(
        "Total unique parent commits with whole test file deletion (i.e original test suties): ",
        len(set(redundant_deleted_tc_with_whole_file_df["Parent"].tolist())),
    )
    print(
        "Total deleted whole test files: ",
        len(set(redundant_deleted_tc_with_whole_file_df["Filepath"].tolist())),
    )
    print(
        "Total deleted redundant tests: ",
        redundant_deleted_tc_with_whole_file_df.shape[0],
    )

    print_info_for_TSR_called[project] = True


def get_redundant_deleted_testcases_with_whole_file_df(project):
    redundant_tests_file_path = Path(f"{REDUNDANT_TESTS_DIR}/{project}.csv")
    if not os.path.exists(f"{redundant_tests_file_path}"):
        print(
            "Error: path does not exit -> ",
            redundant_tests_file_path,
        )
        exit()

    df = pd.read_csv(redundant_tests_file_path)
    redundant_deleted_tc_with_whole_file_df = df[df["Deleted With Whole File"] == "yes"]
    print_info_for_TSR(project, redundant_deleted_tc_with_whole_file_df)
    return redundant_deleted_tc_with_whole_file_df


def get_whole_file_redundant_test_deletion_parent_commits(project):
    redundant_deleted_tc_df = get_redundant_deleted_testcases_with_whole_file_df(
        project
    )
    commits_list = list(set(list(redundant_deleted_tc_df["Parent"])))
    return commits_list


def get_deleted_redundant_testfiles_in_test_deletion_commit_parent(
    project, parent_commit
):
    redundant_deleted_tc_df = get_redundant_deleted_testcases_with_whole_file_df(
        project
    )
    # Note: Input redundant tests file has unparsed commit
    # parsed_commit = parse_commit_as_hyperlink_by_project(project, parent_commit)
    # redundant_deleted_tc_in_commit_df = redundant_deleted_tc_df[
    #     redundant_deleted_tc_df["Parent"] == parsed_commit
    # ]
    redundant_deleted_tc_in_commit_df = redundant_deleted_tc_df[
        redundant_deleted_tc_df["Parent"] == parent_commit
    ]
    classes_deleted = list(set(list(redundant_deleted_tc_in_commit_df["Filepath"])))
    return classes_deleted


def get_no_of_deleted_redundant_testfiles_in_test_deletion_commit_parent(
    project, parent_commit
):
    classes_deleted = get_deleted_redundant_testfiles_in_test_deletion_commit_parent(
        project, parent_commit
    )
    return len(classes_deleted)


def get_redundant_deleted_testcases_by_project_and_removed_filepath(
    project, commit, filepath
):
    validated_tests_file_path = Path(f"{REDUNDANT_TESTS_DIR}/{project}.csv")
    if not os.path.exists(f"{validated_tests_file_path}"):
        print(
            "Error: path does not exit -> ",
            validated_tests_file_path,
        )

    df = pd.read_csv(validated_tests_file_path)

    # Note: Input redundant tests file has unparsed commit
    # parsed_commit = parse_commit_as_hyperlink_by_project(project, commit)
    # redundant_deleted_tc_commit_df = df[df["Parent"] == parsed_commit]

    redundant_deleted_tc_commit_df = df[df["Parent"] == commit]

    # Remove "./" from filepath to match records in deltest csv file
    filepath_csv = filepath[2:]
    redundant_deleted_tc_with_whole_file_df = redundant_deleted_tc_commit_df[
        redundant_deleted_tc_commit_df["Filepath"] == filepath_csv
    ]
    return redundant_deleted_tc_with_whole_file_df
