"""
用一个临时字符串记录当前不重复的子串
todo
"""


class Solution(object):
    def lengthOfLongestSubstring(self, s: str) -> int:
        if not s:
            return 0
        tmp = ''
        max_str = ''
        for idx, chr in enumerate(s):
            if chr not in tmp:
                tmp += chr
                continue
            tmp_len = len(tmp)
            if len(max_str) < tmp_len:
                max_str = tmp
            cur_index = tmp.index(chr)
            tmp = tmp[cur_index + 1:] + chr if cur_index != tmp_len - 1 else chr
            print(tmp)
        return len(tmp) if len(max_str) < len(tmp) else len(max_str)


if __name__ == '__main__':
    print(Solution().lengthOfLongestSubstring("anviaj"))
