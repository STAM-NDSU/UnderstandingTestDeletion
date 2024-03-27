# UnderstandingTestDeletion

---

The artifact repository for the paper titled:

> Understanding Test Deletion in Continious Integgration  
> _Authors:_ Suraj Bhatta, Ajay Jha
> _Conference:_

In this paper, we create a benchmark of manually confirmed 24,431 deleted tests across 2,125 test deletion commits across 7 open-source projects. Additionally, we evaluate the effectiveness of FAST-R appraoches to identify developer deleted tests for permanent test deletion. The projects studied are [gson](https://github.com/google/gson.git), [commons-lang](https://github.com/apache/commons-lang.git), [commons-math](https://github.com/apache/commons-math.git), [pmd](https://github.com/pmd/pmd.git), [jfreechart](https://github.com/jfree/jfreechart.git), [joda-time](https://github.com/JodaOrg/joda-time.git) and [Android Compatibililty Test Suite (CTS)](https://android.googlesource.com/platform/cts).

## Directory Structure

---

The directory is structured as follows:

    UnderstandingTestDeletion/        This is the root directory of the repository.
    |
    |--- FAST/        Implementation of evaluation of FAST-R algorithms to identify developer deleted tests.
    |    |------ analyzer/      Scripts to analyze the generated reduced test suite and compute if algorithm can identify developer deleted tests
    |    |------ artifacts/
    |    |       |------ loose/     Analyzed results for FAST-R algorithms in loose setting
    |    |       |------ strict/    Analyzed results for FAST-R algorithms in strict setting
    |    |------ config/        Configuration files
    |    |------ inputs/
    |    |       |------ deleted-tests/     Test deletion commits and deleted tests information gatherd from deltestbench
    |    |       |------ prepare/   Scripts to prepare original test suites of parent commits of for reduction
    |    |       |------ testcases/     Original test suites of parent commits of test deletion commits prepared for redcution
    |    |------ results/
    |    |       |------ loose/     Reduced test-suites using FAST-R algorithms in loose setting
    |    |       |------ strict/    Reduced test-suites using FAST-R algorithms in strict setting
    |    |------ tools/     Scripts to execute via command
    |    |------ utils/     Utility and helper functions
    |
    |--- deltestbench/        Implementation of process to identify deleted tests and test deletion commits.
    |    |------ analyzer/    Core scripts to compute candidate test deletion commit and deleted tests
    |    |------ artifacts/   Compiled results from manual validation of candidate deleted tests
    |    |------ config/      Configuration files
    |    |------ inputs/
    |    |       |------ projects/     7 studied open-source projects downloaded locally
    |    |       |------ RefactoringMiner/
    |    |       |       |------ artifacts/     Refactorings identified for the projects under study using RefactoringMiner
    |    |------ results/       Candidate test deletion commits and candidate deleted tests generated for projects for across different steps
    |    |------ tools/     Scripts to execute via command
    |    |------ utils/     Utility and helper functions

### Contents

The repository is divided into two groups:

- **deltestbench** : It contains all the input, configuration, results, artifacts and script files used to identify deleted tests and test deletion commits.
- **FAST-R** : Similary, it contains all the files and configurations required to evaluate the effectiveness of FAST-R appraoches to identify developer deleted tests.

## Reproducing Results

---

1. **Install Python:** To run the project, python should be installed on your machine.
   Check if it is installed or not using following command:

```
   python --version
```

If it is not installed, download and install python from [here](https://www.python.org/downloads/).

2. **Clone the repository:** Download this repository using following command:

```
    git clone https://github.com/STAM-NDSU/UnderstandingTestDeletion
    cd UnderstandingTestDeletion
```

3. **Setup virtual environment (optional)**

```
    python3 -m venv venv
    source venv/bin/activate
```

4. **Install the requirements**

```
    pip install -r requirements.txt
```

### deltestbench

Please follow the given steps in correct order to identify test deletion commits and deleted tests from open-source projects under study.

**Steps:**

1. **Prepare input:**

- Please follow the instructions [here](/deltestbench/inputs/projects/README.md) to download the projects. Projects are required to be present in local machine for the other steps to run properly.
- Also, we filter out refactored tests using [RefactoringMiner](https://github.com/tsantalis/RefactoringMiner). Please follow the instructions [here](/deltestbench/inputs/RefactoringMiner/README.md) to run the RefactoringMiner on the downloaded projects and generate the csv file that contains identified refactors throughout the commit history of the project.

2. **Change directory to deltestbench:** From root directory, run the following command:

```
    cd deltestbench
```

3. **Generate Candidate Commits:** To generate candidate test deletion commits, run the following command:

```
    python tools/testdel.py <program> step1
```

**Note: Please replace program with the name of any of the 7 studied projects.**
The value of program should be either of `commons-lang`, `gson`, `commons-math`, `jfreechart`, `joda-time`, `pmd`, and `cts`.

For example:

```
    python tools/testdel.py gson step1
```

Executing this step will generate a csv file containing candidate test deletion commits inside [deltestbench/results/](/deltestbench/results/). The file will be presented inside the respective
specified `program` directory named as `{program}-step1.csv`.

**IMPORTANT: For projects commons-lang, joda-time and cts, we need to filter out outliers from candidate test deletionc commits. It refines the results of the preceding step and narrows down test deletion commits to be considered for identifying candidate deleted tests.**

Please run the following command:

```
    python tools/refine_step1.py <program>
```

Executing this commoand will generate a csv file named as `hydrated_<program>-step1_refined.csv`.

4. **Generate Candidate Deleted Tests:** To generate candidate deleted tests, run the following command:

```
    python tools/testdel.py <program> step2
```

**Note: Please ensure that you have executed command in Step 3 before running this command.**

Executing this step will generate a csv file containing candidate deleted tests inside [deltestbench/results/](/deltestbench/results/). The file will be presented inside the respective
specified `program` directory named as `hydrated_<program>-step2.csv`.

5. **Filter Refactored Tests:** To filter out refactored tests from candidate deleted tests, run the following command:

```
    python tools/testdel.py <program> step3
```

**Note: Please run commands in step 3 and 4 before executing this command. Also, ensure you have followed instruction [here](/deltestbench/inputs/RefactoringMiner/README.md) and placed artifacts file generated using RefactoringMiner inside [deltestbench/inputs](/deltestbench/inputs/RefactoringMiner/artifacts/) directory.**

Executing this step will filter out identified refactored tests from candidate deleted tests and generate a csv file inside [deltestbench/results/](/deltestbench/results/). The file will be presented inside the respective specified `program` directory named as `hydrated_<program>-step3.csv`.

6. **Manual Validation:** After filtering out the refactored tests from candidate deleted tests, we do the manual validation of the tests. The two authors of the paper did manual validation independently and then compiled the results resolving any disagreements. The results are present inside the [deltestbench/artifacts](/deltestbench/artifacts/) directory.
   In the csv file, the record with `Final Result` as `yes` indicates a manually confirmed developer deleted test.

### FAST-R

Please follow the given steps to evaluate FAST-R appraoches on developer deleted tests.

1. **Change directory to deltestbench:** From root directory, run the following command:

```
    cd FAST
```

2. **Prepare input:**

FAST-R alrogithms are used to reduce original test suite of parent commits of test deletion commits. For this, first of all we need to process
test classes present in the instance of parent commits of all the projects under study and compile into a single `text` file.

The original test suites of parent test deletion commits of all projects except `CTS` used for the reduction are present [here](/FAST/inputs/testcases/).
Due to large size of `text` file of CTS, we have not shipped the prepared test suite files with the repository. However, you can run following command locally
to generate test suites for the all the projects provided projects are downloaded and configured correctly following above steps in `testdelbench`.

```
    cd input/prepare/testcases.py
```

This generates compiled text file, for each parent test deletion commit, containing all of test classes present in the parent commit. Results are stored [here](/FAST/inputs/testcases/) on which FAST-R algorithms perform reduction.


`deleted-tests` repository contains the confirmed deleted tests and test deletion commits of each project obtained after performing all of the steps in `deltestbench` and manual validation. The files inside this repository are required to perfrom analysis in Step 6.

4. **Compute Budget for Loose Scenario:** Before performing reduction in loose setting, we need to calculate the budget i.e size of reduced test suite for the project. Run the following command to compute budget for all of the projects.

```
    python3 tools/loose_budget_calc.py 
```

You can configure projects to be considered for evaluation by changing `PROJECTS` in the config file [here](/FAST/config/__init__.py)


5. **Perform Reduction:** To perfrom reduction on test suites using FAST-R algorithms, run the following command

```
    python3 tools/experiment.py <prog> <setting>
```
Please replace `<prog>` with the name of one of project and `<setting>` with either strict or loose. 

For example: Running following cmd for gson in strict setting will generate 50 * 4 reduced test suites(one for each of the FAST-R algorithm and reduction happens for 50 times for each approach) for each of the 23 original test suites. In gson, there
are 23 test deletion commits in which whole test class is deleted and also, 23 unique parent commits of those test deletion commits.

```
    python3 tools/experiment.py gson strict
```

**Note: To perform reduction in the loose setting, please confirm you have followed Step 3 properly.**

6. **Analyze Results:** After performing reduction, we run the following command to get the results of the reduction.

```
    python3 tools/analyzer/main.py <prog> <setting>
```
Please replace `<prog>` with the name of one of project and `<setting>` with either strict or loose. 


For example: Running following cmd for gson in strict setting will generate a json file [here](/FAST/artifacts/strict/gson.json). 
This contains information regarding how many deleted test class and redundant tests can each of the 4 FAST-R algortihms identify.

```
    python3 tools/experiment.py gson strict
```

7. **Generate Summary:** To generate summary of the effectiveness of all 4 FAST-R algorighms to identify deleted test class and redundant tests, 
please run the following command:
```
    python3 tools/experiment.py gson strict
```


## Struggling to reproduce results ?

---

Please file an issue and we will get back to you as soon as possible.

## FAQ

---

- **Can I use it to identify test deletion commits and deleted tests from projects other than the studied projects in the paper?**
  No. However, you can use the steps to identify candidate deleted tests and candidate test deletion commits. The candidate deleted tests should be confirmed as valid deleted tests via manual validation.

## Contributors

---

Suraj Bhatta and Ajay Kumar Jha.
