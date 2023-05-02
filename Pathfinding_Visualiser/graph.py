from collections import deque
import pygame
import threading
import time
import _thread
from cell import Cell
from queue import PriorityQueue

class Graph:
    def __init__(self, rows, cols) -> None:
       self.graph:list[list[Cell]] = [[Cell(pos=(x,y)) for x in range(cols)] for y in range(rows)]
       self.rows = rows
       self.cols = cols


    def reset_graph(self):
        for i in range(self.rows):
            for j in range(self.cols):
                self.graph[i][j].is_in_frontier = False




class Node:
    def __init__(self, state, parent=None, action="", path_cost=0) -> None: #State is the agent
       self.state = state
       self.parent = parent
       self.action = action
       self.path_cost = path_cost

    def __lt__(self, other):
        return self.path_cost < other.path_cost
    
    def __gt__(self, other):
        return self.path_cost > other.path_cost