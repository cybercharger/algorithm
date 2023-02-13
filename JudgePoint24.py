import itertools
from typing import List, Callable, Tuple


class Solution:
    def judgePoint24(self, cards: List[int]) -> bool:
        if not cards:
            return False

        def equals(a: float, b: float) -> bool:
            return abs(a - b) < 0.00001

        def judge(target: float, nums: List[float]) -> bool:
            if len(nums) == 2:
                a, b = nums[0], nums[1]
                if equals(a + b, target):
                    return True
                if equals(abs(a - b), target):
                    return True
                if equals(a * b, target):
                    return True
                if b != 0 and equals(a / b, target):
                    return True
                if a != 0 and equals(b / a, target):
                    return True
                return False

            for a, b in itertools.combinations(range(len(nums)), 2):
                left = [nums[i] for i in range(len(nums)) if i != a and i != b]
                if judge(target, left + [nums[a] + nums[b]]):
                    return True
                if judge(target, left + [nums[a] - nums[b]]) or judge(target, left + [nums[b] - nums[a]]):
                    return True
                if judge(target, left + [nums[a] * nums[b]]):
                    return True
                if nums[b] != 0 and judge(target, left + [nums[a] / nums[b]]):
                    return True
                if nums[a] != 0 and judge(target, left + [nums[b] / nums[a]]):
                    return True

            return False

        return judge(24, cards)
