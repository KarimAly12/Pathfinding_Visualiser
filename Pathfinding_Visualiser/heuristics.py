import math 
from cell import Cell
from graph import*


# def hypot(cell, goal):
#     return math.sqrt((goal.cart_pos[0] - cell.cart_pos[0])**2 + (goal.cart_pos[1]-cell.cart_pos[1])**2)

def manhatan(node:Node, node_goal:Node):
    return (abs(node.state[0] - node_goal.state[0]) + abs(node.state[1] - node_goal.state[1]))
                
