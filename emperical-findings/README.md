# Emperical Findings

### Projects Studied

We select 7 open-source Java projects for our study.

<img src="/emperical-findings/img/projects-studied.png" width="800" />

### deltestbench

We establish a benchmark of manually confirmed 24,431 deleted tests in 2,125 commits from seven projects. Results of individual projects are listed below.

- [commons-lang](../deltestbench/artifacts/commons-lang.csv)
- [gson](../deltestbench/artifacts/gson.csv)
- [commons-math](../deltestbench/artifacts/commons-math.csv)
- [jfreechart](../deltestbench/artifacts/jfreechart.csv)
- [joda-time](../deltestbench/artifacts/joda-time.csv)
- [pmd](../deltestbench/artifacts/pmd.csv)
- [commons-lang](../deltestbench/artifacts/commons-lang.csv)

The following pie-chart shows those manually confirmed deleted tests spread across studied projects:

<img src="/emperical-findings/rq1/deleted-tests.png" width="500" />

### RQ1: How many obsolete and redundant tests do developers delete in the projects?

We analyzed test deletion commits from deltestbench to answer this research question. The compiled data set used to answer this research question is located [here](/emperical-findings/results)
The following stacked horizontal bar graph shows 

<img src="/emperical-findings/rq1/obsolete-and-redundant-tests.png" width="500" />

### RQ2: How often do developers delete tests?

Similar to RQ1, we analyzed test deletion commits from deltestbench and grouped them by version and year. The compiled data set obtained for different versions of projects under 
study is located [here](/emperical-findings/rq2/data/version/). Furthermore, the compiled data set obtained for different years is located [here](/emperical-findings/rq2/data/year/).


<img src="/emperical-findings/rq2/img/testdeletion-frequency.png" width="1200" />

Graphs used for version are located [here](/emperical-findings/rq2/version/) and years are located [here](/emperical-findings/rq2/year/).

### RQ3: How many tests do developers delete in a test deletion commit?
We grouped the deleted tests by commit hash for each project. We then anaylzed test deletion commit and its parent and compiled following data set to answer this research questions.

- [commons-lang](../emperical-finding/rq3/data/commons-lang.csv)
- [gson](../emperical-finding/rq3/data/gson.csv)
- [commons-math](../emperical-finding/rq3/data/commons-math.csv)
- [jfreechart](../emperical-finding/rq3/data/jfreechart.csv)
- [joda-time](../emperical-finding/rq3/data/joda-time.csv)
- [pmd](../emperical-finding/rq3/data/pmd.csv)
- [commons-lang](../emperical-finding/rq3/data/commons-lang.csv)

Violin plots

- Total number of tests deleted
<img src="/emperical-findings/rq3/img/no-of-tests.png" width="500" />

- Percentage of tests deleted
<img src="/emperical-findings/rq3/img/percentage-of-tests.png" width="500" />

### RQ4: RQ4: At what levels of granularity do developers delete tests?
We analyzed the deleted tests and compiled if the test is deleted along with class or individually. The compiled results obtained for this research question can be found [here](/emperical-findings/rq4/data/results.csv).


<img src="/emperical-findings/rq4/testdeletion-granularity.png" width="500" />



### RQ5

We evaluated effectiveness of FAST-R approches: FAST++, FAS-CS, FAST-pw and FAST-all to idenfity developer deleted tests from deltestbench in two different setting: **strict** and **loose**. 

Dataset used for this research question

<img src="/emperical-findings/rq5/dataset.png" width="500" />


The results obtained for **strict** and **loose** setting are as belows:


#### Strict Scenario
- [commons-lang](../FAST/artifacts/strict/commons-lang.csv)
- [gson](../FAST/artifacts/strict/gson.csv)
- [commons-math](../FAST/artifacts/strict/commons-math.csv)
- [jfreechart](../FAST/artifacts/strict/jfreechart.csv)
- [joda-time](../FAST/artifacts/strict/joda-time.csv)
- [pmd](../FAST/artifacts/strict/pmd.csv)
- [commons-lang](../FAST/artifacts/strict/commons-lang.csv)


#### Loose Scenario
- [commons-lang](../FAST/artifacts/loose/commons-lang.csv)
- [gson](../FAST/artifacts/loose/gson.csv)
- [commons-math](../FAST/artifacts/loose/commons-math.csv)
- [jfreechart](../FAST/artifacts/loose/jfreechart.csv)
- [joda-time](../FAST/artifacts/loose/joda-time.csv)
- [pmd](../FAST/artifacts/loose/pmd.csv)
- [commons-lang](../FAST/artifacts/loose/commons-lang.csv)

- Percentage of deleted tests excluded in reduced test suites
<img src="/emperical-findings/rq5/deleted-testclasses-fastr.png" width="500" />

- Percentage of redundant tests excluded in reduced test suites
<img src="/emperical-findings/rq5/redundant-tests-fastr.png" width="500" />
