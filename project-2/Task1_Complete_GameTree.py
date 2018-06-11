# -*- coding: utf-8 -*-
"""
Created on Thu May 24 13:05:15 2018

@author: kamyar.manshaei
"""

import numpy as np



class Tree(object):
    
    def __init__(self, root):
        
        self.root  =root
        self.nodes = [root]
        self.OWinsCounter = 0
        self.XWinsCounter = 0
        self.drawsCounter = 0
        self.leaves = 0
        self.branchingFactor = 0
        
    def calculate_branching_factor(self):
        for node in self.nodes:
            self.branchingFactor += len(node.get_children())
        self.branchingFactor /= self.get_size()
        return self.branchingFactor
        
    def add_node(self, node):
        self.nodes.append(node)
        self.OWinsCounter += node.get_o()
        self.XWinsCounter += node.get_x()
        self.drawsCounter += node.get_draw()
        if(node.get_leaf()):
            self.leaves += 1
        
    def get_node(self,nodeNumber):
        return self.nodes[nodeNumber]
        
    def get_all_nodes(self):
        return self.nodes
        
    
    def get_size(self):
        return len(self.nodes)

    
    def get_OWins(self):
        return self.OWinsCounter
    
    def get_XWins(self):
        return self.XWinsCounter
    
    def get_draws(self):
        return self.drawsCounter
    
    def get_leaves(self):
        return self.leaves

class Node(object):
    
    def __init__(self, nodeNumber, state, parent = None):
        
        self.nodeNumber = nodeNumber
        self.state = state
        self.parent = parent
        self.children = []
        self.x = 0
        self.o = 0
        self.draw = 0
        
        if get_winner(self.get_state()) == 1 or get_winner(self.get_state()) == -1 or not (0 in self.get_state()):
            self.leaf = True
        else:
            self.leaf = False
            
        if(self.leaf == True):
            if get_winner(self.get_state()) == 1:
                self.x = 1
            
            if get_winner(self.get_state()) == -1:
                self.o = 1
            
            if get_winner(self.get_state()) == 0:
                self.draw = 1
            
        
        
        
    def get_nodeNumber(self):
        return self.nodeNumber
    
    def get_state(self):
        return self.state
    
    def get_parent(self):
        return self.parent
    
    def add_children(self, newChild):
        self.children.append(newChild)
        
    def get_children(self):
        return self.children
            
    
            
    def get_leaf(self):
        return self.leaf
            

               
    def get_x(self):
        return self.x
            
      
                
    def get_o(self):
        return self.o
             

                           
                
    def get_draw(self):
        return self.draw
    

    
    
def move_was_winning_move(S, p):
    
    if np.max((np.sum(S, axis=0)) * p) == 3:
        return True
    if np.max((np.sum(S, axis=1)) * p) == 3:
        return True
    if (np.sum(np.diag(S)) * p) == 3:
        return True
    if (np.sum(np.diag(np.rot90(S))) * p) == 3:
        return True
    return False

def get_winner(S):
    
    if np.max((np.sum(S, axis=0))) == 3:
        return 1
    if np.min((np.sum(S, axis=0))) == -3:
        return -1
    if np.max((np.sum(S, axis=1))) == 3:
        return 1
    if np.min((np.sum(S, axis=1))) == -3:
        return -1
    if (np.sum(np.diag(S))) == 3:
        return 1
    if (np.sum(np.diag(S))) == -3:
        return -1
    if (np.sum(np.diag(np.rot90(S)))) == 3: 
        return 1
    if (np.sum(np.diag(np.rot90(S)))) == -3:
        return -1
    return 0



def buildTree(p, S, tree, parentNode):

    succNodes = []
    # if S is not terminal: switch player & compute successors
    if not move_was_winning_move(S, p):
        rs, cs = np.where(S==0)
        for j in range(rs.size):
            Ssucc = np.copy(S)
            Ssucc[rs[j],cs[j]] = p
            newnode = tree.get_size()
            succNodes.append(newnode)
            childnode = Node(nodeNumber=newnode, state=Ssucc, parent=parentNode)
            tree.get_node(parentNode.get_nodeNumber()).add_children(childnode.get_nodeNumber())
            tree.add_node(childnode)
                
    # continue recursively
    p *= -1
    for n in succNodes:
        if tree.get_node(n).get_leaf() == False:
            buildTree(p, tree.get_node(n).get_state(), tree, tree.get_node(n))
        
if __name__ == "__main__":
    S = np.zeros((3,3), dtype=int)
    p = 1
    node = Node(nodeNumber=0, state=S)
    tree = Tree(node)
    buildTree(p, S, tree, tree.get_node(0))
    
     
    print("Number of nodes:")
    print(tree.get_size())
    
    print("\nNumber of states where X wins:")
    print(tree.get_XWins())
    
    print("\nNumber of states where O wins:")
    print(tree.get_OWins())
    
    print("\nNumber of draws:")
    print(tree.get_draws())

    print("\nNumber of leaves:")
    print(tree.get_leaves())
    
    print("\nBranching factor:")
    print(tree.calculate_branching_factor())
    
