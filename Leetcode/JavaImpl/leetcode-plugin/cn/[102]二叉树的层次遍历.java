//给定一个二叉树，返回其按层次遍历的节点值。 （即逐层地，从左到右访问所有节点）。
//
// 例如:
//给定二叉树: [3,9,20,null,null,15,7],
//
//     3
//   / \
//  9  20
//    /  \
//   15   7
//
//
// 返回其层次遍历结果：
//
// [
//  [3],
//  [9,20],
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
    public List<List<Integer>> levelOrder(TreeNode root) {
        List<List<Integer>> results = new ArrayList<>();
        if (root == null) {
            return results;
        }
        List<TreeNode> tmp = new ArrayList<>();
        tmp.add(root);

        while (tmp.size() != 0) {
            List<TreeNode> tmp2 = new ArrayList<>();
            List<Integer> result = new ArrayList<>();
            for (TreeNode node : tmp) {
                result.add(node.val);
                if (node.left != null) {
                    tmp2.add(node.left);
                }
                if (node.right != null) {
                    tmp2.add(node.right);
                }
            }
            results.add(result);
            tmp = tmp2;
        }
        return results;
    }

}
