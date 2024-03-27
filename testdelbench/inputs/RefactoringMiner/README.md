The `artifacts` directory [here](/testdelbench/inputs/RefactoringMiner/artifacts/) contains `json` files generated using [RefactoringMiner](https://github.com/tsantalis/RefactoringMiner) for open-source projects analyzed in our study. These files contain identified refactorings across the history of commits of the repository The filename is in the format `<project-name>.json`.

Please follow the following steps to generate artifacts using RefactoringMiner.

1. **Clone RefactoringMiner:**

```
    git clone https://github.com/tsantalis/RefactoringMiner.git
```

2. **Navigate to RefactoringMiner directory:**

```
    cd RefactoringMiner
```

3. **Build the RefactoringMiner project**
   Please run the following command from the root directory of RefactoringMiner:

```
    ./gradlew jar

```

4. **Navigate to the RefactoringMiner build directory:**
   The build jar file is typically located inside `build/libs` directory from root directory of RefactoringMiner.
   Please run following command from the root directory of RefactoringMiner.

```
    cd build/libs

```

**NOTE: The build Jar file path could be different for you. Please check and customize the path accordingly.**

5. **Run RefactoringMiner:**
Use the following command to execute RefactoringMiner with the appropriate parameters.
```
    java -jar RefactoringMiner.jar -output JSON -gitrepo <path-to-repo> > <repo-name>.json
```
Please replace `<path-to-repo>` with the path to your locally cloned project repository that you would like to analyze. Also, replace `<path-to-repo>` with name of the repository.


6. **Move output file to artifacts directory**
Finally, please move the generated result file into artifacts directory [here](/testdelbench/inputs/RefactoringMiner/artifacts/)


### Skip Generating Files using RefactoringMiner
We have run the RefactoringMiner for all of the 7 projects and made the result file available [here](https://drive.google.com/drive/folders/1oA-78s9DiWCpmZ2iiO40SpxRNCLNfzF2?usp=sharing).
You can directly download those files and place into the artifacts directory.