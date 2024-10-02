## RefactoringMiner for Refactoring Detection

We rely on [RefactoringMiner](https://github.com/tsantalis/RefactoringMiner) to identify refactorings applied throughout the commit history of the projects under study. Upon execution, this tool generates a `json` file named `<project-name>.json` containing detected refactorings. These files are stored within the directory [deltest/inputs/RefactoringMiner/artifacts](/deltest/inputs/RefactoringMiner/artifacts/). Subsequently, the canidate deleted tests identified as refactorings are then filtered out from the pool before manual validation.

Please follow the given steps to generate a `json` file containing refactorings.

1. **Clone RefactoringMiner:**

```
    git clone https://github.com/tsantalis/RefactoringMiner.git
```

2. **Navigate to the RefactoringMiner directory:**

```
    cd RefactoringMiner
```

3. **Build the RefactoringMiner project**
   Execute the following command from the root directory of RefactoringMiner:

```
    ./gradlew jar

```

4. **Navigate to the RefactoringMiner build directory:**
   The build jar file is typically located inside `build/libs` directory from the root directory of RefactoringMiner.
   Run the following command from the root directory of RefactoringMiner:

```
    cd build/libs

```

**NOTE: The path to the build Jar file may vary based on your system configuration. Please verify and adjust the path as needed.**

5. **Run RefactoringMiner:**
   Execute the following command to run RefactoringMiner:

```
    java -jar RefactoringMiner.jar -output JSON -gitrepo <path-to-repo> > <repo-name>.json
```

Please ensure to replace `<path-to-repo>` with the path to your locally cloned project repository. Also, replace `<path-to-repo>` with name of the repository.

**NOTE: For each of the 7 studied projects, we will need to generate a separate `json` file using RefactoringMiner. Please follow the steps provided above for each project individually to generate the corresponding `json` file.**

6. **Move the generated `json` file to artifacts directory**
   Please relocate the generated `json` file into [deltest/inputs/RefactoringMiner/artifacts](/deltest/inputs/RefactoringMiner/artifacts/) directory. This step ensures that the files are in the correct location for further processing.

### Skipping File Generation with RefactoringMiner

We have already executed RefactoringMiner for all 7 projects and provided the result files for download [here](https://drive.google.com/drive/folders/1oA-78s9DiWCpmZ2iiO40SpxRNCLNfzF2?usp=sharing). Simply download these files and place them into the [deltest/inputs/RefactoringMiner/artifacts](/deltest/inputs/RefactoringMiner/artifacts/) directory as instructed.

**NOTE: Due to the large size of these files, we did not include them in this git repository.**
