import unittest

from SegmentOverlap import SegmentOverlap


class MyTestCase(unittest.TestCase):
    def test_max_bruteforce(self):
        cases = {
            (((1, 10), (2, 11), (3, 5)), ((2, 8), (1, 4))): 6,
        }

        for tc, expected in cases.items():
            res = SegmentOverlap.calc_max_overlap_bruteforce(list(tc[0]), list(tc[1]))
            self.assertEqual(expected, res)

    def test_max_overlap(self):
        cases = [
            (((1, 10), (2, 11), (3, 5)), ((2, 8), (1, 4))),
            (((3, 9), (4, 11), (4, 5), (6, 12)), ((2, 8), (1, 4), (3, 18))),
            (((3, 9), (4, 11), (4, 5), (6, 12)), ((2, 8), (1, 4), (3, 9))),
            (((1, 100), (4, 11), (4, 5), (6, 12)), ((2, 98), (1, 4), (3, 9))),
        ]

        for tc in cases:
            g1, g2 = list(tc[0]), list(tc[1])
            expected = SegmentOverlap.calc_max_overlap_bruteforce(g1, g2)
            print(f'{[g1, g2]}: {expected}')
            res = SegmentOverlap.cal_max_overlap(g1, g2)
            self.assertEqual(expected, res)
            res = SegmentOverlap.cal_max_overlap_of_groups([g1, g2])
            self.assertEqual(expected, res)


if __name__ == '__main__':
    unittest.main()
