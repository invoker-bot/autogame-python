import unittest
import doctest


class Example(unittest.TestCase):

    def test(self):
        self.assertTrue(True)


def load_tests(loader, tests, pattern):
    tests.addTests(doctest.DocTestSuite())
    return tests


if __name__ == '__main__':
    unittest.main()
