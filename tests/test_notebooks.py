import unittest
import os
import testipynb

TESTDIR = os.path.abspath(__file__)

NBDIR = os.path.sep.join(TESTDIR.split(os.path.sep)[:-2] + ["notebooks", "dcip"])
Test = testipynb.TestNotebooks(directory=NBDIR, timeout=2100)
TestsDC = Test.get_tests()

NBDIR = os.path.sep.join(TESTDIR.split(os.path.sep)[:-2] + ["notebooks", "em"])
Test = testipynb.TestNotebooks(directory=NBDIR, timeout=2100)
TestsEM = Test.get_tests()

NBDIR = os.path.sep.join(TESTDIR.split(os.path.sep)[:-2] + ["notebooks", "gpr"])
Test = testipynb.TestNotebooks(directory=NBDIR, timeout=2100)
TestsGPR = Test.get_tests()

NBDIR = os.path.sep.join(TESTDIR.split(os.path.sep)[:-2] + ["notebooks", "mag"])
Test = testipynb.TestNotebooks(directory=NBDIR, timeout=2100)
TestsMag = Test.get_tests()

NBDIR = os.path.sep.join(TESTDIR.split(os.path.sep)[:-2] + ["notebooks", "seismic"])
Test = testipynb.TestNotebooks(directory=NBDIR, timeout=2100)
TestsSeis = Test.get_tests()

if __name__ == "__main__":
    unittest.main()
