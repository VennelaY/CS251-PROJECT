from DSA import *
from copy import copy

# Singly Linked List
L = SinglyLinkedList()
L.insert(2)
L.printer()
L2 = copy(L)
L.insert(1)
L.printer(' ')
L.reverse()
L.printer()
L2 = merge(L,L2)
L2.printer()

# Doubly Linked List
L = DoublyLinkedList()
L.insert(2)
L.printer()
L.insert(1)
L.printer(' ')
L.reverse()
L.printer()