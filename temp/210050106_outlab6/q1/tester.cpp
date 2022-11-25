#include "DSA.cpp"
using namespace std;

int main (int argc, char* argv []) {

    // Singly Linked List
    SinglyLinkedList L;
    L.insert(2);
    L.printer();
    SinglyLinkedList L2 = L;
    L.insert(1);
    L.printer(" ");
    L.reverse();
    L.printer();
    L2 = merge(L,L2);
    L2.printer();

    // Doubly Linked List
    DoublyLinkedList L1;
    L1.insert(2);
    L1.printer();
    L1.insert(1);
    L1.printer(" ");
    L1.reverse();
    L1.printer();

}