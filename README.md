# UnderstandingTestDeletion



The artifact repository for the paper titled:

> Understanding Test Deletion in Continious Integgration  
> _Authors:_ Suraj Bhatta, Ajay Kumar Jha  
> _Conference:_

In this paper, we establish a benchmark comprising 24,431 manually confirmed deleted tests spanning 2,125 test deletion commits across 7 open-source projects. Furthermore, we conduct an evaluation of the effectiveness of FAST-R appraoches to identifying developer-deleted tests leading to permanent test deletion. The projects studied include: [gson](https://github.com/google/gson.git), [commons-lang](https://github.com/apache/commons-lang.git), [commons-math](https://github.com/apache/commons-math.git), [pmd](https://github.com/pmd/pmd.git), [jfreechart](https://github.com/jfree/jfreechart.git), [joda-time](https://github.com/JodaOrg/joda-time.git) and [cts](https://android.googlesource.com/platform/cts).


## Contents

The repository is divided into two groups:

- [**deltestbench**](/deltestbench/) : This section is dedicated to identifying test deletion commits and deleted tests.
    -   Contains input, configuration, artifacts, and scripts necessary for this purpose.
- [**FAST**](/FAST/) : This section focuses on evaluating the effectiveness of FAST-R approaches in identifying developer deleted tests.
    -   Includes input, configuration, artifacts, and scripts essential for conducting the evaluation.

Both group contain necessary input, configuration, artifacts and scripts files that are required to achieve respective objectives.


## Directory Structure

The directory is structured as follows:

    UnderstandingTestDeletion/        Root directory of the repository.
    |
    |--- deltestbench/        Implementation of process to identify deleted tests and test deletion commits.
    |    |------ analyzer/    Core logic for computing candidate test deletion commits and deleted tests.
    |    |------ artifacts/   Compiled results from manual validation of candidate deleted tests.
    |    |------ config/      Configuration files.
    |    |------ inputs/      Input files.
    |    |       |------ projects/     Locally cloned 7 studied open-source projects.
    |    |       |------ RefactoringMiner/
    |    |       |       |------ artifacts/      Refactorings identified for 7 projects under study using RefactoringMiner.
    |    |------ results/       Candidate test deletion commits and candidate deleted tests generated across different steps.
    |    |------ tools/     Scripts to execute via command line.
    |    |------ utils/     Utility and helper functions.
    |
    |--- FAST/        Implementation of evaluation of FAST-R algorithms to identify developer deleted tests.
    |    |------ analyzer/      Analysis of whether the algorithm can identify developer deleted tests (i.e., exclude them in reduced test suites).
    |    |------ artifacts/     Results after evaluating FAST-R approaches.
    |    |       |------ loose/     Results after FAST-R algorithms in loose setting.
    |    |       |------ strict/    Results after FAST-R algorithms in strict setting.
    |    |------ config/        Configuration files.
    |    |------ inputs/    Input files.
    |    |       |------ deleted-tests/     Test deletion commits and deleted tests information gathered from deltestbench.
    |    |       |------ prepare/   Scripts to prepare original test suites of parent commits of test deletion commits for reduction.
    |    |       |------ testcases/     Original test suites of parent commits of test deletion commits prepared for redcution.
    |    |------ results/      Reduced test suites using FAST-R.
    |    |       |------ loose/     Reduced test-suites using FAST-R algorithms in loose setting.
    |    |       |------ strict/    Reduced test-suites using FAST-R algorithms in strict setting.
    |    |------ tools/     Scripts to execute for reducing test suties using FAST-R algorithms and analyzing results.
    |    |       |------ analyzer/     Scripts to analyze the performance of FAST-R algorithms.
    |    |------ utils/     Utility and helper functions.




## Reproducing Results


1. **Install Python:** To replicate the experiment results, python should be installed on your machine.
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

### [deltestbench](/deltestbench/)

Please follow the given steps in correct order to identify test deletion commits and deleted tests.

**Steps:**

1. **Prepare input:**

- Please follow the instructions provided [here](/deltestbench/inputs/projects/README.md) to download the required projects. It is essential to have these projects present locally to execute subsequent steps smoothly.
- Additionally, we utilize [RefactoringMiner](https://github.com/tsantalis/RefactoringMiner) to filter out refactored tests. Kindly follow the guidelines outlined [here](/deltestbench/inputs/RefactoringMiner/README.md) to run the RefactoringMiner on the projects cloned locally. This process generates a csv file containing identified refactors across the commit history of each project.

2. **Change directory to deltestbench:** From root directory, run the following command:

```
    cd deltestbench
```

3. **Generate Candidate Commits:** To generate candidate test deletion commits, run the following command:

```
    python tools/testdel.py <program> step1
```

**Note: Please replace `program` with the name of any of the 7 studied projects: `commons-lang`, `gson`, `commons-math`, `jfreechart`, `joda-time`, `pmd`, and `cts`.**

For example: Executing the following command:

```
    python tools/testdel.py gson step1
```

will generate a csv file inside the directory [deltestbench/results/](/deltestbench/results/). This file contains candidate test deletion commits and will be located within the specified `program` directory, named as `hydrated_{program}-step1.csv`. An example of generated file can be found [here](/deltestbench/results//gson/hydrated_gson-step1.csv).

**IMPORTANT: For projects commons-lang, joda-time and cts, we need to filter out outliers from candidate test deletion commits. These outliers were identified during manual inspection. To do this, please run the following command:**

```
    python tools/refine_step1.py <program>
```

Executing this commoand will generate a csv file named `hydrated_<program>-step1_refined.csv`. The process refines the results found in the `hydrated_{program}-step1.csv`, narrowing down test deletion commits to be considered for identifying candidate deleted tests.

4. **Generate Candidate Deleted Tests:** To generate candidate deleted tests, run the following command:

```
    python tools/testdel.py <program> step2
```

**Note: Please ensure that you have executed the command in Step 3 before running this step.**

Executing this step will generate a csv file containing candidate deleted tests inside directory [deltestbench/results/](/deltestbench/results/). The file will be located inside the respective specified `program` directory and named `hydrated_<program>-step2.csv`.

5. **Filter Refactored Tests:** To filter out refactored tests from candidate deleted tests, run the following command:

```
    python tools/testdel.py <program> step3
```

**Note: Before executing this command, please ensure you have run commands in steps 3 and 4. Additionally, make sure you have followed instruction provided [here](/deltestbench/inputs/RefactoringMiner/README.md) and placed artifacts file generated using RefactoringMiner inside the directory [deltestbench/inputs](/deltestbench/inputs/RefactoringMiner/artifacts/)y.**

Executing this step will filter out identified refactored tests from candidate deleted tests and generate a csv file inside the directory [deltestbench/results/](/deltestbench/results/). The file will be located within the respective specified `program` directory and named as `hydrated_<program>-step3.csv`.

6. **Manual Validation:** After filtering out the refactored tests from candidate deleted tests, we do the manual validation of the tests is conducted. The two authors of the paper perform manual validation independently and then compile the results, resolving any disagreements. The results are located within the directory [deltestbench/artifacts](/deltestbench/artifacts/) .

In the csv file, the record with `Final Result` set to `yes` indicates a developer deleted test that has been manually confirmed.

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

For example: Running following cmd for gson in strict setting will generate 50 \* 4 reduced test suites(one for each of the FAST-R algorithm and reduction happens for 50 times for each approach) for each of the 23 original test suites. In gson, there
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



Please file an issue and we will get back to you as soon as possible.

## FAQ



- **Can I use it to identify candidate test deletion commits and deleted tests from projects other than the studied projects in the paper?**
Yes. The steps used in this project can be used to identify any candidate test deletion commits and deleted tests in any other Java projects. However, make sure to sure RefactoringMiner on the new project and place inside inside input directory [here](/deltestbench/inputs/RefactoringMiner/artifacts/). The candidate deleted tests are then confirmed as valid deleted tests via manual validation.

## Contributors

---

Suraj Bhatta and Ajay Kumar Jha.
