import sys

sys.path.append("../")

import logging
from timeit import default_timer as timer
from datetime import timedelta
from experimentBudgetCore import main
from config import ROOT_DIR

usage = """USAGE: python3 experimentCustom.py <prog> <setting:loose|strict>
  """

logging.basicConfig(
    filename=f"{ROOT_DIR}/app.log",
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
    level=logging.DEBUG,
)


if __name__ == "__main__":
    script, prog, setting = sys.argv
    start = timer()
    main(prog, setting)
    end = timer()
    logging.info(
        prog
        + " "
        + setting
        + " completed execution in "
        + str(timedelta(seconds=end - start))
        + " seconds"
    )
