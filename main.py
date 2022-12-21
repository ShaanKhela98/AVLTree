#Shaan Khela
#Implementation of AVL self-balancing binary algorithm using text file for operations.

#Python Libraries
import math
import os
from ntpath import split


#Debug flag for terminal output
Debug = False

#BST & Node creation
class node:
    def __init__(self, value=None):
        self.value=value
        self.left_child = None
        self.right_child = None
        self.parent = None
        
class binary_search_tree:
    def __init__(self, alpha):
        self.root = None
        self.weight = alpha
        
#---------------------------------------------------------------------

    def isBalanced(self):
        weighted_value = math.log(self.weight, 1.0/self.weight) + 1
        
        if Debug == True:
            print('\n', "Height = "+ str(self.height()) +  " | L to R diff = " + str(self.diff()) +" | Weight Value = "+ str(weighted_value))
       
        if self.diff() > weighted_value: #evaluates height difference and compares value to math.log(self.weight, 1.0/self.weight) + 1
            #print("Tree rebalanced")
            return True
        else:
            return False
            
#-----------------------------------------------------------------

    def Insert(self, value): #Arguments are AVL tree & value for insertion
        if self.root == None: #Check for root value
            self.root = node(value) #set root value with no parent
            
        else:
            self._insert(value, self.root) #pass value + root to insert function

 
    def _insert(self, value, current_node): #Arguments are AVL tree, value, node
        if value < current_node.value: #Validates value verses tree node
            if current_node.left_child == None: #Check for left side (smaller value)
                current_node.left_child = node(value) #Create node for value on left
                current_node.left_child.parent = current_node #Set parent value
           
            else:
                self._insert(value, current_node.left_child) #Recurse w/ new node left

        elif value > current_node.value: #Validates value verses tree node
            if current_node.right_child == None: #Check for right side (larger value)
                    current_node.right_child = node(value) #Create node for value on right
                    current_node.right_child.parent = current_node #Set parent value

            else:
                self._insert(value, current_node.right_child) #Recurse w/ new node right
            
        else:
            print('Cannot insert value, number found in AVL Tree!')
            
#=================================================================================

    def height(self):
        if self.root != None:
            return self._height(self.root, 0)
        else:
            return 0

    def _height(self, current_node, current_height):
        if current_node == None: 
            return current_height
      
        left_height = self._height(current_node.left_child, current_height+1)
        right_height = self._height(current_node.right_child, current_height+1)
        
        measured_difference = left_height - right_height
        
        return max(left_height, right_height)

#=====================================================================

    def diff(self): #Grabs difference in left subtree and right subtree for rebalance algorithm
        if self.root != None:
            return self._diff(self.root, 0)
        else:
            return 0

    def _diff(self, current_node, current_height):
        if current_node == None:
            return current_height
      
        left_height = self._diff(current_node.left_child, current_height+1)
        right_height = self._diff(current_node.right_child, current_height+1)
        
        measured_difference = left_height - right_height
        
        return (measured_difference)

#===================================================================================

    def search(self, value):
        if self.root != None: #Verify root isn't empty
            return self._search(value, self.root) #Pass search value and tree root
       
        else:
            return False #tree is technically empty

    def _search(self, value, current_node): # Tree, search value, node are arguments
        if value == current_node.value: #checks to see if search value is in AVL Tree
            return True
            
        elif value < current_node.value and current_node.left_child != None: #Checks if search value is smaller and left child node is present then we pass that node for recursion
            return self._search(value, current_node.left_child)
        
        elif value > current_node.value and current_node.right_child != None: #Checks if search value is larger and right child node is present then we pass that node for recursion
            return self._search(value, current_node.right_child)
        
        else:
            return False #Search value cannot be found

#===================================================================================

    def find(self, value): #Same as search but incoorperated with delete function
        if self.root != None:
            return self._find(value, self.root) #Passing value to be deleted
        else:
            return None

    def _find(self, value, current_node): #Searching for value and passing the node
        if value == current_node.value:
            return current_node
        elif value < current_node.value and current_node.left_child != None:
            return self._find(value, current_node.left_child) #Recurse using node (less)
        elif value > current_node.value and current_node.right_child != None:
            return self._find(value, current_node.right_child) #Recuse using node (greater)
            
    def delete_value(self, value):
        return self.delete_node(self.find(value))

    def delete_node(self, node):
                
        def min_value_node(n): #returns the node with minimum value in tree
            current = n
            while current.left_child != None:
                current = current.left_child
            return current

        def num_children(n): #returns the number of children for the specified node
            num_children = 0
            if n.left_child != None: 
                num_children += 1

            if n.right_child != None: 
                num_children += 1

            return num_children

        node_parent = node.parent #get parent node to be deleted
        node_children = num_children(node) #deletion node's number of children

        #Case 1 (node has no children)
        if node_children == 0:
            if node_parent.left_child == node: #remove reference to the node from the parent
                node_parent.left_child = None
            else:
                node_parent.right_child = None

        #Case 2 (node has a single child)
        if node_children == 1:
            if node.left_child != None: #Get single child node
                child = node.left_child
            else:
                child = node.right_child

            if node_parent.left_child == node: #Replace left child's parent node
                node_parent.left_child = child
            else:
                node_parent.right_child = child

            child.parent = node_parent #Correct the parent pointer in node

        #Case 3 (node has two children)
        if node_children == 2:
            successor = min_value_node(node.right_child) #inorder successor of the deleted node
         
            node.value = successor.value  #Holding the value we wished to be deleted
            self.delete_node(successor)  #Copy successor's value to the former node

