# 给定一个二叉树，判断其是否是一个有效的二叉搜索树。
#
# 假设一个二叉搜索树具有如下特征： 
#
# 
# 节点的左子树只包含小于当前节点的数。 
# 节点的右子树只包含大于当前节点的数。 
# 所有左子树和右子树自身必须也是二叉搜索树。 
# 
#
# 示例 1: 
#
# 输入:
#    2
#   / \
#  1   3
# 输出: true
# 
#
# 示例 2: 
#
# 输入:
#    5
#   / \
#  1   4
#      / \
#     3   6
# 输出: false
# 解释: 输入为: [5,1,4,null,null,3,6]。
#      根节点的值为 5 ，但是其右子节点值为 4 。
# 
# Related Topics 树 深度优先搜索


# leetcode submit region begin(Prohibit modification and deletion)
# Definition for a binary tree node.
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


class Solution(object):
    def core(self, node):
        left_max, right_min, flag = node.val, node.val, True
        if node.left:
            l_max, r_min, left_flag = self.core(node.left)
            if not left_flag or l_max >= node.val:
                flag = False
            left_max = max(l_max, left_max)
            right_min = min(right_min, r_min)
        if node.right:
            l_max, r_min, right_flag = self.core(node.right)
            if not right_flag or r_min <= node.val:
                flag = False
            left_max = max(l_max, left_max)
            right_min = min(r_min, right_min)
        return left_max, right_min, flag

    def isValidBST(self, root):
        if not root:
            return True
        _, __, flag = self.core(root)
        return flag


def gene_tree(_arr):
    node_dict = {}
    for idx, num in enumerate(_arr):
        if not num:
            continue
        node_dict[idx] = TreeNode(num)
        if idx == 0:
            continue
        p_idx = (idx - 1) // 2
        if idx % 2 == 0:
            node_dict[p_idx].right = node_dict[idx]
        else:
            node_dict[p_idx].left = node_dict[idx]
    return node_dict[0] if node_dict else None


if __name__ == '__main__':
    arr = [5, 1, 4, None, None, 3, 6]
    # arr = [10, 5, 15, None, None, 6, 20]
    # arr=[2,1,3]
    root = gene_tree(arr)
    print(Solution().isValidBST(root))
