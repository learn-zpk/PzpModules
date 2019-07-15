import java.util.ArrayList;
import java.util.List;

/**
 * @author learnzpk
 * @date 2019/05/22
 * @description
 */
public class Solution004MedianOfTwoSortedArrays {
    public double findMedianSortedArrays(int[] nums1, int[] nums2) {
        int idx1 = 0, idx2 = 0;
        int nums1Len = nums1.length, nums2Len = nums2.length;
        int cur = 0;
        List<Integer> returnList = new ArrayList<>(2);
        while (idx1 < nums1Len || idx2 < nums2Len) {
            if (2 * cur - 2 - nums1Len > nums2Len) {
                break;
            }

            int value1 = idx1 == nums1Len ? Integer.MAX_VALUE : nums1[idx1];
            int value2 = idx2 == nums2Len ? Integer.MAX_VALUE : nums2[idx2];
            cur++;
            boolean bool = 2 * cur - 2 - nums1Len <= nums2Len && nums2Len <= 2 * cur - nums1Len;
            if (value1 < value2) {
                if (bool) {
                    returnList.add(value1);
                }
                idx1++;
            } else {
                if (bool) {
                    returnList.add(value2);
                }
                idx2++;
            }

        }
        int total = 0;
        for (int i : returnList) {
            total += i;
        }
        return (double) total / returnList.size();
    }

    public static void main(String[] args) {
        System.out.println(new Solution004MedianOfTwoSortedArrays().findMedianSortedArrays(new int[]{-1, 3}, new int[]{}));
    }
}
