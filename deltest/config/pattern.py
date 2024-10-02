from enum import Enum


class Pattern(str, Enum):
    # Define useful regular patterns
    JAVA_FILENAME = "*.java"
    # TEST_FILENAME = "^(.*)Test(.*).java$" # contains Test in the filename
    TEST_FILENAME = "^Test(.*).java$|(.*)Test.java"  # contains Test at the beginning or at the end in the filename
    TEST_FUNCTION = (
        "([ \t]*)(public)([ \t\n\r]*)([a-zA-Z0-9<>._?, ]+)([ \t\n\r]*)test([a-zA-Z0-9_]+)"
        "([ \t\n\r]*)\\("
    )
    TEST_FUNCTION2 = (
        "([ \t]*)@Test(.*?)([ \t\n\r]*)(([ \t]*)@(.*?)([ \t\n\r]*))*([ \t]*)(public)([ \t\n\r]*)([a-zA-Z0-9<>._?, ]+)([ \t\n\r\\-]*)([a-zA-Z0-9_]+)"
        "([ \t\n\r]*)\\("
    )
    REMOVED_TEST_FUNCTION = (
        "-([ \t]*)(public)([ \t\n\r\\-]*)([a-zA-Z0-9<>._?, ]+)([ \t\n\r\\-]*)test([a-zA-Z0-9_]+)"
        "([ \t\n\r\\-]*)\\("
    )
    REMOVED_TEST_FUNCTION2 = (
        "-([ \t]*)@Test(.*?)([ \t\n\r]*)(-([ \t]*)@(.*?)([ \t\n\r]*))*-([ \t]*)(public)([ \t\n\r\\-]*)([a-zA-Z0-9<>._?, ]+)([ \t\n\r\\-]*)([a-zA-Z0-9_]+)"
        "([ \t\n\r\\-]*)\\("
    )
    FUNCTION_NAME_AND_SIGNATURE = "([a-zA-Z0-9_]+)[ \t\n\r]*)([a-zA-Z0-9<>\\[\\]._?, \t\n\r\\+\\-]*\\)"  # can be for both added/deleted testcases
    TEST_FUNCTION_NAME = "test([a-zA-Z0-9_]+)([ \t]*)\\("
    FUNCTION_NAME_WITH_SPACE_BEFORE = " ([a-zA-Z0-9_]+)([ \t]*)\\("  # QUICK FIX FOR mutilple annotations before testcase issue
    FUNCTION_NAME = "([a-zA-Z0-9_]+)([ \t]*)\\("
