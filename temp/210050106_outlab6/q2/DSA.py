################################## Data Structures ################################

# ------------------------------- Singly Linked List -----------------------------

class SinglyLinkedListNode:
    """The class SinglyLinkedListNode is implementation of data structure Sindle Linked List 
    | It has constructor with 1 parameter 
    | def __init__(self, data) 
    | It has 1 converter 
    | def __str__(self) 
    | It has no member functions\n
    :param data: value to be stored in node 
    :type data: long long int
    :param next: gives pointer to next node
    :type next: SingleLinkedListNode*
    """
    def __init__(self, data):
        """Constructor of the class SinglyLinkedListNode, takes one argument data.\n
        :param data: value of a node
        :type data: long long int\n
        :Example:
            >>> import DSA
            >>> Node = DSA.SinglyLinkedListNode(5)
            >>> x = Node.data
            >>> print(x)
            5
        """        
        self.data = data
        self.next = None
    
    def __str__(self):
        """This is conventor which returns srting representation of object \n
        :return: data stored in node
        :rtype: string
        :Example:
            >>> import DSA
            >>> L=DSA.SinglyLinkedListNode(2)
            >>> p= L.__str__()
            >>> print(p)
            2
        """
        return str(self.data)

class SinglyLinkedList:
    """The class SinglyLinkedList is implementation of data structure Sindle Linked List \n 
    | It has  1 constructor with no parameters 
    | def __init__(self)
    | It has following member functions 
    | (i)def insert(self, data) 
    | (ii)def find(self, data)   
    | (iii)def deleteVal(self, data) 
    | (iv)def printer(self, sep = ', ')
    | (v)def reverse(self) \n
    :param head: pointer to first element in linkedlist
    :type head: SinglyLinkedListNode *
    :param tail: pointer to last element in Linkedlist
    :type tail: SingleLinkedListNode*
    """
    def __init__(self):
        """constructor taking no parameters \n
        Whenever this constructor is caleed it initialises variable head to none and variable tail to none \n
        :Example:
            >>> import DSA
            >>> SL = DSA.SinglyLinkedList()
        """
        self.head = None
        self.tail = None

    def insert(self, data):
        """This functions inserts a node with value data at end of list and updates variable tail to pointer of inserted node \n
        :param data: value of node to be inserted in list
        :type data: long long int
        :return: none
        :rtype: none
        :Example:
            >>> import DSA
            >>> SL = DSA.SinglyLinkedList()
            >>> SL.insert(30)
            >>> SL.insert(40)
        """
        node = SinglyLinkedListNode(data) # new node
        if not self.head: # no head
            self.head = node
        else:
            self.tail.next = node # add behind tail
        self.tail = node # move tail
    
    def find(self, data):
        """This function find node whose value is data in linkedlist by traversing throigh list from head to tail until node is found \n
        :param data: value of node which is to be find in list
        :type data: long long int
        :return: returns pointer to prev node if found else returns none
        :rtype: SinglyLinkedListNode *
        :Example:
            >>> import DSA
            >>> SL = DSA.SinglyLinkedList()
            >>> SL.insert(30)
            >>> SL.insert(40)
            >>> l=SL.find(40)
            >>> p=l.data
            >>> print(p)
            30
        """
        head = self.head
        prev = None
        while head != None and head.data != data:
            prev = head
            head = head.next
        return prev
    
    def deleteVal(self, data):
        """This function deletes node whose value is data if not found returns false if found points next for prev of this node to next of node to be deleted \n
        :param data: value of node which is to be deleted
        :type data: long long int
        :return: if node is found returns true else returns false
        :rtype: bool
        :Example:
            >>> import DSA
            >>> SL = DSA.SinglyLinkedList()
            >>> SL.insert(30)
            >>> SL.insert(40)
            >>> SL.deleteVal(40)
            True
        """
        prevPos = self.find(data)
        if prevPos.next == None:
            return False
        prevPos.next.next = prevPos.next
        return True
    
    def printer(self, sep = ', '):
        """This function prints pointers for all nodes from head to tail by traversing through list \n
        :return: none
        :rtype: none
        :Example:
            >>> import DSA
            >>> SL = DSA.SinglyLinkedList()
            >>> SL.insert(30)
            >>> SL.insert(40)
            >>> SL.insert(10)
            >>> SL.printer()
            [30, 40, 10]
        """
        ptr = self.head
        print('[', end = '')
        while ptr != None:
            print(ptr, end = '')
            ptr = ptr.next
            if ptr != None:
                print(sep, end = '')
        print(']')
    
    def reverse(self):
        """This function reverses the whole list \n
        :return: none
        :rtype: none
        :Example:
            >>> import DSA
            >>> SL = DSA.SinglyLinkedList()
            >>> SL.insert(30)
            >>> SL.insert(40)
            >>> SL.insert(10)
            >>> SL.reverse()
            >>> SL.printer()
            [10, 40, 30]
        """

        head = self.head # head pointer
        prev = None # previous pointer
        while head != None: # while there is forward link left
            newHead = head.next # save extra pointer to next element
            head.next = prev # reverse the link of current element
            prev = head # move pointer to previous element
            head = newHead # use extra pointer to move to next element
        self.tail = self.head
        self.head = prev

