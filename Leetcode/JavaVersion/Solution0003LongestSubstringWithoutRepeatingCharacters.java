import java.util.HashMap;
import java.util.Map;

/**
 * @author learnzpk
 * @date 2019/05/21
 * @description
 */
public class Solution0003LongestSubstringWithoutRepeatingCharacters {
    /**
     * 用一个临时字符串记录当前不重复子串
     */
    public int lengthOfLongestSubstring(String s) {
        int curMaxLen = 0;
        StringBuilder tmp = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            String tmpStr = tmp.toString();
            int findIndex = tmpStr.indexOf(s.charAt(i));
            if (-1 == findIndex) {
                tmp.append(s.charAt(i));
                continue;
            }
            curMaxLen = Math.max(curMaxLen, tmp.length());
            tmp = new StringBuilder(tmpStr.substring(findIndex + 1));
            tmp.append(s.charAt(i));
        }

        return Math.max(curMaxLen, tmp.length());
    }

    /**
     * 双指针的解法: 指针i用于扫描字符串，指针j用于记录最后一个发现相同字符的位置
     */
    public int lengthOfLongestSubstring2(String s) {
        int curMaxLen = 0;
        Map<Character, Integer> map = new HashMap<>(16);
        for (int i = 0, j = 0; i < s.length(); ++i) {
            Character chr = s.charAt(i);
            if (map.containsKey(chr)) {
                j = Math.max(j, map.get(chr) + 1);
            }
            map.put(chr, i);
            curMaxLen = Math.max(curMaxLen, i - j + 1);
        }
        return curMaxLen;
    }

    public static void main(String[] args) {
        System.out.println(new Solution0003LongestSubstringWithoutRepeatingCharacters().lengthOfLongestSubstring2(""));
    }
}
