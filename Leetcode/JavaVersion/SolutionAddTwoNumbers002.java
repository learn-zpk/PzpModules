import Base.ListNode;

/**
 * @author learnzpk
 */
public class SolutionAddTwoNumbers002 {
    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        if (l1 == null && l2 == null) {
            return null;
        }
        ListNode result = new ListNode(0);
        ListNode tmp = result;
        int carryVal = 0;
        while (l1 != null || l2 != null || carryVal != 0) {
            if (l1 == null) {
                l1 = new ListNode(0);
            }
            if (l2 == null) {
                l2 = new ListNode(0);
            }
            tmp.val = (l1.val + l2.val + carryVal) % 10;
            carryVal = (l1.val + l2.val + carryVal) / 10;
            l1 = l1.next;
            l2 = l2.next;
            if(l1 != null || l2 != null || carryVal != 0){
                tmp.next = new ListNode(0);
                tmp = tmp.next;
            }
        }
        return result;
    }

    public static void main(String[] args) {

    }
}