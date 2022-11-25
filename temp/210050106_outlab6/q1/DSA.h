/**
*@file DSA.cpp
*@author Narkedamilli Harika
*@date 21/09/2022
*@brief This file contains classes SingleLinkedListNode,SingleLinkedList,DoublyClassLinkedListNode,DoublyLinkedList,BSTNode,BinarySearchTree,Trie
which contains all required definitions and basic utilities functions of datastructures like Singly Linked List,Doubly Linked List,Binary Search Tree,Suffix Trie
*/
#include <bits/stdc++.h>
#define ll long long int
#define vi vector<int>
#define vll vector<ll>
using namespace std;

/* ------------------------------- Data Structures ---------------------------------- */

// ------------------------------- Singly Linked List -----------------------------


/**
 * @class SinglyLinkedListNode
 * @brief SinglyLinkedListNode
 * It contains 2 types of constructor (i)SinglyLinkedListNode () (ii)SinglyLinkedListNode (ll val) which creates node with given value by default value is -1 and point next to NULL \n
 * It has no member functions \n
 * @param  data Datatype ll
 * @param next Datatype SinglyLinkedListNode*
 */
class SinglyLinkedListNode 
{
    public:
        /**
        * @brief  data Datatype ll
        */
        ll data;
        /**
        * @brief next Datatype SinglyLinkedListNode*
        */
        SinglyLinkedListNode* next;
        /**
        *@brief constructor taking no parameters \n
        *Whenever this constructor is called it initialises variable data to -1 and variable next to NULL
        */
        SinglyLinkedListNode () ;
        /**
        *@brief constructor taking 1 parameter \n
        *Whenever this constructor is called it initialises variable data to val and variable next to NULL \n
        *@param[in] val of datatype ll
        */
        SinglyLinkedListNode (ll val) ;
};
/**
*defines the operator <<,the function takes two parameters
*@param [in] out
*@param [in] node
*@return ostream&
*/
ostream& operator<<(ostream &out, const SinglyLinkedListNode &node);
/**
*@class SinglyLinkedList
*@brief SinglyLinkedList
*It contains constructor with no parameters SinglyLinkedList ()which when instantiated points head and tail to NULL \n
*It contains member functions (i)void insert(ll data) (ii)SinglyLinkedListNode* find (ll data) (iii)bool deleteVal (ll data) (iv)void printer (string sep = ", ") \n
(v)void reverse () \n
*@param head Datatype SingleListNode*
*@param tail Datatype SingleListNode*
*/
class SinglyLinkedList {

    public:
        /**
        * @brief  head Datatype SingleListNode*
        */
        SinglyLinkedListNode *head;
        /**
        * @brief  tail Datatype SingleListNode*
        */
        SinglyLinkedListNode *tail;

        /**
        *constructor taking no parameters \n
        *Whenever this constructor is called it initialises variable head to NULL and variable tail to NULL \n
        */
        SinglyLinkedList () ;

        /**
        *@fn void insert (ll data)
        *@brief It is a member function and has 1 parameter \n
        *First it instantiates class SinglyListNode(data) and equates to node if head is NULL then it points head to node else points next of tail to node
        then points tail to node \n
        *@param [in] data of datatype ll
        */
        void insert (ll data) ;

        /**
        *@fn SinglyLinkedListNode* find (ll data)
        *@brief It is a member function and has 1 parameter \n
        *First it creates two variables ptr and prev of datatypes SinglyLinkedListNode* and initialises to head and prev then by using while loop it traverse through list to find node if founf then returns \n
        *@param [in] data of datatype ll 
        *@return which returns prev to function
        */
        SinglyLinkedListNode* find (ll data) ;

        /**
        *@fn bool deleteVal (ll data)
        *@brief It is a member function and has 1 parameter \n
        *It goes to node which is to be deleted and delete taht node and retirn true if found else return false \n
        *@param [in] data of datatype ll
        *@return which returns true/false according to function
        */
        bool deleteVal (ll data) ;

        /**
        *@fn void printer (string sep = ", ")
        *@brief It is a member function and has 1 parameter \n
        *It traverse through list and prints all nodes until tail starting from head \n
        *@param [in] sep of datatype string
        */
        void printer (string sep = ", ");

