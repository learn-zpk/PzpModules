"""
hard
最笨的方法，遍历O(n2),检查需要O(n/2)
"""


class Solution:
    def longestPalindrome(self, s):
        def checkPalindrome(_str, begin, end):
            while begin <= end:
                if _str[begin] != _str[end]:
                    return False
                begin += 1
                end -= 1
            return True

        if not s:
            return None
        i = 0
        cur_len = len(s)
        longest_str = ''
        while i < cur_len:
            j = i + 1
            while j < cur_len:
                if checkPalindrome(s, i, j):
                    if len(s[i:j + 1]) > len(longest_str):
                        longest_str = s[i:j + 1]
                j += 1
            i += 1
        return longest_str


if __name__ == '__main__':
    print(Solution().longestPalindrome('babad'))
