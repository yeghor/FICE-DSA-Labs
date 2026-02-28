from __future__ import annotations
import random
import string


class Node:
    """
    Doubly connected linked list node
    """

    def __init__(self, val: str, next_: Node | None = None, prev: Node | None = None):
        if len(val) > 5:
            raise ValueError("Maximum value length exceeded!")

        self.val = val
        self.next = next_
        self.prev = prev

    def __str__(self):
        return f"[{self.val}]"

    def __repr__(self):
        return f"[{self.val}]"


class LinkedList:
    @staticmethod
    def validate_value(val: any) -> None:
        """Raises: ValueError on invalid val"""
        if len(val) > 5:
            raise ValueError("Maximum value length exceeded!")
        elif not isinstance(val, str):
            raise ValueError("Invalid value type. Must be str!")

    def __init__(self, head: Node | None = None):
        self.__head = head
        self.__tail = head

    @property
    def head(self) -> str | None:
        if self.__head:
            return f"[{self.__head.val}]"

    @property
    def tail(self) -> str | None:
        if self.__tail:
            return f"[{self.__tail.val}]"

    def __str__(self) -> str:
        string = ""

        curr = self.__head
        idx = 0
        while curr:
            string += f"{idx}: {curr} -> "
            curr = curr.next
            idx += 1

        if string:
            string += "None"
        else:
            string = "Empty List"

        return string

    def clear(self) -> None:
        # Garbage collector will delete sequent nodes
        # Since we are nulling head & tail, nothing will refer to rest of the nodes
        self.__head = None
        self.__tail = None

    def __len__(self) -> int:
        length = 0
        curr = self.__head

        while curr:
            length += 1
            curr = curr.next

        return length

    def reverse_in_place(self) -> None:
        if not self.__head:
            return

        curr = self.__tail

        # Swapping list head and tail
        self.__head, self.__tail = curr, self.__head

        while curr:
            temp = curr.prev

            curr.prev = curr.next
            curr.next = temp

            curr = temp

    def append(self, val: str) -> None:
        self.validate_value(val)

        new_node = Node(val, None, None)

        if not self.__head:
            self.__head = new_node
            self.__tail = new_node
            return

        self.__tail.next = new_node
        new_node.prev = self.__tail

        self.__tail = new_node

    def delete_by_value(self, val: str) -> bool:
        """Returns boolean value whether the node was deleted. \n\n Deletes only first matching value found"""

        if not self.__head:
            return False

        curr = self.__head

        while curr:
            if curr.val == val:
                if not curr.prev:
                    self.__head = curr.next
                    if self.__head:
                        self.__head.prev = None
                        return True
                    self.__tail = self.__head
                    return True
                if not curr.next:
                    curr.prev.next = None
                    self.__tail = curr.prev
                    return True

                prev = curr.prev
                next_ = curr.next

                prev.next = next_
                next_.prev = prev

                return True
            else:
                curr = curr.next

        return False


if __name__ == "__main__":
    ll = LinkedList()

    n = int(input("Enter the list length (digit, greater than zero): "))

    for i in range(n):
        val = "".join([random.choice(string.ascii_lowercase) for _ in range(5)])
        ll.append(val)

    print("Original list:")
    print(ll)

    ll.reverse_in_place()

    print("Reversed list:")
    print(ll)

    print(f"List's head: {ll.head}")
    print(f"List's tail: {ll.tail}")

    while 1:
        if len(ll) == 0:
            break

        to_delete = input(
            "Choose value of node you want to delete (type 'exit' to finish): "
        )

        if to_delete == "exit":
            break

        ll.delete_by_value(to_delete)

        print(ll)
        print(f"List's head after deletion: {ll.head}")
        print(f"List's tail after deletion: {ll.tail}")
