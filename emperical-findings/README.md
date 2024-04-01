# Emperical Findings

### Projects Studied

We selected 7 open-source Java projects for our study.

<img src="/emperical-findings/img/projects-studied.png" width="800" />

### deltestbench

We establish a benchmark comprising 24,431 manually confirmed developer deleted tests in 2,125 commits from the selected projects. 

Results of individual projects:

- [commons-lang](../deltestbench/artifacts/commons-lang.csv)
- [gson](../deltestbench/artifacts/gson.csv)
- [commons-math](../deltestbench/artifacts/commons-math.csv)
- [jfreechart](../deltestbench/artifacts/jfreechart.csv)
- [joda-time](../deltestbench/artifacts/joda-time.csv)
- [pmd](../deltestbench/artifacts/pmd.csv)
- [cts](../deltestbench/artifacts/cts.csv)


Developer deleted tests spread across studied projects:

<img src="/emperical-findings/rq1/img/deleted-tests.png" width="500" />

## RQ1: How many obsolete and redundant tests do developers delete in the projects?

We analyzed test deletion commits from **deltestbench** to answer this question. The compiled dataset used is located [here](/emperical-findings/results).

Obsolete and redundant tests across non-CTS projects:

<img src="/emperical-findings/rq1/img/obsolete-and-redundant-tests.png" width="500" />

## RQ2: How often do developers delete tests?

Similar to RQ1, we analyzed test deletion commits and grouped them by version and year. The compiled datasets for different versions and years are located [here](/emperical-findings/rq2/data/version/) and [here](/emperical-findings/rq2/data/year/) respectively.


<img src="/emperical-findings/rq2/img/testdeletion-frequency.png" width="1200" />

Graphs used for version are located [here](/emperical-findings/rq2/version/) and years are located [here](/emperical-findings/rq2/year/).

## RQ3: How many tests do developers delete in a test deletion commit?

We grouped the deleted tests by commit hash for each project and compiled datasets to answer this question:

- [commons-lang](../emperical-finding/rq3/data/commons-lang.csv)
- [gson](../emperical-finding/rq3/data/gson.csv)
- [commons-math](../emperical-finding/rq3/data/commons-math.csv)
- [jfreechart](../emperical-finding/rq3/data/jfreechart.csv)
- [joda-time](../emperical-finding/rq3/data/joda-time.csv)
- [pmd](../emperical-finding/rq3/data/pmd.csv)
- [cts](../emperical-finding/rq3/data/cts.csv)



Total number of tests deleted:

<img src="/emperical-findings/rq3/img/no-of-tests.png" width="500" />

Percentage of tests deleted:

<img src="/emperical-findings/rq3/img/percentage-of-tests.png" width="500" />

**NOTE: The above violin plots are truncated from right to clearly display mean and median values and might not represent actual maximum values.**

## RQ4: At what levels of granularity do developers delete tests?
We analyzed the deleted tests to determine if they were deleted along with class or individually. The compiled results can be found [here](/emperical-findings/rq4/data/results.csv).

<img src="/emperical-findings/rq4/img/testdeletion-granularity.png" width="500" />



## RQ5: How many of the obsolete and redundant developers’ deleted tests do TSR approaches identify?

We evaluated effectiveness of FAST-R approches (`FAST++`, `FAS-CS`, `FAST-pw` and `FAST-all`) to idenfity developer deleted tests from **deltestbench** in two different setting: `strict` and `loose`. 



<img src="/emperical-findings/rq5/dataset.png" width="500" />



Results for `strict` scenario:

- [commons-lang](../FAST/artifacts/strict/commons-lang.csv)
- [gson](../FAST/artifacts/strict/gson.csv)
- [commons-math](../FAST/artifacts/strict/commons-math.csv)
- [jfreechart](../FAST/artifacts/strict/jfreechart.csv)
- [joda-time](../FAST/artifacts/strict/joda-time.csv)
- [pmd](../FAST/artifacts/strict/pmd.csv)
- [cts](../FAST/artifacts/strict/cts.csv)


Results for `loose` scenario:
- [commons-lang](../FAST/artifacts/loose/commons-lang.csv)
- [gson](../FAST/artifacts/loose/gson.csv)
- [commons-math](../FAST/artifacts/loose/commons-math.csv)
- [jfreechart](../FAST/artifacts/loose/jfreechart.csv)
- [joda-time](../FAST/artifacts/loose/joda-time.csv)
- [pmd](../FAST/artifacts/loose/pmd.csv)
- [cts](../FAST/artifacts/loose/cts.csv)

Percentage of deleted tests excluded in reduced test suites:

<img src="/emperical-findings/rq5/deleted-testclasses-fastr.png" width="1100" />

Percentage of redundant tests excluded in reduced test suites:

<img src="/emperical-findings/rq5/redundant-tests-fastr.png" width="1100" />

**NOTE: Percentage of deleted tests and redundant tests excluded in reduced test suites were not reported in the paper for FAST-CS and FAST-pw due to lack of space.**