        /**
        *@fn void reverse ()
        *@brief It is a member function and has no parameters \n
        *It traverse through list and reverse list by just replacing left and right nodes and moving from ends to center
        */
        void reverse () ;

};
/**
*@fn SinglyLinkedList merge (SinglyLinkedList list1, SinglyLinkedList list2) 
*@brief It is a  function and has 2 parameters \n
*It merges two Singlylinkedlists and returns a combined lists \n
*@param [in] list1 of datatype SinglyLinkedList
*@param [in] list2 of datatype SinglyLinkedList
*@return which returns a merged SinglyLinkedList
*/
SinglyLinkedList merge (SinglyLinkedList list1, SinglyLinkedList list2) ;

// ------------------------------- Doubly Linked List -----------------------------
/**
*@class DoublyLinkedListNode
*@brief DoublyLinkedListNode \n
*It contains 2 types of constructor (i)DoublyLinkedListNode () (ii)DoublyLinkedListNode (ll val) which creates node with given value by default value is -1 and point next and prev to NULL \n
*It has no member functions \n
*@param data Datatype ll
*@param next Datatype DoubleLinkedListNode*
*@param prev Datatype DoubleLinkedListNode*
*/
class DoublyLinkedListNode {
    public:
        /**
        * @brief  data Datatype ll
        */
        ll data;
        /**
        * @brief  next Datatype DoublyLinkedListNode*
        */
        DoublyLinkedListNode *next;
        /**
        * @brief  prev Datatype DoublyLinkedListNode*
        */
        DoublyLinkedListNode *prev;

        /**
        *@brief constructor taking no parameters \n
        *Whenever this constructor is called it initialises variable data to -1 and variable next to NULL and variable prev to NULL
        */
        DoublyLinkedListNode () ;

        /**
        *@brief constructor taking 1 parameter \n
        *Whenever this constructor is called it initialises variable data to val and variable next to NULL and variable prev to NULL \n
        *@param[in] val of datatype ll 
        */
        DoublyLinkedListNode (ll val) ;

};

/**
*defines the operator <<,the function takes two parameters
*@param [in] out
*@param [in] node
*@return ostream&
*/
ostream& operator<<(ostream &out, const DoublyLinkedListNode &node);

/**
*@class DoublyLinkedList
*@brief DoublyLinkedList \n
*It contains a  constructor with no parameters DoublyLinkedListNode() \n
*It has following member functions (i)void insert (ll data) (ii)void printer (string sep = ", ") (iii)void reverse () \n
*@param head Datatype DoubleLinkedListNode* \n
*@param tail Datatype DoubleLinkedListNode* \n
*/
class DoublyLinkedList {
    public:
        /**
        * @brief  head Datatype DoublyLinkedListNode*
        */
        DoublyLinkedListNode *head; 
        /**
        * @brief  tail Datatype DoublyLinkedListNode*
        */
        DoublyLinkedListNode *tail;
        /**
        *constructor taking no parameters \n
        *Whenever this constructor is called it initialises variable head to NULL and variable tail to NULL
        */
        DoublyLinkedList () ;

        /**
        *@fn void insert (ll data)
        *@brief It is a member function and has 1 parameter \n
        *First it instantiates class SinglyListNode(data) and equates to node if head is NULL then it points head to node else points next of tail to node and points prev of node to tail
        then points tail to node \n
        *@param [in] data of datatype ll
        */
        void insert (ll data) ;

        /**
        *@fn void printer (string sep = ", ")
        *@brief It is a member function and has 1 parameter \n
        *It traverse through list and prints all nodes until tail starting from head \n
        *@param [in] sep of datatype sep
        */
        void printer (string sep = ", ") ;

        /**
        *@fn void reverse ()
        *@brief It is a member function and has no parameters \n
        *It traverse through list and reverse list by just replacing left and right nodes and moving from ends to center
        */
        void reverse () ;

};

// ------------------------------- Binary Search Tree -----------------------------
/**
*@class BSTNode
*@brief BSTNode
*It contains a  constructor BSTNode(ll val) \n
*It has no member functions \n
*@param info Datatype ll
*@param level Datatype ll
*@param left Datatype BSTNode*
*@param right Datatype BSTNode*
*/
class BSTNode {
    public:
        /**
        * @brief  info Datatype ll
        */
        ll info;
        /**
        * @brief  level Datatype ll
        */
        ll level;
        /**
        * @brief  left Datatype BSTNode*
        */
        BSTNode *left;
        /**
        * @brief  right Datatype BSTNode*
        */
        BSTNode *right;

