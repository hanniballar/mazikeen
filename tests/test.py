import unittest
import subprocess
import os
import re
from mazikeen.Utils import diff, rmtree, diffStrategy
from xmldiff import main
from collections import OrderedDict

testDir = "TestFiles/Blackbox_test/testsuitsNtestcases/"
print(main.diff_files(testDir + "TestOutput/report/report_diff.xml", testDir + "TestExpected/report/report_diff.xml"))
