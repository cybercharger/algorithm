from typing import List


class Solution:

    @staticmethod
    def permute(nums: List[int]) -> List[List[int]]:
        if not nums:
            return []

        result = []

        def permute_recursive(start: int, length: int) -> None:
            if start == length - 1:
                result.append(nums.copy())

            for i in range(start, length):
                nums[start], nums[i] = nums[i], nums[start]
                permute_recursive(start + 1, length)
                nums[start], nums[i] = nums[i], nums[start]

        permute_recursive(0, len(nums))

        return result

    @staticmethod
    def permute_unique(nums: List[int]) -> List[List[int]]:
        if not nums:
            return []

        counter = dict()
        for i in nums:
            counter[i] = counter.get(i, 0) + 1

        result = []

        def permute_recursive(buffer: List[int]) -> None:
            if len(buffer) == len(nums):
                result.append(buffer.copy())

            for num in counter:
                if counter[num] <= 0:
                    continue
                counter[num] -= 1
                buffer.append(num)
                permute_recursive(buffer)
                buffer.pop()
                counter[num] += 1

        permute_recursive([])
        return result
