"""
中心扩展法
"""


class Solution:
    def longestPalindrome(self, s):
        def return_palindrome(_str, middle):
            left, right = middle - 1, middle + 1
            while right < len(s) and _str[middle] == _str[right]:
                right += 1
            while left >= 0 and right < len(s) and _str[left] == _str[right]:
                left -= 1
                right += 1
            return _str[left + 1:right]

        if not s:
            return None
        longest_str = ''
        for idx, _ in enumerate(s):
            cur_palindrome = return_palindrome(s, idx)
            if len(cur_palindrome) > len(longest_str):
                longest_str = cur_palindrome
        return longest_str


if __name__ == '__main__':
    print(Solution().longestPalindrome('babbbbddasdad'))
