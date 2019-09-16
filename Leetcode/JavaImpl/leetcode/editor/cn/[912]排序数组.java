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

/*快速排序: 交换排序 不稳定 O(nlogn)*/
class Solution3 {
    public int sortCore(int[] nums, int left, int right) {
        int middleVal = nums[left];
        while (left < right) {
            while (left < right && nums[right] >= middleVal) {
                right--;
            }
            nums[left] = nums[right];
            while (left < right && nums[left] <= middleVal) {
                left++;
            }
            nums[right] = nums[left];
        }
        nums[left] = middleVal;
        return left;
    }

    private void sortTemp(int[] nums, int left, int right) {
        if (left >= right) {
            return;
        }
        int middle = sortCore(nums, left, right);

        sortTemp(nums, left, middle - 1);
        sortTemp(nums, middle + 1, right);
        return;
    }

    public int[] sortArray(int[] nums) {
        int left = 0, right = nums.length - 1;
        sortTemp(nums, left, right);
        return nums;
    }
}

/*冒泡排序: 交换排序 稳定，O(n2)*/
class Solution2 {
    public int[] sortArray(int[] nums) {
        for (int i = 0; i < nums.length - 1; i++) {
            for (int j = 0; j < nums.length - i - 1; j++) {
                if (nums[j] > nums[j + 1]) {
                    int tmp = nums[j + 1];
                    nums[j + 1] = nums[j];
                    nums[j] = tmp;
                }
            }
        }
        return nums;
    }
}

/*简单选择排序: 选择排序 不稳定 O(n2)*/
class Solution1 {
    public int[] sortArray(int[] nums) {
        for (int i = 0; i < nums.length - 1; i++) {
            int minIndex = i;
            for (int j = i; j < nums.length; j++) {
                if (nums[j] < nums[minIndex]) {
                    minIndex = j;
                }
            }
            if (minIndex != i) {
                int tmp = nums[minIndex];
                nums[minIndex] = nums[i];
                nums[i] = tmp;
            }
        }
        return nums;
    }
}

/*直接插入排序: 插入排序 稳定 O(n2)*/
class Solution4 {
    public int[] sortArray(int[] nums) {
        for (int i = 0; i < nums.length - 1; i++) {
            int current = nums[i + 1];
            int preIdx = i;
            while (preIdx >= 0 && current < nums[preIdx]) {
                nums[preIdx + 1] = nums[preIdx];
                preIdx--;
            }
            nums[preIdx + 1] = current;
        }
        return nums;
    }
}

/*希尔排序: 插入排序*/
class Solution4 {
    public int[] sortArray(int[] nums) {
        int round = nums.length / 2;
        while (round >= 1) {
            for (int i = 0; i < nums.length - round; i+=round) {
                int current = nums[i + round];
                int preIdx = i;
                while (preIdx >= 0 && current < nums[preIdx]) {
                    nums[preIdx + round] = nums[preIdx];
                    preIdx-=round;
                }
                nums[preIdx + round] = current;
            }
            round /= 2;
        }

        return nums;
    }
}

