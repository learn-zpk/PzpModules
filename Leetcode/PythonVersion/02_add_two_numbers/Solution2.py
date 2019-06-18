"""

"""


# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:

    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        begin_node = ListNode(-1)
        cur_node = begin_node
        carry = 0
        while carry != 0 or l1 != None or l2 != None:
            l1_val = l1.val if l1 else 0
            l2_val = l2.val if l2 else 0
            sum = l1_val + l2_val + carry
            cur_node.next = ListNode(sum % 10)
            carry = sum // 10
            cur_node = cur_node.next
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None
        return begin_node.next
