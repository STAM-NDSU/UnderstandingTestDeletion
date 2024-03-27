usuage = """
USAGE: python3 tools/experiment.py <prog> <setting>
"""

import sys

sys.path.append("../")

import logging
from timeit import default_timer as timer
from datetime import timedelta
from FAST.py.experimentBudgetModified import main
from FAST.config import LOG_FILEPATH, PROJECTS, SETTINGS


logging.basicConfig(
    filename=f"{LOG_FILEPATH}",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.DEBUG,
)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Please provide all the required arguments.")
        print(usuage)
        exit(1)

    script, prog, setting = sys.argv

    if prog not in PROJECTS:
        print(
            "Please provide a valid project name. It should be one of the 7 analyzed projects in the study."
        )

    if setting not in SETTINGS:
        print(
            "Please provide a valid setting. Setting should be either 'strict' or 'loose'. "
        )

    start = timer()
    main(prog, setting)
    end = timer()
    diff = timedelta(seconds=end - start)
    logging.info(
        f"{prog} in {setting} setting completed execution in {str(diff)} seconds"
    )