#=============================================================================

    def print_tree(self): #Prints tree sideways
        if self.root != None:
            self._print_tree(self.root, 0)
        
    def _print_tree(self, current_node, depth):
        if current_node != None:
            self._print_tree(current_node.right_child, depth+1)
            
            for i in range(0, depth):
                print('\t', end="") # adds necessary number of tabs
            
            print (current_node.value) # prints node with tabs
            
            self._print_tree(current_node.left_child, depth+1)

#=============================================================================

    def buildListfromTree(self, array_list): #Builds list using tree values
        if self.root != None:
            self._buildListfromTree(self.root, array_list)
   
    def _buildListfromTree(self, current_node, array_list):
        if current_node is None:
            return None
            
        array_list.append(current_node.value)
        
        self._buildListfromTree(current_node.left_child, array_list)
        self._buildListfromTree(current_node.right_child, array_list)
     
    
    def myRebuildTree(self, nodes_list):# Builds a balanced binary tree based old tree
        
        if len(nodes_list) == 0:
            return None
        
        mid = int(math.ceil(0 + len(nodes_list)) / 2.0) # Created mid point for inserting value into new tree
        
        self.Insert(nodes_list[mid])
        
        list_1 = []
        list_2 = []
        
        for number in nodes_list:
            if number < nodes_list[mid]:
                list_1.append(number) #Creating list for values smaller than inserted value
                
            if number > nodes_list[mid]:
                list_2.append(number) # Creating list for values larger than inserted value
        
        
        nodes_list.pop(mid)
        
        self.myRebuildTree(list_1) #Pass left branch
        self.myRebuildTree(list_2) #Pass right branch

#=============================================================================

def main():
    reader = open('tree.txt', 'r') #Read file
    for commands in reader: #Parse File
        
        key_break = commands.split(' ') #Split line in file (array for parse)
        
      
        if commands.startswith('BuildTree') == True: #Creates AVL tree w/ root
            
            alpha = key_break[1].split(',') #Grab weight to use for self-balance
            
            global_weight = float(alpha[0])
            tree = binary_search_tree(global_weight) #AVL tree initialized
        
            number = key_break[2].splitlines() #Grab first value for insertion
            tree.Insert(int(number[0])) #initialize root value (in this case)
            
            if Debug == True:
                print ("BUILDING TREE...", "Weight =", alpha[0]," Value =", key_break[2])
                
            else:
                print("AVL tree created with root value " + str(number))
                

 
        if commands.startswith('Insert') == True: #Create new node with key value
            
            number = key_break[1].splitlines() #Grab value for AVL tree insertion
            
            if Debug == True:
                print ("INSERTING...", number[0])
                
            tree.Insert(int(number[0])) # insert value
          
            if tree.isBalanced() == False:
                array_list = []
                tree.buildListfromTree(array_list)
                array_list.sort()
                
                del tree
                tree = binary_search_tree(global_weight)
                tree.myRebuildTree(array_list)
                                


        if commands.startswith('Search') == True: #Search for key value
          
            number = key_break[1].splitlines() #Grab value for search
            
            if Debug == True:
                print ("SEARCHING...", number[0],  "is",  tree.search(int(number[0])))
            
            else:
                if tree.search(int(number[0])) == True:
                    print(number[0], "found inside AVL Tree!")
                
                else:
                    print(number[0], "does not exist in Tree")
                    

        if commands.startswith('Delete') == True: #Delete specified key value
          
            number = key_break[1].splitlines() #Grab value for deletion
            
            if Debug == True:
                print ("DELETING...", number[0])
            
            if (tree.search(int(number[0]))) == True:
                tree.delete_value(int(number[0]))
                
                if tree.isBalanced() == False:
                    array_list = []
                    tree.buildListfromTree(array_list)
                    array_list.sort()
                   
                    del tree
                    tree = binary_search_tree(global_weight)
                    tree.myRebuildTree(array_list)
        
            else:
                print ("Attempted to delete", number[0], "but value not found!")
                


        if commands.startswith('Print') == True: #Print tree structure
            print("--------------------------------")
            print("Printing Tree via text command")
            print ("Tree height: ", tree.height(), '\n')
            tree.print_tree()
            print('\n')
            print("--------------------------------")
            

      
        if commands.startswith('Done') == True: #Exits program
            if Debug == 1:
                print ("EXITING")
                
            exit()


if __name__=='__main__':
     main()
