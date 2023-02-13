import itertools
import unittest

import Permutation


class MyTestCase(unittest.TestCase):
    def test_permute(self):
        test_cases = [
            [],
            [1],
            [1, 2, 3],
            [1, 2, 3, 4, 5, 6]
        ]

        for tc in test_cases:
            if not tc:
                self.assertEqual([], Permutation.Solution.permute(tc))
                continue
            expected = set(itertools.permutations(tc))
            actual = {tuple(p) for p in Permutation.Solution.permute(tc)}
            self.assertEqual(expected, actual)

        itertools.combinations


if __name__ == '__main__':
    unittest.main()
