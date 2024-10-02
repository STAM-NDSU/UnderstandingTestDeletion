LOG_FILEPATH = "./app.log"
REDUNDANT_TESTS_DIR = "./inputs/redundant-tests"
TESTCASES_DIR = "./inputs/testcases"
RESULTS_DIR = "./results"
BUDGET_FILEPATH = "./artifacts/budget.json"
ARTIFACTS_DIR = "./artifacts"

# FAST-R algorithms used to reduce test suite
ALGOS = ["FAST++", "FAST-all", "FAST-CS", "FAST-pw"]

# In our study, we compute budget in two different setting
SETTINGS = ["loose", "strict"]

# Only 3 of the analyzed projects have developer deleted redundant tests removed along with whole file.
# FAST-R approaches are used to identify redundant test classes
# TODO: ADD ARTIFACT LINK
PROJECTS = [
    "commons-math",
    "joda-time",
    "pmd",
]

COMPILED_RESULTS_FILEPATH = "./artifacts/compiled_results.json"

# No. of times a test suite is reduced;
# Using the same value as used by authors of FAST-R algorithms
REPEATS = 50

deltest_PROJECTS_DIR = "../deltest/inputs/projects"