def merge(list1, list2):
    """This function merges two linked lists list1 and list 2 \n
    :param list1: first list which is to be merged with another list
    :type list1: SinglyLinkedList
    :param list2: second list which is to be merged with another list
    :type list2: SinglyLinkedList
    :return: the merged list
    :rtype: SinglyLinkedList
    :Example:
        >>> import DSA
        >>> L1 = DSA.SinglyLinkedList()
        >>> L1.insert(30)
        >>> L1.insert(40)
        >>> L1.insert(10)
        >>> L2 = DSA.SinglyLinkedList()
        >>> L2.insert(70)
        >>> L2.insert(5)
        >>> L2.insert(20)
        >>> L3=DSA.merge(L1,L2)
        >>> L3.printer()
        [30, 40, 10, 70, 5, 20]
        """
    merged = SinglyLinkedList()
    head1 = list1.head
    head2 = list2.head
    while head1 != None and head2 != None: # both lists not empty
        if head1.data < head2.data: # link node with smaller data
            merged.insert(head1.data)
            head1 = head1.next
        else:
            merged.insert(head2.data)
            head2 = head2.next
    if head1 == None and head2 != None: # list 1 finished
        merged.tail.next = head2 # add remaining list 2 as is
    if head1 != None and head2 == None: # list 2 finished
        merged.tail.next = head1 # add remaining list 1 as is
    return merged

# ------------------------------ Doubly Linked List ----------------------------

class DoublyLinkedListNode:
    """The class DoublyLinkedListNode is implementation of data structure Doubly Linked List \n 
    | It has constructor with 1 parameter 
    | def __init__(self,data) 
    | It has conventor 
    | def __str__(self) 
    | It has no member functions \n
    :param data: value to be inserted in node
    :type data: long long int
    :param next: pointer to next node
    :type next: DoubleLinkedListNode*
    :param prev: pointer to prev node
    :type prev: DoubltLinkedListNode*
    """
    def __init__(self, data):
        """constructor with 1 parameter \n
        Whenever this constructor is called it initialises variable data to none and variable next to none and variable pre to none \n
        :param data: value to be inserted in node
        :type data: long long int
        :Example:
            >>> import DSA
            >>> DL = DSA.DoublyLinkedListNode(2)
            >>> p = DL.data
            >>> print(p)
            2
        """

        self.data = data
        self.next = None
        self.prev = None
    
    def __str__(self):
        """This is conventor which returns srting representation of object \n
        :return: data stored in node
        :rtype: string
        :Example:
            >>> import DSA
            >>> L=DSA.DoublyLinkedListNode(2)
            >>> p= L.__str__()
            >>> print(p)
            2
        """
        return str(self.data) 

