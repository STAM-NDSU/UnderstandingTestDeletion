from enum import Enum


class RemoteBaseUrl(str, Enum):
    gson = "https://android.googlesource.com/platform/cts/+/"
    joda_time = "https://github.com/JodaOrg/joda-time/commit/"
    cts = "https://android.googlesource.com/platform/cts/+/"
    jfreechart = "https://github.com/jfree/jfreechart/commit/"
    commons_math = "https://github.com/apache/commons-math/commit/"
    commons_lang = "https://github.com/apache/commons-lang/commit/"
    pmd = "https://github.com/pmd/pmd/commit/"
