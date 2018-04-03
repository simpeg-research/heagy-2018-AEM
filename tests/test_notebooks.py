import os
import nbtest
import unittest

NBDIR = os.path.sep.join(
    os.path.abspath(__file__).split(os.path.sep)[:-2] + ['notebooks']
)
# IGNORE = ["TEM_VerticalConductor_1D_stiched_invrsion"]

class TestNotebooks(unittest.TestCase):

    def test_notebooks(self):
        Test = nbtest.TestNotebooks(directory=NBDIR)
        self.assertTrue(Test.run_tests())

if __name__ == "__main__":
    unittest.main()