class DoublyLinkedList:
    """The class DoublyLinkedList is implementation of data structure Doubly Linked List \n 
    | It has constructor with no parameters 
    | def __init__(self) 
    | It has following member functions 
    | (i)def insert(self, data) 
    | (ii)def printer(self, sep = ', ') 
    | (iii)def reverse(self) \n
    :param head: gives pointer to head of linkedlist
    :type head: DoublyLinkedListNode*
    :param tail: gives pointer to tail of linkedlist
    :type tail: DoublyLinkedListNode*
    """
    def __init__(self):
        """constructor with 0 parameters \n
        Whenever this constructor is called it initialises variable head to none and variable tail to none \n
        :Example:
            >>> import DSA
            >>> DL = DSA.DoublyLinkedList()
        """
        self.head = None
        self.tail = None
    
    def insert(self, data):
        """
        This function inserts node with value data at tail of list by  pointing next of tail of list to new node and pointing prev of new node to tail and then updating tail of list to new node \n
        :param data: value to be stored in node which is to be inserted
        :type data: long long int
        :return: none
        :rtype: none
        :Example:
            >>> import DSA
            >>> DL = DSA.DoublyLinkedList()
            >>> DL.insert(30)
            >>> DL.insert(40)
        """
        node = DoublyLinkedListNode(data) # new node
        if not self.head: # no head
            self.head = node
        else:
            self.tail.next = node # add behind tail
            node.prev = self.tail
        self.tail = node # move tail
    
    def printer(self, sep = ', '):
        """This function prints pointers for all nodes from head to tail by traversing through list \n
        :return: none
        :rtype: none
        :Example:
            >>> import DSA
            >>> DL = DSA.DoublyLinkedList()
            >>> DL.insert(30)
            >>> DL.insert(40)
            >>> DL.insert(10)
            >>> DL.printer(sep = ', ')
            [30, 40, 10]
        """
        ptr = self.head
        print('[', end = '')
        while ptr != None:
            print(ptr, end = '')
            ptr = ptr.next
            if ptr != None:
                print(sep, end = '')
        print(']')
    
    def reverse(self):
        """This function reverses the whole list \n
        :return: none
        :rtype: none
        :Example:
            >>> import DSA
            >>> DL = DSA.DoublyLinkedList()
            >>> DL.insert(30)
            >>> DL.insert(40)
            >>> DL.insert(10)
            >>> DL.reverse()
            >>> DL.printer()
            [10, 40, 30]
        """
        head = self.head # head pointer
        prev = None # previous pointer
        while head != None: # new node left
            newHead = head.next # save pointer to next node (cut forward link)
            if newHead != None: # check if next node has a reverse link
                newHead.prev = head # save pointer to previous node (cut reverse link)
            head.next = prev # reverse the forward link
            head.prev = newHead # reverse the reverse link
            prev = head # move pointer to previous element
            head = newHead # use saved pointer to move head
        self.tail = self.head
        self.head = prev

# -------------------------- Binary Search Tree ------------------------------


class BSTNode:
    """The class BSTNode is implementation of data structure Binary Search Tree \n 
    | It has constructor with 1 parameter 
    | def __init__(self,info) 
    | It has 1 conventor 
    | def __str__(self)
    | It has no member functions. \n
    :param info: value to be stored in node
    :type info: long long int
    :param left: gives pointer to its left BSTnode
    :type left: BSTNode*
    :param right: gives pointer to its right BSTnode
    :type right: BSTNode*
    :param level: gives level of BSTnode
    :type level: long long int
    """
    def __init__(self, info):
        """constructor taking 1 paramter\n
        Whenever this constructor is called it initialises variable info to given info and variable left to none and variable right to none and variable level to 0 \n
        :param info: value to be stored in node
        :type info: long long int
        :Example:
            >>> import DSA
            >>> B = DSA.BSTNode(5)
            >>> p = B.info
            >>> print(p)
            5
        """
        self.info = info
        self.left = None
        self.right = None
        self.level = 0
    
    def __str__(self):
        """This is conventor which returns srting representation of object \n
        :return: value stored in node
        :rtype: string
        :Example:
            >>> import DSA
            >>> L=DSA.BSTNode(5)
            >>> p= L.__str__()
            >>> print(p)
            5
        """
        return str(self.info)

