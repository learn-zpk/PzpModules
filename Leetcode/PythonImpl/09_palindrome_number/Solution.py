"""
Determine whether an integer is a palindrome. An integer is a palindrome when it reads the same backward as forward.

Example 1:

Input: 121
Output: true
Example 2:

Input: -121
Output: false
Explanation: From left to right, it reads -121. From right to left, it becomes 121-. Therefore it is not a palindrome.
Example 3:

Input: 10
Output: false
Explanation: Reads 01 from right to left. Therefore it is not a palindrome.
"""


class Solution:
    def isPalindrome2(self, x: int):
        s = str(x)
        left = 0
        right = len(s) - 1
        while left <= right:
            if s[left] != s[right]:
                return False
            left += 1
            right -= 1
        return True

    def isPalindrome(self, x: int):
        if x <= 0:
            return False
        i = x
        tmp = 0
        while i != 0:
            tmp = 10 * tmp + i % 10
            i = i // 10
        return tmp == x


if __name__ == '__main__':
    # print(Solution().myAtoi('42') == 42)
    # print(Solution().myAtoi("   -42") == -42)
    # print(Solution().myAtoi('-91283472332') == -2147483648)
    # print(Solution().myAtoi('words and 987') == 0)
    # print(Solution().myAtoi('4193 with words') == 4193)
    # print(Solution().myAtoi('+-1') == 0)
    print(Solution().isPalindrome(121))
