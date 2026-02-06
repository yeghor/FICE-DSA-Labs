from __future__ import annotations

class Node:
    """
    Doubly connected linked list node
    """
    def __init__(self, val: str, next: Node | None = None, prev: Node | None = None):
        if len(val) < 5:
            raise ValueError("Maximum value length exceeded!")

        self.val = val
        self.next = next
        self.prev = prev
    
    def __str__(self):
        return f'[{self.val}]'

    def __repr__(self):
        return f'[{self.val}]'

class LinkedList:
    @staticmethod
    def validate_value(self, val: any) -> None:
        """Raises: ValueError"""
        if len(val) < 5:
            raise ValueError("Maximum value length exceeded!")
        elif not isinstance(val, str):
            raise ValueError("Invalid value type. Must be str!")

    def __init__(self, head: Node):
        self.__head = head

    def __str__(self):
        string = ""

        curr = self.__head
        
        while curr:
            string += f"{curr} -> "
            curr = curr.next
        
        string += "None"

        return string

    def reverse_in_place(self) -> None:
        if not self.__head:
            return
        
        curr = self.__head

        # Traveling until we get the last node
        while curr.next:
            curr = curr.next

        # Updating the list head to the last node of the original list
        self.__head = curr

        while curr:
            temp = curr.prev
            curr.next = temp
            curr.prev = curr.next

            curr = temp


    def append(self, val: str) -> None:


        curr = self.__head

        while curr.next:
            curr = curr.next

        curr.next = Node(val, None, curr)
    
    def delete_by_value(self, val: str) -> bool:
        """Returns boolean value whether the node was deleted. \n\n Deletes only first matching value found"""

        if not self.__head:
            return False
        
        curr = self.__head

        while curr:
            if curr.val == val:
                if not curr.prev:
                    self.__head = curr.next
                    return True
                if not curr.next:
                    prev = curr.prev
                    prev.next = None
                    return True

                prev = curr.prev
                next_ = curr.next

                prev.next = next_
                next_.prev = prev

                return True

            else:
                curr = curr.next
