"""
Given a 32-bit signed integer, reverse digits of an integer.

Example 1:

Input: 123
Output: 321
Example 2:

Input: -123
Output: -321
Example 3:

Input: 120
Output: 21
Note:
Assume we are dealing with an environment which could only store integers within the 32-bit signed integer range: [−2^31,  2^31 − 1]. For the purpose of this problem, assume that your function returns 0 when the reversed integer overflows.
todo
"""


class Solution:
    def reverse(self, x):
        tmp = 0
        a = 1
        if x < 0:
            a = -1
            x = a * x

        while x != 0:
            tmp = 10 * tmp + x % 10
            x = x // 10
        x = a * tmp
        if not -2 ** 31 <= x <= 2 ** 31 - 1:
            return 0
        return x


if __name__ == '__main__':
    print(Solution().reverse(120) == 21)
