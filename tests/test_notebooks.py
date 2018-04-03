import nbtest
import unittest

NBDIR = '../notebooks'
# IGNORE = ["TEM_VerticalConductor_1D_stiched_invrsion"]

class TestNotebooks(unittest.TestCase):

    def test_notebooks(self):
        Test = nbtest.TestNotebooks(directory=NBDIR)
        self.assertTrue(Test.run_tests())

if __name__ == "__main__":
    unittest.main()