class BinarySearchTree:
    """The class BinarySearchTree is implementation of data structure Binary Search Tree \n 
    | It has constructor with no parameters 
    | def __init__(self) 
    | It has following member functions 
    | (i)def insert(self, val) 
    | (ii)def traverse(self, order) 
    | (iii)def height(self, root). \n
    :param root: root of tree
    :type root: BSTNode*
    """
    def __init__(self):
        """constructor taking no parameter \n
        Whenever this constructor is called it initialises variable root  to none \n
        :Example:
            >>> import DSA
            >>> BST = DSA.BinarySearchTree()
        """
        self.root = None
    
    def insert(self, val):
        """This functions inserts node with value val in tree by finding its correct position in tree. \n
        :param val: value of node to be inserted
        :type val: long long int
        :return: none
        :rtype: none
        :Example:
            >>> import DSA
            >>> BST = DSA.BinarySearchTree()
            >>> BST.insert(70)
        """
        if self.root == None:
            self.root = BSTNode(val)
        else:
            current = self.root
            while True:
                if val < current.info: # move to left sub-tree
                    if current.left:
                        current = current.left # root moved
                    else:
                        current.left = BSTNode(val) # left init
                        break
                elif val > current.info: # move to right sub-tree
                    if current.right:
                        current = current.right # root moved
                    else:
                        current.right = BSTNode(val) # right init
                        break
                else:
                    break # value exists
    
    def traverse(self, order):
        """This functions prints all nodes in tree by  traversing tree according to order i.e pre/post/in \n
        :param order: decides which function to be called i.e preorder/inOrder/postOrder
        :type order: string
        :return: none
        :rtype: none
        :Example:
            >>> import DSA
            >>> BST = DSA.BinarySearchTree()
            >>> BST.insert(5)
            >>> BST.insert(10)
            >>> BST.insert(4)
            >>> BST.insert(1)
            >>> BST.insert(15)
            >>> BST.traverse("PRE")
            5 4 1 10 15 
            >>> BST.traverse("IN")
            1 4 5 10 15 
            >>> BST.traverse("POST")
            1 4 15 10 5 
        """
        def preOrder(root):
            print(root.info, end = ' ')
            if root.left != None:
                preOrder(root.left)
            if root.right != None:
                preOrder(root.right)
        def inOrder(root):
            if root.left != None:
                inOrder(root.left)
            print(root.info, end = ' ')
            if root.right != None:
                inOrder(root.right)
        def postOrder(root):
            if root.left != None:
                postOrder(root.left)
            if root.right != None:
                postOrder(root.right)
            print(root.info, end = ' ')
        if order == 'PRE':
            preOrder(self.root)
        elif order == 'IN':
            inOrder(self.root)
        elif order == 'POST':
            postOrder(self.root)
    
    def height(self, root):
        """This functions calculates height of root \n
        :param root: Node for which height should be calculated 
        :type root: BSTNode*
        :return: height of root
        :rtype: int
        :example:
            >>> import DSA
            >>> BST = DSA.BinarySearchTree()
            >>> BST.insert(5)
            >>> BST.insert(10)
            >>> BST.insert(4)
            >>> BST.insert(1)
            >>> BST.insert(15)
            >>> BST.height(BST.root)
            2
            >>> BST.height(BST.root.left)
            1
            >>> BST.height(BST.root.right)
            1
        """
        if root.left == None and root.right == None:
            return 0
        elif root.right == None:
            return 1 + self.height(root.left)
        elif root.left == None:
            return 1 + self.height(root.right)
        else:
            return 1 + max(self.height(root.left),self.height(root.right))

# --------------------------------- Suffix Trie --------------------------------

