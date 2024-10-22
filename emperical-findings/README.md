# Emperical Findings

### Projects Studied

We selected 7 open-source Java projects for our study.

<img src="/emperical-findings/img/projects-studied.png" width="800" />

### deltest

We create a dataset comprising 24,431 manually confirmed developer deleted tests in 2,125 commits from the selected projects.

Results of individual projects:

- [commons-lang](../deltest/artifacts/commons-lang.csv)
- [gson](../deltest/artifacts/gson.csv)
- [commons-math](../deltest/artifacts/commons-math.csv)
- [jfreechart](../deltest/artifacts/jfreechart.csv)
- [joda-time](../deltest/artifacts/joda-time.csv)
- [pmd](../deltest/artifacts/pmd.csv)
- [cts](../deltest/artifacts/cts.csv)

**NOTE: In the csv file, the record with `Final Result` set to `yes` indicates a developer deleted test that has been manually confirmed.**



## RQ1: How many tests do developers delete in the projects and commits?

Developer deleted tests spread across studied projects:

<img src="/emperical-findings/rq1/img/deleted-tests.png" width="500" />

To find the number of tests deleted per commit, we grouped the deleted tests by commit hash for each project and compiled datasets:

- [commons-lang](../emperical-finding/rq3/data/commons-lang.csv)
- [gson](../emperical-finding/rq3/data/gson.csv)
- [commons-math](../emperical-finding/rq3/data/commons-math.csv)
- [jfreechart](../emperical-finding/rq3/data/jfreechart.csv)
- [joda-time](../emperical-finding/rq3/data/joda-time.csv)
- [pmd](../emperical-finding/rq3/data/pmd.csv)
- [cts](../emperical-finding/rq3/data/cts.csv)


Total number of tests deleted:

<img src="/emperical-findings/rq1/img/no-of-tests-deleted.png" width="500" />

Percentage of tests deleted:

<img src="/emperical-findings/rq1/img/percentage-of-tests-deleted.png" width="500" />

**NOTE: The above violin plots are truncated from right to clearly display mean and median values and might not represent actual maximum values.**


## RQ2: How often do developers delete tests?

Similar to RQ1, we analyzed test deletion commits and grouped them by version and year. The compiled datasets for different versions and years are located [here](/emperical-findings/rq2/data/version/) and [here](/emperical-findings/rq2/data/year/) respectively.

<img src="/emperical-findings/rq2/img/testdeletion-frequency.png" width="1200" />

Graphs used for version are located [here](/emperical-findings/rq2/version/) and years are located [here](/emperical-findings/rq2/year/).

## RQ3: At what levels of granularity do developers delete tests?

We analyzed the deleted tests to determine if they were deleted along with class or individually. The compiled results can be found [here](/emperical-findings/rq4/data/results.csv).

<img src="/emperical-findings/rq4/img/testdeletion-granularity.png" width="500" />


## RQ4: Why do developers delete tests?

We analyzed the reasons of test deletion and compiled following datasets to answer this question:

Obsolete tests:

- [commons-lang](../emperical-finding/rq4/data/obsolete/commons-lang.csv)
- [gson](../emperical-finding/rq4/data/obsolete/gson.csv)
- [commons-math](../emperical-finding/rq4/data/obsolete/commons-math.csv)
- [jfreechart](../emperical-finding/rq4/data/obsolete/jfreechart.csv)
- [joda-time](../emperical-finding/rq4/data/obsolete/joda-time.csv)
- [pmd](../emperical-finding/rq4/data/obsolete/pmd.csv)

Failed tests:

- [joda-time](../emperical-finding/rq4/data/failed/joda-time.csv)

Redundant tests:

- [commons-lang](../emperical-finding/rq3/data/redundant/commons-lang.csv)
- [commons-math](../emperical-finding/rq3/data/redundant/commons-math.csv)
- [joda-time](../emperical-finding/rq3/data/redundant/joda-time.csv)
- [pmd](../emperical-finding/rq3/data/redundant/pmd.csv)

Note: CSV files also contains branch coverage, line coverage, and mutation score loss computed for redundant tests. 

Reasons for test deletions:

<img src="/emperical-findings/rq4/img/delted-test-categories.png" width="500" />


Coverage & Mutation Loss by Redundant Tests:

<img src="/emperical-findings/rq4/img/coverage-mutation-loss.png" width="500" />


Note: Only 4 projects contain redundant tests


## RQ5: How many of the developers' deleted redundant tests do TSR approaches identify?

We evaluated effectiveness of FAST-R approches (`FAST++`, `FAS-CS`, `FAST-pw` and `FAST-all`) to idenfity developer deleted redundant tests from **deltest** in two different setting: `strict` and `loose`.

<img src="/emperical-findings/rq5/dataset.png" width="500" />

Results for `strict` scenario:


- [commons-math](../FAST/artifacts/strict/commons-math.csv)
- [joda-time](../FAST/artifacts/strict/joda-time.csv)
- [pmd](../FAST/artifacts/strict/pmd.csv)


Results for `loose` scenario:

- [commons-math](../FAST/artifacts/loose/commons-math.csv)
- [joda-time](../FAST/artifacts/loose/joda-time.csv)
- [pmd](../FAST/artifacts/loose/pmd.csv)



**NOTE: Only 3 projects (commons-math, joda-time and pmd) were used in the study for RQ5 as shown in the table above.**

Percentage of deleted test classes excluded in reduced test suites:

<img src="/emperical-findings/rq5/FASTR-percentage-of-deleted-test-classes.png" width="1100" />

Percentage of redundant tests excluded in reduced test suites:

<img src="/emperical-findings/rq5/FASTR-percentage-of-redundant-tests.png" width="1100" />

