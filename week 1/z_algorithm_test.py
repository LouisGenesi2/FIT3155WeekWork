# test_z_algorithm.py

import unittest
from z_algorithm import z_algorithm

class TestZAlgorithm(unittest.TestCase):
    def test_basic_case(self):
        self.assertEqual(z_algorithm("aabxaabxcaabxaabxay"), 
                         [19, 1, 0, 0, 4, 1, 0, 0, 0, 8, 1, 0, 0, 5, 0, 0, 0, 1, 0])

    def test_all_same_characters(self):
        self.assertEqual(z_algorithm("aaaaaa"), [6, 5, 4, 3, 2, 1])

    def test_no_repeats(self):
        self.assertEqual(z_algorithm("abcdef"), [6, 0, 0, 0, 0, 0])

    def test_empty_string(self):
        self.assertEqual(z_algorithm(""), [])

    def test_single_character(self):
        self.assertEqual(z_algorithm("z"), [1])

    def test_partial_repeats(self):
        self.assertEqual(z_algorithm("abcababcab"), [10, 0, 0, 2, 0, 5, 0, 0, 2, 0])

if __name__ == '__main__':
    unittest.main()
