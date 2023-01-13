from typing import List, Tuple


class Solution:
    def __int__(self):
        pass

    @staticmethod
    def to_complement(number: str) -> list:
        if number is None:
            return []
        valid = number.lstrip().lstrip('0')
        if valid[0] != '-':
            res = [0] + [int(d) for d in valid]
            return res if res[0] < 5 else [0] + res

        res = []
        carry_over = 1
        for i in range(len(valid) - 1, 0, -1):
            digit = int(valid[i])
            if digit < 0:
                raise ValueError()
            value = 9 + carry_over - digit
            res.insert(0, value % 10)
            carry_over = value // 10

        return [9] + res if res[0] < 5 else res

    @staticmethod
    def align(num1: list, num2: list) -> Tuple[List[int], List[int]]:
        len1 = len(num1)
        len2 = len(num2)
        target = num1 if len2 > len1 else num2
        digit = 9 if target[0] >= 5 else 0
        for i in range(0, abs(len1 - len2)):
            target.insert(0, digit)
        return num1, num2

    @staticmethod
    def sub(num1: list, num2: list) -> list:
        Solution.align(num1, num2)
        res = []
        carry_over = 0
        for i in range(1, len(num1) + 1):
            cur = num1[-i] - num2[-i] + carry_over
            res.insert(0, cur % 10)
            carry_over = cur // 10
        return res

    @staticmethod
    def to_string(num: list) -> str:
        # positive number
        if num[0] < 5:
            negative = False
            res = num
        else:
            negative = True
            res = []
            carry_over = 1
            for i in range(1, len(num) + 1):
                cur = 9 + carry_over - num[-i]
                res.insert(0, cur % 10)
                carry_over = cur // 10

        res = ''.join(str(x) for x in res).lstrip('0')
        if len(res) == 0:
            return '0'

        return res if not negative else '-' + res

    @staticmethod
    def subtract(num1: str, num2: str) -> str:
        res = Solution.sub(Solution.to_complement(num1), Solution.to_complement(num2))
        return Solution.to_string(res)
