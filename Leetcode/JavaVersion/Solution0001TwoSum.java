package JavaVersion;

import java.util.HashMap;
import java.util.Map;

/**
 * @author learnzpk
 * @date 2019/05/20
 * @description
 */
public class Solution0001TwoSum {
    public int[] twoSum(int[] nums, int target) {
        int[] result = new int[2];
        Map<Integer, Integer> map = new HashMap(16);

        for (int i = 0; i < nums.length; i++) {
            Integer needKey = target - nums[i];
            if (map.containsKey(needKey)) {
                result[0] = map.get(needKey);
                result[1] = i;
                return result;
            }
            map.put(nums[i], i);
        }
        return result;
    }

    public static void main(String[] args) {
        int[] nums = {2, 7, 11, 15};
        int target = 22;
        int[] result = new JavaVersion.Solution0001TwoSum().twoSum(nums, target);
        System.out.println("" + result[0] + "" + result[1]);
    }
}
