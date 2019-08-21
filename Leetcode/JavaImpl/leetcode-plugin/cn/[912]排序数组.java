//给定一个整数数组 nums，将该数组升序排列。
//
//
//
//
//
//
// 示例 1：
//
//
//输入：[5,2,3,1]
//输出：[1,2,3,5]
//
//
// 示例 2：
//
//
//输入：[5,1,1,2,0,0]
//输出：[0,0,1,1,2,5]
//
//
//
//
// 提示：
//
//
// 1 <= A.length <= 10000
// -50000 <= A[i] <= 50000
//
//

class Solution {
    public int quickCore(int[] nums, int left, int right){
        int key=nums[left];
        while(left<right){
            while(nums[right]>=key && left<right){
                right--;
            }
            nums[right]=nums[left];
            while(nums[left]<=key && left<right){
                left++;
            }
            nums[left]=nums[right];
        }
        nums[left]=key;
        return left;
    }
    public void qucikSortArray(int[] nums, int left, int right) {
        if (left >= right) {
            return;
        }
        int idx = quickCore(nums, left, right);

        qucikSortArray(nums, idx + 1, right);
        qucikSortArray(nums, left, idx - 1);
    }

    public int[] sortArray(int[] nums) {
        qucikSortArray(nums, 0, nums.length-1);
        return nums;
    }
}
