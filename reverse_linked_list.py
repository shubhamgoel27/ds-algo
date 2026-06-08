from typing import Optional


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """Reverse a singly linked list iteratively. O(n) time, O(1) space.

        Invariant: `prev` is the head of the already-reversed prefix, `curr` is
        the front of the untouched suffix. Each step detaches `curr`, points it
        back at `prev`, and advances both. Save `curr.next` first -- once we
        overwrite it the rest of the list is unreachable.
        """
        prev, curr = None, head
        while curr is not None:
            temp = curr.next      # save the next link before clobbering it
            curr.next = prev      # reverse this node's pointer
            prev = curr           # extend the reversed prefix
            curr = temp           # advance into the suffix
        return prev               # new head = last node visited

    def reverseList_recursive(self, head: Optional[ListNode]) -> Optional[ListNode]:
        """Recursive variant. O(n) time, O(n) stack."""
        if head is None or head.next is None:
            return head
        new_head = self.reverseList_recursive(head.next)
        head.next.next = head     # the node ahead now points back at us
        head.next = None          # and we become the tail
        return new_head


def _build(values):
    head = None
    for v in reversed(values):
        head = ListNode(v, head)
    return head


def _to_list(head):
    out = []
    while head:
        out.append(head.val)
        head = head.next
    return out


if __name__ == "__main__":
    solution = Solution()
    test_cases = [[1, 2, 3, 4, 5], [], [1], [1, 2]]
    for values in test_cases:
        expected = values[::-1]
        assert _to_list(solution.reverseList(_build(values))) == expected, f"iterative failed on {values}"
        assert _to_list(solution.reverseList_recursive(_build(values))) == expected, f"recursive failed on {values}"
    print("All tests passed.")
