import unittest

from subtraction import *


class MyTestCase(unittest.TestCase):
    def test_get_complement(self):
        cases = {
            '   0123': [0, 1, 2, 3],
            '789': [0, 7, 8, 9],
            '-123': [9, 8, 7, 7],
            ' -500': [9, 5, 0, 0],
            '-501': [9, 4, 9, 9]
        }

        for case, expected in cases.items():
            self.assertEqual(expected, Solution.to_complement(case))

    def test_align(self):
        cases = {
            ((1, 2, 3), (1, 2)): ([1, 2, 3], [0, 1, 2]),
            ((5, 0, 0), (1, 2)): ([5, 0, 0], [0, 1, 2]),
            ((5, 0), (4, 9, 9)): ([9, 5, 0], [4, 9, 9]),
            ((9, 8), (0, 5)): ([9, 8], [0, 5]),
        }

        for case, expected in cases.items():
            self.assertEqual(expected, Solution.align(*[list(x) for x in case]))

    def test_to_string(self):
        cases = {
            (0, 1, 2, 3): '123',
            (9, 5, 0, 1): '-499',
            (9, 2, 3, 4): '-766',
            (5, 0, 0): '-500',
        }

        for case, expected in cases.items():
            self.assertEqual(expected, Solution.to_string(list(case)))

    def test_sub(self):
        cases = {
            ((1, 2), (3,)): [0, 9],
            ((1, 2), (3, 1)): [8, 1],
            ((2,), (2, 3)): [7, 9],
            ((9, 8), (0, 5)): [9, 3],
        }
        for case, expected in cases.items():
            self.assertEqual(expected, Solution.sub(*[list(x) for x in case]))

    def test_subtract(self):
        cases = [
            # ['123', '789'],
            ['-2', '4'],
            ['-2', '-1'],
            ['-2', '-3'],
            ['12', '-4'],
            ['-82', '-82'],
            ['-99', '9'],
            ['-6', '3'],
        ]

        for case in cases:
            expected = str(int(case[0]) - int(case[1]))
            print(f'({case[0]}) - ({case[1]}) = {expected}')
            self.assertEqual(expected, Solution.subtract(*case))

    @staticmethod
    def calc_overlap(b1: int, e1: int, b2: int, e2: int) -> int:
        """
        Calculate overlap of two segments
        :param b1: begin of segment1
        :param e1: end of segment1
        :param b2: begin of segment2
        :param e2: end of segment2
        :return: length of overlap
        """
        if b1 > e1:
            b1, e1 = e1, b1
        if b2 > e2:
            b2, e2 = e2, b2

        return max(0, min(e1, e2) - max(b1, b2))


if __name__ == '__main__':
    unittest.main()
