## Download Projects

To ensure the smooth computation of candidate deleted tests and test deletion commits, it's essential to download the studied 7 open-source projects and have them locally available. Here are the steps to follow:

1. **Navigate from root directory to the projects directory**

```
cd deltestbench/inputs/projects
```

2. **Clone the projects using the following commands:**

```
git clone -–single-branch  https://github.com/google/gson.git 
git clone -–single-branch https://github.com/apache/commons-lang.git
git clone -–single-branch https://github.com/apache/commons-math.git 
git clone -–single-branch https://github.com/pmd/pmd.git 
git clone -–single-branch https://github.com/jfree/jfreechart.git
git clone -–single-branch https://github.com/JodaOrg/joda-time.git
git clone -–single-branch https://android.googlesource.com/platform/cts
```

We mentione `--single-branch` option to clone only the primary branch of the projects. The studied 7 open-source projects should be downloaded inside the directory [/deltestben/inputs/projects](/deltestbench/inputs/projects/).

**NOTE: Prior to cloning, please ensure that your machine has sufficient available disk space.**

