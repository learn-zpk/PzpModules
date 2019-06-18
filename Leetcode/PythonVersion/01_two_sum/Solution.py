"""
1. 基本方法: 两层遍历
2. 遍历一次，利用一个Map存储之前遍历过的num:idx
"""


class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        # num_dict = {num: idx for idx, num in enumerate(nums)}
        # for idx, num in enumerate(nums):
        #     tmp = target - num
        #     if tmp in num_dict:
        #         if idx != num_dict.get(tmp):
        #             return [idx, num_dict.get(tmp)]
        # return None

        num_dict = {}
        for idx, num in enumerate(nums):
            diff = target - num
            if diff in num_dict:
                return [idx, num_dict.get(diff)]
            num_dict[num] = idx
        return None


if __name__ == '__main__':
    nums = [2, 7, 11, 15]
    target = 9
    print(Solution().twoSum(nums, target))
