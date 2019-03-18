"""
hard
todo
"""


class Solution:
    def findMedianSortedArrays(self, nums1, nums2):
        nums1_len, nums2_len = len(nums1), len(nums2)
        target = 1 if (nums1_len - nums2_len) % 2 == 0 else 0
        cur_length = 0
        tmp1, tmp2 = 0, 0
        idx1, idx2 = 0, 0

        while (nums1 and nums2) and 2 * cur_length - nums1_len - nums2_len < target and (
                idx2 < nums2_len or idx1 < nums1_len):
            cur_length += 1
            if idx2 == nums2_len - 1:
                tmp1, tmp2 = nums1[idx1], tmp1
                idx1 += 1
                continue
            if idx1 == nums1_len - 1:
                tmp1, tmp2 = nums2[idx2], tmp1
                idx2 += 1
                continue
            if nums1[idx1] > nums2[idx2]:
                tmp1, tmp2 = nums2[idx2], tmp1
                idx2 += 1
            elif nums1[idx1] <= nums2[idx2]:
                tmp1, tmp2 = nums1[idx1], tmp1
                idx1 += 1
        if not nums1 or not nums2:
            if not nums1 and not nums2:
                return None
            if not nums1:
                nums1, nums2 = nums2, nums1
            tmp1 = nums1[(len(nums1) + 1) // 2 - 1]
            if target == 1:
                tmp2 = nums1[(len(nums1) + 1) // 2]
        return tmp1 if target == 0 else float((tmp1 + tmp2) / 2)


if __name__ == '__main__':
    print(Solution().findMedianSortedArrays([1], [1]))
