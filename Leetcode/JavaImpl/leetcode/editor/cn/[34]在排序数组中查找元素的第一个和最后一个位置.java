//给定一个按照升序排列的整数数组 nums，和一个目标值 target。找出给定目标值在数组中的开始位置和结束位置。
//
// 你的算法时间复杂度必须是 O(log n) 级别。
//
// 如果数组中不存在目标值，返回 [-1, -1]。
//
// 示例 1:
//
// 输入: nums = [5,7,7,8,8,10], target = 8
//输出: [3,4]
//
// 示例 2:
//
// 输入: nums = [5,7,7,8,8,10], target = 6
//输出: [-1,-1]
//

/**
 * fixed 二分法需要考虑边界
 * */
class Solution {
    public int[] searchRange(int[] nums, int target) {
        int[] result = new int[]{-1, -1};
        int left = 0, right = nums.length - 1;
        int middle = (right + left) / 2;
        while (left <= right) {
            if (nums[middle] == target) {
                result[0] = middle;
                result[1] = middle;
                while (result[1] <= right && result[1] != nums.length - 1) {
                    if (nums[result[1] + 1] != target) {
                        break;
                    }
                    result[1] += 1;
                }
                while (result[0] >= left && result[0] != 0) {
                    if (nums[result[0] - 1] != target) {
                        break;
                    }
                    result[0] -= 1;
                }
                break;
            } else if (nums[middle] < target) {
                left = middle+1;
            } else {
                right = middle-1;
            }
        }
        return result;
    }
}
