//反转一个单链表。
//
// 示例:
//
// 输入: 1->2->3->4->5->NULL
//输出: 5->4->3->2->1->NULL
//
// 进阶:
//你可以迭代或递归地反转链表。你能否用两种方法解决这道题？
//

/**
 * Definition for singly-linked list.
 * public class ListNode {
 * int val;
 * ListNode next;
 * ListNode(int x) { val = x; }
 * }
 */
class Solution {
    public ListNode reverseList(ListNode head) {
//        ListNode result = new ListNode(0);
//        while (head != null) {
//            ListNode tmp = result.next;
//            result.next = head;
//            head = head.next;
//            result.next.next = tmp;
//        }
//        return result.next;
        ListNode result=null;
        ListNode cur=head;
        while(cur!=null){
            ListNode tmp=cur.next; // 记录下一指针
            cur.next=result; // 当前翻转结果接入当前节点之后
            result=cur; // 记录新的翻转结果
            cur=tmp; // 进入下一轮
        }
        return result;
    }
}
