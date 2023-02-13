import unittest

from JudgePoint24 import Solution


class MyTestCase(unittest.TestCase):
    def test_something(self):
        test_cases = [
            # ([4, 1, 8, 7], True),
            ([1, 3, 4, 6], True),
            # ([1, 2, 1, 2], False),
            # ([1, 5, 9, 1], False),
            # ([1, 7, 4, 7], True),
        ]
        s = Solution()
        for tc, expected in test_cases:
            self.assertEqual(expected, s.judgePoint24(tc), f'{tc} - {expected}')


if __name__ == '__main__':
    unittest.main()
