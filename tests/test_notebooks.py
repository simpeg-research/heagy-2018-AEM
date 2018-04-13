import os
import testipynb
import unittest

NBDIR = os.path.sep.join(
    os.path.abspath(__file__).split(os.path.sep)[:-2] + ['notebooks']
)
# IGNORE = ["TEM_VerticalConductor_1D_stiched_invrsion"]

Test = testipynb.TestNotebooks(directory=NBDIR, timeout=2000)
TestNotebooks = Test.get_tests()

if __name__ == "__main__":
    unittest.main()