class Trie:
    """The class Trie is implementation of data structure Suffix Trie \n 
    | It has constructor with no parameters 
    | def __init__(self) 
    | It has following member functions 
    | (i)def find(self, root, c) 
    | (ii)def insert(self, s) 
    | (iii)def checkPrefix(self, s) 
    | (iv)def countPrefix(self, s).. \n
    :param T: to store list of words inserted in trie
    :type T: string
    """
    def __init__(self):
        """constructor taking no parameter \n
        Whenever this constructor is called it initialises variable T to empty set \n
        :Example:
            >>> import DSA
            >>> T = DSA.Trie()
        """
        self.T = {}
    
    def find(self, root, c):
        """This function finds whether c is present in root if present return true else return false \n
        :param root: root of trie in which we have to search c
        :type root: Trie*
        :param c: character need to be searched in trie
        :type c: char
        :return: if present true else false
        :rtype: bool
        :Example:
            >>> import DSA
            >>> trie = DSA.Trie()
            >>> trie.insert("cat")
            >>> trie.insert("car")
            >>> trie.insert("bat")
            >>> trie.insert("cat")
            >>> trie.find(trie.T,'c')
            True
        """
        return (c in root)
    
    def insert(self, s):
        """This function inserts string s in trie \n 
        :param s: string to be inserted
        :type s: string
        :return: none
        :rtype: none
        :Example:
            >>> import DSA
            >>> trie = DSA.Trie()
            >>> trie.insert("cat")
            >>> trie.insert("car")
            >>> trie.insert("bat")
        """
        root = self.T
        for c in s:
            if not self.find(root,c):
                root[c] = {}
            root = root[c]
            root.setdefault('#',0)
            root['#'] += 1
    
    def checkPrefix(self, s):
        """This function checks whether string s is a prefix for any word in trie / not if yes return true else return false \n
        :param s: prefix string
        :type s: string
        :return: if s is prefix then true else false
        :rtype: bool
        :Example:
            >>> import DSA
            >>> trie = DSA.Trie()
            >>> trie.insert("cat")
            >>> trie.insert("car")
            >>> trie.insert("bat")
            >>> trie.checkPrefix("ca")
            True
            >>> trie.checkPrefix("cap")
            False
        """
        root = self.T
        for idx, char in enumerate(s):
            if char not in root:
                if idx == len(s) - 1:    
                    root[char] = '#'
                else:
                    root[char] = {}
            elif root[char] == '#' or idx == len(s) - 1:
                return True
            root = root[char]
        return False
    
    def countPrefix(self, s):
        """This function counts for any words in trie string s is prefix \n
        :param s: prefix string
        :type s: string
        :return: count of no.of words
        :rtype: int 
        :Example:
            >>> import DSA
            >>> trie = DSA.Trie()
            >>> trie.insert("cat")
            >>> trie.insert("car")
            >>> trie.insert("bat")
            >>> trie.countPrefix("ca")
            2
            >>> trie.countPrefix("ar")
            0
        """
        found = True
        root = self.T
        for c in s:
            if self.find(root,c):
                root = root[c]
            else:
                found = False
                break
        if found:
            return root['#']
        return 0
