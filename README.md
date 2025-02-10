# UnderstandingTestDeletion

The artifact repository for the paper titled:

> Understanding Test Deletion in Java Applications  
> _Authors:_ Suraj Bhatta, Frank Kendemah, Ajay Kumar Jha  
> _Conference:_ 22nd IEEE/ACM International Conference on Mining Software Repositories (MSR). 2025

In this paper, we establish a dataset comprising 24,431 manually confirmed developer deleted tests spanning 2,125 test deletion commits across 7 open-source projects. Furthermore, we conduct an evaluation of the effectiveness of FAST-R approaches in identifying developer deleted redundant tests for permanent test deletion. The projects studied include: [gson](https://github.com/google/gson.git), [commons-lang](https://github.com/apache/commons-lang.git), [commons-math](https://github.com/apache/commons-math.git), [pmd](https://github.com/pmd/pmd.git), [jfreechart](https://github.com/jfree/jfreechart.git), [joda-time](https://github.com/JodaOrg/joda-time.git) and [cts](https://android.googlesource.com/platform/cts).

## Contents

The repository is divided into three groups:

- [**deltest**](/deltest/) : This section is dedicated to identifying test deletion commits and deleted tests. Contains input, configuration, artifacts, and scripts necessary for this purpose.

- [**FAST**](/FAST/) : This section focuses on evaluating the effectiveness of FAST-R approaches in identifying developer deleted redundant tests. Includes input, configuration, artifacts, and scripts essential for conducting the evaluation.

- [**emperical-findings**](/emperical-findings/) : This section contains the emperical findings of our study. Results of each RQ is explained in detail [here](/emperical-findings/README.md).

## Directory Structure

The directory is structured as follows:

    UnderstandingTestDeletion/        Root directory of the repository.
    |
    |--- deltest/        Implementation of process to identify deleted tests and test deletion commits.
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
    |    |       |------ deleted-tests/     Test deletion commits and deleted tests information gathered from deltest.
    |    |       |------ prepare/   Scripts to prepare original test suites of parent commits of test deletion commits for reduction.
    |    |       |------ testcases/     Original test suites of parent commits of test deletion commits prepared for redcution.
    |    |------ results/      Reduced test suites using FAST-R.
    |    |       |------ loose/     Reduced test-suites using FAST-R algorithms in loose setting.
    |    |       |------ strict/    Reduced test-suites using FAST-R algorithms in strict setting.
    |    |------ tools/     Scripts to execute for reducing test suties using FAST-R algorithms and analyzing results.
    |    |       |------ analyzer/     Scripts to analyze the performance of FAST-R algorithms.
    |    |------ utils/     Utility and helper functions.
    |
    |--- emperical-findings/  Results of our experiments

## Emperical Results and Data

The results of our experiments as well as the datasets used for our statistical analysis are available [here](/emperical-findings/).

## Reproducing Results

1. **Install Python:** To replicate the experiment results, Python should be installed on your machine.
   Check if it is installed or not using the following command:

```
   python --version
```

If it is not installed, download and install Python from [here](https://www.python.org/downloads/).

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

### [deltest](/deltest/)

To successfully identify test deletion commits and deleted tests, please follow these steps in the correct order:

**Steps:**

1. **Prepare input:**

- Please follow the instructions provided [here](/deltest/inputs/projects/README.md) to download the required projects. It is essential to have these projects present locally to execute subsequent steps smoothly.
- Additionally, we utilize [RefactoringMiner](https://github.com/tsantalis/RefactoringMiner) to filter out refactored tests. Kindly follow the guidelines outlined [here](/deltest/inputs/RefactoringMiner/README.md) to run the RefactoringMiner on the projects cloned locally. This process generates a csv file for each project containing identified refactorings across the commit history of each project.

2. **Change directory to deltest:** From root directory, run the following command:

```
    cd deltest
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

will generate a csv file inside the directory [deltest/results/](/deltest/results/). This file contains candidate test deletion commits and will be located within the specified `program` directory, named as `hydrated_{program}-step1.csv`. An example of generated file can be found [here](/deltest/results//gson/hydrated_gson-step1.csv).

Note: The filename has prefix 'hydrated' to indicate that each rows has columns filled with values (i.e non-empty) to indicate the information is self-sufficient for inspection.
But, for the ease of the readibility during manual, we strip away common information such as commit hash, commit description etc from consequtive rows (i.e deleted tests) belonging to same commit and name the file as `{program}-step1.csv`.

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

Executing this step will generate a csv file containing candidate deleted tests inside directory [deltest/results/](/deltest/results/). The file will be located inside the respective specified `program` directory and named `hydrated_<program>-step2.csv`.

5. **Filter Refactored Tests:** To filter out refactored tests from candidate deleted tests, run the following command:

```
    python tools/testdel.py <program> step3
```

**Note: Before executing this command, please ensure you have run commands in steps 3 and 4. Additionally, make sure you have followed instruction provided [here](/deltest/inputs/RefactoringMiner/README.md) and placed artifacts file generated using RefactoringMiner inside the directory [deltest/inputs](/deltest/inputs/RefactoringMiner/artifacts/).**

Executing this step will filter out identified refactored tests from candidate deleted tests and generate a csv file inside the directory [deltest/results/](/deltest/results/). The file will be located within the respective specified `program` directory and named as `hydrated_<program>-step3.csv`.

6. **Manual Validation:** After filtering out the refactored tests from candidate deleted tests, manual validation of the tests is conducted. For the paper, the two authors of the paper perform manual validation independently and then compile the results, resolving any disagreements. The results are located within the directory [deltest/artifacts](/deltest/artifacts/) .

In the csv file, the record with `Final Result` set to `yes` indicates a developer deleted test that has been manually confirmed.

### [FAST-R](/FAST/)

Please follow the given steps to evaluate FAST-R appraoches on developer deleted redundant tests. 

**Steps:**

1. **Change directory to FAST:** Navigate to the FAST directory from the root directory by running the following command:

```
    cd FAST
```

2. **Prepare Input:**

FAST-R alrogithms are utilized to reduce test suites of parent commits of test deletion commits to which redundant tests belong. To accomplish this, we first need to process the
test classes present in the instance of parent commits of all the projects under study and compile them into a single `text` file.
The original test suites of parent test deletion commits of all projects are available in the directory [FAST/inputs/testcases/](/FAST/inputs/testcases/).
However, you can re-generate test suites for all the projects by running the following command:

```
    cd tools/prepare/testcases.py
```

**NOTE: Please ensure that the projects are downloaded and configured correctly following the mentioned Step 1 in the section [deltest](#deltest)**

This command generates a text file for each parent test deletion commit, containing all of test classes present in the parent commit. The results are stored within the directory [/FAST/inputs/testcases/](/FAST/inputs/testcases/), on which FAST-R algorithms perform reduction.

The [/FAST/inputs/deleted-tests/](/FAST/inputs/deleted-tests/) directory contains the confirmed deleted tests and test deletion commits of each project obtained after performing all the steps in [deltest](#deltest). The files are named `project`.csv and are required for the further processing.

4. **Compute Budget for Loose Scenario:** Before conducting test suite reduction, it is necessary to calculate the budget i.e the size of the reduced test suite for each project. Execute the following command to compute budget for the projects under study:

```
    python3 tools/budget_calc.py
```

Note: Above command generates budget metadata file `budget.json`. For loose scenrios, we relay on the Min Budget computed for each project. And for strict scenarios, we compute the budget on the go i.e while performing reduction (Step 5) by diving total number of test files not removed by total number of testfiles present in the parent commit of test deletion commit.

You can configure projects to be considered for evaluation by modifying `PROJECTS` variable in the configuration file located [here](/FAST/config/__init__.py)

5. **Perform Reduction:** To conduct reduction on test suites using FAST-R algorithms, execute the following command:

```
    python3 tools/experiment.py <prog> <setting>
```

Replace `<prog>` with the name of one of projects and `<setting>` with either `strict` or `loose`.
**IMPORTANT: Please ensure that you perform this step for all of the projects for both the `strict` and `loose` settings.**

For example: Running the following command for `joda-time` project in `strict` setting will generate 50 \* 4 reduced test suites(one for each of the FAST-R algorithm, with reduction happening 50 times for each approach) for each of the 23 original test suites. In gson, there are 23 test deletion commits in which the whole test class is deleted, and also 23 unique parent commits of those test deletion commits.

```
    python3 tools/experiment.py joda-time strict
```

**Note: To perform reduction in the loose setting, please ensure you have followed the instructions in the Step 3 properly.**

6. **Analyze Results:** After performing reduction, execute the following command to obtain the results of the reduction.

```
    python3 tools/analyzer/main.py <prog> <setting>
```

Replace `<prog>` with the name of one of the projects and `<setting>` with either `strict` or `loose`.

For example, running following command for `joda-time` in `strict` setting will generate a `json` file inside the directory [/FAST/artifacts/strict/](/FAST/artifacts/strict/).
This file is named `joda-time.json` and contains information regarding how many deleted test classes and redundant tests each of the 4 FAST-R algortihms can identify.

```
    python3 tools/analyzer/main.py joda-time strict
```

**NOTE: The files generated from our study after executing this step for loose and strict setting are located inside the directory [FAST/artifacts/loose](/FAST/artifacts/loose) and [FAST/artifacts/loose](/FAST/artifacts/loose) respectively.**

You can generate equivalent csv files for the generated `.json` file by running following command: 

```
    python3 tools/analyzer/results_json_to_csv.py
```

7. **Generate Summary:** To generate a summary of the effectiveness of all 4 FAST-R algorithms in identifying deleted test classes and redundant tests, please run the following command:

```
    python3 tools/analyzer/compile_results.py
```

This command compiles the results generated for all of the FAST-R algorithms in both strict and loose setting and creates a single `compiled_results.json` file within the [FAST/artifacts](/FAST/artifacts/) directory

**NOTE: The file generated from our study after executing this step is located [here](/FAST/artifacts/compiled_results.json).**



## Have Trouble Reproducing Results?

If you are struggling to reproduce the results, don't hesitate to file an issue, and we'll address it promptly.

## Frequently Asked Questions (FAQ)

- **Can I use this tool to identify candidate test deletion commits and deleted tests from projects other than the ones studied in the paper?**

Yes, absolutely. The steps outlined in this project can be used to identify candidate test deletion commits and deleted tests in any Java projects. However, ensure to run RefactoringMiner on the new project and place the artifacts inside inside the input directory [here](/deltest/inputs/RefactoringMiner/artifacts/). Subsequently, the candidate deleted tests are confirmed as valid deleted tests through manual validation.

## Contributors
