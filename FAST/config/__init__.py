LOG_FILEPATH = "./app.log"
DELETED_TESTS_DIR = "./inputs/deleted-tests"
TESTCASES_DIR = "./inputs/testcases"
RESULTS_DIR = "./results"
BUDGET_FILEPATH = "./artifacts/budget.json"
ARTIFACTS_DIR = "./artifacts"

# FAST-R algorithms used to reduce test suite
ALGOS = ["FAST++", "FAST-all", "FAST-CS", "FAST-pw"]

# In our study, we compute budget in two different setting
SETTINGS = ["loose", "strict"]

# Projects analyzed in the study
PROJECTS = [
    "commons-lang",
    "gson",
    "commons-math",
    "jfreechart",
    "joda-time",
    "pmd",
    "cts",
]

COMPILED_RESULTS_FILEPATH = "./artifacts/compiled_results.json"

# No. of times a test suite is reduced;
# Using the same value as used by authors of FAST-R algorithms
REPEATS = 50

TESTDELBENCH_PROJECTS_DIR = "../testdelbench/inputs/projects"
