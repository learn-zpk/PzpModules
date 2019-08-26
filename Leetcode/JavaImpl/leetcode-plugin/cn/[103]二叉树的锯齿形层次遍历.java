//给定一个二叉树，返回其节点值的锯齿形层次遍历。（即先从左往右，再从右往左进行下一层遍历，以此类推，层与层之间交替进行）。
//
// 例如：
//给定二叉树 [3,9,20,null,null,15,7],
//
//     3
//   / \
//  9  20
//    /  \
//   15   7
//
//
// 返回锯齿形层次遍历如下：
//
// [
//  [3],
//  [20,9],
//  [15,7]
//]
//
//

/**
 * Definition for a binary tree node.
 * public class TreeNode {
 * int val;
 * TreeNode left;
 * TreeNode right;
 * TreeNode(int x) { val = x; }
 * }
 */
class Solution {
    public List<List<Integer>> zigzagLevelOrder(TreeNode root) {
        List<List<Integer>> results = new ArrayList<>();
        if (root == null) {
            return results;
        }
        List<TreeNode> tmp = new ArrayList<>();
        tmp.add(root);
        int flag = 1;
        while (tmp.size() != 0) {
            List<TreeNode> tmp2 = new ArrayList<>();
            LinkedList<Integer> result = new LinkedList<>();
            for (TreeNode node : tmp) {
                if (flag == 1) {
                    result.addLast(node.val);
                } else {
                    result.addFirst(node.val);
                }

                if (node.left != null) {
                    tmp2.add(node.left);
                }
                if (node.right != null) {
                    tmp2.add(node.right);
                }
            }
            results.add(result);
            tmp = tmp2;
            flag = -1 * flag;
        }
        return results;
    }

}