        /**
        *@brief constructor taking 1 parameter \n
        *Whenever this constructor is called it initialises variable info to val and variable level to o and variable left to NULL and variable right to NULL \n
        *@param[in] val of datatype ll
        */
        BSTNode (ll val);
};
/**
*defines the operator <<,the function takes two parameters
*@param [in] out
*@param [in] node
*@return ostream&
*/
ostream& operator<<(ostream &out, const BSTNode &node) ;
/**
*@class BinarySearchTree
*@brief BinarySearchTree
*It has constructor with no parameters  BinarySearchTree () \n
*It has following member functions (i)void insert(ll val) (ii)void traverse (BSTNode* T, order tt) (iii)ll height(BSTNode *T) \n
*@param root Datatype BSTNode* \n

*/

class BinarySearchTree {
    public:
        /**
        *@brief root Datatype BSTNode*
        */
        BSTNode *root;
        /**
        *@brief order 
        */
        enum order {PRE, IN, POST};
        /**
        *constructor taking no parameters \n
        *Whenever this constructor is called it initialises variable root to NULL
        */
        BinarySearchTree () ;

        /**
         *@fn insert(ll val)
         *@brief It is a member function and having 1 parameter1 \n
         *First it traverse through BST to find correct position to insert this new node and then change parent of this node to which we should make node a child and also make child of prev node to new node \n
         *@param [in] val of datatype ll
         */
        void insert(ll val) ;

        /**
        *@fn traverse (BSTNode* T, order tt)
        *@brief It is a member function and having 2 parameters \n
        *It traverses through Binary search tree according to whether it is pre/IN/POST and then prints all nodes according to it
        *@param [in] T of datatype BSTNode*
        *@param [in] tt of datatype order
        */
        void traverse (BSTNode* T, order tt) ;

        /**
        *@fn ll height(BSTNode *T)
        *@brief It is a member function and having 1 parameter \n
        *It traverses through Binary search tree and find height of tree by using recursion \n
        *@param [in] T of datatype BSTNode*
        *@return 1+max of height of left tree and right tree
        */
        ll height(BSTNode *T) ;
};

// ------------------------------- Suffix Trie -----------------------------
/**
*@class Trie
*@brief Trie \n
*It has constructor with no parameters Trie () \n
*It has following member functions (i)bool find(Trie* T, char c) (ii)void insert(string s) (iii)bool checkPrefix(string s)  (iv)ll countPrefix(string s) \n
*@param count Datatype ll
*/
class Trie {
    public:
        /**
        *@brief count Datatype ll
        */
        ll count;
        /**
        *@brief nodes of Datatype map<char,Trie*>
        */
        map<char,Trie*> nodes;

        /**
        *@brief constructor taking no parameters \n
        *Whenever this constructor is called it initialises variable count to 0 and variable nodes to map<char,Trie*>();
        */
        Trie () ;

        /**
        *@fn bool find(Trie* T, char c)
        *@brief It is a member function and having 2 parameter \n
        *It returns true if c is present in Trie else return false \n
        *@param [in] T of datatype Trie*
        *@param [in] c of datatype char
        *@return which returns true/false*/
        bool find(Trie* T, char c) ;

        /**
        *@fn void insert(string s)
        *@brief It is a member function and having 1 parameter \n
        *If c is not present in Trie then it inserts a new c into Trie \n
        *@param [in] s of datatype string
        */
        void insert(string s) ;

        /**
        *@fn bool checkPrefix(string s) 
        *@brief It is a member function and having 1 parameter \n
        *It checks whether string s is prefix for any word or not \n
        *@param [in] s of datatype string \n
        */
        bool checkPrefix(string s) ;

        /**
        *@fn ll countPrefix(string s)
        *@brief It is a member function and having 1 parameter \n
        *It counts for how many words string s is prefix  \n
        *@param [in] s of datatype string
        *@return which returns count of prefix
        */
        ll countPrefix(string s) ;

};