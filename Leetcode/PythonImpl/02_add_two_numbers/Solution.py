"""
将list转换成数字
"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:

    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        def node2num(node):
            num = 0
            multiple = 1
            while node != None:
                num = num + multiple * node.val
                multiple *= 10
                node = node.next
            return num

        def num2node(num):
            begin_node = ListNode(-1)
            cur_node = begin_node
            if num == 0:
                return ListNode(0)
            while num / 10 != 0:
                cur_node.next = ListNode(num % 10)
                cur_node = cur_node.next
                num = num // 10
            return begin_node.next

        return num2node(node2num(l1) + node2num(l2))