class Heap:
    """The class heap is implementation of data structure heap \n 
    | It has constructor with 1 parameter 
    | def __init__(self, cap)  
    | It has following member functions 
    | (i)def parent(self, i) 
    | (ii)def left(self, i) 
    | (iii)def right(self, i) 
    | (iv)def insert(self, val)
    | (v)def min(self) 
    | (vi)def Heapify(self, root) 
    | (vii)def deleteMin(self). \n
    :param H: array list which stores heap values
    :type H: list
    :param n: no.of values present
    :type n: int
    :param M: it is max no.of elements that can be stored
    :type M: int

    """
    def __init__(self, cap):
        """constructor taking 1 parameter \n
        Whenever this constructor is called it initialises variable M to cap and variable n to 0 and makes H to an empty array list \n
        :param cap: capacity of heap
        :type cap: int
        :Example:
            >>> import DSA
            >>> heap = DSA.Heap(40)
            >>> p = heap.M
            >>> print(p)
            40
        """
        self.H = [0]*(cap)
        self.n = 0
        self.M = cap
    
    def parent(self, i):
        """This functions gives index of its parent \n
        :param i: index of node
        :type i: int
        :return: index of parent
        :rtype: int
        :Example:
            >>> import DSA
            >>> heap = DSA.Heap(40)
            >>> heap.insert(40)
            >>> heap.insert(70)
            >>> heap.insert(80)
            >>> heap.parent(1)
            0
        """
        return (i - 1) // 2
    
    def left(self, i):
        """This functions gives index of its left child \n
        :param i: index of node
        :type i: int
        :return: index of left child
        :rtype: int
        :Example:
            >>> import DSA
            >>> heap = DSA.Heap(40)
            >>> heap.insert(40)
            >>> heap.insert(70)
            >>> heap.insert(80)
            >>> heap.left(0)
            1
        """
        return (2 * i) + 1
    
    def right(self, i):
        """This functions gives index of its right child \n
        :param i: index of node
        :type i: int
        :return: index of right child
        :rtype: int
        :Example:
            >>> import DSA
            >>> heap = DSA.Heap(40)
            >>> heap.insert(40)
            >>> heap.insert(70)
            >>> heap.insert(80)
            >>> heap.right(0)
            2
        """
        return 2 * (i + 1)
    
    def insert(self, val):
        """This functions inserts new node whose value is val into heap by finding appropriate position\n
        It has single parameter \n
        :param val: value of node
        :type val: int
        :return: none
        :rtype: none
        :Example:
            >>> import DSA
            >>> heap = DSA.Heap(40)
            >>> heap.insert(40)
            >>> heap.insert(70)
            >>> heap.insert(80)
        """
        if self.n != self.M:
            self.H[self.n] = val
            i = self.n
            self.n += 1
            while i != 0 and self.H[self.parent(i)] > self.H[i]:
                self.H[i], self.H[self.parent(i)] = self.H[self.parent(i)], self.H[i]
                i = self.parent(i)
    
    def min(self):
        """This function gives minimum of heap\n
        It has no parameters \n
        :return: if list is not empty returns value at H[0](returns min element)
        :rtype: int
        :Example:
            >>> import DSA
            >>> heap = DSA.Heap(40)
            >>> heap.insert(40)
            >>> heap.insert(70)
            >>> heap.insert(80)
            >>> heap.min()
            40
        """
        if (self.n != 0):
            return self.H[0]
        return -1
    
    def Heapify(self, root):
        """This function heapify the heap\n
        It has 1 parameter\n
        Starting from node compare to its child find first largest element and swap current element with smallest child continue this until smallest child is not found \n
        :param root: index of element for which we have to do heapify
        :type root: int
        :return: none
        :rtype: none
        :Example:
            >>> import DSA
            >>> heap = DSA.Heap(40)
            >>> heap.insert(90)
            >>> heap.insert(70)
            >>> heap.insert(80)
            >>> heap.Heapify(0)
            >>> heap.min()
            70
        """
        l = self.left(root)
        r = self.right(root)
        s = root
        if (l < self.n and self.H[l] < self.H[root]):
            s = l
        if (r < self.n and self.H[r] < self.H[s]):
            s = r
        if s != root:
            self.H[root], self.H[s] = self.H[s], self.H[root]
            self.Heapify(s)
        
    def deleteMin(self):
        """This function delete min element\n
        It has no parameters\n
        If size of heap is 1 then make heap an empty list else just delete element at H[0] by keeping last element in its position and reducing size of list by 1 \n
        :return: none
        :rtype: none
        :Example:
            >>> import DSA
            >>> heap = DSA.Heap(40)
            >>> heap.insert(70)
            >>> heap.insert(80)
            >>> heap.insert(90)
            >>> heap.insert(100)
            >>> heap.Heapify(0)
            >>> heap.deleteMin()
            >>> heap.min()
            80
        """
        if self.n > 0:
            if self.n == 1:
                self.H = []
                self.n = 0
            else:
                self.n -= 1
                self.H[0] = self.H[self.n]
                self.H.pop()
                self.Heapify(0)        
