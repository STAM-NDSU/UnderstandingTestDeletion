from enum import Enum


class Branch(str, Enum):
    gson = "main"
    joda_time = "main"
    cts = "master"
    jfreechart = "master"
    commons_math = "master"
    commons_lang = "master"
    pmd = "master"
