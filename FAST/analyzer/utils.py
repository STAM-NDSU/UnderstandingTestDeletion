import sys

sys.path.append("../")

from FAST.utils.utils import *
import json
from FAST.config import TESTCASES_DIR


def get_line_no_history_testfiles(program, commit, testfiles):
    testcase_history_file_path = "{}/{}/{}-{}-tsh.json".format(
        TESTCASES_DIR, program, program, commit
    )
    testcase_history = json.load(open(testcase_history_file_path))
    line_no = []
    for testfile in testfiles:
        testfilepath = "./" + testfile

        if testfilepath in testcase_history:
            line_no.append(testcase_history[testfilepath])
        else:
            print("Test file with line no file not found in TSH JSON")
            print(testfile, testfilepath, program, commit)
    return line_no


def get_test_filename_by_line_no(program, commit, line_no):
    testcase_history_file_path = "{}/{}/{}-{}-tsh.json".format(
        TESTCASES_DIR, program, program, commit
    )
    testcase_history = json.load(open(testcase_history_file_path))

    # list out keys and values separately
    key_list = list(testcase_history.keys())
    val_list = list(testcase_history.values())

    # key with matching value
    position = val_list.index(line_no)
    return key_list[position]


def get_no_of_testfiles_in_commit(
    program,
    commit,
):
    testcase_file = "{}/{}/{}-{}-ts.txt".format(TESTCASES_DIR, program, program, commit)
    numOfTCS = sum((1 for _ in open(testcase_file)))
    return numOfTCS
