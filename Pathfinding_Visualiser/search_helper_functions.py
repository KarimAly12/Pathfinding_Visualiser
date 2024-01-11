from graph import*
from cell import Cell
import copy

#retrun the path cost of a solution.
def get_path_cost(node:Node):
        path_cost = 0
        while(node != None):
                path_cost += 1
                node = node.parent
        return path_cost

#check if the node state is repeated in the same branch.
def is_cycle(node:Node):
        node_parent:Node = node.parent
        while(node_parent != None):
            if(node_parent.state == node.state):
                return True
            node_parent = node_parent.parent
        return False


def join_nodes(node1, node2:Node):

    nodes:list[Node] = []
    n = copy.deepcopy(node2.parent) 
    while(n != None):
        nodes.append(n)
        n = n.parent
        
    n2 =copy.deepcopy(node1)  
    for i in range(len(nodes)):
        # if nodes[i].parent != None:
        #     nodes[i].parent.action = reverse_acrtion(nodes[i].parent.action)
        nodes[i].parent = n2
        n2 = nodes[i]
        if(i == len(nodes) - 1):
                return nodes[i]
        

# def modify_BAstar_actions(node):
#     node2 = node
#     directions = []
#     #nodes = []
#     if node2.parent.state[0] - node2.state[0] == 1:
#         return "RIHGT"
#     elif node2.parent.state[0] - node2.state[0] == -1:
#         return "LEFT"
#     elif node2.parent.state[1] - node2.state[1] == -1:
#         return "UP"
#     elif node2.parent.state[1] - node2.state[1] == 1:
#         return "DOWN"
        
#         #nodes.append(node)


#Becuase of the joined nodes in the BA* the nodes actions are not in the correct order. This function will return correct path directions
# def modify_BAstar_actions(node):
#     node2 = node
#     directions = []
#     #nodes = []
#     while(node2.parent != None):
#         #means we move right from child to parent
#         if node2.parent.state[0] - node2.state[0] == 1:
#             directions.append("RIHGT")
#         #means we move left from child to parent
#         elif node2.parent.state[0] - node2.state[0] == -1:
#             directions.append("LEFT") 
#         #means we move up from child to parent
#         elif node2.parent.state[1] - node2.state[1] == -1:
#             directions.append("UP") 
#         #means we move down from child to parent
#         elif node2.parent.state[1] - node2.state[1] == 1:
#             directions.append("DOWN") 
#         node2 = node2.parent
#         #nodes.append(node)
#     return directions



def reverse_acrtion(action):
    a = ""
    if action == "LEFT":
        a = "RIGHT"
        return a
    if action == "RIGHT":
        a = "LEFT"
        return a
    if action == "UP":
        a = "DOWN"
        return a
    if action == "DOWN":
        a = "UP"
        return a

#return the depth of the node in the tree.
def node_depth(node:Node):
        node_copy:Node = node
        i:int = 0
        while node_copy.parent != None:
            i+=1
            node_copy = node_copy.parent
        return i   

if __name__ == "__main__":
     node1 = Node(state=(0,0))
     node2 = Node(state=(0,0), parent=node1)

     print(is_cycle(node2))